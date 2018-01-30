# ============================================================================
# FILE: searcher.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os


class searcher(object):
    def __init__(self, nvim, buffer):
        self.nvim = nvim
        self.buffer = buffer
        # Attribute to distinguish from explorer
        self.isSearcher = True

    def groupResults(self):
        pass

    def search(self, dir, filePattern, inputPattern):
        self.prevbuffer = self.nvim.current.buffer
        self.nvim.current.buffer = self.buffer
        self.dir = dir
        self.inputPattern = inputPattern
        self.filePattern = filePattern
        self.command = "cd %s && " % dir
        if(not filePattern.startswith('-')):
                filePattern = '-t' + filePattern
        if(inputPattern is not ''):
            self.command += "rg %s %s --vimgrep" % (filePattern, inputPattern)
        else:
            filePattern = filePattern.replace('-t', '-g')
            self.command += "rg %s --files" % (filePattern)
        self.buffer[:] = []
        self.nvim.command("r !\"%s\"" % self.command)
        self.buffer.append(self.command)
        self.nvim.current.buffer = self.prevbuffer

    def updateListing(self, pattern):
        pass

    def changeSelection(self, offset):
        pass

    def draw(self):
        pass
