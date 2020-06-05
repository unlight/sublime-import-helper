import sublime
from ..import_helper import PROJECT_NAME, SOURCE_MODULES
from .debug import debug
from .get_source_folders import get_source_folders
from .get_exclude_patterns import get_exclude_patterns
from .exec_command import run_command_async


def update_source_modules():
    source_folders = get_source_folders()
    debug("update_source_modules:source_folders", source_folders)
    exclude_patterns = get_exclude_patterns()
    run_command_async(
        "exportsFromFolders",
        {"folders": source_folders, "excludePatterns": exclude_patterns},
        get_source_modules_callback,
    )


def get_source_modules_callback(err, result):
    if err:
        sublime.error_message(PROJECT_NAME + "\n" + str(err))
        return
    SOURCE_MODULES.clear()
    if type(result) is not list:
        sublime.error_message(
            PROJECT_NAME + "\n" + "Unexpected type of result: " + type(result)
        )
        return
    for item in result:
        filepath = item.get("filepath")
        if filepath is None:
            continue
        SOURCE_MODULES.append(item)
    sublime.status_message(
        "{0}: {1} source modules found".format(PROJECT_NAME, len(SOURCE_MODULES))
    )
    debug("Update source modules", len(SOURCE_MODULES))
