# ============================================================================
# FILE: searcher.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os


class resultGroup(object):
    def __init__(self, fileName):
        self.lines = []
        self.matches = 0
        self.fileName = fileName


class searcher(object):
    def __init__(self, nvim, buffer):
        self.nvim = nvim
        self.buffer = buffer
        # Attribute to distinguish from explorer
        self.isSearcher = True

    def createResultStructure(self):
        self.results = {}
        for line in self.buffer[1:len(self.buffer)]:
            # Process each line
            f = line.split(':')
            if(f is not None):
                if(not f[0] in self.results):
                    self.results[f[0]] = resultGroup(f[0])
                self.results[f[0]].lines.append(line)
                self.results[f[0]].matches += 1

    def search(self, dir, filePattern, inputPattern):
        self.prevbuffer = self.nvim.current.buffer
        self.nvim.current.buffer = self.buffer
        self.nvim.command('setlocal filetype=vim_tc_search_result')
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
        self.nvim.current.buffer = self.prevbuffer
        self.createResultStructure()

    def updateListing(self, pattern):
        pass

    def changeSelection(self, offset):
        pass

    def draw(self):
        fLines = []
        for f in self.results:
            fLines.append('+' + f + ' | %s matches' % self.results[f].matches)
        self.buffer[:] = fLines
        # Debug
        # self.buffer.append(self.command)
