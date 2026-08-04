import random

import pygame
from display import get_screen_size, transform_image, get_image_size

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
pygame.init()


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

        self.show_title()

    def show_title(self):
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

        self.buttons()


    def buttons(self):
        start = font.render("START", True, (0, 0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), [self.size[0]/2 - 100, self.size[1]/2 - 100, 200, 50], 0, 10)
        self.screen.blit(start, (self.size[0]/2 - 40, self.size[1]/2 -93, 200, 50))

        endless = font.render("ENDLESS", True, (0, 0, 0))
        pygame.draw.rect(self.screen, (0, 0, 255), [self.size[0]/2 - 100, self.size[1]/2 - 20, 200, 50], 0, 10)
        self.screen.blit(endless, (self.size[0]/2 - 57, self.size[1]/2 - 13, 200, 50))

        exit_ = font.render("EXIT", True, (0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), [self.size[0]/2 - 100, self.size[1]/2 + 60, 200, 50], 0, 10)
        self.screen.blit(exit_, (self.size[0] / 2 - 30, self.size[1] / 2 + 67, 200, 50))


    def get_button(self, i, j):
        if self.size[0]/2 - 100 <= i <= self.size[0]/2 + 100:
            if self.size[1]/2 - 100 <= j <= self.size[1]/2 - 50:
                return "START"
            if self.size[1]/2 - 20 <= j <= self.size[1]/2 + 30:
                return "ENDLESS"
            if self.size[1]/2 + 60 <= j <= self.size[1]/2 + 110:
                return "ESCAPE"
        return None
