import sublime
import sublime_plugin
import os
import re
from .utils import *

# view.run_command('do_insert_import', args=({'item': {'filepath': 'xxx', 'name': 'aaa', 'isDefault': False}, 'typescript_paths': []}))
# view.run_command('do_insert_import', args=({'name': 'AbcComponent', 'filepath': 'D:\\Progs\\Sublime-Text-3\\Data\\Packages\\ImportHelper\\test_playground\\component\\abc.component.ts', 'isDefault': False}))

class DoInsertImportCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super().__init__(view)

    def run(self, edit, item, typescript_paths = []):
        if (item.get('module')):
            from_path = item['module']
        else:
            typescript_path = self.try_typescript_path(item['filepath'], typescript_paths)
            if typescript_path is not None:
                from_path = unixify(typescript_path)
            else:
                file_name = self.view.file_name() or '.'
                from_path = os.path.relpath(item['filepath'], os.path.dirname(file_name))
                from_path = unixify(from_path)
                if from_path[0] != '.':
                    from_path = './' + from_path
        from_quote = get_setting('from_quote', "'")
        import_end = ';' if get_setting('from_semicolon', True) else ''
        import_string = "import {{0}} from {0}{{1}}{0}{1}\n".format(from_quote, import_end)
        name = item['name']
        import_info = self.get_import_info(from_path)
        debug("import_info", import_info)
        if not import_info.get('line_region') or item['isDefault']:
            if not item['isDefault']:
                name = self.wrap_imports([name])
            import_string = import_string.format(name, from_path)
            debug('Import string', import_string)
            pos = 0
            if 'end' == get_setting('insert_position', 'end'):
                pos = self.view.text_point(import_info['last_import_row'] + 1, 0)
            self.view.insert(edit, pos, import_string)
        else:
            imports = import_info['imports']
            line_region = import_info['line_region']
            try: imports.remove(name)
            except: pass
            imports.append(name)
            name = self.wrap_imports(imports)
            import_string = import_string.format(name, from_path)
            debug('Import string', import_string)
            self.view.replace(edit, line_region, import_string)

    def get_import_info(self, from_path):
        row = -1
        found = False
        last_row = self.view.rowcol(self.view.size())[0]
        last_import_row = row
        while row <= last_row:
            row = row + 1
            line_region = self.view.full_line(self.view.text_point(row, 0))
            line_contents = self.view.substr(line_region)
            match = re.search(r"^import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            # match = re.search(r"import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            if match:
                last_import_row = row
                if match.group(3) == from_path:
                    found = True
                    break
        if not found:
            return {'last_import_row': last_import_row}
        dirty_names = match.group(1)
        if dirty_names[0] != '{' and dirty_names[-1] != '}':
            # Found unexpected statement.
            return {'last_import_row': last_import_row}
        else:
            imports = []
            for m in re.finditer(r"(\w+(\s+as\s+\w+)?)", dirty_names):
                imports.append(m.group(1))
            return {'imports': imports, 'line_region': line_region, 'last_import_row': last_import_row}

    def wrap_imports(self, imports):
        start = '{'
        end = '}'
        if get_setting('space_around_braces', True):
            start = start + ' '
            end = ' ' + end
        return start + ', '.join(imports) + end

    def is_spaced_import(self, statement):
        return statement.startswith('{ ')

    def try_typescript_path(self, filepath, typescript_paths):
        import_path_mapping = get_setting('import_path_mapping', 'none')
        if import_path_mapping == 'enabled':
            (drive, filepath) = os.path.splitdrive(filepath)
            filepath = filepath.replace('\\', '/')
            # debug("filepath", filepath)
            for ts_path in typescript_paths:
                base_dir = ts_path['base_dir']
                path_value = ts_path['path_value']
                path_to = ts_path['path_to']
                (drive, test_path) = os.path.splitdrive(os.path.normpath(os.path.join(base_dir, path_value)).replace('\\', '/'))
                # debug("test_path", test_path)
                # "@app/*" :["app/*"]
                if test_path[-2:] == '/*' and path_to[-2:] == '/*':
                    test_path = test_path[0:-2]
                    if filepath.startswith(test_path):
                        test_path = path_to[0:-2] + filepath[len(test_path):]
                        return test_path
                # "@lib": ["app/lib"]
                if filepath == test_path or filepath in [test_path + '/index.ts', test_path + '/index.tsx', test_path + '/index.js', test_path + '/index.jsx']:
                    return path_to
        return None
