import os
from .get_setting import get_setting


def try_typescript_path(filepath, typescript_paths):
    import_path_mapping = get_setting("import_path_mapping", "none")
    if import_path_mapping == "enabled":
        (drive, filepath) = os.path.splitdrive(filepath)
        filepath = filepath.replace("\\", "/")
        # debug("filepath", filepath)
        for ts_path in typescript_paths:
            base_dir = ts_path["base_dir"]
            path_value = ts_path["path_value"]
            path_to = ts_path["path_to"]
            (drive, test_path) = os.path.splitdrive(
                os.path.normpath(os.path.join(base_dir, path_value)).replace("\\", "/")
            )
            # debug("test_path", test_path)
            # "@app/*" :["app/*"]
            if test_path[-2:] == "/*" and path_to[-2:] == "/*":
                test_path = test_path[0:-2]
                if filepath.startswith(test_path):
                    test_path = path_to[0:-2] + filepath[len(test_path) :]
                    return test_path
            # "@lib": ["app/lib"]
            if filepath == test_path or filepath in [
                test_path + "/index.ts",
                test_path + "/index.tsx",
                test_path + "/index.js",
                test_path + "/index.jsx",
            ]:
                return path_to
    return None
