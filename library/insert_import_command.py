import re
import sublime
from functools import partial

from .debug import debug
from .get_import_root import get_import_root
from .get_panel_item import get_panel_item


def insert_import_command(args):
    view = args.get("view")
    point = args.get("point")
    notify = args.get("notify")
    entry_modules = args.get("entry_modules")
    typescript_paths = args.get("typescript_paths") or []
    name = args.get("name") or get_name_candidate({"view": view, "point": point})
    name = re.sub(r"[^\w\-\@\/]", "", name)
    if not name:
        return
    debug("insert_import: trying to import", "`{0}`".format(name))
    import_root = get_import_root()
    match_items = []
    panel_items = []
    for item in entry_modules:
        if item.get("name") == name:
            panel_item = get_panel_item(import_root, item)
            if panel_item is not None:
                panel_items.append(panel_item)
                match_items.append(item)
    if len(panel_items) == 0 and notify:
        view.show_popup("No imports found for `<strong>{0}</strong>`".format(name))
        return
    if len(panel_items) == 1:
        item = match_items[0]
        view.run_command(
            "paste_import", {"item": item, "typescript_paths": typescript_paths}
        )
        return

    def on_select(index):
        if index == -1:
            return
        selected_item = match_items[index]
        debug("insert_import: on_select", selected_item)
        view.run_command(
            "paste_import",
            {"item": selected_item, "typescript_paths": typescript_paths},
        )

    view.window().show_quick_panel(panel_items, on_select)


def get_name_candidate(args):
    view = args.get("view")
    point = args.get("point")
    point_region = view.sel()[0]
    if point is not None:
        point_region = sublime.Region(point, point)
    name = view.substr(point_region).strip()
    if not name:
        cursor_region = view.expand_by_class(
            point_region,
            sublime.CLASS_WORD_START
            | sublime.CLASS_LINE_START
            | sublime.CLASS_PUNCTUATION_START
            | sublime.CLASS_WORD_END
            | sublime.CLASS_PUNCTUATION_END
            | sublime.CLASS_LINE_END,
        )
        name = view.substr(cursor_region)
    return name
