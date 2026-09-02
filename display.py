import pygame


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def get_screen_size():
    return screen.get_size()

def get_image_size(image):
    return image.get_size()

def transform_image(path):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (35, 35))
    return image

def transform_tile(path, size):
    if size == 10: return pygame.image.load(path)
    image = pygame.image.load(path)
    if size == 20:
        image = pygame.transform.scale(image, (40, 40))
    else:
        image = pygame.transform.scale(image, (25, 25))
    return image
