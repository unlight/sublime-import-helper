def get_modules_callback(err, result, sender=None):
    if err:
        sublime.error_message("{0}:\n{1}".format(PROJECT_NAME, str(err)))
        return
    if type(result) is not list:
        sublime.error_message(
            "{0}:\nUnexpected type of result: {1}".format(PROJECT_NAME, type(result))
        )
        return
    node_modules.extend(result)
    message = "{0}: {1} node modules found".format(PROJECT_NAME, len(node_modules))
    if sender is not None:
        message = message + ", {0} +{1}".format(sender["name"], sender["count"])
    sublime.status_message(message)
    debug("get_modules_callback: len(result)", len(result))
