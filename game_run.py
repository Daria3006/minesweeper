from screen import *
from game_logic import Mechanics , display_board
from movement import get_movement
from timer.timer import display_timer

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
go_font = pygame.font.SysFont("Arial", 60, bold=True)
pygame.init()

game = Mechanics(screen, 10)

def movement():
    movement, i, j = get_movement(game.game_running)

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
    screen.fill((90, 90, 90))

    display_board(game)

    current_count = game.get_bomb_count()
    bomb_text = font.render(f"Bombs: {current_count}", True, (255, 255, 255))
    screen.blit(bomb_text, (screen.get_width() - 200, 50))

    if not game.game_running:
        msg = go_font.render("GAME OVER", True, (255, 0, 0))
        rect = msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(msg, rect)

    if not movement():
        running = False

    pygame.display.update()

pygame.quit()