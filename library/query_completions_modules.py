def query_completions_modules(prefix, source_modules, node_modules):
    result = []
    for item in source_modules:
        name = item.get("name")
        if name is None:
            continue
        if not name.startswith(prefix):
            continue
        result.append([name + "\tsource_modules", name])
    for item in node_modules:
        name = item.get("name")
        module = item.get("module")
        if name is None or module is None:
            continue
        if not name.startswith(prefix):
            continue
        result.append([name + "\tnode_modules/" + module, name])
    return result
