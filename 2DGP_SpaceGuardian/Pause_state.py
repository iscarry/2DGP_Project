import pygame
import game_framework
import Play_state
import title_state

image = None
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
WHITE = (200, 200, 200)

def enter():
    global image
    image = pygame.image.load('Pause.png')

def exit():
    global image
    del image

def update():
    pass

def draw():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)
    Play_state.draw_world()
    screen.blit(image, (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 4))
    pygame.display.flip()

def handle_events():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_framework.quit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_1:
                    game_framework.change_state(title_state)
                case pygame.K_2:
                    game_framework.pop_state()



