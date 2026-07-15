from screen import *
from game_logic import Mechanics
from movement import get_movement
from timer.timer import display_timer

pygame.init()

game = Mechanics(screen, 10)

def movement():
    movement, i, j = get_movement()

    if movement == "R":
        game.reset_board()
    elif movement == "ESCAPE":
        return False
    elif movement == "REVEAL":
        game.reveal_block(i, j)
    else:
        game.place_flag(i, j)

    return True

running = True

while running:
    # display_timer()
    if not movement():
        running = False
    pygame.display.update()

pygame.quit()