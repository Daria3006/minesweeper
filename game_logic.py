import random
import time

import pygame.image


def display_board(logic):
    for i in range(9):
        for j in range(9):
            logic.screen.blit(pygame.image.load(logic.tiles.get(logic.board[i][j])),
                                   (logic.coordinates[i], logic.coordinates[j]))

class Initialization:
    def __init__(self, screen):
        self.screen = screen
        self.board = [["hidden" for _ in range(9)] for _ in range(9)]
        self.logic_board = [[0 for _ in range(9)] for _ in range(9)]
        self.coordinates = {0: 100, 1: 160, 2: 220, 3: 280, 4: 340, 5: 400, 6: 460, 7: 520, 8: 580, 9: 640}
        self.tiles = {0: "asseturi\\default.png", 1: "asseturi\\1.png", 2: "asseturi\\2.png", 3: "asseturi\\3.png",
                      4: "asseturi\\4.png", 5: "asseturi\\5.png", 6: "asseturi\\6.png", 7: "asseturi\\7.png",
                      8: "asseturi\\8.png", 'x': "asseturi\\bomb.png", "hidden": "asseturi\\hidden.png",
                      "flag": "asseturi\\flag.png"}


    def initialize_bombs(self):
        bombs = []
        while len(bombs) < 10:
            bomb = (random.randint(0, 8), random.randint(0, 8))
            if bomb not in bombs:
                bombs.append(bomb)
                self.logic_board[bomb[0]][bomb[1]] = 'x'

        self.initialize_numbers()


    def isbomb(self, i, j):
        if self.logic_board[i][j] != 'x':
            return False
        return True

    def increment(self, i, j):
        if not self.isbomb(i, j):
            self.logic_board[i][j] += 1

    def initialize_numbers(self):
        for i in range(9):
            for j in range(9):
                if self.logic_board[i][j] == 'x':
                    # top left corner
                    if i == 0 and j == 0:
                        self.increment(i + 1, j)
                        self.increment(i, j + 1)
                        self.increment(i + 1, j + 1)
                    # top right corner
                    elif i == 0 and j == 8:
                        self.increment(i, j - 1)
                        self.increment(i + 1, j - 1)
                        self.increment(i + 1, j)
                    # top border
                    elif i == 0:
                        self.increment(i, j - 1)
                        self.increment(i, j + 1)
                        self.increment(i + 1, j - 1)
                        self.increment(i + 1, j)
                        self.increment(i + 1, j + 1)
                    # bottom left corner
                    elif i == 8 and j == 0:
                        self.increment(i - 1, j)
                        self.increment(i - 1, j + 1)
                        self.increment(i, j + 1)
                    # bottom right corner
                    elif i == 8 and j == 8:
                        self.increment(i, j - 1)
                        self.increment(i - 1, j - 1)
                        self.increment(i - 1, j)
                    # bottom border
                    elif i == 8:
                        self.increment(i, j - 1)
                        self.increment(i, j + 1)
                        self.increment(i - 1, j - 1)
                        self.increment(i - 1, j)
                        self.increment(i - 1, j + 1)
                    # left border
                    elif j == 0:
                        self.increment(i - 1, j)
                        self.increment(i + 1, j)
                        self.increment(i - 1, j + 1)
                        self.increment(i, j + 1)
                        self.increment(i + 1, j + 1)
                    # right border
                    elif j == 8:
                        self.increment(i - 1, j)
                        self.increment(i + 1, j)
                        self.increment(i - 1, j - 1)
                        self.increment(i, j - 1)
                        self.increment(i + 1, j - 1)
                    else:
                        self.increment(i - 1, j - 1)
                        self.increment(i - 1, j)
                        self.increment(i - 1, j + 1)
                        self.increment(i, j - 1)
                        self.increment(i, j + 1)
                        self.increment(i + 1, j - 1)
                        self.increment(i + 1, j)
                        self.increment(i + 1, j + 1)

        display_board(self)

    def new_boards(self):
        self.board = [["hidden" for _ in range(9)] for _ in range(9)]
        self.logic_board = [[0 for _ in range(9)] for _ in range(9)]
        self.initialize_bombs()

    # TODO make only bombs reveal (when press on bomb)
    def reset_board(self):
        self.board = self.logic_board[:]
        display_board(self)
        pygame.display.update()
        time.sleep(0.85)
        self.new_boards()

class Mechanics(Initialization):
    def __init__(self, screen):
        super().__init__(screen)
        self.initialize_bombs()

    def mouse_pos(self ,i , j):
        a = -10000
        b = -10000
        for x in range (9):
            if self.coordinates[x] <= i < self.coordinates[x + 1]:
                a = x
            if self.coordinates[x] <= j < self.coordinates[x + 1]:
                b = x
        ok = True
        if a == -10000 or b == -10000:
            ok = False
        return a , b , ok

    def complete_path(self, i, j):
        if self.logic_board[i][j] == 'default':
            self.reveal_block(i , j)
            self.complete_path(i - 1 , j)
            self.complete_path(i - 1 , j -1)
            self.complete_path(i - 1 , j + 1)
            self.complete_path(i + 1 , j)
            self.complete_path(i + 1 , j - 1)
            self.complete_path(i + 1 , j + 1)
            self.complete_path(i, j - 1)
            self.complete_path(i , j + 1)

        #TODO number implementation
        if self.logic_board[i][j] == "":
            self.reveal_block(i , j)
            return

    def place_flag(self , i , j):
        i , j , ok = self.mouse_pos(i , j)
        if ok:
            if self.board[i][j] == 'flag':
                self.delete_flag(i , j)
            elif self.board[i][j] == 'hidden':
                self.board[i][j] = "flag"
            display_board(self)

    def reveal_block(self , i , j):
        i , j , ok = self.mouse_pos(i , j)
        if ok and self.board[i][j] == "hidden":
            self.board[i][j] = self.logic_board[i][j]
            display_board(self)

    #ALALAL
    def delete_flag(self , i , j):
        self.board[i][j] = "hidden"



