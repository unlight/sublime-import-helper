import sublime
import sublime_plugin
import os
import re


# view.run_command('paste_import', args=({'item': {'filepath': 'xxx', 'name': 'aaa', 'isDefault': False}, 'typescript_paths': []}))
# view.run_command('paste_import', args=({'item': {'isDefault': True, 'module': 'worker_threads', 'name': 'worker_threads'}}))
