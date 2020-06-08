is_debug = True


def debug(s, data=None, force=False):
    if is_debug or force:
        message = str(s)
        if data is not None:
            message = "--- " + message + " ---" + "\n" + str(data)
        print(message)
        print()
