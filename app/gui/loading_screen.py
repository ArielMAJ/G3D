"""
This module implements the loading screen class.
"""

from tkinter import Tk, Label
from PIL import Image, ImageTk  # type: ignore[import]


class LoadingScreen(Tk):
    """
    This top level will create a loading screen and display it for a given amount of seconds.
    It can accept a list of threads to wait for before closing itself and showing the main screen.
    """

    def __init__(
        self,
        *,
        seconds: float = 0.5,
        image_path: str = "./images/icon.png",
        wait_for: list = None,
    ):
        super().__init__()
        self.seconds: float = seconds
        self.image_path: str = image_path

        self.wait_for: list = wait_for if wait_for is not None else []

        self.logo = Image.open(self.image_path)
        self.logo_tk = ImageTk.PhotoImage(self.logo)

        self._draw_window()
        self._wait()

    def _draw_window(self) -> None:
        label = Label(self, image=self.logo_tk, bg="black")
        label.place(x=0, y=0)

        self.withdraw()
        self.geometry(f"{self.logo.size[0]}x{self.logo.size[1]}")
        # self.update()

        offset = {
            "x": int(self.winfo_screenwidth() // 2 - self.logo.size[0] // 2),
            "y": int(self.winfo_screenheight() // 2 - self.logo.size[1] // 2),
        }
        self.geometry(f"+{offset['x']}+{offset['y']}")

        self.overrideredirect(True)
        # self.attributes("-topmost", True)
        self.attributes("-disabled", True)
        self.attributes("-transparentcolor", "black")
        self.attributes("-alpha", 0.8)

        self.lift()
        self.deiconify()

    def _wait(self) -> None:
        for thread in self.wait_for:
            self.after(int(self.seconds * 1000) + 50, thread.join)

        self.after(int(self.seconds * 1000) + 200, self.destroy)


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will only show the loading
    screen and then a blank screen (this won't load main screen). You should run this module from
    the same folder as main.py (e.g.: py .\\gui\\top_levels\\loading_screen.py), otherwise it won't
    run.
    """
    root = LoadingScreen(seconds=2)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
