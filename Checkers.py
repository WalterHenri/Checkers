import pygame

from Board import Board
from Constants import *


class Checkers:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board = Board(self.screen, COLORA, COLORB)
        self.running = True

    def run(self):
        while self.running:
            self.events()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.board.update(event)

    def draw(self):
        self.board.draw()
        pygame.display.update()








