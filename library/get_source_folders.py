import sublime

from .utils import norm_path


def get_source_folders():
    return sublime.active_window().folders()
