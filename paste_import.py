import sublime
import sublime_plugin
import os
import re
from .utils import *

# view.run_command('paste_import', args=({'item': {'filepath': 'xxx', 'name': 'aaa', 'isDefault': False}, 'typescript_paths': []}))
# view.run_command('paste_import', args=({'item': {'isDefault': True, 'module': 'worker_threads', 'name': 'worker_threads'}}))

class PasteImportCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super().__init__(view)

    def run(self, edit, item, typescript_paths = []):
        debug('paste_import: item', item)
        file_name = self.view.file_name() or '.'
        from_paths = get_from_paths(item, file_name, typescript_paths)
        if len(from_paths) == 0:
            raise Exception('len from_paths must be not empty')
        if len(from_paths) > 1:
            choices = [{'item': item, 'path': path} for path in from_paths]
            def on_select(selected):
                item = selected.get('item')
                item['module'] = selected.get('path')
                self.view.run_command('paste_import', {'item': item, 'typescript_paths': []})
            self.view.window().show_quick_panel(from_paths, on_done_func(choices, on_select))
            return
        # Get import line information
        from_path = from_paths[0]
        import_line_info = get_import_line_info(self.view, from_path)
        debug('paste_import: import_line_info', import_line_info)
        # Prepare import string template
        from_quote = get_setting('from_quote', "'")
        import_end = ';' if get_setting('from_semicolon', True) else ''
        import_string = 'import {{0}} from {0}{2}{0}{1}\n'.format(from_quote, import_end, from_path)
        # Name to import
        name = item['name']
        if item.get('from_package') == True:
            name = get_identifier_name(name)
        # Not found in existing paths
        if (import_line_info['import_row'] == -1):
            pos = 0
            if 'end' == get_setting('insert_position', 'end'):
                pos = self.view.text_point(import_line_info['last_import_row'] + 1, 0)
            if not item['isDefault']:
                name = wrap_imports([name])
            self.view.insert(edit, pos, import_string.format(name))
            return
        # Found import default
        if (import_line_info['import_row'] != -1 and item['isDefault']):
            if is_import_default(import_line_info['line_contents']):
                name = '* as ' + name
            line_region = self.view.full_line(self.view.text_point(import_line_info['import_row'], 0))
            self.view.replace(edit, line_region, import_string.format(name))
            return
        # Regular import
        imports = import_line_info['imports']
        try: imports.remove(name)
        except: pass
        imports.append(name)
        line_region = self.view.full_line(self.view.text_point(import_line_info['import_row'], 0))
        name = wrap_imports(imports)
        self.view.replace(edit, line_region, import_string.format(name))
