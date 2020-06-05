import sublime

from .utils import norm_path


def get_source_folders():
    window = sublime.active_window()
    project_file = window.project_file_name()
    project_data = window.project_data()
    result = []
    for folder in project_data.get("folders") or []:
        folder_path = folder.get("path")
        if folder_path is None:
            continue
        path_source = project_data.get("path_source")
        if bool(path_source):
            folder_path = path_source
        folder_path = norm_path(project_file, folder_path)
        result.append(folder_path)
    return result
