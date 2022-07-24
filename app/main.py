"""
Main script for loading this app.
Display loading screen -> Load app in the "background" -> Destroy loading screen and display main
screen.
"""

# This package's dependencies are expected to be installed in a virtual enviroment. This is
# just another option for activating the VENV.
# try:
#     with open("./resources/activate_this.path", encoding="utf-8") as path:
#         activate_this = path.read()
#     with open(activate_this, encoding="utf-8") as py_file:
#         code = compile(py_file.read(), activate_this, "exec")
#         exec(code, dict(__file__=activate_this))
# except FileNotFoundError as err:
#     # print(err)
#     pass

# Imports will only correctly happen if the venv is activated.
from gui import main_window  # type: ignore[import]
from gui.loading_screen import LoadingScreen  # type: ignore[import]

# If you don't want to activate HiDPI compatibility in your python executables, uncomment these two:
# from ctypes import windll
# windll.shcore.SetProcessDpiAwareness(1)


def main() -> int:
    """
    This function will start the app.
    """
    # This will force loading screen to stay up until rembg is imported (it is a slow import).
    loading_screen = LoadingScreen(wait_for=[main_window.imp_th])
    loading_screen.mainloop()

    root = main_window.MainWindow()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
