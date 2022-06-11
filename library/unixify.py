def unixify(path, extension_option="remove"):
    path = path.replace("\\", "/")

    if extension_option == "as_is":
        return path

    extension = tjsx_extension(path)

    if type(extension) == str:
        if extension_option == "remove":
            return path[0 : -len(extension)]
        elif extension_option == "js":
            return path[0 : -len(extension)] + ".js"

    return path


def tjsx_extension(path):
    ext3 = path[-3:]
    if ext3 == ".ts" or ext3 == ".js":
        return ext3
    ext4 = path[-4:]
    if ext4 == ".tsx" or ext4 == ".jsx":
        return ext4
