"""
This module implements the app's main window class.
"""

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk  # type: ignore[import]

try:
    from utilities.im_processing import load_img  # type: ignore[import]
    from utilities.im_bg import rm_bg, rm_bg_from_folder, imp_th  # type: ignore[import]
    from utilities.paths import join_pr  # type: ignore[import]
except ImportError:
    import sys

    sys.path.insert(0, os.path.abspath(".."))
    from utilities.im_processing import load_img  # type: ignore[import]
    from utilities.im_bg import rm_bg, rm_bg_from_folder, imp_th  # type: ignore[import]
    from utilities.paths import join_pr  # type: ignore[import]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainWindow(ctk.CTk):
    """
    All the app's main functionality should be acessible through this window.
    """

    def __init__(self):
        super().__init__()
        self.widgets: dict = {}
        self.settings: dict = {}
        self.vars: dict = {}
        self.images: dict = {}
        # self.font = ("Arial", 12)

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
        self._check_and_load_settings()

        self.images["icon"] = load_img(join_pr("images", "icon.png"), (30, 30))
        self.images["upload"] = load_img(join_pr("images", "upload.png"), (40, 40))
        self.images["sync"] = load_img(join_pr("images", "sync.png"), (40, 40))
        self.images["search"] = load_img(join_pr("images", "search.png"), (40, 40))
        self.images["bg"] = load_img(join_pr("images", "background.png"), (40, 40))
        self.images["template"] = load_img(join_pr("images", "layout.png"), (40, 40))

        self.title(self.settings["title"])
        self.iconphoto(False, self.images["icon"])
        # self.minsize(width=800, height=600)
        self.resizable(width=False, height=False)

        self.config(padx=20, pady=30)

        self.vars["folder_path"] = tk.StringVar()
        self.vars["folder_path"].set(self.settings["default_path_to_images"])

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _check_and_load_settings(self) -> None:
        """
        This function will load the app's current settings. If it doesn't exist, it should
        partially create a settings file with some defaults.
        """

        resources = join_pr("resources", "settings.json")
        try:
            with open(resources, encoding="utf-8") as settings_file:
                self.settings = json.load(settings_file)
        except FileNotFoundError:
            self.settings = {
                "default_path_to_images": "/",
                "padx": 5,
                "pady": 2,
                "ipady": 3,
                "title": "",
                "auth": "",
                "api_link": "",
            }
            if not os.path.exists(folder_path := join_pr("resources")):
                os.mkdir(folder_path)
            with open(resources, "w", encoding="utf-8") as settings_file:
                json.dump(self.settings, settings_file, indent=4)

    def _place_widgets(self):
        """
        This function should handle creating and placing most of the widgets.
        """

        row = 1
        self.widgets["lbl_folder"] = ctk.CTkLabel(
            self,
            text="Pasta:",  # Folder
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg_color="green",  # self.colors["app_bg_color"],
            width=5,
            # anchor="w",
            # justify="left",
        )
        self.widgets["lbl_folder"].grid(
            row=row,
            column=0,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["lbl_folder_path"] = ctk.CTkLabel(
            self,
            textvariable=self.vars["folder_path"],
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg_color="green",  # self.colors["app_bg_color"],
            anchor=self._path_anchor,
            justify="left",
        )
        self.widgets["lbl_folder_path"].grid(
            row=row,
            column=1,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_search_folder"] = ctk.CTkButton(
            self,
            text="MUDAR        ",  # Change folder
            image=self.images["search"],
            command=self.search_folder_button_press,
            corner_radius=5,
        )
        self.widgets["btn_search_folder"].grid(
            row=row,
            column=2,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            ipady=self.settings["ipady"],
            sticky="NEWS",
        )

        self.widgets["lbl_folders_to_process"] = ctk.CTkLabel(
            text="...",  # self.label_templates_disponiveis(),
            # width=45,
            # fg_color=self.colors["text_color"],
            # font=self.font,
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg_color="red",
            # anchor="center",
        )
        self.widgets["lbl_folders_to_process"].grid(
            row=(row := row + 1),
            column=1,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_refresh"] = ctk.CTkButton(
            text="ATUALIZAR ",  # Refresh .
            image=self.images["sync"],
            compound="left",
            # padx=self.settings["padx"],
            corner_radius=5,
            # border=0,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            command=lambda: print("Click"),
        )
        self.widgets["btn_refresh"].grid(
            row=row,
            column=2,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            ipady=self.settings["ipady"],
            sticky="NEWS",
        )

        self.widgets["btn_rembg_FOLDER"] = ctk.CTkButton(
            self,
            # Remove background (all subfolders)
            text="FUNDOS      ",
            image=self.images["bg"],
            corner_radius=5,
            command=self.folder_remove_background_button_press,
        )
        self.widgets["btn_rembg_FOLDER"].grid(
            row=(row := row + 1),
            column=2,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            ipady=self.settings["ipady"],
            sticky="NEWS",
        )

        self.widgets["btn_montar"] = ctk.CTkButton(
            text="TEMPLATES",  # "Assemble" templates.
            image=self.images["template"],
            # padx=self.settings["padx"],
            # border=0,
            corner_radius=5,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            command=lambda: print("Click"),
        )
        self.widgets["btn_montar"].grid(
            row=(row := row + 1),
            column=2,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            ipady=self.settings["ipady"],
            sticky="NEWS",
        )

        self.widgets["lbl_folders_to_upload"] = ctk.CTkLabel(
            text="...",  # self.label_templates_upload(),
            # width=45,
            # fg=self.colors["text_color"],
            # font=self.font,
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            bg_color="blue",
            # anchor="center",
        )
        self.widgets["lbl_folders_to_upload"].grid(
            row=row,
            column=1,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_upload"] = ctk.CTkButton(
            text="UPLOAD      ",  # Upload images.
            image=self.images["upload"],
            compound="left",
            # padx=self.settings["padx"],
            corner_radius=5,
            # border=0,
            # bg=self.colors["app_bg_color"],
            # activebackground=self.colors["app_bg_color"],
            command=lambda: print("Click"),
        )

        self.widgets["btn_upload"].grid(
            row=(row := row + 1),
            column=2,
            padx=self.settings["padx"],
            pady=self.settings["pady"],
            ipady=self.settings["ipady"],
            sticky="NEWS",
        )

        # self.update()
        # if self.widgets["lbl_folder_path"].winfo_width() > 410:
        #     self.widgets["lbl_folder_path"].configure(width=40)

    def _place_window_on_screen(self):
        # self.update()
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
        self.set_scaling(1, 1, 1)

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
        rm_bg_from_folder(self.settings["default_path_to_images"])

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
        with open(join_pr("resources", "settings.json"), "w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4)

        self.vars["folder_path"].set(selected_folder)
        self.widgets["lbl_folder_path"].configure(anchor=self._path_anchor)


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
