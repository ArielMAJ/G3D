# G3D

This is a tkinter project for facilitating handling certain tasks with images such as:
- Removing image background (one at a time and in batches);
- Merging multiple images into one (e.g. placing them side by side/in certain positions);

Image background removal will use [rembg](https://github.com/danielgatis/rembg). You should download u2net_human_seg.pth 
[here](https://github.com/xuebinqin/U-2-Net) and place it in the correct folder.

Some of this app's functionality should be easily accessible to anyone. But there will be parts that will need 
a key for accessing a private API for getting sensitive/personal data online (and thus won't be accessible).
I might try to make these parts usable and testable even without access to the API.

The code should be 100% in english, but the UI will be in PT-BR. I'm up for eventually adding a language settings
option if anyone's interested in contributing.
