import pygame
from Constants import *
from Piece import Piece


class Board:
    def __init__(self, screen, color_a, color_b, x=BOARD_X, y=BOARD_Y, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        self.board = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.pieces = []
        self.colorB = color_b
        self.colorA = color_a
        self.create_board()
        self.selected_piece = None
        # valid moves are [( newpos, 0 or 1 )] newpos is a tuple (x, y) and 0 is not eating and 1 is eating
        self.valid_moves = []
        self.turn = 0
        self.need_to_eat = False

    def create_board(self):
        for i in range(8):
            self.board.append([])
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.board[i].append(None)
                else:
                    if j < 3:
                        self.board[i].append(Piece(0, (i, j)))
                    elif j > 4:
                        self.board[i].append(Piece(1, (i, j)))
                    else:
                        self.board[i].append(None)

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, self.colorA,
                                     (self.x + i * SQUARE_SIZE, self.y + j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.screen, self.colorB,
                                     (self.x + i * SQUARE_SIZE, self.y + j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    piece.calc_pos((i, j), self)
                    piece.draw(self.screen)

    def draw_valid_moves(self):
        for move in self.valid_moves:
            pos = move[0]
            x = pos[0]
            y = pos[1]
            pygame.draw.circle(self.screen, COLORC,
                               (self.x + x * SQUARE_SIZE + SQUARE_SIZE // 2,
                                self.y + y * SQUARE_SIZE + SQUARE_SIZE // 2),
                               SQUARE_SIZE // 4)

    @staticmethod
    def not_in_bounds(new_pos):
        return new_pos[0] < 0 or new_pos[0] > 7 or new_pos[1] < 0 or new_pos[1] > 7

    def update_valid_moves(self, x, y):
        piece = self.board[x][y]

        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.color == 0:
            directions = [(-1, -1), (-1, 1)]
        else:
            directions = [(1, -1), (1, 1)]

        for direction in directions:
            new_pos = (x + direction[0], y + direction[1])
            if self.not_in_bounds(new_pos):
                continue
            piece_to_eat = self.board[new_pos[0]][new_pos[1]]
            if piece_to_eat is not None:
                if piece_to_eat.color == self.turn:
                    break
                else:
                    new_pos = (new_pos[0] + direction[0], new_pos[1] + direction[1])
                    if self.not_in_bounds(new_pos):
                        continue
                    piece_to_eat = self.board[new_pos[0]][new_pos[1]]
                    if piece_to_eat is None:
                        self.valid_moves.append((new_pos, 1))
                        if not self.need_to_eat:
                            self.need_to_eat = True
                            self.valid_moves = [move for move in self.valid_moves if move[1] == 1]
                            self.update_valid_moves(new_pos[0], new_pos[1])
            else:
                if not self.need_to_eat:
                    self.valid_moves.append((new_pos, 0))

    def draw(self):
        self.draw_board()
        self.draw_pieces()
        self.draw_valid_moves()

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
                x = (pos[0] - self.x) // SQUARE_SIZE
                y = (pos[1] - self.y) // SQUARE_SIZE
                piece = self.board[x][y]
                if piece is not None:
                    self.selected_piece = piece
                    self.update_valid_moves(x, y)
                else:
                    if self.selected_piece is not None:
                        if (x, y) in self.valid_moves:
                            self.selected_piece.move((x, y), self)
                            self.selected_piece = None
                            self.valid_moves = {}
