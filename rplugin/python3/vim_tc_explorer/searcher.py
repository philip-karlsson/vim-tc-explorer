# ============================================================================
# FILE: searcher.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================


class searcher(object):
    def __init__(self, buffer):
        self.buffer = buffer
        # Attribute to distinguish from explorer
        self.isSearcher = True

    def search(self, dir, inputPattern, filePattern):
        pass

    def updateListing(self, pattern):
        pass

    def changeSelection(self, offset):
        pass

    def draw(self):
        buf = self.buffer
        buf[:] = []
        buf.append('hello world from searcher')
