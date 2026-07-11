from pygame import *
import pygame


def get_movement():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_r:
                return "R", 0, 0
            if event.key == K_ESCAPE:
                return "ESCAPE", 0, 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                i , j = pygame.mouse.get_pos()
                return "REVEAL", i, j
            if event.button == 3:
                i , j = pygame.mouse.get_pos()
                return "PLACE", i, j
    return 0, 0, 0