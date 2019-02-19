import sublime_plugin
from .import_helper import typescript_paths, node_modules, source_modules
from .utils import *

# Command list_imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    # Show all available imports

    def run(self, edit):
        import_root = get_import_root()
        match_items = []
        panel_items = []
        for item in source_modules + node_modules:
            panel_item = get_panel_item(import_root, item)
            if panel_item is not None:
                panel_items.append(panel_item)
                match_items.append(item)
        on_done = on_done_func(match_items, self.on_select)
        self.view.window().show_quick_panel(panel_items, on_done)

    def on_select(self, selected_item):
        debug('list_imports:on_select', selected_item)
        self.view.run_command('paste_import', {'item': selected_item, 'typescript_paths': typescript_paths})