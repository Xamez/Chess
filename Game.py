from Board import Board

class Game:

    def __init__(self, time):
        self.__time = time
        self.__board = Board()

    def getBoard(self):
        return self.__board