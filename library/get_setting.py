import sublime


def get_setting(name, default, settings={}):
    result = settings.get(name)
    if result is not None:
        return result
    project_data = sublime.active_window().project_data()
    if project_data is not None:
        result = project_data.get(name)
    if result is None:
        settings = sublime.load_settings("import_helper.sublime-settings") or {}
        result = settings.get(name)
    if result is None:
        preferences = sublime.load_settings("Preferences.sublime-settings")
        result = preferences.get(name)
    if result is None:
        result = default
    return result
