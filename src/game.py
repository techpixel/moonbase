import curses
import time
import getkey
from curses.textpad import Textbox, rectangle

class Termtype:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()

        self.track = 0

        self.editwin = curses.newwin(1, 50, 2, 1)
        self.logwin = curses.newwin(20, 50, 4, 1)

        self.screen.addstr(0, 1, "Moonbase Alpha", curses.A_BOLD)
        self.screen.addstr(" Command Shell")

        self.setup()
        self.screen.refresh()

        self.box = Textbox(self.editwin)


    def print(self, text, x=None, y=None, attr=None):
        try:
            if not (x or y):
                if attr:
                    self.logwin.addstr(self.track, 0, text, attr)
                else:
                    self.logwin.addstr(self.track, 0, text)
                self.track += 1
            else:
                self.logwin.addstr(y, x, text + '\n')
            self.logwin.refresh()
        except:
            self.logwin.erase()

    def slowprint(self, text, interval=0.05, y=None, x=None):
        for char in text:
            time.sleep(interval)
            self.logwin.addch(char)
            self.logwin.refresh()
        self.logwin.addch('\n')
        self.track += 1
    
    def clear(self):
        self.logwin.erase()
        self.track = 0

    def input(self):
        self.box.edit(validate=Termtype._validator)
        # Get resulting contents
        return self.box.gather()[:-1]

    def _validator(chr):
        if chr == getkey.keys.ENTER:
            return 0x07
        else:
            return chr

    def setup(self):
        rectangle(self.screen, 1,0, 3, 51)

    def close(self):
        curses.endwin()

def main():
    import time

    display = Termtype()

    display.slowprint('Initalizing...')
    display.slowprint('Getting Status Report...')
    display.slowprint('Running Checks...')
    display.slowprint('Updating Runtime...')

    time.sleep(0.5)

    display.clear()
    display.print('Moonbase Alpha', attr=curses.A_BOLD)
    
    index = display.menu(["Hello", "World"])