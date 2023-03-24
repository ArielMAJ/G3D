"""
Utility commands for processing and uploading images.
"""

from glob import glob
import os
import io
import multiprocessing
import datetime
import time
import threading
from skimage.io import imsave  # type: ignore[import]
import requests  # type: ignore[import]
from PIL import ImageDraw, Image, ImageFont  # type: ignore[import]
import numpy as np
from .my_secrets import get_secrets

# import skimage


def background(func, args=None):
    if args is not None:
        thread = threading.Thread(target=func, args=args)
    else:
        thread = threading.Thread(target=func)
    thread.start()


def read_and_process_image(position_path: tuple[int, str]) -> np.ndarray:
    """
    This function will read a given image and resize it accordingly.
    """
    position, path = position_path

    # print(f'Carregando e redimensionando imagem {position}.')
    img = Image.open(glob(f'{path + "/" + str(position)}*MG*[0-9]*.jpg')[0])

    if position > 3:
        return np.array(img.resize((1025, 732))).astype(int)

    return np.array(img.resize((716, 1074))).astype(int)


def montar_template(patient_id, path_pasta, template):
    def info_paciente_para_template(patient_id):
        secret = get_secrets()
        headers = {"authorization": secret["auth"]}
        params = {secret["patient_id_key"]: f"{patient_id}"}
        url = secret["api_link"]
        response = requests.get(
            url, headers=headers, data=params
        )  # Pesquisando o paciente pelo Nº Manager
        info_dict = response.json()[0]

        imagem_dados_paciente = Image.new("RGB", (1200, 308), color=(255, 255, 255))
        draw_img = ImageDraw.Draw(imagem_dados_paciente)

        font1 = ImageFont.truetype("./Fontes/verdanab.ttf", 55)
        font2 = ImageFont.truetype("./Fontes/verdana.ttf", 55)

        nome_paciente_escrever = info_dict["patient_datum"]["name"]
        nome_dr = info_dict["dentist_datum"]["name"]
        nome_dr_escrever = f"Dr(a). {nome_dr}"

        birth_date = datetime.datetime.strptime(
            info_dict["patient_datum"]["birthdate"], "%Y-%m-%d"
        )
        end_date = datetime.datetime.strptime(
            info_dict["date"][:-10], "%Y-%m-%dT%H:%M:%S"
        )
        idade = (end_date - birth_date) / datetime.timedelta(days=365.2425)  # 365.2425
        idade_escrever = f"{int(idade)}a {int((idade - int(idade)) * 12)}m"
        nascimento = birth_date.strftime("%d/%m/%Y")
        nascimento_escrever = f"Data Nasc.: {nascimento} Idade: {idade_escrever}"
        data = end_date.strftime("%d/%m/%Y")
        data_escrever = f"Data: {data}"

        left_border_dist = 35
        draw_img.text(
            (left_border_dist, 35), nome_paciente_escrever, font=font1, fill=(0, 0, 0)
        )
        draw_img.text(
            (left_border_dist, 105), nome_dr_escrever, font=font2, fill=(0, 0, 0)
        )
        draw_img.text(
            (left_border_dist, 175), nascimento_escrever, font=font2, fill=(0, 0, 0)
        )
        draw_img.text(
            (left_border_dist, 245), data_escrever, font=font2, fill=(0, 0, 0)
        )

        imagem_dados_paciente = np.array(imagem_dados_paciente)
        return imagem_dados_paciente, nome_paciente_escrever

    # print('''Carregando imagens...\nAguarde alguns instantes...''')
    try:
        patient_id = int(patient_id)
    except ValueError:
        try:
            patient_id = int(patient_id.split("-")[0])
        except ValueError:
            salvar_info_erro("Erro ao identificar ID.\n"):
            raise ValueError # TODO: Create custom exception.

    # print(f'Procurando dados do paciente {patient_id} e escrevendo no template...\n')

    cabecalho, nome_paciente = info_paciente_para_template(patient_id)
    template[:308, :1200, :] = cabecalho

    with multiprocessing.Pool() as pool:
        images = pool.map(
            read_and_process_image,
            list(map(lambda n: (n, path_pasta), tuple(range(1, 9)))),
        )

    # 716x1074
    # ExtraOral Frontal
    template[485 : 485 + 1074, 48 : 48 + 716, :] = images[1 - 1]
    # ExtraOral Lateral
    template[485 : 485 + 1074, 844 : 844 + 716, :] = images[3 - 1]
    # ExtraOral Frontal Sorriso
    template[485 : 485 + 1074, 1588 : 1588 + 716, :] = images[2 - 1]

    # 1025x732
    # IntraOral Oclusal Superior
    template[20 : 20 + 732, 2410 : 2410 + 1025, :] = images[8 - 1]
    # IntraOral Oclusal Inferior
    template[827 : 827 + 732, 2410 : 2410 + 1025, :] = images[7 - 1]
    # IntraOral Lateral Direita
    template[1654 : 1654 + 732, 48 : 48 + 1025, :] = images[5 - 1]
    # IntraOral Frontal
    template[1654 : 1654 + 732, 1220 : 1220 + 1025, :] = images[4 - 1]
    # IntraOral Lateral Esquerda
    template[1654 : 1654 + 732, 2410 : 2410 + 1025, :] = images[6 - 1]

    template_file_name = f'\\{patient_id}_{"_".join(nome_paciente.split())}.jpg'
    imsave(path_pasta + template_file_name, template)

    objetiva = path_pasta + "\\OBJETIVA"
    if os.path.exists(objetiva):
        # p_id = path_pasta.split("\\")[-1]
        # print(f'Montando template OBJETIVA do paciente {p_id}\n')
        montar_template(patient_id, objetiva, template)


def salvar_info_erro(error_info):
    with open("./Resources/Erros/erros.txt", "a", encoding="utf-8") as file:
        file.write(
            f'{time.strftime("%H:%M:%S %d/%m/%Y", time.localtime())} - {error_info}\n'
        )


def upload_template(path, patient_id):
    try:
        patient_id = int(patient_id)
    except ValueError:
        try:
            patient_id = int(patient_id.split("-")[0])
        except ValueError:
            salvar_info_erro(f"ID {patient_id}: Erro conversão str->int")
            return
    try:
        template_file_name = f"\\{patient_id}_*.jpg"
        template_path = glob(path + template_file_name)[0]
    except:
        salvar_info_erro(f"ID {patient_id}: Template não existe")
        return

    secrets = get_secrets()
    try:
        headers = {"authorization": secrets["auth"]}

        data = {secrets["patient_id_key"]: f"{patient_id}"}

        url = secrets["api_link"]

        # Pesquisando o paciente pelo Nº Manager
        response = requests.get(url, headers=headers, data=data)
        basic_info = response.json()[0]
        # print(f'Nome: {basic_info["patient_datum"]["name"]}')

        # Obtém o resquest_id para acessar todas informações do paciente
        request_id = basic_info["id"]

        url = f"{url}/{request_id}"
        # r2 = requests.get(url,headers=headers) #Obtém informações completas do paciente

        pil_im = Image.open(template_path)
        bytes_io = io.BytesIO()
        pil_im.save(bytes_io, "jpeg")
        im_bytes = bytes_io.getvalue()

        files = {secrets["files"]: im_bytes}
        requests.put(
            url, headers=headers, files=files
        )  # Pesquisando o paciente pelo Nº Manager
    except:
        salvar_info_erro(f"ID {patient_id}: Erro no upload do template")
        return
