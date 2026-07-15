import random
import time

import pygame.image

from display import get_screen_size, get_image_size


def display_board(logic):
    for i in range(logic.n):
        for j in range(logic.n):
            logic.screen.blit(pygame.image.load(logic.tiles.get(logic.board[i][j])), (logic.coordinates[j][0], logic.coordinates[i][1]))

class Initialization:
    def __init__(self, screen, n):
        self.n = n
        self.screen = screen
        self.board = [["hidden" for _ in range(n)] for _ in range(n)]
        self.logic_board = [[0 for _ in range(n)] for _ in range(n)]
        self.bombs = []
        self.coordinates = []
        self.initialize_coordinates()
        self.tiles = {0: "asseturi\\tiles\\default.png", 1: "asseturi\\tiles\\1.png", 2: "asseturi\\tiles\\2.png", 3: "asseturi\\tiles\\3.png",
                      4: "asseturi\\tiles\\4.png", 5: "asseturi\\tiles\\5.png", 6: "asseturi\\tiles\\6.png", 7: "asseturi\\tiles\\7.png",
                      8: "asseturi\\tiles\\8.png", 'x': "asseturi\\tiles\\bomb.png", "hidden": "asseturi\\tiles\\hidden.png",
                      "flag": "asseturi\\tiles\\flag.png"}

    def initialize_coordinates(self):
        x = []
        y = []

        screen_size = get_screen_size()
        image_size = get_image_size("asseturi\\tiles\\default.png")
        if self.n % 2 == 0:
            x.append(screen_size[0] / 2 - (self.n / 2 * image_size[0]))
            y.append(screen_size[1] / 2 - (self.n / 2 * image_size[1]))
        else:
            x.append(screen_size[0] / 2- ((self.n - 1) / 2) * image_size[0] - (image_size[0] / 2) )
            y.append(screen_size[1] / 2 - ((self.n - 1) / 2) * image_size[1] - (image_size[1] / 2) )
        for _ in range (self.n):
            x.append(x[len(x) - 1] + 60)
            y.append(y[len(y) - 1] + 60)

        for i in range (len(x)):
            self.coordinates.append((x[i], y[i]))

    def initialize_bombs(self):
        while len(self.bombs) < self.n:
            bomb = (random.randint(0, self.n -1), random.randint(0, self.n -1))
            if bomb not in self.bombs:
                self.bombs.append(bomb)
                self.logic_board[bomb[0]][bomb[1]] = "x"

        self.initialize_numbers()


    def isbomb(self, i, j):
        if self.logic_board[i][j] != "x":
            return False
        return True

    def isnumber(self , i , j):
        if 1 <= self.logic_board[i][j] <= 8:
            return True
        return False

    def increment(self, i, j):
        if not self.isbomb(i, j):
            self.logic_board[i][j] += 1

    def initialize_numbers(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.logic_board[i][j] == "x":
                    # top left corner
                    if i == 0 and j == 0:
                        self.increment(i + 1, j)
                        self.increment(i, j + 1)
                        self.increment(i + 1, j + 1)
                    # top right corner
                    elif i == 0 and j == self.n - 1:
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
                    elif i == self.n - 1 and j == 0:
                        self.increment(i - 1, j)
                        self.increment(i - 1, j + 1)
                        self.increment(i, j + 1)
                    # bottom right corner
                    elif i == self.n - 1 and j == self.n - 1:
                        self.increment(i, j - 1)
                        self.increment(i - 1, j - 1)
                        self.increment(i - 1, j)
                    # bottom border
                    elif i == self.n - 1:
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
                    elif j == self.n - 1:
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
        self.board = [["hidden" for _ in range(self.n)] for _ in range(self.n)]
        self.logic_board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.initialize_bombs()

    # TODO make only bombs reveal (when press on bomb)
    def reset_board(self):
        self.board = self.logic_board[:]
        display_board(self)
        pygame.display.update()
        time.sleep(0.85)
        self.new_boards()



class Mechanics(Initialization):
    def __init__(self, screen, n):
        super().__init__(screen, n)
        self.initialize_bombs()

    def mouse_pos(self, x, y):
        a = -10000
        b = -10000

        for cord in range (len(self.coordinates) - 1):
            if self.coordinates[cord][1] <= y < self.coordinates[cord + 1][1]:
                a = cord
            if self.coordinates[cord][0] <= x < self.coordinates[cord + 1][0]:
                b = cord

        ok = True
        if a == -10000 or b == -10000:
            ok = False
        return a , b , ok

    def complete_path(self, i, j , visited):
        if (i  , j) not in visited:
            visited.append((i , j))
            if self.logic_board[i][j] == 0:
                self.board[i][j] = self.logic_board[i][j]

                if i == 0:
                    if j == 0:
                        self.complete_path(i, j + 1 , visited)
                        self.complete_path(i + 1, j + 1 , visited)
                    elif j == self.n - 1:
                        self.complete_path(i , j - 1 , visited)
                        self.complete_path(i + 1, j-1 , visited)
                    else:
                        self.complete_path(i + 1, j , visited)
                        self.complete_path(i, j + 1, visited)
                        self.complete_path(i + 1, j + 1, visited)
                        self.complete_path(i, j - 1, visited)
                        self.complete_path(i + 1, j - 1, visited)

                elif i == self.n - 1:
                    if j == 0:
                        self.complete_path(i, j + 1 , visited)
                        self.complete_path(i - 1, j + 1 , visited )
                    elif j == self.n - 1:
                        self.complete_path(i , j - 1 , visited)
                        self.complete_path(i - 1, j-1 , visited)
                    else:
                        self.complete_path(i - 1 , j , visited)
                        self.complete_path(i, j + 1, visited)
                        self.complete_path(i - 1, j + 1, visited)
                        self.complete_path(i, j - 1, visited)
                        self.complete_path(i - 1, j - 1, visited)

                elif j == 0:
                    self.complete_path(i - 1, j, visited)
                    self.complete_path(i - 1, j + 1 , visited)
                    self.complete_path(i, j + 1, visited)
                    self.complete_path(i + 1, j, visited)
                    self.complete_path(i + 1, j + 1, visited)

                elif j == self.n - 1:
                    self.complete_path(i - 1, j, visited)
                    self.complete_path(i - 1, j - 1, visited)
                    self.complete_path(i, j - 1, visited)
                    self.complete_path(i + 1, j - 1, visited)
                    self.complete_path(i + 1, j, visited)
                else:
                    self.complete_path(i - 1 , j , visited)
                    self.complete_path(i - 1 , j -1 , visited)
                    self.complete_path(i - 1 , j + 1 , visited)
                    self.complete_path(i + 1 , j , visited)
                    self.complete_path(i + 1 , j - 1 , visited)
                    self.complete_path(i + 1 , j + 1 , visited)
                    self.complete_path(i, j - 1 , visited)
                    self.complete_path(i , j + 1 , visited)


            if self.isnumber(i  , j):
                self.board[i][j] = self.logic_board[i][j]
                return

    def place_flag(self , x , y):
        i , j , ok = self.mouse_pos(x , y)
        if ok:
            if self.board[i][j] == "flag":
                self.delete_flag(i , j)
            elif self.board[i][j] == "hidden":
                self.board[i][j] = "flag"
            display_board(self)

    def reveal_block(self , x , y):
        i , j , ok = self.mouse_pos(x , y)
        if ok and self.board[i][j] == "hidden":
            if self.logic_board[i][j] == "x":
                self.game_over()
            if self.logic_board[i][j] == 0:
                self.complete_path(i , j , [])
                display_board(self)
            else:
                self.board[i][j] = self.logic_board[i][j]
                display_board(self)



    def delete_flag(self , i , j):
        self.board[i][j] = "hidden"

    def reveal_bomb(self , i , j):
        self.board[i][j] = self.logic_board[i][j]

    def game_over(self):
        for bomb in self.bombs:
            self.reveal_bomb(bomb[0] , bomb[1])
        self.bombs = []
        display_board(self)




