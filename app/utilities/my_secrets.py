"""
This module will load the app's secrets.
"""

import os
import json
from utilities.paths import join_pr


def get_secrets() -> dict:
    """
    This function will load the app's current secrets. If it doesn't exist, it should
    partially create a secrets file with some defaults.
    It'll return the secrets
    """

    resources = join_pr("resources", "secrets.json")
    try:
        with open(resources, encoding="utf-8") as secrets_file:
            secrets = json.load(secrets_file)
    except FileNotFoundError:
        secrets = {
            "default_path_to_images": "/",
            "padx": 5,
            "pady": 2,
            "ipady": 3,
            "title": "",
            "auth": "",
            "api_link": "",
            "patient_id_key": "",
            "files": "",
        }
        if not os.path.exists(folder_path := join_pr("resources")):
            os.mkdir(folder_path)
        with open(resources, "w", encoding="utf-8") as secrets_file:
            json.dump(secrets, secrets_file, indent=4)

    return secrets
