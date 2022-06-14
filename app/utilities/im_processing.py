"""
Short image processing functions.
"""

from typing import Union
from PIL import Image, ImageTk  # type: ignore[import]


# Vs code is showing me this error: Union requires two or more type arguments.
def load_img(path, size: Union[tuple[int] | float] = None):
    """
    This should load images.

    The size parameter can be:
        A tuple of ints, for resizing;
        A float, for indicating a percentage to resize; or
        None, to keep original size.
    """

    if size is None:
        return ImageTk.PhotoImage(Image.open(path))

    if isinstance(size, tuple):
        return ImageTk.PhotoImage(Image.open(path).resize(size))

    if isinstance(size, float):
        img = Image.open(path)
        new_size = tuple(int(length * size) for length in img.size)
        return ImageTk.PhotoImage(img.resize(new_size))

    
#Grammar correction tuble to tuple 

    raise ValueError("Expected size to be either a tuple of ints, a float or None.")
