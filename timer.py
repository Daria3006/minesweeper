import pygame
pygame.init()

def create_timer():
    timer_font = pygame.font.SysFont("Arial", 30)
    timer_sec = 300
    timer_text = timer_font.render("05:00", True, (255, 255, 255))
    timer = pygame.USEREVENT + 1
    pygame.time.set_timer(timer, 1000)
    return timer_font , timer_sec, timer_text
