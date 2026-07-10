import pygame
from pygame import *

from game_logic import Game
from menu import Menu

pygame.init()


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Minesweeper")

screen.fill((90, 90, 90))
pygame.display.flip()

board = Game(screen)
board.initialize_bombs()

running = True
while running:
    menu = Menu(screen)
    menu.display()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_r:
                board.reset_board()
            if event.key == K_ESCAPE:
                running = False
                break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                i , j = pygame.mouse.get_pos()
                board.reveal_block(i , j)
            if event.button == 3:
                i , j = pygame.mouse.get_pos()
                board.place_flag(i ,j)
    pygame.display.update()

pygame.quit()
