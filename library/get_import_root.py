import sublime
import os

from .common_path import common_path
from .debug import debug
from .get_source_folders import get_source_folders
from .utils import norm_path


def get_import_root(project_data=None, project_file=None, folders=[]):
    if project_data is None:
        project_data = sublime.active_window().project_data() or {}
    import_root = project_data.get("import_root")
    if import_root:
        result = import_root
        project_file = project_file or sublime.active_window().project_file_name()
        if project_file is not None:
            result = norm_path(project_file, result)
        return result
    folders = folders or sublime.active_window().folders()
    if len(folders) > 0:
        result = folders[0]
        if len(folders) != 1:
            result = common_path(folders)
            if bool(result) and os.path.isdir(result):
                result = os.path.dirname(result)
        return result
    active_view = sublime.active_window().active_view()
    result = None
    if active_view:
        file_name = active_view.file_name()
        if not file_name:
            result = os.path.dirname(file_name)
    return result
