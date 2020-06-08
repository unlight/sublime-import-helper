import sublime
from .get_setting import get_setting
from .debug import debug
from .utils import norm_path

# Returns Record<path, { folderExcludePatterns: string[], fileExcludePatterns: string[] }
def get_exclude_patterns(project_data=None, project_file=None):
    if project_data is None:
        project_data = sublime.active_window().project_data()
    if project_file is None:
        project_file = sublime.active_window().project_file_name()
    result = {}
    all_folder_exclude_patterns = get_setting("folder_exclude_patterns", [])
    all_file_exclude_patterns = get_setting("file_exclude_patterns", []) + get_setting(
        "binary_file_patterns", []
    )
    for folder in (project_data or {}).get("folders") or []:
        folder_exclude_patterns = folder.get("folder_exclude_patterns") or []
        file_exclude_patterns = (folder.get("file_exclude_patterns") or []) + (
            folder.get("binary_file_patterns") or []
        )
        path = folder.get("path")
        if project_file:
            path = norm_path(project_file, path)
        result[path] = {
            "folderExcludePatterns": all_folder_exclude_patterns
            + folder_exclude_patterns,
            "fileExcludePatterns": all_file_exclude_patterns + file_exclude_patterns,
        }
    return result
