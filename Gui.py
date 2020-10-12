import os
import sys
from math import ceil
import random
import pygame
from Utils import Utils

class Gui:

    def __init__(self, game, width, height):

        self.__running = True
        self.__game = game
        self.__player = 0
        self.__board = self.__game.getBoard()
        self.__stateBoard = self.__board.getStateBoard()
        self.__width = width
        self.__height = height
        self.__padding = 50
        self.__cellSize = int((width - 2*self.__padding) / 8)
        self.__ressources = self.loadRessourcesPieces()
        self.__dot = self.loadRessourcesDot()
        self.__selected = ()
        self.__lastMove = ()

        # pygame
        pygame.init()
        pygame.font.init()
        self.__font = pygame.font.SysFont('consolas', 30)
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption("Chess Game")

        while self.__running:

            self.displayBoard()
            self.highlightPiece()
            self.displayPiece()
            self.displayPossibleMoves()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    y, x = event.pos
                    x = (x - self.__padding) // self.__cellSize
                    y = (y - self.__padding) // self.__cellSize
                    if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                        if pygame.mouse.get_pressed()[0]:
                            if self.__selected:
                                if self.__stateBoard[x][y] != "_":
                                    if self.__stateBoard[x][y].getColor() != self.__board.getPiece(self.__selected).getColor():
                                        move = self.__board.movePiece(self.__board.getPiece(self.__selected), (x, y))
                                        if move:
                                            self.__lastMove = move
                                            self.__selected = ()
                                            self.__player = (self.__player + 1) % 2
                                        else:
                                            self.__selected = (x, y)
                                    else:
                                        if self.__stateBoard[x][y].getColor() == Utils.getPlayerColor(self.__player):
                                            self.__selected = (x, y)
                                else:
                                    move = self.__board.movePiece(self.__board.getPiece(self.__selected), (x, y))
                                    if move:
                                        self.__lastMove = move
                                        self.__selected = ()
                                        self.__player = (self.__player + 1) % 2
                            else:
                                if self.__stateBoard[x][y] != "_":
                                    if self.__stateBoard[x][y].getColor() == Utils.getPlayerColor(self.__player):
                                        self.__selected = (x, y)
                        else:
                            self.__selected = ()
            
            pygame.display.update()

    
    def displayPossibleMoves(self):
        if self.__selected == ():
            return
        positions = self.__board.getMoves(self.__board.getPiece(self.__selected))
        for pos in positions:
            y, x = pos
            if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                color = self.__dot[0] if self.__board.getPiece(self.__selected).getColor() == "B" else self.__dot[1]
                self.__screen.blit(color, (x*self.__cellSize + self.__padding, y*self.__cellSize + self.__padding))

    def highlightPiece(self):

        # TODO HIGHLIGHT ALL ATTACKED PIECE

        # last move
        if self.__lastMove:
            y, x, y1, x1 = self.__lastMove
            pygame.draw.rect(self.__screen, (118, 149, 84),
                            (self.__padding + x*self.__cellSize, self.__padding + y*self.__cellSize, self.__cellSize, self.__cellSize))
            pygame.draw.rect(self.__screen, (118, 149, 84),
                            (self.__padding + x1*self.__cellSize, self.__padding + y1*self.__cellSize, self.__cellSize, self.__cellSize))

        # selected
        if self.__selected:
            y, x = self.__selected
            pygame.draw.rect(self.__screen, (50, 200, 40),
                            (self.__padding + x*self.__cellSize, self.__padding + y*self.__cellSize, self.__cellSize, self.__cellSize))


    def loadRessourcesPieces(self):
        pieces = {}
        for element in os.listdir("ressources/pieces/"):
            surface = pygame.image.load("ressources/pieces/" + element)
            surface = pygame.transform.scale(surface, (ceil(self.__cellSize * 3/4), ceil(self.__cellSize * 3/4)))
            pieces.update({element[:-4]: surface}) # element[:-4] to remove suffix ".png"
        return pieces

    def loadRessourcesDot(self):
        dots = []
        surface_dot_B = pygame.image.load("ressources/others/B_DOT.png")
        surface_dot_B = pygame.transform.scale(surface_dot_B, (self.__cellSize, self.__cellSize))
        surface_dot_W = pygame.image.load("ressources/others/W_DOT.png")
        surface_dot_W = pygame.transform.scale(surface_dot_W, (self.__cellSize, self.__cellSize))
        dots.append(surface_dot_B)
        dots.append(surface_dot_W)
        return dots
    

    def displayBoard(self):
        self.__screen.fill((20, 20, 20))

        # display cells
        i = 0
        for x in range(8):
            for y in range(8):
                if i % 2 == 1:
                    pygame.draw.rect(self.__screen, (209, 139, 70),
                                    (self.__padding + x*self.__cellSize, self.__padding + y*self.__cellSize, self.__cellSize, self.__cellSize))
                else:
                    pygame.draw.rect(self.__screen, (255, 207, 159),
                                    (self.__padding + x*self.__cellSize, self.__padding + y*self.__cellSize, self.__cellSize, self.__cellSize))
                i += 1
            i += 1
        
        # display texts
        for i in range(1, 9):
            text_surface = self.__font.render(f'{9 - i}', True, (255, 255, 255))
            self.__screen.blit(text_surface, (2/3 * self.__padding - 10, 2/3 * self.__padding + (i - 1)*self.__cellSize + self.__cellSize * 0.6))
            self.__screen.blit(text_surface, (8*self.__cellSize + self.__padding + 10, 2/3 * self.__padding + (i - 1)*self.__cellSize + self.__cellSize * 0.6))

        for j, letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            text_surface = self.__font.render(f'{letter}', True, (255, 255, 255))
            self.__screen.blit(text_surface, (2/3 * self.__padding + j*self.__cellSize + self.__cellSize *0.6, 2/3 * self.__padding - 20))
            self.__screen.blit(text_surface, (2/3 * self.__padding + j*self.__cellSize + self.__cellSize * 0.6, 8*self.__cellSize + self.__padding + 10))

    def displayPiece(self):

        for x in range(8):
            for y in range(8):
                element = self.__stateBoard[x][y]
                if element != "_":
                    surface = self.__ressources.get(f"{element.getColor()}_{element.getType()}")
                    self.__screen.blit(surface,
                                      (self.__padding + y*self.__cellSize + self.__cellSize/8, self.__padding + x*self.__cellSize + self.__cellSize/8))