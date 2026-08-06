import pygame
pygame.init()

screen = pygame.display.set_mode((450, 600))

timer_font = pygame.font.SysFont("Arial", 30)
timer_sec = 300
timer_text = timer_font.render("05:00", True, (255, 255, 255))


timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1000)    # sets timer with USEREVENT and delay in milliseconds

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == timer:    # checks for timer event
            if timer_sec > 0:
                timer_sec -= 100
                min = timer_sec // 60
                sec = timer_sec % 60
                if timer_sec % 60 == 0:
                    timer_text = timer_font.render("%02d:%02d" % (min , sec), True, (255, 0, 0))
                else:
                    timer_text = timer_font.render("%02d:%02d" % (min, sec), True, (255, 255, 255))
            else:
                pygame.time.set_timer(timer, 0)    # turns off timer event

# add another "if timer_sec > 0" here if you want the timer to disappear after reaching 0
    screen.blit(timer_text, (300, 20))
    pygame.display.update()