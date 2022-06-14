"""
This module implements the loading screen class.
"""

from tkinter import Toplevel, Tk, Label
from PIL import Image, ImageTk  # type: ignore[import]


class LoadingScreen(Toplevel):
    """
    This top level will create a loading screen and display it for a given amount of seconds.
    """

    def __init__(
        self, parent: Tk, *, seconds: int = 1, image_path: str = "./images/icon.png"
    ):
        super().__init__(parent)
        self.parent = parent
        self.seconds = seconds
        self.image_path = image_path

        self.logo = Image.open(self.image_path)
        self.logo_tk = ImageTk.PhotoImage(self.logo)

        self._draw_window()

    def _draw_window(self) -> None:

        label = Label(self, image=self.logo_tk, bg="black")
        label.place(x=0, y=0)

        self.parent.withdraw()
        self.withdraw()
        self.geometry(f"{self.logo.size[0]}x{self.logo.size[1]}")
        # self.update()

        offset = {
            "x": int(0.5 * self.winfo_screenwidth() - self.logo.size[0] // 2),
            "y": int(0.5 * self.winfo_screenheight() - self.logo.size[1] // 2),
        }
        self.geometry(f"+{offset['x']}+{offset['y']}")

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-disabled", True)
        self.attributes("-transparentcolor", "black")
        self.attributes("-alpha", 0.8)

        self.lift()
        self.deiconify()
        self.after(int(self.seconds * 950), self.parent.deiconify)
        self.after(int(self.seconds * 1000), self.destroy)


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will only show the loading
    screen and then a blank screen (this won't load main screen). You should run this module from
    the same folder as main.py (e.g.: py .\\gui\\top_levels\\loading_screen.py), otherwise it won't
    run.
    """
    root = Tk()
    LoadingScreen(root, seconds=2)
    root.after(4000, root.destroy)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
