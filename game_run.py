from screen import *
from game_logic import Mechanics , display_board
from movement import get_movement
from menu import Menu
from timer import create_timer

pygame.font.init()
#Fonts!!
font = pygame.font.SysFont("Arial", 30)
go_font = pygame.font.SysFont("Arial", 60, bold=True)

#Timer!!
timer_font , timer_sec , timer_text = create_timer()

pygame.init()

def movement():
    movement, i, j = get_movement(game.game_running)

    if movement == "R":
        game.reset_board()
    elif movement == "ESCAPE":
        return "MENU"
    elif movement == "REVEAL":
        game.reveal_block(i, j)
    else:
        game.place_flag(i, j)

    return True

running = True

while running:
    menu = Menu(screen)
    # Refresh screen at every frame
    screen.fill((90, 90, 90))

    menu.initialize_board()
    pygame.display.update()

    menu_button = 0
    board_size = 0
    in_menu = True

    while in_menu and running:
        i, j = -1 , -1
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                i, j = pygame.mouse.get_pos()

        msg = menu.get_button(i, j)

        if menu_button == 0:
            if msg == "1":
                menu.size_buttons()
                pygame.display.update()
                menu_button = 1
            if msg == "2":
                menu_button = 2
            elif msg == "3":
                running = False
                in_menu = False
        #Normal Mode
        elif menu_button == 1:
            if msg == "1":
                board_size = 10
                in_menu = False
            if msg == "2":
                board_size = 20
                in_menu = False
            elif msg == "3":
                board_size = 30
                in_menu = False
        #Endless Mode
        elif menu_button == 2:
            board_size = 10
            in_menu = False

    if not running:
        break

    #Start Game
    screen.fill((90, 90, 90))
    game = Mechanics(screen, board_size)
    in_game = True

    #Timer ticks
    last_tick = pygame.time.get_ticks()

    while in_game and running:
        screen.fill((90, 90, 90))
        move = movement()

        if move == "MENU":
            in_game = False
            break
        elif not move:
            running = False
            break

        display_board(game)
        if menu_button == 2:
            current_time = pygame.time.get_ticks()
            if current_time - last_tick >= 1000:
                if timer_sec > 0:
                    timer_sec -= 100
                last_tick = current_time

            minutes = timer_sec // 60
            sec = timer_sec % 60
            if sec == 0 and minutes == 0:
                timer_text = timer_font.render("%02d:%02d" % (minutes, sec), True, (255, 0, 0))
            else:
                timer_text = timer_font.render("%02d:%02d" % (minutes, sec), True, (255, 255, 255))

            screen.blit(timer_text, (300, 20))


        #Bomb text(count)
        current_count = game.get_bomb_count()
        bomb_text = font.render(f"Bombs: {current_count}", True, (255, 255, 255))
        screen.blit(bomb_text, (screen.get_width() - 200, 50))

        #WIN condition + text
        if game.win_condition():
            msg = go_font.render("WIN WIN WIN", True, (0, 128, 0))
            rect = msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(msg, rect)

        #LOSE condition + text
        if not game.game_running:
            msg = go_font.render("GAME OVER", True, (255, 0, 0))
            rect = msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(msg, rect)

        pygame.display.update()

pygame.quit()