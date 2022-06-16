"""
This module implements the app's main window class.
"""

# from sys import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from utilities import im_processing, im_bg  # type: ignore[import]

# try:
#     import top_levels
# except ImportError:
#     from . import top_levels

# from time import sleep
# from PIL import Image, ImageTk
# import threading


class MainWindow(tk.Tk):
    """
    All the app's main functionality should be acessible through this window.
    """

    def __init__(self, *, draw_after_mainloop: bool = True):
        super().__init__()
        self.widgets: dict = {}

        self.font = ("Arial", 12)
        self.colors: dict[str, str] = {
            "yellow": "#FCE388",
            "blue": "#C2CEFF",
            "red": "#B52C30",
            "green": "#256A49",
            "gray": "#525a49",
        }

        self.colors["text_color"] = self.colors["gray"]
        self.colors["app_bg_color"] = self.colors["yellow"]

        self.settings = None

        if draw_after_mainloop:
            # Loading screen will be responsible for hiding and showing main screen.
            self.after(300, self._draw_window)
        else:
            # Else the main screen should hide and show itself.
            self.withdraw()
            self._draw_window()
            self.deiconify()

    def _draw_window(self):
        self._basic_configs()
        self._place_menu_bar()
        self._place_widgets()
        self._place_window_on_screen()

    def _basic_configs(self):
        self.title("")
        self.iconphoto(False, im_processing.load_img("./images/icon.png", (30, 30)))
        # self.minsize(width=800, height=600)
        self.config(padx=10, pady=10, bg=self.colors["app_bg_color"])

    def _place_menu_bar(self):
        # Menu Bar object.
        self.widgets["menu_bar"] = tk.Menu(self)
        self.config(menu=self.widgets["menu_bar"])

        # File button in menu.
        self.widgets["menu_file"] = tk.Menu(self.widgets["menu_bar"], tearoff="off")
        self.widgets["menu_file"].add_cascade(
            label="Print", command=lambda: print("Hi")
        )
        self.widgets["menu_file"].add_separator()
        self.widgets["menu_file"].add_cascade(label="Exit", command=self.destroy)

        # rembg button in menu.
        self.widgets["menu_rembg"] = tk.Menu(self.widgets["menu_bar"], tearoff="off")

        # Adding buttons to menu bar.
        self.widgets["menu_bar"].add_cascade(
            label="File", menu=self.widgets["menu_file"]
        )
        self.widgets["menu_bar"].add_command(
            # self.widgets["menu_rembg"],
            label="Remover Fundo",
            command=self.remove_background_button_press,
        )

    def _place_widgets(self):
        self.widgets["test_label"] = tk.Label(self, text="erh...", bg="yellow")
        self.widgets["test_label"].pack()

        self.widgets["btn_rembg_FOLDER"] = tk.Button(
            self,
            text="Remover fundo de todas as pastas",
            command=self.folder_remove_background_button_press,
        )
        self.widgets["btn_rembg_FOLDER"].pack()

    def _place_window_on_screen(self):
        self.update()
        width = self.winfo_width() if self.winfo_width() > 800 else 800
        height = self.winfo_height() if self.winfo_height() > 600 else 600
        offset = {
            "x": int(0.5 * self.winfo_screenwidth() - width // 2),
            "y": int(0.5 * self.winfo_screenheight() - height // 2 - 20),
        }
        # print(self.winfo_screenwidth(), self.winfo_width())
        # print(self.winfo_screenheight(), self.winfo_height())
        # print(offset, self.geometry())
        self.geometry(f"{width}x{height}+{offset['x']}+{offset['y']}")

    def remove_background_button_press(self) -> None:
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
            im_bg.rm_bg(img_file_path)

        messagebox.showinfo(
            title="Finalizado",
            message="Fundos removidos com sucesso!",
            # This specific icon removes the bell noise from the messagebox.
            # icon="question",
            parent=self,
        )

    def folder_remove_background_button_press(self) -> None:
        """
        Implementation of the background removing button.

        - This should open a file navigator dialog to get an amount of image paths.
        - These images should all be JPGs.
        - If no image is selected the function should return. If any amount of images
        are selected, they should have their background removed.
        """
        selected_folder = filedialog.askdirectory(
            # Select JPG images to remove background
            title="Selecionar pasta com subpastas com imagens",
        )
        if not selected_folder:
            return
            
        im_bg.rm_bg_from_folder(selected_folder)

        messagebox.showinfo(
            title="Finalizado",
            message="Fundos removidos com sucesso!",
            # This specific icon removes the bell noise from the messagebox.
            # icon="question",
            parent=self,
        )


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will skip  the loading
    screen. To get this function to run, you'll need to run this module as a "package" from the
    same folder as main.py (e.g.: py -m gui.main_window), otherwise it won't run.
    """
    root = MainWindow(draw_after_mainloop=False)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
