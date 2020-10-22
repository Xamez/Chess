from Utils import Utils
from Piece import Piece

class Board:

    def __init__(self):
        self.__stateBoard = self.createBoard()

    def createBoard(self):

        board = [
                    ["B_R", "B_N", "B_B", "B_Q", "B_K", "B_B", "B_N", "B_R"],
                    ["B_P" for x in range(8)],
                    ["_" for x in range(8)],
                    ["_" for x in range(8)],
                    ["_" for x in range(8)],
                    ["_" for x in range(8)],
                    ["W_P" for x in range(8)],
                    ["W_R", "W_N", "W_B", "W_Q", "W_K", "W_B", "W_N", "W_R"]
                ]   
        for x in range(8):
            for y in range(8):
                value = tuple(board[x][y]) # transform "B_R" to ('B', '_', 'R') -> 'B' = black, R = type
                if value[0] != "_":
                    board[x][y] = Piece(value[0], value[2], (x, y))

        return board

    def getStateBoard(self):
        return self.__stateBoard

    def getPiece(self, position):
        x, y = position
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            return False if self.__stateBoard[x][y] == "_" else self.__stateBoard[x][y]
        return False

    # position -> piece to remove | piece -> attacker
    def removePiece(self, position):
        piece = self.getPiece(position)
        piece.setState(False)
        x, y = position
        self.__stateBoard[x][y] = "_"

    def getMoves(self, piece):

        # TODO FINISH THAT METHOD
        # TODO ADD THE CASE WHEN WE CAN'T MOVE BECAUSE OF CHECK
        # TODO ADD THEN CASE WHEN "EN PASSANT" 

        possibilities = []
        x, y = piece.getPosition()
        signe = 1 if piece.getColor() == "W" else -1

        if piece.getType() == "P":

            if self.getPiece((x+(-1*signe), y-1)):
                if not self.getPiece((x+(-1*signe), y-1)).getColor() == piece.getColor():
                    possibilities.append((x+(-1*signe), y-1))
            if self.getPiece((x+(-1*signe), y+1)):
                if not self.getPiece((x+(-1*signe), y+1)).getColor() == piece.getColor():
                    possibilities.append((x+(-1*signe), y+1))
            if not self.getPiece((x+(-1*signe), y)):
                possibilities.append((x+(-1*signe), y))
                if len(piece.getHistory()) == 0:
                    possibilities.append((x+(-2*signe), y))

            pieces = []
            if self.getPiece((x, y-1)):
                pieces.append(self.getPiece((x, y-1)))
            if self.getPiece((x, y+1)):
                pieces.append(self.getPiece((x, y+1)))
            for p in pieces:
                if len(p.getHistory()) > 0:
                    x, y = p.getPosition()
                    if p.getHistory()[-1] == f"{Utils.getFullColorName(p.getColor())} Pawn: {Utils.PositionToString((x+(-2*signe), y))} -> {Utils.PositionToString(p.getPosition())}":
                        if not p.getColor() == piece.getColor():
                            possibilities.append((x+(-1*signe), y))

        if piece.getType() == "R":
            possibilities = self.canMoveHV(x, y, piece)

        elif piece.getType() == "B":
            possibilities = self.canMoveDiagonaly(x, y, piece)

        elif piece.getType() == "N":
            pos = [
                    (x-2, y+1), (x-2, y-1),
                    (x+2, y+1), (x+2, y-1),
                    (x+1, y-2), (x-1, y-2),
                    (x+1, y+2), (x-1, y+2)
                  ]
            for element in pos:
                if self.getPiece(element):
                    if not self.getPiece(element).getColor() == piece.getColor():
                        possibilities.append(element)
                else:
                    possibilities.append(element)

        elif piece.getType() == "Q":
            possibilities = self.canMoveHV(x, y, piece)
            possibilities += self.canMoveDiagonaly(x, y, piece)

        elif piece.getType() == "K":
            pos = [
                    (x-1, y-1), (x-1, y), (x-1, y+1),
                    (x, y-1),               (x, y+1), 
                    (x+1, y-1), (x+1, y), (x+1, y+1)
                  ]

            Lrock = self.getPiece((x, y+3))
            Brock = self.getPiece((x, y-4))
            if Lrock:
                if len(piece.getHistory()) == 0 and len(Lrock.getHistory()) == 0:
                    if not self.getPiece((x, y+1)) and not self.getPiece((x, y+2)):
                        possibilities.append((x, y+2))
            if Brock:
                if len(piece.getHistory()) == 0 and len(Brock.getHistory()) == 0:
                    if not self.getPiece((x, y-1)) and not self.getPiece((x, y-2)) and not self.getPiece((x, y-3)):
                        possibilities.append((x, y-2))

            for element in pos:
                if self.getPiece(element):
                    if not self.getPiece(element).getColor() == piece.getColor():
                        possibilities.append(element)
                else:
                    possibilities.append(element)

        return possibilities

    def canMove(self, position, possibilities):
        return True if position in possibilities else False
    
    def canMoveHV(self, x, y, piece):
        left = y
        right = 7 - left
        up = x
        down = 7 - up
        possibilities = []
        for u in range(1, up+1):
            if self.getPiece((x-u, y)):
                if not self.getPiece((x-u, y)).getColor() == piece.getColor():
                    possibilities.append((x-u, y))
                    break
                break
            else:
                possibilities.append((x-u, y))
        for d in range(1, down+1):
            if self.getPiece((x+d, y)):
                if not self.getPiece((x+d, y)).getColor() == piece.getColor():
                    possibilities.append((x+d, y))
                    break
                break
            else:
                possibilities.append((x+d, y))
        for l in range(1, left+1):
            if self.getPiece((x, y-l)):
                if not self.getPiece((x, y-l)).getColor() == piece.getColor():
                    possibilities.append((x, y-l))
                    break
                break
            else:
                possibilities.append((x, y-l))
        for r in range(1, right+1):
            if self.getPiece((x, y+r)):
                if not self.getPiece((x, y+r)).getColor() == piece.getColor():
                    possibilities.append((x, y+r))
                    break
                break
            else:
                possibilities.append((x, y+r))

        return possibilities

    def canMoveDiagonaly(self, x, y, piece):
        left = y
        right = 7 - left
        up = x
        down = 7 - up
        possibilities = []
        for ul in range(1, up+1): # up left
            if self.getPiece((x-ul, y-ul)):
                if not self.getPiece((x-ul, y-ul)).getColor() == piece.getColor():
                    possibilities.append((x-ul, y-ul))
                    break
                break
            else:
                possibilities.append((x-ul, y-ul))
        for dr in range(1, right+1): # down left
            if self.getPiece((x-dr, y+dr)):
                if not self.getPiece((x-dr, y+dr)).getColor() == piece.getColor():
                    possibilities.append((x-dr, y+dr))
                    break
                break
            else:
                possibilities.append((x-dr, y+dr))
        for ul in range(1, left+1): # up right
            if self.getPiece((x+ul, y-ul)):
                if not self.getPiece((x+ul, y-ul)).getColor() == piece.getColor():
                    possibilities.append((x+ul, y-ul))
                    break
                break
            else:
                possibilities.append((x+ul, y-ul))
        for dr in range(1, down+1): # down right
            if self.getPiece((x+dr, y+dr)):
                if not self.getPiece((x+dr, y+dr)).getColor() == piece.getColor():
                    possibilities.append((x+dr, y+dr))
                    break
                break
            else:
                possibilities.append((x+dr, y+dr))

        return possibilities

    def movePiece(self, piece, position):
        signe = 1 if piece.getColor() == "W" else -1
        old_x, old_y = piece.getPosition()
        x, y = position
        if self.canMove(position, self.getMoves(piece)):
            if self.getPiece(position):
                self.removePiece(position)
            else:
                # EN PASSANT CASE
                if piece.getType() == "P":
                    if not old_y == y:
                        print(Utils.PositionToString((x+(-1*signe), y)))
                        self.removePiece((x+(+1*signe), y))
            self.__stateBoard[x][y] = piece
            self.removePiece(piece.getPosition())
            self.__stateBoard[x][y].setPosition(position)

            
            
            # CASTLING CASE
            if piece.getType() == "K":
                if len(piece.getHistory()) == 1: # 1 because we've just moved it just above
                    old_y = y
                    if y == 6:
                        history = f"{Utils.getFullColorName(piece.getColor())}: 0-0"
                        y = 7
                        y2 = 5
                    elif y == 2:
                        history = f"{Utils.getFullColorName(piece.getColor())}: 0-0-0"
                        y = 0
                        y2 = 3
                    else:
                        return (old_x, old_y, x, y)
                    Rpiece = self.__stateBoard[x][y]
                    self.__stateBoard[x][y2] = Rpiece
                    self.removePiece(Rpiece.getPosition())
                    self.__stateBoard[x][y2].setPosition((x, y2))
                    Rpiece.removeHistory()
                    Rpiece.addHistory(history)
                    piece.removeHistory()
                    piece.addHistory(history)
                    return (x, old_y, x, y2)
            return (old_x, old_y, x, y)
        return ()