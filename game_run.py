from screen import *
from game_logic import Logic

pygame.init()
running = True
while running:
    game = Logic(screen)
    if not game.movement():
        running = False
    pygame.display.update()

pygame.quit()