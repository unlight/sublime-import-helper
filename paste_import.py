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
        if len(from_paths) > 1:
            choices = [{'item': item, 'path': path} for path in from_paths]
            def on_select(selected):
                item = selected.get('item')
                item['module'] = selected.get('path')
                self.view.run_command('paste_import', {'item': item, 'typescript_paths': []})
            self.view.window().show_quick_panel(from_paths, on_done_func(choices, on_select))
            return
        from_quote = get_setting('from_quote', "'")
        import_end = ';' if get_setting('from_semicolon', True) else ''
        import_string = "import {{0}} from {0}{{1}}{0}{1}\n".format(from_quote, import_end)
        name = item['name']
        if item.get('from_package') == True:
            name = get_identifier_name(name)
        import_info = self.get_import_info(item, from_paths)
        debug('paste_import: import_info', import_info)
        from_path = import_info['from_path']
        if not import_info.get('line_region') or item['isDefault']:
            if import_info.get('default_all') == True and item['isDefault']:
                row = import_info.get('last_import_row')
                line_region = self.view.full_line(self.view.text_point(row, 0))
                line_contents = self.view.substr(line_region)
                if is_import_default(line_contents):
                    import_string = import_string.format('* as ' + name, from_path)
                else:
                    import_string = import_string.format(name, from_path)
                self.view.replace(edit, line_region, import_string)
                return
            if not item['isDefault']:
                name = wrap_imports([name])
            import_string = import_string.format(name, from_path)
            debug('paste_import: import_string', import_string)
            pos = 0
            if 'end' == get_setting('insert_position', 'end'):
                pos = self.view.text_point(import_info['last_import_row'] + 1, 0)
            self.view.insert(edit, pos, import_string)
            return
        imports = import_info['imports']
        line_region = import_info['line_region']
        try: imports.remove(name)
        except: pass
        imports.append(name)
        name = wrap_imports(imports)
        import_string = import_string.format(name, from_path)
        debug('paste_import: import_string', import_string)
        self.view.replace(edit, line_region, import_string)

    def get_import_info(self, item, from_paths):
        is_default_import = item.get('isDefault') == True
        from_path = from_paths[0];
        row = -1
        found = False
        last_row = self.view.rowcol(self.view.size())[0]
        last_import_row = row
        while row <= last_row:
            row = row + 1
            line_region = self.view.full_line(self.view.text_point(row, 0))
            line_contents = self.view.substr(line_region)
            match = re.search(r"^import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            if match and is_default_import == bool(is_import_default(line_contents) or is_import_all(line_contents)):
                last_import_row = row
                test_path = match.group(3)
                for from_path in from_paths:
                    if test_path == from_path:
                        debug('get_import_info: found from_path', from_path)
                        found = True
                        break
                if found:
                    break
        if not found:
            from_path = from_paths[0];
            return {'from_path': from_path, 'last_import_row': last_import_row, 'found': False}
        dirty_names = match.group(1)
        if dirty_names[0] != '{' and dirty_names[-1] != '}':
            # Found unexpected statement.
            return {'from_path': from_path, 'last_import_row': last_import_row, 'default_all': True, 'found': True}
        else:
            imports = []
            for m in re.finditer(r"(\w+(\s+as\s+\w+)?)", dirty_names):
                imports.append(m.group(1))
            return {'from_path': from_path, 'found': True, 'imports': imports, 'line_region': line_region, 'last_import_row': last_import_row}

