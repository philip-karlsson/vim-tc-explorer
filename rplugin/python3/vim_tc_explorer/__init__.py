# ============================================================================
# FILE: __init__.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================

import neovim
from vim_tc_explorer.vim_tc_explorer import vim_tc_explorer


@neovim.plugin
class VimTcExplorerHandlers(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.TcExplorer = vim_tc_explorer(nvim)

    @neovim.command("Tc", range='', nargs='*', sync=True)
    def tc_explore(self, args, range):
        self.TcExplorer.tc_explore(args, range)

    @neovim.command("TcExpEnter", range='', nargs='*', sync=True)
    def tc_enter(self, args, range):
        self.TcExplorer.tc_enter(args, range)

    @neovim.autocmd("TextChangedI", pattern='TC_Input', sync=True)
    def on_insert_enter(self):
        self.TcExplorer.on_insert_enter()
