import sublime

from .get_source_folders import get_source_folders
from .utils import norm_path


def get_import_root():
    window = sublime.active_window()
    project_file = window.project_file_name()
    if project_file is None:
        return None
    project_data = window.project_data() or {}
    result = project_data.get("import_root")
    if result is None:
        # TODO: Handle multiple roots
        result = get_source_folders()[0]
    return norm_path(project_file, result)
