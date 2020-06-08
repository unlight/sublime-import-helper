import os

# Return the longest common sub-path of the sequence of paths given as input.
# The paths are not normalized before comparing them (this is the
# responsibility of the caller). Any trailing separator is stripped from the
# returned path.


def common_path(paths):
    """Given a sequence of path names, returns the longest common sub-path."""
    if not paths:
        raise ValueError("common_path() arg is an empty sequence")
    sep = "/"
    curdir = "."

    try:
        (isabs,) = set(p[:1] == sep for p in paths)
    except ValueError:
        raise ValueError("Can't mix absolute and relative paths") from None

    split_paths = []
    for path in paths:
        path = path.replace("\\", sep)
        if os.name == "nt":
            path = path.lower()
        parts = path.split(sep)
        split_paths.append(parts)

    split_paths = [[c for c in s if c and c != curdir] for s in split_paths]
    s1 = min(split_paths)
    s2 = max(split_paths)
    common = s1
    for i, c in enumerate(s1):
        if c != s2[i]:
            common = s1[:i]
            break

    prefix = sep if isabs else sep[:0]
    result = prefix + sep.join(common)
    return result
