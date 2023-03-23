"""
This module implements the app's main window class.
"""

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from glob import glob
import numpy as np
from PIL import Image  # type: ignore[import]
import customtkinter as ctk  # type: ignore[import]

try:
    from utilities.im_processing import load_img  # type: ignore[import]
    from utilities.im_bg import rm_bg, rm_bg_from_folder, imp_th  # type: ignore[import]
    from utilities.paths import join_pr  # type: ignore[import]
    from utilities.my_secrets import get_secrets  # type: ignore[import]
    from utilities import commands  # type: ignore[import]
except ImportError:
    import sys

    sys.path.insert(0, os.path.abspath(".."))
    from utilities.im_processing import load_img  # type: ignore[import]
    from utilities.im_bg import rm_bg, rm_bg_from_folder, imp_th  # type: ignore[import]
    from utilities.paths import join_pr  # type: ignore[import]
    from utilities.my_secrets import get_secrets  # type: ignore[import]
    from utilities import commands  # type: ignore[import]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainWindow(ctk.CTk):
    """
    All the app's main functionality should be acessible through this window.
    """

    def __init__(self):
        super().__init__()
        self.widgets: dict = {}
        self.secrets: dict = {}
        self.vars: dict = {}
        self.images: dict = {}
        # self.font = ("Arial", 12)

        self.YELLOW = "#FCE388"
        self.BLUE = "#C2CEFF"
        self.RED = "#B52C30"
        self.GREEN = "#256A49"
        self.GRAY = "#525a49"

        self.paths_e_ids_pastas_8_imagens = []
        self.paths_e_ids_pastas_8_imagens_para_upload = []
        self.template = np.array(
            Image.open(join_pr("images", "templates", "template.jpg"))
        )

        self._load_window()

    def _load_window(self):
        """
        This function will call subfunctions to load the app.
        """
        # self.withdraw()
        self._basic_configs()
        self._place_widgets()
        self._place_window_on_screen()
        # self.deiconify()

    def _basic_configs(self):
        """
        This function should contain all basic configurations such as:
        - Loading images/files/etc;
        - Creating variables (StringVar, IntVar, etc);
        """
        self._check_and_load_secrets()
        self.refresh_paths_list()

        self.images["icon"] = load_img(join_pr("images", "icon.png"), (30, 30))
        self.images["upload"] = load_img(join_pr("images", "upload.png"), (40, 40))
        self.images["sync"] = load_img(join_pr("images", "sync.png"), (40, 40))
        self.images["search"] = load_img(join_pr("images", "search.png"), (40, 40))
        self.images["bg"] = load_img(join_pr("images", "background.png"), (40, 40))
        self.images["template"] = load_img(join_pr("images", "layout.png"), (40, 40))

        self.title(self.secrets["title"])
        self.iconphoto(False, self.images["icon"])
        # self.minsize(width=800, height=600)
        self.resizable(width=False, height=False)

        self.config(padx=20, pady=30)

        self.vars["folder_path"] = tk.StringVar()
        self.vars["folder_path"].set(self.secrets["default_path_to_images"])

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _check_and_load_secrets(self) -> None:
        """
        This function will load the app's current secrets. If it doesn't exist, it should
        partially create a secrets file with some defaults.
        """

        resources = join_pr("resources", "secrets.json")
        self.secrets = get_secrets()

    def _place_widgets(self):
        """
        This function should handle creating and placing most of the widgets.
        """

        row = 1
        self.widgets["lbl_folder"] = ctk.CTkLabel(
            master=self,
            text="Pasta:",  # Folder
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            # bg_color="green",  # self.colors["app_bg_color"],
            width=5,
            # anchor="w",
            # justify="left",
        )
        self.widgets["lbl_folder"].grid(
            row=row,
            column=0,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            sticky="NEWS",
        )

        self.widgets["lbl_folder_path"] = ctk.CTkLabel(
            master=self,
            textvariable=self.vars["folder_path"],
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            # bg_color="green",  # self.colors["app_bg_color"],
            anchor=self._path_anchor,
            justify="left",
        )
        self.widgets["lbl_folder_path"].grid(
            row=row,
            column=1,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_search_folder"] = ctk.CTkButton(
            master=self,
            text="MUDAR        ",  # Change folder
            image=self.images["search"],
            command=self.search_folder_button_press,
            corner_radius=5,
        )
        self.widgets["btn_search_folder"].grid(
            row=row,
            column=2,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            ipady=self.secrets["ipady"],
            sticky="NEWS",
        )

        self.widgets["lbl_to_process"] = ctk.CTkLabel(
            master=self,
            text=self.lbl_to_process(),
            # width=45,
            # fg_color=self.colors["text_color"],
            # font=self.font,
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            # bg_color="red",
            # anchor="center",
        )
        self.widgets["lbl_to_process"].grid(
            row=(row := row + 1),
            column=1,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_refresh"] = ctk.CTkButton(
            master=self,
            text="ATUALIZAR ",  # Refresh .
            image=self.images["sync"],
            compound="left",
            # padx=self.secrets["padx"],
            corner_radius=5,
            # border=0,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            command=self.check_folders,
        )
        self.widgets["btn_refresh"].grid(
            row=row,
            column=2,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            ipady=self.secrets["ipady"],
            sticky="NEWS",
        )

        self.widgets["btn_rembg_FOLDER"] = ctk.CTkButton(
            master=self,
            # Remove background (all subfolders)
            text="FUNDOS      ",
            image=self.images["bg"],
            corner_radius=5,
            command=self.folder_remove_background_button_press,
        )
        self.widgets["btn_rembg_FOLDER"].grid(
            row=(row := row + 1),
            column=2,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            ipady=self.secrets["ipady"],
            sticky="NEWS",
        )

        self.widgets["btn_assemble"] = ctk.CTkButton(
            master=self,
            text="TEMPLATES",  # "Assemble" templates.
            image=self.images["template"],
            # padx=self.secrets["padx"],
            # border=0,
            corner_radius=5,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            command=lambda: commands.background(self.assemble_all_templates),
        )
        self.widgets["btn_assemble"].grid(
            row=(row := row + 1),
            column=2,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            ipady=self.secrets["ipady"],
            sticky="NEWS",
        )

        self.widgets["lbl_to_upload"] = ctk.CTkLabel(
            master=self,
            text=self.lbl_to_upload(),
            # width=45,
            # fg=self.colors["text_color"],
            # font=self.font,
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            # bg_color="blue",
            # anchor="center",
        )
        self.widgets["lbl_to_upload"].grid(
            row=row,
            column=1,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_upload"] = ctk.CTkButton(
            master=self,
            text="UPLOAD      ",  # Upload images.
            image=self.images["upload"],
            compound="left",
            # padx=self.secrets["padx"],
            corner_radius=5,
            # border=0,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            # command=lambda: print("Click"),
            command=lambda: commands.background(self.upload_all_templates),
        )

        self.widgets["btn_upload"].grid(
            row=(row := row + 1),
            column=2,
            padx=self.secrets["padx"],
            pady=self.secrets["pady"],
            ipady=self.secrets["ipady"],
            sticky="NEWS",
        )

        # self.update()
        # if self.widgets["lbl_folder_path"].winfo_width() > 410:
        #     self.widgets["lbl_folder_path"].configure(width=40)

    def _place_window_on_screen(self):
        # self.update()
        width = 550
        height = 250

        true_screen_width = self.winfo_vrootwidth()
        perceived_screen_width = self.winfo_screenwidth()

        true_screen_height = self.winfo_vrootheight()
        perceived_screen_height = self.winfo_screenheight()

        offset = {
            "x": int(
                (self.winfo_vrootwidth() // 2)
                - (true_screen_width / perceived_screen_width * width // 2)
            ),
            "y": int(
                (self.winfo_vrootheight() // 2)
                - (true_screen_height / perceived_screen_height * height // 2)
            ),
        }

        self.geometry(f"{width}x{height}+{offset['x']}+{offset['y']}")
        # self.set_scaling(1, 1, 1)

    @property
    def _path_anchor(self) -> str:
        return "center" if len(self.vars["folder_path"].get()) <= 85 else "w"

    def remove_background_button_press(
        self,
        model_name: str = "u2net_human_seg",
        alpha_matting: bool = False,
    ) -> None:
        """
        Implementation of the background removing button.

        - This should open a file navigator dialog to get an amount of image paths.
        - These images should all be JPGs.
        - If no image is selected the function should return. If any amount of images
        are selected, they should have their background removed.
        """
        selected_files = filedialog.askopenfilenames(
            # initialdir=r"/",
            # Select JPG images to remove background
            title="Selecionar imagens JPG para remover fundo",
            filetypes=(
                ("Imagens", "*.jpg"),  # Images
                ("Imagens", "*.jpeg"),  # Images
                ("Imagens", "*.png"),  # Images
                ("Todos os arquivos", "*.*"),  # All files.
            ),
        )
        if len(selected_files) == 0:
            return

        for img_file_path in selected_files:
            rm_bg(
                img_file_path,
                model_name=model_name,
                alpha_matting=alpha_matting,
            )

        messagebox.showinfo(
            # Finished
            title="Finalizado",
            # Backgrounds removed successfully!
            message="Fundos removidos com sucesso!",
            parent=self,
            # This specific icon removes the bell noise from the messagebox.
            # icon="question",
        )

    def folder_remove_background_button_press(self) -> None:
        """
        Implementation of the background removing button for folder with subfolders containing
        images.

        - The images should be JPGs only;
        - Images should start with numbers 1 to 3;
        - They shouldn't end in "G" (e.g. 1_IMG will be read but 1_IMG_NO_BG.jpg won't);
        """
        rm_bg_from_folder(self.secrets["default_path_to_images"])

        messagebox.showinfo(
            # Finished
            title="Finalizado",
            # Backgrounds removed successfully!
            message="Fundos removidos com sucesso!",
            parent=self,
            # This specific icon removes the bell noise from the messagebox.
            # icon="question",
        )

    def search_folder_button_press(self) -> None:
        """
        This will open a folder navigator dialog to get a folder path.
        This will update the secrets.json file if a folder is selected and is different from the
        current one. It will also update the label showing the current selected folder.
        """
        selected_folder = filedialog.askdirectory(
            # Select folder with subfolders containing images to remove.
            title="Selecionar pasta com subpastas com imagens",
        )
        if (
            not selected_folder
            or selected_folder == self.secrets["default_path_to_images"]
        ):
            return

        self._check_and_load_secrets()
        self.secrets["default_path_to_images"] = selected_folder
        with open(join_pr("resources", "secrets.json"), "w", encoding="utf-8") as file:
            json.dump(self.secrets, file, indent=4)

        self.vars["folder_path"].set(selected_folder)
        self.widgets["lbl_folder_path"].configure(anchor=self._path_anchor)
        self.check_folders()

    ##########################################################################################
    ##########################################################################################
    ##########################################################################################
    ##########################################################################################

    def refresh_paths_list(self):
        def renomear_imagens(path):
            # clearCMD()
            # print(f'Renomeando imagens da pasta {path_e_id[1]}')

            for number, image_path in enumerate(glob(path + "\\*MG*.jpg")):
                split_image_path = image_path.split("\\")
                if split_image_path[-1][0] not in "0123456789":
                    split_image_path[-1] = str(number + 1) + "_" + split_image_path[-1]
                    os.rename(image_path, "\\".join(split_image_path))

            objetiva = path + "\\OBJETIVA"
            if os.path.exists(objetiva):
                renomear_imagens(objetiva)

        self.paths_e_ids_pastas_8_imagens = []
        self.paths_e_ids_pastas_8_imagens_para_upload = []
        if os.path.exists(self.secrets["default_path_to_images"]):
            path_pastas_pacientes = glob(
                self.secrets["default_path_to_images"] + "\\*[0-9][0-9]*"
            )
            if len(path_pastas_pacientes) > 0:
                paths_e_ids = [
                    (path, path.split("\\")[-1]) for path in path_pastas_pacientes
                ]
                for path_pasta, patient_id in paths_e_ids:
                    quantidade_fotos = len(glob(path_pasta + "\\*MG*.jpg"))
                    ja_tem_template = (
                        len(glob(path_pasta + f"\\{patient_id}_*.jpg")) > 0
                    )
                    if ja_tem_template:
                        self.paths_e_ids_pastas_8_imagens_para_upload.append(
                            (path_pasta, patient_id)
                        )
                    elif quantidade_fotos == 8:
                        self.paths_e_ids_pastas_8_imagens.append(
                            (path_pasta, patient_id)
                        )

                for path, patient_id in self.paths_e_ids_pastas_8_imagens:
                    renomear_imagens(path)

    def button_states(self, state):
        self.widgets["btn_search_folder"].configure(state=state)
        self.widgets["btn_refresh"].configure(state=state)
        self.widgets["btn_assemble"].configure(state=state)
        self.widgets["btn_upload"].configure(state=state)
        self.widgets["btn_rembg_FOLDER"].configure(state=state)

    def assemble_all_templates(self):
        self.button_states(tk.DISABLED)
        self.check_folders()
        for path_pasta, patient_id in self.paths_e_ids_pastas_8_imagens:
            self.widgets["lbl_to_process"].configure(
                text=f"Montando template do paciente {patient_id}",
                # fg=self.RED,
            )
            commands.montar_template(patient_id, path_pasta, self.template)
        self.widgets["lbl_to_process"].configure(
            text="Templates montados",
            # fg=self.GREEN,
        )
        # self.after(
        # 3000, lambda: self.widgets["lbl_to_process"].configure(fg=self.TEXT_COLOR)
        # )
        self.after(3000, lambda: (self.check_folders(), self.button_states(tk.NORMAL)))
        messagebox.showinfo(
            # Finished
            title="Templates montados.",
            message="Todos templates montados com sucesso!",
            parent=self,
            # This specific icon removes the bell noise from the messagebox.
            # icon="question",
        )

    def upload_all_templates(self):
        self.button_states(tk.DISABLED)
        self.check_folders()
        for path_pasta, patient_id in self.paths_e_ids_pastas_8_imagens_para_upload:
            self.widgets["lbl_to_upload"].configure(
                text=f"Fazendo upload template {patient_id}",
                # fg=self.RED,
            )
            commands.upload_template(path_pasta, patient_id)
        self.widgets["lbl_to_upload"].configure(
            text="Uploads finalizados.",
            # fg=self.GREEN,
        )
        # self.after(
        # 3000, lambda: self.widgets["lbl_to_upload"].configure(fg=self.TEXT_COLOR)
        # )
        self.after(3000, lambda: (self.check_folders(), self.button_states(tk.NORMAL)))
        messagebox.showinfo(
            # Finished
            title="Upload finalizado.",
            message="Upload de templates realizados com sucesso!",
            parent=self,
            # This specific icon removes the bell noise from the messagebox.
            # icon="question",
        )

    # def update_template_on_screen(self):
    # tktemplate = ImageTk.PhotoImage(
    # Image.fromarray(np.array(self.template)).resize((350, 250))
    # )
    #     self.canvas.itemconfig(self.img_container, image=tktemplate)

    def lbl_to_process(self):
        if len(self.paths_e_ids_pastas_8_imagens) > 0:
            txt = ", ".join([p_id for _, p_id in self.paths_e_ids_pastas_8_imagens])
        else:
            txt = "Vazio"
        return f"Pastas com 8 imagens sem templates montados:\n{txt}"

    def lbl_to_upload(self):
        if len(self.paths_e_ids_pastas_8_imagens_para_upload) > 0:
            txt = ", ".join(
                [p_id for _, p_id in self.paths_e_ids_pastas_8_imagens_para_upload]
            )
        else:
            txt = "Vazio"
        return f"Templates para upload:\n{txt}"

    def check_folders(self):
        self.refresh_paths_list()
        self.widgets["lbl_to_process"].configure(text=self.lbl_to_process())
        self.widgets["lbl_to_upload"].configure(text=self.lbl_to_upload())


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will skip the loading
    screen.
    """
    root = MainWindow()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
