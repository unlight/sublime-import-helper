import sublime
import sys
from unittest import TestCase

import_helper = sys.modules["ImportHelper.import_helper"]
get_import_root = sys.modules["ImportHelper.library.get_import_root"].get_import_root
common_path = sys.modules["ImportHelper.library.common_path"].common_path
unixify = sys.modules["ImportHelper.library.unixify"].unixify
panel_items = sys.modules["ImportHelper.library.panel_items"].panel_items
query_completions_modules = sys.modules[
    "ImportHelper.library.query_completions_modules"
].query_completions_modules
find_executable = sys.modules["ImportHelper.library.find_executable"].find_executable
get_setting = sys.modules["ImportHelper.library.get_setting"].get_setting
get_exclude_patterns = sys.modules[
    "ImportHelper.library.get_exclude_patterns"
].get_exclude_patterns


class TestLibraryFunctions(TestCase):
    def test_common_path_raises(self):
        self.assertRaises(ValueError, common_path, [])

    def test_common_path_1(self):
        result = common_path(["/usr/project1", "/usr/project2"])
        self.assertEqual(result, "/usr")

    def test_common_path_2(self):
        result = common_path(
            ["d:\\dev\\project\\server\\do", "d:\\dev\\project\\client"]
        )
        self.assertEqual(result, "d:/dev/project")

    def test_common_path_single_arg(self):
        result = common_path(["/usr/project"])
        self.assertEqual(result, "/usr/project")

    def test_get_import_root(self):
        get_import_root()

    def test_panel_items(self):
        import_root = "/usr"
        entry_modules = [
            {"name": "entry1", "filepath": "/usr/src/1"},
            {"name": "entry2", "filepath": "/usr/src/2"},
            {"name": "entry3", "filepath": "/usr/src/3"},
        ]
        (items, matches) = panel_items(
            entry_modules=entry_modules, import_root=import_root
        )
        self.assertEqual(len(items), 3)
        self.assertEqual(len(matches), 3)

    def test_panel_items_filter_by_name(self):
        import_root = "/usr"
        entry_modules = [
            {"name": "entry1", "filepath": "/usr/src/1"},
            {"name": "entry2", "filepath": "/usr/src/2"},
        ]
        (items, matches) = panel_items(
            name="entry1", entry_modules=entry_modules, import_root=import_root
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], "src/1/entry1")
        self.assertEqual(len(matches), 1)

    def test_unixify(self):
        testFile = "\\local\\some\\file"
        self.assertEqual(unixify(testFile), "/local/some/file")

    def test_unixify_ts(self):
        self.assertEqual(unixify("some\\file.ts"), "some/file")

    def test_unixify_tsx(self):
        self.assertEqual(unixify("d/file.tsx"), "d/file")

    def test_unixify_js(self):
        self.assertEqual(unixify("some\\file.js"), "some/file")

    def test_get_setting(self):
        self.assertEqual(get_setting("from_quote", None), "'")
        self.assertEqual(get_setting("unknown", "default_value"), "default_value")

    def test_find_executable(self):
        result = find_executable("node")
        self.assertNotEqual("node", result)

    def test_query_completions_modules(self):
        source_modules = [
            {"name": "good", "filepath": "/usr/home/good"},
            {"name": "ugly", "filepath": "/usr/home/ugly"},
        ]
        node_modules = [{"name": "Chicky", "module": "chicken"}]
        result = query_completions_modules("goo", source_modules, node_modules)
        self.assertListEqual(result, [["good\tsource_modules", "good"]])
        result = query_completions_modules("Chic", source_modules, node_modules)
        self.assertListEqual(result, [["Chicky\tnode_modules/chicken", "Chicky"]])

    def test_get_exclude_patterns_fault_tollerance(self):
        result = get_exclude_patterns({"folders": {}})
        self.assertDictEqual(result, {})
