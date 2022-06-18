"""
This module implements the app's main window class.
"""

# from sys import platform
import os
import json
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

    def __init__(self, *, load_after_mainloop: bool = True):
        super().__init__()
        self.widgets: dict = {}
        self.settings: dict = {}
        self.vars: dict = {}

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

        if load_after_mainloop:
            # Loading screen will be responsible for hiding and showing main screen.
            self.after(50, self._load_window)
        else:
            # Else the main screen should hide and show itself.
            self.withdraw()
            self._load_window()
            self.deiconify()

    def _load_window(self):
        """
        This function will call subfunctions to load the app.
        """
        self._basic_configs()
        self._place_menu_bar()
        self._place_widgets()
        self._place_window_on_screen()

    def _basic_configs(self):
        """
        This function should contain all basic configurations such as:
        - Loading images/files/etc;
        - Creating variables (StringVar, IntVar, etc);
        """
        self._check_and_load_settings()

        self.title(self.settings["title"])
        self.iconphoto(False, im_processing.load_img("./images/icon.png", (30, 30)))
        # self.minsize(width=800, height=600)
        self.resizable(width=False, height=False)

        self.config(padx=20, pady=30, bg=self.colors["app_bg_color"])

        self.vars["folder_path"] = tk.StringVar()
        self.vars["folder_path"].set(self.settings["default_path_to_images"])

        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _check_and_load_settings(self) -> None:
        """
        This function will load the app's current settings. If it doesn't exist, it should
        partially create a settings file with some defaults.
        """
        try:
            with open(
                "./resources/settings.json", "r", encoding="utf-8"
            ) as settings_file:
                self.settings = json.load(settings_file)
        except FileNotFoundError:
            self.settings = {
                "default_path_to_images": "/",
                "padx": 2,
                "pady": 1,
                "title": "",
            }
            if not os.path.exists("./resources"):
                os.mkdir("./resources")
            with open(
                "./resources/settings.json", "w", encoding="utf-8"
            ) as settings_file:
                json.dump(self.settings, settings_file, indent=4)

    def _place_menu_bar(self):
        """
        This function should handle the menu bar creation.
        """
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
        """
        This function should handle the non-menubar widgets.
        """

        self.widgets["lbl_folder"] = tk.Label(
            self,
            text="Pasta:",  # Folder
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg="yellow",  # self.colors["app_bg_color"],
            width=5,
            anchor="w",
            # justify="left",
        )
        self.widgets["lbl_folder"].grid(
            row=0,
            column=0,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["lbl_folder_path"] = tk.Label(
            self,
            textvariable=self.vars["folder_path"],
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg="red",  # self.colors["app_bg_color"],
            width=60,
            anchor=self._path_anchor,
            # justify="left",
        )
        self.widgets["lbl_folder_path"].grid(
            row=0,
            column=1,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_search_folder"] = tk.Button(
            self,
            text="Mudar pasta",  # Change folder
            command=self.search_folder_button_press,
        )
        self.widgets["btn_search_folder"].grid(
            row=0,
            column=2,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_rembg_FOLDER"] = tk.Button(
            self,
            # Remove background (all subfolders)
            text="Remover fundos\n(todas subpastas)",
            command=self.folder_remove_background_button_press,
        )
        self.widgets["btn_rembg_FOLDER"].grid(
            row=2,
            column=2,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["lbl_folders_to_process"] = tk.Label(
            text="...",  # self.label_templates_disponiveis(),
            width=45,
            fg=self.colors["text_color"],
            font=self.font,
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg="lightblue",
            anchor="center",
        )
        self.widgets["lbl_folders_to_process"].grid(
            column=1,
            row=1,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_montar"] = tk.Button(
            text="Montar Templates",  # "Assemble" templates.
            # image=img_start,
            padx=self.settings["padx"],
            # border=0,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            # command=...,
        )
        self.widgets["btn_montar"].grid(
            column=2,
            row=3,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["lbl_folders_to_upload"] = tk.Label(
            text="...",  # self.label_templates_upload(),
            # width=45,
            fg=self.colors["text_color"],
            font=self.font,
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg="lightblue",
            anchor="center",
        )
        self.widgets["lbl_folders_to_upload"].grid(
            column=1,
            row=3,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_upload"] = tk.Button(
            text="Fazer Upload",  # Upload images.
            # image=img_start,
            padx=self.settings["padx"],
            # border=0,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            # command=...,
        )

        self.widgets["btn_upload"].grid(
            column=2,
            row=4,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_refresh"] = tk.Button(
            text="Atualizar",  # Refresh .
            # image=img_start,
            padx=self.settings["padx"],
            # border=0,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            # command=...,
        )
        self.widgets["btn_refresh"].grid(
            column=2,
            row=1,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        # self.update()
        # if self.widgets["lbl_folder_path"].winfo_width() > 410:
        #     self.widgets["lbl_folder_path"].configure(width=40)

    def _place_window_on_screen(self):
        self.update()
        width = self.winfo_reqwidth() if self.winfo_reqwidth() > 1000 else 1000
        height = self.winfo_reqheight() if self.winfo_reqheight() > 600 else 600
        offset = {
            "x": int(0.5 * self.winfo_screenwidth() - width // 2),
            "y": int(0.5 * self.winfo_screenheight() - height // 2 - 20),
        }
        # print(self.winfo_screenwidth(), self.winfo_width())
        # print(self.winfo_screenheight(), self.winfo_height())
        # print(offset, self.geometry())
        self.geometry(f"{width}x{height}+{offset['x']}+{offset['y']}")

    @property
    def _path_anchor(self) -> str:
        return "center" if len(self.vars["folder_path"].get()) <= 85 else "e"

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
        im_bg.rm_bg_from_folder(self.settings["default_path_to_images"])

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
        This will update the settings.json file if a folder is selected and is different from the
        current one. It will also update the label showing the current selected folder.
        """
        selected_folder = filedialog.askdirectory(
            # Select folder with subfolders containing images to remove.
            title="Selecionar pasta com subpastas com imagens",
        )
        if (
            not selected_folder
            or selected_folder == self.settings["default_path_to_images"]
        ):
            return

        self._check_and_load_settings()
        self.settings["default_path_to_images"] = selected_folder
        with open("./resources/settings.json", "w", encoding="utf-8") as settings_file:
            json.dump(self.settings, settings_file, indent=4)

        self.vars["folder_path"].set(selected_folder)
        self.widgets["lbl_folder_path"].configure(anchor=self._path_anchor)


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will skip  the loading
    screen. To get this function to run, you'll need to run this module as a "package" from the
    same folder as main.py (e.g.: py -m gui.main_window), otherwise it won't run.
    """
    root = MainWindow(load_after_mainloop=False)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
