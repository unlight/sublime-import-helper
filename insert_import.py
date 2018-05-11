import sublime
import sublime_plugin
import re
from .import_helper import typescript_paths, node_modules, source_modules
from .utils import *

# Command insert_import
class InsertImportCommand(sublime_plugin.TextCommand):
    # Adds import of identifier near cursor

    def run(self, edit, name=None, point=None, notify=True):
        if name is None:
            point_region = self.view.sel()[0]
            if point is not None:
                point_region = sublime.Region(point, point)
            name = self.view.substr(point_region).strip()
            if not name:
                cursor_region = self.view.expand_by_class(point_region, sublime.CLASS_WORD_START | sublime.CLASS_LINE_START | sublime.CLASS_PUNCTUATION_START | sublime.CLASS_WORD_END | sublime.CLASS_PUNCTUATION_END | sublime.CLASS_LINE_END)
                name = self.view.substr(cursor_region)
        name = re.sub(r'\W', '', name)
        if not name:
            return
        debug('Trying to import', '`{0}`'.format(name))
        import_root = get_import_root()
        match_items = []
        panel_items = []
        # Iterate through source modules + node modules
        for item in source_modules + node_modules:
            if (item.get('name') == name):
                panel_item = get_panel_item(import_root, item)
                if panel_item is not None:
                    panel_items.append(panel_item)
                    match_items.append(item)
        if (len(panel_items) == 0 and notify):
            self.view.show_popup('No imports found for `<strong>{0}</strong>`'.format(name))
            return
        if (len(panel_items) == 1):
            item = match_items[0]
            self.view.run_command('paste_import', {'item': item, 'typescript_paths': typescript_paths})
            return
        on_done = on_done_func(match_items, self.on_select)
        self.view.window().show_quick_panel(panel_items, on_done)
        
    def on_select(self, selected_item):
        debug('Selected item', selected_item)
        self.view.run_command('paste_import', {'item': selected_item, 'typescript_paths': typescript_paths})
