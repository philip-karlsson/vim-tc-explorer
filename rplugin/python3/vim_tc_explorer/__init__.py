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
        self.TcExplorer = vim_tc_explorer(nvim, log=False)

    @neovim.command("Tc", range='', nargs='*', sync=True)
    def tc_explore(self, args, range):
        self.TcExplorer.tc_explore(args, range)

    @neovim.command("TcExpEnter", range='', nargs='*', sync=True)
    def tc_enter(self, args, range):
        self.TcExplorer.tc_enter(args, range)

    @neovim.command("TcExpUp", range='', nargs='*', sync=True)
    def tc_up(self, args, range):
        self.TcExplorer.tc_up(args, range)

    @neovim.command("TcExpDown", range='', nargs='*', sync=True)
    def tc_down(self, args, range):
        self.TcExplorer.tc_down(args, range)

    @neovim.command("TcExpClose", range='', nargs='*', sync=True)
    def tc_close(self, args, range):
        self.TcExplorer.tc_close(args, range)

    @neovim.autocmd("TextChangedI", pattern='TC_Input', sync=True)
    def insert_changed(self):
        self.TcExplorer.handle_input()
