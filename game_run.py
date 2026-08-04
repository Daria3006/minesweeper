from screen import *
from game_logic import Mechanics , display_board
from movement import get_movement
from timer.timer import display_timer
from menu import Menu

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
go_font = pygame.font.SysFont("Arial", 60, bold=True)
pygame.init()


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

screen.fill((90, 90, 90))

menu = Menu(screen)
menu.initialize_board()
pygame.display.update()

buttons = 0
n = 0
while True:
    i, j = 0, 0
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            i, j = pygame.mouse.get_pos()
    msg = menu.get_button(i, j)

    if buttons == 0:
        if msg == "1":
            menu.size_buttons()
            pygame.display.update()
            buttons = 1
        if msg == "2":
            break
        elif msg == "3":
            running = False
            break
    elif buttons == 1:
        if msg == "1":
            n = 10
            break
        if msg == "2":
            n = 20
            break
        elif msg == "3":
            n = 30
            break

screen.fill((90, 90, 90))

game = Mechanics(screen, n)


while running:

    if not movement():
        running = False

    display_board(game)

    current_count = game.get_bomb_count()
    bomb_text = font.render(f"Bombs: {current_count}", True, (255, 255, 255))
    screen.blit(bomb_text, (screen.get_width() - 200, 50))

    if not game.game_running:
        msg = go_font.render("GAME OVER", True, (255, 0, 0))
        rect = msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(msg, rect)



    pygame.display.update()

pygame.quit()