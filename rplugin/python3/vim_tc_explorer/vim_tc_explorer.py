# ============================================================================
# FILE: vim_tc_explorer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
from vim_tc_explorer.explorer import explorer


class vim_tc_explorer(object):
    """ Main class for the plugin, manages
        the input commands and the spawning of
        explorers """
    def __init__(self, nvim, log=False):
        self.nvim = nvim
        # Setup debugging
        self.useLogging = log
        if(self.useLogging):
            self.nvim.command('e TC_Debug')
            self.logBuffer = self.nvim.current.buffer
            self.nvim.command('setlocal buftype=nofile')
            self.nvim.command('setlocal filetype=vim_tc_input')
            self.nvim.command('normal! bn')
        # Start the explorer in cwd
        self.cwd = os.path.abspath(os.getcwd())
        # Create both explorers but only show one depending on cmd?
        self.explorers = []
        self.explorers.append(explorer(self.cwd))
        self.explorers.append(explorer(self.cwd))
        # Index to keep track of which explorer that is currently selected
        self.selectedExplorer = 0

# ============================================================================
# Helpers
# ============================================================================
    def log(self, msg):
        if(self.useLogging):
            self.logBuffer.append(msg)

    def close(self, withFile=True):
        # Method used to close the plugin
        # Delete both buffers
        self.nvim.command('stopinsert')
        if(withFile is False):
            # Shift to the OG buffer
            self.nvim.current.buffer = self.ogBuffer
        self.nvim.command('bd %s' % self.explorerBufferNumberOne)
        if(self.explorerBufferNumberTwo is not None):
            self.nvim.command('bd %s' % self.explorerBufferNumberTwo)
        self.nvim.command('bd %s' % self.inputBufferNumber)

# ============================================================================
# Commands
# ============================================================================
    def tc_explore(self, args, range):
        """ Single pane explorer """
        self.numExplorers = 1
        self.selectedExplorer = 0
        # Remember the OG buffer
        self.ogBuffer = self.nvim.current.buffer
        # Create the input buffer
        self.nvim.command('e TC_Input')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_input')
        # Might be wrong bcz ref
        self.inputBufferNumber = self.nvim.current.buffer.number

        # Create the explorer buffer
        self.nvim.command('split TC_Explorer')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        self.explorerBufferNumberOne = self.nvim.current.buffer.number
        # Only one explorer
        self.explorerBufferNumberTwo = None
        exp = self.explorers[self.selectedExplorer]
        exp.assignBuffer(self.nvim.buffers[self.explorerBufferNumberOne])
        # Go back to the input buffer window
        self.nvim.command('wincmd j')
        # FIXME: Add one more line for quick help
        self.nvim.current.window.height = 1
        # Change to input buffer
        self.nvim.current.buffer = self.nvim.buffers[self.inputBufferNumber]
        self.nvim.command("startinsert!")
        # Remap keys for the input layer
        # Enter
        self.nvim.command("inoremap <buffer> <CR> <ESC>:TcExpEnter<CR>")
        # Backspace
        self.nvim.command("inoremap <buffer> <BS> %")
        # Up
        self.nvim.command("inoremap <buffer> <C-k> <ESC>:TcExpUp<CR>")
        # Down
        self.nvim.command("inoremap <buffer> <C-j> <ESC>:TcExpDown<CR>")
        # Close
        self.nvim.command("inoremap <buffer> <C-q> <ESC>:TcExpClose<CR>")
        # Draw first frame
        self.explorers[self.selectedExplorer].draw()

    def tc_explore_dual(self, args, range):
        """ Single pane explorer """
        self.numExplorers = 2
        self.selectedExplorer = 0
        # Remember the OG buffer
        self.ogBuffer = self.nvim.current.buffer
        # Create the input buffer
        self.nvim.command('e TC_Input')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_input')
        # Might be wrong bcz ref
        self.inputBufferNumber = self.nvim.current.buffer.number

        # Create the explorer buffers
        self.nvim.command('split TC_Explorer_2')  # 2 Bcz split, (inverted)
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        self.explorerBufferNumberOne = self.nvim.current.buffer.number
        exp = self.explorers[0]
        exp.assignBuffer(self.nvim.buffers[self.explorerBufferNumberOne])
        # Two explorers
        self.nvim.command('vsplit TC_Explorer_1')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        self.explorerBufferNumberTwo = self.nvim.current.buffer.number
        exp = self.explorers[1]
        exp.assignBuffer(self.nvim.buffers[self.explorerBufferNumberTwo])
        # Go back to the input buffer window
        self.nvim.command('wincmd j')
        # FIXME: Add one more line for quick help
        self.nvim.current.window.height = 1
        # Change to input buffer
        self.nvim.current.buffer = self.nvim.buffers[self.inputBufferNumber]
        self.nvim.command("startinsert!")
        # Remap keys for the input layer
        # Enter
        self.nvim.command("inoremap <buffer> <CR> <ESC>:TcExpEnter<CR>")
        # Backspace
        self.nvim.command("inoremap <buffer> <BS> %")
        # Up
        self.nvim.command("inoremap <buffer> <C-k> <ESC>:TcExpUp<CR>")
        # Down
        self.nvim.command("inoremap <buffer> <C-j> <ESC>:TcExpDown<CR>")
        # Tab
        self.nvim.command("inoremap <buffer> <tab> <ESC>:TcExpTab<CR>")
        # Close
        self.nvim.command("inoremap <buffer> <C-q> <ESC>:TcExpClose<CR>")
        # Draw first frame
        self.explorers[self.selectedExplorer].active = True
        self.explorers[0].draw()
        self.explorers[1].draw()

# ============================================================================
# Handlers
# ============================================================================
    def tc_enter(self, args, range):
        # Handle enter
        exp = self.explorers[self.selectedExplorer]
        selFile = exp.getSelected()
        if os.path.isdir(os.path.join(exp.cwd,
                         selFile)):
            exp.cd(selFile)
            exp.draw()
            # Clear the line
            self.nvim.current.line = ''
            self.nvim.command('startinsert')
        else:
            # Need to solve this part to get syntax, something with the nested
            filePath = os.path.join(exp.cwd, selFile)
            self.nvim.command('e %s' % os.path.abspath(filePath))
            self.close()
            return

    def tc_up(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.changeSelection(-1)
        exp.draw()
        self.nvim.command('startinsert')

    def tc_down(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.changeSelection(1)
        exp.draw()
        self.nvim.command('startinsert')

    def tc_tab(self, args, range):
        if(self.numExplorers > 1):
            if(self.selectedExplorer == 1):
                self.selectedExplorer = 0
                self.explorers[0].active = True
                self.explorers[1].active = False
            else:
                self.selectedExplorer = 1
                self.explorers[0].active = False
                self.explorers[1].active = True
            self.explorers[0].draw()
            self.explorers[1].draw()
        self.nvim.command('startinsert')

    def tc_close(self, args, range):
        self.close()

    def handle_input(self):
        """ Input handler for filter """
        exp = self.explorers[self.selectedExplorer]
        inputLine = self.nvim.current.line
        # Check for backspace
        if inputLine.endswith('%'):
            inputLine = inputLine.replace("%", "")
            # Handle backspace
            if not inputLine:
                # Change directory to the parrent
                exp.cd('..')
            inputLine = inputLine[:-1]
        # FIXME: These matches shall be commands instead, just like for "enter"
        elif inputLine.endswith('!'):
            inputLine = inputLine.replace("!", "")
            # Handle selection up
            exp.changeSelection(-1)
        elif inputLine.endswith('@'):
            inputLine = inputLine.replace("@", "")
            # Handle selection down
            exp.changeSelection(1)
        elif inputLine.endswith('?'):
            # Close
            self.close(False)
            return
        self.nvim.current.line = inputLine
        exp.updateListing(inputLine)
        # Draw
        exp.draw()
