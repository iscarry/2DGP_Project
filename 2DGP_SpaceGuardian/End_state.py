import pygame
import game_framework
import title_state

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
WHITE = (200, 200, 200)
YELLOW = (250, 250, 50)


def draw_text(screen, text, font, x, y, color):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = x, y
    screen.blit(text_obj, text_rect)


def enter():
    global image
    image = pygame.image.load('sprite/End_earth.jpg')



def exit():
    global image
    del image

def handle_events():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return True
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                game_framework.change_state(title_state)

def draw():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    default_font = pygame.font.Font(None, 28)
    draw_x = int(SCREEN_WIDTH / 2)
    draw_y = int(SCREEN_HEIGHT / 4)
    screen.blit(image, image.get_rect())
    draw_text(screen, 'The Earth is destroyed', default_font, draw_x, draw_y, YELLOW)
    draw_text(screen, 'Press Tap Button', default_font, draw_x, draw_y + 200, WHITE)
    draw_text(screen, 'Go to title', default_font, draw_x, draw_y + 250, WHITE)
    pygame.display.flip()

def update():
    pass

def pause():
    pass

def resume():
    pass


