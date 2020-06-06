from ..import_helper import DEBUG


def debug(s, data=None, force=False):
    if DEBUG or force:
        message = str(s)
        if data is not None:
            message = "--- " + message + " ---" + "\n" + str(data)
        print(message)
