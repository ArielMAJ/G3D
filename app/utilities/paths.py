"""
This moudle implements some simple things related to paths.
"""

import os


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))


def join_pr(*args, join_project_root=True):
    """
    This is basically a wrapper for os.path.join, but it adds the project's root folder
    full path by default.
    """
    if join_project_root:
        return os.path.join(ROOT_DIR, *args)
    return os.path.join(*args)
