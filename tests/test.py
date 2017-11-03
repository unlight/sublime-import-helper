import sublime
import sys
from unittest import TestCase
import_helper = sys.modules['ImportHelper.import_helper']

class TestDoInsertImport(TestCase):
    
    def setUp(self):
        self.view = sublime.active_window().new_file()
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_smoke(self):
        self.setText('')
        self.view.run_command('do_insert_import', {'item': {'filepath': 'dinah_widdoes', 'name': 'Lakia', 'isDefault': False}})
        first_row = self.getRow(0)
        self.assertTrue(first_row.startswith('import {'))
        self.assertIn('}', first_row)
        self.assertIn('Lakia', first_row)
        self.assertIn('dinah_widdoes', first_row)

class TestUpdateImports(TestCase):
    # window.run_command('update_imports')

    def setUp(self):
        self.window = sublime.active_window()
        self.window.run_command('update_imports')

    def test_check_node_modules(self):
        yield 5000
        self.assertNotEqual(len(import_helper.node_modules), 0)

    def test_check_source_modules(self):
        yield 1000
        self.assertNotEqual(len(import_helper.source_modules), 0)

    def test_exclude_should_work(self):
        ignored = [item for item in import_helper.source_modules if 'ignored' in item['filepath']]
        self.assertEqual(len(ignored), 0)

class TestUtilFunctions(TestCase):

    def test_debug_disabled(self):
        self.assertFalse(import_helper.DEBUG)

    def test_run_path_should_point_to_debug_version(self):
        run_path = import_helper.RUN_PATH
        self.assertIn('backend_run', run_path)

    def test_unixify(self):
        unixify = import_helper.unixify
        _ = '\\local\\some\\file'
        self.assertTrue(unixify(_) == '/local/some/file')
        
    def test_unixify_ts(self):
        unixify = import_helper.unixify
        _ = 'some\\file.ts'
        self.assertTrue(unixify(_) == 'some/file')
        
    def test_unixify_tsx(self):
        unixify = import_helper.unixify
        path = 'd/file.tsx'
        self.assertTrue(unixify(path) == 'd/file')

    def test_unixify_js(self):
        unixify = import_helper.unixify
        _ = 'some\\file.js'
        self.assertTrue(unixify(_) == 'some/file')

    def test_is_excluded_file(self):
        is_excluded_file = import_helper.is_excluded_file
        self.assertTrue(is_excluded_file('dir/file1.ts', ['*.ts']))
        self.assertTrue(is_excluded_file('dir1/file1.ts', ['dir1']))

    def test_get_setting(self):
        get_setting = import_helper.get_setting
        self.assertEqual(get_setting('insert_position', None), 'end')
        self.assertEqual(get_setting('from_quote', None), "'")
        self.assertEqual(get_setting('space_around_braces', None), False)
        self.assertEqual(get_setting('unknown', 'default_value'), 'default_value')

    def test_get_import_root(self):
        get_import_root = import_helper.get_import_root
        result = get_import_root()
        self.assertTrue('ImportHelper' in result)

class TestUnsedImports(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_partial_as(self):
        self.setText("import { FullName as f, createname as cr } from './createname'; // Partial")
        self.view.run_command('edit_remove_unsed_imports', args=({'data': {"1":[{"line":1,"pos":22,"name":"f"}]}}))
        first_row = self.getRow(0)
        self.assertEqual(first_row, "import { createname as cr } from './createname'; // Partial")

    def test_unused_all(self):
        self.setText("import {a, b, xx as c} from './createname';  // Unused all")
        line1 = [{"line":1,"name":"a"}, {"line":1,"name":"b"}, {"line":1,"name":"c"}]
        self.view.run_command('edit_remove_unsed_imports', args=({'data': {"1":line1}}))
        first_row = self.getRow(0)
        self.assertEqual(first_row, "")

    def test_unused_single_as(self):
        self.setText("import { Greeter as gr } from './greeter'; // Unused")
        line1 = [{"line":1,"name":"gr"}]
        self.view.run_command('edit_remove_unsed_imports', args=({'data': {"1":line1}}))
        first_row = self.getRow(0)
        self.assertEqual(first_row, "")

    def test_used_should_not_be_removed(self):
        self.setText("import {a} from './greeter';\nimport { b } from './greeter';")
        line1 = [{"line":1,"name":"a"}]
        self.view.run_command('edit_remove_unsed_imports', args=({'data': {"1":line1}}))
        first_row = self.getRow(0)
        self.assertEqual(first_row, "import { b } from './greeter';")

class TestExample(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_smoke(self):
        self.assertTrue(True)
        
    def test_hello_world(self):
        self.view.run_command("hello_world")
        first_row = self.getRow(0)
