import sublime

from .get_setting import get_setting
from .get_from_paths import get_from_paths
from .on_done_func import on_done_func
from .debug import debug
from .exec_command import run_command, run_command_async

# view.run_command('paste_import', args=({'item': {'filepath': 'xxx', 'name': 'aaa', 'isDefault': False}, 'typescript_paths': []}))
# view.run_command('paste_import', args=({'item': {'isDefault': True, 'module': 'worker_threads', 'name': 'worker_threads'}}))
def paste_import_command(view, item, typescript_paths=[], test_selected_index=-1):
    debug("paste_import_command:item", item)
    file_name = view.file_name() or "."
    from_paths = get_from_paths(item, file_name, typescript_paths)

    if len(from_paths) > 1:
        choices = [{"item": item, "path": path} for path in from_paths]

        def on_select(selected):
            item = selected.get("item")
            item["module"] = selected.get("path")
            view.run_command("paste_import", {"item": item, "typescript_paths": []})

        if test_selected_index != -1:
            on_select(choices[test_selected_index])
            return
        view.window().show_quick_panel(from_paths, on_done_func(choices, on_select))
        return

    if len(from_paths) == 0:
        raise Exception("len from_paths must be not empty")

    specifier = from_paths[0]
    soucefile_content = view.substr(sublime.Region(0, view.size()))
    result = run_command(
        "insertImport",
        {
            "declaration": {
                "name": item["name"],
                "specifier": specifier,
                "isDefault": item.get("isDefault"),
            },
            "sourceFileContent": soucefile_content,
            "manipulationSettings": {"quoteKind": get_setting("from_quote", "'")},
        },
    )
    # debug("paste_import_command:result", result)
    return result
