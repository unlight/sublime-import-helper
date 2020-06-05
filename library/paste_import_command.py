import sublime

from ..import_helper import PROJECT_NAME
from .get_setting import get_setting
from .get_from_paths import get_from_paths
from .on_done_func import on_done_func
from .identifier_name import identifier_name
from .debug import debug
from .exec_command import run_command, run_command_async

# view.run_command('paste_import', args=({'item': {'filepath': 'xxx', 'name': 'aaa', 'isDefault': False}, 'typescript_paths': []}))
# view.run_command('paste_import', args=({'item': {'isDefault': True, 'module': 'worker_threads', 'name': 'worker_threads'}}))
def paste_import_command(args):
    view = args.get("view")
    item = args.get("item")
    typescript_paths = args.get("typescript_paths") or []
    debug("paste_import_command:item", item)
    file_name = view.file_name() or "."
    from_paths = get_from_paths(item, file_name, typescript_paths)

    if len(from_paths) > 1:
        choices = [{"item": item, "path": path} for path in from_paths]

        def on_select(selected):
            item = selected.get("item")
            item["module"] = selected.get("path")
            view.run_command("paste_import", {"item": item, "typescript_paths": []})

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
        },
    )
    debug("paste_import_command:result", result)
    return result


# def insert_import_callback(err):
#     if err:
#         sublime.error_message(PROJECT_NAME + "\n" + str(err))
#         return

# Get import line information
# from_path = from_paths[0]
# import_line_info = get_import_line_info(view, from_path)
# debug("paste_import: import_line_info", import_line_info)
# # Prepare import string template
# from_quote = get_setting("from_quote", "'")
# import_end = ";"
# import_string = "import {{0}} from {0}{2}{0}{1}\n".format(
#     from_quote, import_end, from_path
# )
# # Name to import
# name = item["name"]
# if item.get("from_package") == True:
#     name = identifier_name(name)
# # Not found in existing paths
# if import_line_info["import_row"] == -1:
#     pos = 0
#     if "end" == get_setting("insert_position", "end"):
#         pos = view.text_point(import_line_info["last_import_row"] + 1, 0)
#     if not item["isDefault"]:
#         name = wrap_imports([name])
#     view.insert(edit, pos, import_string.format(name))
#     return
# # Import row found
# debug("import_line_info", import_line_info)
# line_region = view.full_line(
#     view.text_point(import_line_info["import_row"], 0)
# )
# # Trying to import in import default row
# if (
#     is_import_default(import_line_info["line_contents"])
#     and item["isDefault"] == False
# ):
#     name = import_line_info["imports"][0] + ", { " + name + " }"
#     debug("name", name)
#     view.replace(edit, line_region, import_string.format(name))
# # Trying to import non default item to mixed line
# elif (
#     is_import_mixed(import_line_info["line_contents"])
#     and item["isDefault"] == False
# ):
#     other_imports = import_line_info["imports"][1:]
#     try:
#         other_imports.remove(name)
#     except:
#         pass
#     other_imports.append(name)
#     name = import_line_info["imports"][0] + ", { " + ", ".join(other_imports) + " }"
#     debug("name", name)
#     view.replace(edit, line_region, import_string.format(name))
# # Ttrying to import item default
# elif item["isDefault"]:
#     if is_import_default(import_line_info["line_contents"]):
#         name = "* as " + name
#     debug("name", name)
#     view.replace(edit, line_region, import_string.format(name))
# # Regular import
# else:
#     imports = import_line_info["imports"]
#     try:
#         imports.remove(name)
#     except:
#         pass
#     imports.append(name)
#     line_region = view.full_line(
#         view.text_point(import_line_info["import_row"], 0)
#     )
#     name = wrap_imports(imports)
#     debug("name", name)
#     view.replace(edit, line_region, import_string.format(name))
