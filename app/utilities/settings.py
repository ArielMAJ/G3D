"""
This module will load the app's settings.
"""

import os
import json
from utilities.paths import join_pr


def get_settings() -> dict:
    """
    This function will load the app's current settings. If it doesn't exist, it should
    partially create a settings file with some defaults.
    It'll return the settings
    """

    resources = join_pr("resources", "settings.json")
    try:
        with open(resources, encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
    except FileNotFoundError:
        settings = {
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
            json.dump(settings, settings_file, indent=4)

    return settings