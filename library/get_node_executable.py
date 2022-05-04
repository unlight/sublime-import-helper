from .get_setting import get_setting
from .find_executable import find_executable


def get_node_executable():
    node_executable = get_setting("node_bin", "")
    if not bool(node_executable):
        node_executable = find_executable("node")
    if not bool(node_executable):
        node_executable = "node"

    return node_executable
