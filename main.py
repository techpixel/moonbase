import os

os.chdir(os.path.join(os.getcwd(), 'src'))

from src import game

game.main()