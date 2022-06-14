"""
Implementation of image background removing functions.
"""

# import os
import io
# import sys
# import shutil
# from glob import glob
from PIL import Image  # type: ignore[import]
from rembg import bg  # type: ignore[import]


def main() -> int:
    """Main function."""
    rm_bg("test.JPG")
    return 0


def rm_bg(img_path: str):
    """
    This function will remove the background of a given image. It should receive a JPG image path.
    It will create and save a JPG image with white background.
    """

    # Making sure we got the correct input.
    dot_pos = img_path.rfind(".")
    if dot_pos == -1 or not img_path[dot_pos + 1 :].lower() in ["jpg"]:
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


if __name__ == "__main__":
    raise SystemExit(main())
