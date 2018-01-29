# ============================================================================
# FILE: explorer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
from vim_tc_explorer.filter import filter


class explorer(object):
    """ Class for an explorer that is used in the panes """
    def __init__(self, cwd):
        # Instance of the filter
        self.filter = filter()
        self.cwd = cwd
        # The the current files
        self.currentFiles = os.listdir(self.cwd)
        self.fileredFiles = self.currentFiles
        # Index that tracks which file that is selected
        self.selected = 0

    def assignBuffer(self, buffer):
        self.buffer = buffer

    def draw(self):
        explorer = self.buffer
        explorer[:] = ['==== TC explorer (alpha) ===']
        # Draw current path
        explorer.append(self.cwd)
        explorer.append('----------------------------')
        # FIXME: Add coloring
        for idx, val in enumerate(self.fileredFiles):
            if idx == self.selected:
                token = "===> "
            else:
                token = "     "
            explorer.append(token + val)

    def cd(self, path):
        self.cwd = os.path.abspath(os.path.join(self.cwd, path))
        self.currentFiles = os.listdir(self.cwd)
        self.fileredFiles = self.currentFiles[:]
        self.changeSelection(0)

    def updateListing(self, pattern):
        self.filter.filter(self.currentFiles, pattern, self.fileredFiles)
        self.changeSelection(0)

    def changeSelection(self, offset):
        self.selected += offset
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.fileredFiles):
            self.selected = len(self.fileredFiles)-1

    def getSelected(self):
        return self.fileredFiles[self.selected]
