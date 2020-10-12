class Utils:

    @staticmethod
    def PositionToString(position): # ! BUGGED
        (y, x) = position
        x = chr(x+65)
        return f"{x}{8-y}"

    def getFullPieceName(name):

        names = {
                "R": "Rook",
                "N": "Knight",
                "B": "Bushop",
                "Q": "Queen",
                "K": "King",
                "P": "Pawn"
                }
        return names[name]

    @staticmethod
    def getFullColorName(color):

        colors = {
                "B": "Black",
                "W": "White"
                 }
        return colors[color]

    @staticmethod
    def getPoints():
        # TODO
        return {
                "R": 5,
                "N": 3,
                "B": 3,
                "Q": 999,
                "K": 9,
                "P": 1
               }

    @staticmethod
    def getPlayerColor(color):
        colors = {
                 0: "W",
                 1: "B"
               }
        return colors[color]
