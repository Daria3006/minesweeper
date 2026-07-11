from screen import *
from game_logic import Logic

pygame.init()
running = True
game = Logic(screen)
while running:
    if not game.movement():
        running = False
    pygame.display.update()

pygame.quit()