import curses
import time, json, random

class GameDisplay:
    def __init__(self, title):
        self.title = title

        self.screen = curses.initscr()
        curses.noecho()

        self.titlewin = curses.newwin(1, 40, 0, 0)
        self.logwin = curses.newwin(15, 40, 1, 0)
        self.splitbar = curses.newwin(1, 40, 16, 0)
        self.statuswin = curses.newwin(10, 40, 17, 0)

        self.splitbar.addstr(' '*39, curses.A_REVERSE)
        self.splitbar.refresh()

        self.addtitle()

        self.track = 2

        self.logwin.refresh()

    def log(self, text, interval=0.05, attr=None):
        if attr:
            for char in text:
                self.logwin.addch(char, attr)
                time.sleep(interval)
                self.logwin.refresh()  
        else:
            for char in text:
                self.logwin.addch(char)
                time.sleep(interval)
                self.logwin.refresh()
        self.logwin.addch('\n')
        self.logwin.refresh()
    
    def statuswrite(self, text, yloc, attr=None):
        if attr:
            self.statuswin.addstr(yloc, 0, text, attr)
        else:
            self.statuswin.addstr(yloc, 0, text)
        self.statuswin.refresh()
    
    def statusclear(self):
        self.statuswin.erase()
        self.statuswin.refresh()

    def clear(self):
        self.logwin.erase()
        self.logwin.refresh()

    def addtitle(self, title=None):
        if title:
            self.title = title
        self.titlewin.addstr(' ' + self.title + ' ' * (38 - len(self.title)), curses.A_REVERSE)
        self.titlewin.refresh()
#        self.titlewin.addstr(self.title, curses.A_REVERSE)
    def menu(self, menu):
        indx = 0

        currentLoc = self.logwin.getyx()

        while True:
            self.logwin.move(*currentLoc)
            self.logwin.refresh()

            for option in menu:
                if menu.index(option) == indx:
                    self.logwin.addstr(option + '\n', curses.A_BOLD)
                else:
                    self.logwin.addstr(option + '\n')

            control = self.logwin.getch()

            if control == 119:
                indx -= 1
            if control == 115:
                indx += 1
            if control == 101:
                return indx

            if indx > len(menu) - 1:
                indx -= 1
            if indx < 0:
                indx += 1

class Game:
    def __init__(self):
        self.display = GameDisplay("Moonbase Alpha")

        with open('events.json', 'r') as f:
            self.events = json.loads(f.read())

        self.save = {}

    def createsave(self):
        self.save = {
            "status":{
                "Fuel":3,
                "Health":3,
                "Systems":3,
                "Materials":0
            },
            "built":{
                1:{
                    "Improved Farming Station":0,
                    "Increased Oxygen Tank":0,
                    "Mining Station":0,
                },
                2:{
                    "ComSat":0,
                    "Rocket Core":0,
                    "Rocket":0
                },
                3:{
                    "Launch":0
                }
            },
        }
    
    def loadstatus(self):
        self.display.statusclear()
        curr_indx = 0
        for status, value in self.save["status"].items():
            self.display.statuswrite(status + ' | ' + '═' * value, curr_indx)
            curr_indx += 1

    def start(self):
        self.display.clear()
        self.display.statusclear()
        self.loadstatus()
        while True:
            event = random.choice(list(self.events.items()))
            self.display.log(event[0], attr=curses.A_BOLD)
            self.display.log(event[1]["desc"])

            titles, options = self.parseOptions(event[1]["opt"])
            
            selection = self.display.menu(titles)
            
            result = options[selection]

            self.result(result)
            self.scan()

            self.display.clear()
            self.display.statusclear()
            self.loadstatus()

    def scan(self):
        pass

    def parseOptions(self, options):
        
        titles = [i[0] for i in options]
        operations = [i[1:] for i in options]

        return titles, operations

    def result(self, results):
        for result in results:
            status = result[0]
            modifier = result[1]

            self.save["status"][status] += modifier

def main():
    game = Game()

    #main menu

    while True:
        game.display.clear()
        game.display.statuswrite("Welcome to Moonbase Alpha Alpha 0.2.1", 0)
        game.display.statuswrite("A game made by Manitej Boorgu", 1)
        game.display.statuswrite("Use the WASD keys to move around.", 8, attr=curses.A_BOLD)
        game.display.statuswrite("Use the E key to select an option.", 9, attr=curses.A_BOLD)
        game.display.log("Moonbase Alpha Alpha 0.2.1", attr=curses.A_BOLD)
        game.display.log("Welcome! Load or start a new game.")
        
        
        option = game.display.menu(("Load", "New"))
        
        if option == 0:
            #load the current save
            game.display.clear()
        elif option == 1:
            #game will erase current save
            game.createsave()
            game.start()


    while 1: pass