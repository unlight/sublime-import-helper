def update_typescript_paths():
    typescript_paths.clear()
    # source_folders = get_source_folders()
    source_folders = [get_import_root()]
    for folder in source_folders:
        tsconfig_file = os.path.normpath(os.path.join(folder, "tsconfig.json"))
        if not os.path.isfile(tsconfig_file):
            continue
        tsconfig = read_json(tsconfig_file) or {}
        compilerOptions = tsconfig.get("compilerOptions")
        if compilerOptions is None:
            continue
        baseUrl = compilerOptions.get("baseUrl")
        if baseUrl is None:
            continue
        base_dir = os.path.normpath(
            os.path.join(os.path.dirname(tsconfig_file), baseUrl)
        )
        paths = compilerOptions.get("paths")
        if not paths:
            continue
        for path_to, pathValues in paths.items():
            for path_value in pathValues:
                typescript_paths.append(
                    {"base_dir": base_dir, "path_value": path_value, "path_to": path_to}
                )
    debug("typescript_paths", typescript_paths)
