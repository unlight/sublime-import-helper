import sublime

from .debug import debug
from .get_source_folders import get_source_folders
from .get_exclude_patterns import get_exclude_patterns
from .error_message import error_message
from .exec_command import run_command_async


def update_source_modules(source_modules=[]):
    source_folders = get_source_folders()
    debug("update_source_modules:source_folders", source_folders)
    exclude_patterns = get_exclude_patterns()

    def callback(err, result):
        get_source_modules_callback(err, result, source_modules)

    run_command_async(
        "exportsFromFolders",
        {"folders": source_folders, "excludePatterns": exclude_patterns},
        callback,
    )


def get_source_modules_callback(err, result, source_modules):
    if err:
        return error_message(err)
    source_modules.clear()
    if type(result) is not list:
        return error_message("Unexpected type of result: " + type(result))
    for item in result:
        filepath = item.get("filepath")
        if filepath is None:
            continue
        source_modules.append(item)
    sublime.status_message(
        "{0}: {1} source modules found".format(PROJECT_NAME, len(source_modules))
    )
    debug("Update source modules", len(source_modules))
