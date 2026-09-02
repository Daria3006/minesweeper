from screen import *
from game_logic import Mechanics , display_board
from movement import get_movement
from menu import Menu
from timer import create_timer

pygame.font.init()
# Fonts!!
font = pygame.font.SysFont("Arial", 30)
go_font = pygame.font.SysFont("Arial", 60, bold=True)
small_font = pygame.font.SysFont("Arial", 25)

# Timer!!
timer_font, timer_sec, timer_text = create_timer()

pygame.init()


def movement(menu_button):
    is_game_over = not game.game_running or game.win_condition()
    movement, i, j = get_movement(not is_game_over)

    if movement == "R":
        if menu_button == 1:
            game.reset_board()
    elif movement == "ESCAPE":
        return "MENU"
    elif not is_game_over:
        if movement == "REVEAL":
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
        i, j = -1, -1
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
        # Normal Mode
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
        # Endless Mode
        elif menu_button == 2:
            board_size = 10
            in_menu = False
            # Reset timer to 300 seconds (5 minutes) when entering endless mode
            timer_sec = 300
    print(menu_button)

    if not running:
        break

    # Start Game
    screen.fill((90, 90, 90))
    game = Mechanics(screen, board_size)
    in_game = True

    # Timer ticks
    last_tick = pygame.time.get_ticks()
    timer_flash_timer = 0
    timer_flash_color = (255, 255, 255)

    while in_game and running:
        screen.fill((90, 90, 90))
        move = movement(menu_button)

        if move == "MENU":
            in_game = False
            break
        elif not move:
            running = False
            break

        # Check if Endless Mode timer ran out of time completely
        if menu_button == 2 and timer_sec <= 0:
            game.game_running = False

        if menu_button == 2:

            if game.win_condition():
                if board_size < 30:
                    board_size += 10
                else:
                    board_size = 10

                if board_size == 10:
                    timer_sec += 30
                elif board_size == 20:
                    timer_sec += 60
                else:
                    timer_sec += 120
                timer_flash_color = (0, 255, 0)
                timer_flash_timer = pygame.time.get_ticks()



                screen.fill((90, 90, 90))
                display_board(game)

                minutes = timer_sec // 60
                sec = timer_sec % 60
                timer_text = timer_font.render("%02d:%02d" % (minutes, sec), True, timer_flash_color)
                screen.blit(timer_text, (200, 20))

                current_count = game.get_bomb_count()
                bomb_text = font.render(f"Bombs: {current_count}", True, (255, 255, 255))
                screen.blit(bomb_text, (screen.get_width() - 200, 50))

                pygame.display.update()
                pygame.time.delay(1000)

                game = Mechanics(screen, board_size)
                last_tick = pygame.time.get_ticks()

            if not game.game_running:
                timer_sec = max(0, timer_sec - 10)
                timer_flash_color = (255, 0, 0)
                timer_flash_timer = pygame.time.get_ticks()



                if timer_sec <= 0:
                    game.game_running = False
                else:
                    screen.fill((90, 90, 90))
                    display_board(game)

                    minutes = timer_sec // 60
                    sec = timer_sec % 60
                    timer_text = timer_font.render("%02d:%02d" % (minutes, sec), True, timer_flash_color)
                    screen.blit(timer_text, (200, 20))

                    current_count = game.get_bomb_count()
                    bomb_text = font.render(f"Bombs: {current_count}", True, (255, 255, 255))
                    screen.blit(bomb_text, (screen.get_width() - 200, 50))

                    pygame.display.update()
                    pygame.time.delay(1500)

                    game = Mechanics(screen, board_size)
                    last_tick = pygame.time.get_ticks()

        display_board(game)
        current_time = pygame.time.get_ticks()

        if menu_button == 2 and game.game_running:
            if current_time - last_tick >= 1000:
                if timer_sec > 0:
                    timer_sec -= 1
                last_tick = current_time

            if timer_sec <= 0:
                timer_sec = 0
                game.game_running = False

        if menu_button == 2:
            minutes = timer_sec // 60
            sec = timer_sec % 60

            if current_time - timer_flash_timer < 1000:
                current_color = timer_flash_color
            elif timer_sec <= 10:
                current_color = (255, 0, 0)
            else:
                current_color = (255, 255, 255)

            timer_text = timer_font.render("%02d:%02d" % (minutes, sec), True, current_color)
            screen.blit(timer_text, (200, 20))

        # Bomb text(count)
        current_count = game.get_bomb_count()
        bomb_text = font.render(f"Bombs: {current_count}", True, (255, 255, 255))
        screen.blit(bomb_text, (screen.get_width() - 200, 50))

        # WIN condition + text (Only for Normal Mode now)
        if game.win_condition() and menu_button == 1:
            msg = go_font.render("WIN WIN WIN", True, (0, 128, 0))
            rect = msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(msg, rect)

            sub_msg = small_font.render("Press R to Restart or ESC for Menu", True, (255, 255, 255))
            sub_rect = sub_msg.get_rect(center=(screen.get_width() // 2, (screen.get_height() // 2) + 50))
            screen.blit(sub_msg, sub_rect)


        if not game.game_running:
            msg = go_font.render("GAME OVER", True, (255, 0, 0))
            rect = msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(msg, rect)
            if menu_button == 1:
                sub_msg = small_font.render("Press R to Restart or ESC for Menu", True, (255, 255, 255))
                sub_rect = sub_msg.get_rect(center=(screen.get_width() // 2, (screen.get_height() // 2) + 50))
            else:
                sub_msg = small_font.render("ESC for Menu", True, (255, 255, 255))
                sub_rect = sub_msg.get_rect(center=(screen.get_width() // 2, (screen.get_height() // 2) + 50))
            screen.blit(sub_msg, sub_rect)

        pygame.display.update()

pygame.quit()