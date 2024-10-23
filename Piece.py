import pygame

from Constants import *


class Piece:
    """
    Class to represent a piece in the game of checkers.
    color = 0 to black, 1 to white
    """
    def __init__(self, color, initial_pos):
        self.color = color
        self.pos = initial_pos
        self.king = False
        self.x = 0
        self.y = 0

    def make_king(self):
        self.king = True

    def move(self, new_pos, board):
        self.pos = new_pos
        self.calc_pos(new_pos, board)

    def calc_pos(self, new_pos, board):
        self.x = board.x + new_pos[0] * SQUARE_SIZE
        self.y = board.y + new_pos[1] * SQUARE_SIZE

    def draw(self, screen):
        if self.color == 0:
            pygame.draw.circle(screen, RED, (self.x + SQUARE_SIZE // 2, self.y + SQUARE_SIZE // 2), 20)
        else:
            pygame.draw.circle(screen, BLUE, (self.x + SQUARE_SIZE // 2, self.y + SQUARE_SIZE // 2), 20)

        if self.king and self.color == 0:
            pygame.draw.circle(screen, WHITE, (self.x + SQUARE_SIZE // 2, self.y + SQUARE_SIZE // 2), 10)


