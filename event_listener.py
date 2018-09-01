import sublime_plugin
from .import_helper import node_modules, source_modules, update_source_modules
from .utils import *

class ImportHelperEventListener(sublime_plugin.EventListener):

    def __init__(self):
        self.viewIds = []

    def on_new(self, view):
        self.viewIds.append(view.id())

    def on_post_save(self, view):
        if view.id() in self.viewIds:
            self.viewIds.remove(view.id())
            update_source_modules()