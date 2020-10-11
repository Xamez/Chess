from Game import Game
from Gui import Gui

class Main:
    def __init__(self):
        self.__game = self.createGame()
        self.__gui = self.displayGUI()

    def createGame(self):
        return Game(900) # 900 in seconds = 15 minutes

    def displayGUI(self):
        return Gui(self.__game, 800, 800)

    def getGame(self):
        return self.__game

    def getGui(self):
        return self.__gui

if __name__ == "__main__":
    Main()