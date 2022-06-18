"""
Implementation of image background removing functions.
"""

# import sys
import os
import io
import shutil
from glob import glob
import threading
from PIL import Image  # type: ignore[import]


def importer():
    """
    This import is really slow when loading the app. Importing it either inside the function that
    uses it or in a different thread feels like it makes for a better user experience.
    """
    global bg
    from rembg import bg  # type: ignore[import]


imp_th = threading.Thread(target=importer)
imp_th.start()


def main() -> int:
    """Main function."""
    # rm_bg("test.JPG")
    return 0


def rm_bg(img_path: str) -> None:
    """
    This function will remove the background of a given image. It should receive a JPG image path.
    It will create and save a JPG image with white background.
    """

    # Making sure we got the correct input.
    dot_pos = img_path.rfind(".")
    if dot_pos == -1 or not img_path[dot_pos + 1 :].lower() in ["jpg", "jpeg"]:
        raise ValueError("Expected JPG images.")

    # Replacing "\" to "/" because *Windows*.
    img_path = img_path.replace("\\", "/")

    # Opening/reading image as bytes.
    with open(img_path, "rb") as input_as_bytes:
        input_img = input_as_bytes.read()

    # Removing background from image using u2net_human_seg.
    output_as_bytes = bg.remove(
        input_img, alpha_matting=True, model_name="u2net_human_seg"
    )
    # Converting the output as bytes to a PIL Image.
    pil_img = Image.open(io.BytesIO(output_as_bytes))

    # Tuple representing the new RGB background color (the image we get from rembg is a transparent
    # PNG).
    fill_color = (255, 255, 255)
    pil_img = pil_img.convert("RGBA")
    if pil_img.mode in ("RGBA", "LA"):
        # Removing transparency and making background white.
        background = Image.new(pil_img.mode[:-1], pil_img.size, fill_color)
        background.paste(pil_img, pil_img.split()[-1])  # omit transparency
        pil_img = background

    # Saving the new image in the same folder with a similar name.
    pil_img.convert("RGB").save(img_path[:dot_pos] + "_NO_BG.jpg")


def rm_bg_from_folder(imgs_folder: str) -> None:
    """
    This function will remove the background of images starting with number 1 through 3
    in all subfolders of a given imgs_folder.
    """
    # Getting subfolders of the current folder.
    folder_paths = glob(imgs_folder + "/*")

    # Iterating through each subfolder.
    for folder in folder_paths:
        # Checking for the existence of a "backup" folder called "FACES_BG".
        if not os.path.exists(backup_dir := folder + "/FACES_BG"):
            # Creating the subfolder if it doesn't exist.
            os.mkdir(backup_dir)

        # Getting the images in the current subfolder.
        # Images with background already removed will end in "_NO_BG". So, ignoring "G" in the end
        # of their names will ignore those images (we don't want to remove the background twice).
        imgs_paths = glob(folder + "/[1-3]*[!G].jpg")
        # Iterating through the images in this subfolder.
        for input_path in imgs_paths:
            # Replacing "\" to "/" because *Windows*.
            input_path = input_path.replace("\\", "/")
            # Removing background of this image.
            rm_bg(input_path)
            # Moving the original image to the "backup folder".
            shutil.move(input_path, backup_dir + "/" + input_path.split("/")[-1])


if __name__ == "__main__":
    raise SystemExit(main())
