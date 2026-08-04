import random

import pygame
from display import get_screen_size, transform_image, get_image_size


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.size = get_screen_size()
        self.mine = [[1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                     [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                     [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
                     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
                     [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1]]

        self.sweeper = [[1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
                        [0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                        [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1]]

    def initialize_board(self):
        image = transform_image("asseturi\\tiles\\hidden.png")

        for i in range(0, self.size[0], 35):
            for j in range(0, self.size[1], 35):
                self.screen.blit(image, (i, j))

        self.reveal_blocks()

    def reveal_blocks(self):
        columns_mine = (self.size[0] // 35 - 23) // 2
        columns_sweeper = (self.size[0] // 35 - 41) // 2
        r_list = []
        for i in range(1, 4):
            img = transform_image(f"asseturi\\tiles\\{i}.png")
            r_list.append(img)


        for i in range(5):
            for j in range(23):
                if self.mine[i][j]:
                    r = random.randint(0, len(r_list))
                    self.screen.blit(r_list[r - 1], (columns_mine * 35 + j * 35 , (i + 2) * 35))

        for i in range(5):
            for j in range(41):
                if self.sweeper[i][j]:
                    r = random.randint(0, len(r_list))
                    self.screen.blit(r_list[r - 1], (columns_sweeper * 35 + j * 35, (self.size[1] - (5 - i + 2) * 35) + 10))
