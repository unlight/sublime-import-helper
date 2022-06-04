def unixify(path, stripext=True):
    path = path.replace("\\", "/")
    if stripext:
        ext3 = path[-3:]
        if ext3 == ".ts" or ext3 == ".js":
            return path[0:-3]
        ext4 = path[-4:]
        if ext4 == ".tsx" or ext4 == ".jsx":
            return path[0:-4]
    return path
