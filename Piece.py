from Utils import Utils

class Piece:

    def __init__(self, color, type, position):
        self.__color = color
        self.__type = type
        self.__position = position
        self.__history = []
        self.__state = True

    def getColor(self):
        return self.__color
    
    def getType(self):
        return self.__type

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.addHistory(f"{Utils.getFullColorName(self.__color)} {Utils.getFullPieceName(self.__type)}: {Utils.PositionToString(self.__position)} -> {Utils.PositionToString(position)}")
        self.__position = position

    def getHistory(self):
        return self.__history

    def addHistory(self, move):
        self.__history.append(move)

    def removeHistory(self):
        self.__history.pop()

    def getState(self):
        return self.__state

    def setState(self, state):
        self.__state = state