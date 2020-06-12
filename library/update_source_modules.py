import sublime
from .debug import debug
from .get_source_folders import get_source_folders
from .get_exclude_patterns import get_exclude_patterns
from .utils import error_message, status_message
from .exec_command import run_command_async


def update_source_modules(source_modules):
    source_folders = get_source_folders()
    exclude_patterns = get_exclude_patterns()

    debug("update_source_modules:source_folders", source_folders)

    def callback(err, result):
        source_modules_callback(err, result, source_modules)
        next()

    def next():
        if len(source_folders) > 0:
            source_folder = source_folders.pop(0)
            folder_patterns = exclude_patterns.get(source_folder) or {}
            debug("folder_patterns", folder_patterns)
            run_command_async(
                "exportsFromDirectory",
                {
                    "directory": source_folder,
                    "folderExcludePatterns": folder_patterns.get(
                        "folderExcludePatterns"
                    ),
                    "fileExcludePatterns": folder_patterns.get("fileExcludePatterns"),
                },
                callback,
            )

    source_modules.clear()
    next()


def source_modules_callback(err, result, source_modules):
    if err:
        return error_message(err)
    if type(result) is not list:
        return error_message("Unexpected type of result: " + type(result))
    for item in result:
        filepath = item.get("filepath")
        if filepath is None:
            continue
        source_modules.append(item)
    count = len(source_modules)
    status_message("{0} source modules found".format(count))
    debug("Update source modules", count)
