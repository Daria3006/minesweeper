from display import get_image_size, get_screen_size


class Menu:
    def __init__(self, screen):
        self.screen = screen

    def display(self):
        screen_x = get_screen_size()[0]
        x = screen_x / 2 - get_image_size("asseturi\\menu\\title.png")[0] / 2
        y = 100
        self.screen.blit(pygame.image.load("asseturi\\menu\\title.png"), (x, y))

        x = screen_x / 2 - get_image_size("asseturi\\menu\\10x10.png")[0] / 2
        y = y + 20 + get_image_size("asseturi\\menu\\10x10.png")[1]
        self.screen.blit(pygame.image.load("asseturi\\menu\\10x10.png"), (x, y))


