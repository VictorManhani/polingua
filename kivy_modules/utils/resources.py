import os
import sys
from kivy.utils import platform

def resource_path(relative_path):
    """
        It is used to find the temp path if exists 
        else return the absolute path of a relative_path."""

    abs_path = os.path.join(os.path.abspath("."), relative_path)

    if platform == "android":
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return abs_path
    else:
        if os.path.exists(abs_path):
            return abs_path
        elif hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)

    raise Exception(f"Don't find the path: {abs_path}")
