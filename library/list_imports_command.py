from functools import partial

from .get_import_root import get_import_root
from .panel_items import panel_items
from .debug import debug


def list_imports_command(view, import_root, entry_modules=[], typescript_paths=[]):

    (items, matches) = panel_items(entry_modules=entry_modules, import_root=import_root)

    def on_select(index):
        if index == -1:
            return
        selected_item = matches[index]
        debug("list_imports_command:on_select", selected_item)
        view.run_command(
            "paste_import",
            {"item": selected_item, "typescript_paths": typescript_paths},
        )

    view.window().show_quick_panel(items, on_select)
