import pygame


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def get_screen_size():
    return screen.get_size()

def get_image_size(path):
    image = pygame.image.load(path)
    return image.get_size()
