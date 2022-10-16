import pygame
import os
import sys
import random
from time import sleep


# 정의
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

FPS = 60

#클레스

class BattleShip(pygame.sprite.Sprite):
    def __init__(self):
        super(BattleShip, self).__init__()
        self.images = []
        # 0 가만히 있는 상태
        self.images.append(pygame.image.load('Battleship.png'))
        # 1 ~ 2 오른쪽 움직임
        self.images.append(pygame.image.load('Battleship_R1.png'))
        self.images.append(pygame.image.load('Battleship_R2.png'))
        # 3 ~ 4 왼쪽 움직임
        self.images.append(pygame.image.load('Battleship_L1.png'))
        self.images.append(pygame.image.load('Battleship_L2.png'))
        # 5 ~ 6 위쪽 움직임
        self.images.append(pygame.image.load('Battleship_U1.png'))
        self.images.append(pygame.image.load('Battleship_U2.png'))
        # 7 ~ 8 아래쪽 움직임
        self.images.append(pygame.image.load('Battleship_D1.png'))
        self.images.append(pygame.image.load('Battleship_D2.png'))

        self.images_stay = self.images
        self.images_right = self.images
        self.images_left = self.images
        self.images_up = self.images
        self.images_down = self.images
        self.state = 0
        self.direction = 'stay'
        self.velocity_x = 0
        self.velocity_y = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.frame = round(100 / len(self.images*100), 2)
        self.current_time = 0
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.rect.x = (SCREEN_WIDTH * 0.4)
        self.rect.y = (SCREEN_HEIGHT * 0.8)
    def update(self):

        # 상태를 처리
        if self.state == 0:
            count = 1
            start_index = 0
            self.velocity_x = 0
            self.velocity_y = 0
        elif self.state == 1:
            count = 2
            start_index = 1
            self.velocity_x = 5
            self.velocity_y = 0
        elif self.state == 2:
            count = 2
            start_index = 3
            self.velocity_x = 5
            self.velocity_y = 0

        elif self.state == 3:
            count = 2
            start_index = 5
            self.velocity_x = 0
            self.velocity_y = 5

        elif self.state == 4:
            count = 2
            start_index = 7
            self.velocity_x = 0
            self.velocity_y = 5


        if self.direction == 'stay':
            self.images = self.images_stay
        elif self.direction == 'right':
            self.images = self.images_right
        elif self.direction == 'left':
            self.images = self.images_left
            self.velocity_x = abs(self.velocity_x) * -1
        elif self.direction == 'up':
            self.images = self.images_up
            self.velocity_y = abs(self.velocity_y) * -1
        elif self.direction == 'down':
            self.images = self.images_down

        self.current_time += self.clock.tick(FPS)

        if self.current_time >= self.frame:
            self.current_time = 0

            self.index = (self.index % count) + start_index
            self.image = self.images[self.index]
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # 스크린에서 나가지 않게 해주는 코드
        if self.rect.x < 0 or self.rect.x + self.rect.width > SCREEN_WIDTH:
            self.rect.x -= self.velocity_x

        if self.rect.y < 0 or self.rect.y + self.rect.height > SCREEN_HEIGHT:
            self.rect.y -= self.velocity_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def colide(self):
        pass



class Fire(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Fire, self).__init__()
        self.image = pygame.image.load('Fire.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed

    def colide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        self.rock01 = pygame.image.load('Rock01.png')
        self.G_rock = pygame.image.load('G_Rock.png')
        self.U_Rock = pygame.image.load('unique_rock.png')

        self.image = random.randint(1, 3)
        if self.image == 1:
            self.image = self.rock01
        elif self.image == 2:
            self.image = self.U_Rock
        else:
            if random.randint(1, 10) == 1:
                self.image = self.G_rock
            else:
                self.image = self.rock01

        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed



    def update(self):
        self.rect.y += self.speed

    def Count_miss_rock(self):
        if self.rect.y > SCREEN_HEIGHT:
            return True
class Game():
    def __init__(self):
        self.background_image = pygame.image.load('background.png')
        self.menu_image = pygame.image.load('menu_BG.png')
        self.battleship = BattleShip()
        self.fires = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()

        self.count_miss = 0
        self.destroied_rock = 0
        self.default_font = pygame.font.Font(None, 28)
        self.menu_on = True

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if self.menu_on:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.menu_on = False
            else:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.battleship.direction = "left"
                        self.battleship.state = 2
                    elif event.key == pygame.K_RIGHT:
                        self.battleship.direction = "right"
                        self.battleship.state = 1
                    elif event.key == pygame.K_UP:
                        self.battleship.direction = "up"
                        self.battleship.state = 3
                    elif event.key == pygame.K_DOWN:
                        self.battleship.direction = "down"
                        self.battleship.state = 4
                    elif event.key == pygame.K_SPACE:
                        fire = Fire(self.battleship.rect.centerx, self.battleship.rect.y, 10)
                        self.fires.add(fire)
                    elif event.key == pygame.K_ESCAPE:
                        return True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        self.battleship.direction = "stay"
                        self.battleship.state = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.battleship.direction = "stay"
                        self.battleship.state = 0


        return False

    def game_logic(self, screen):
        Ocur_Rock = 1
        Rock_Speed = 1
        Max_Speed = 2

        if random.randint(1, 60) == 1:
            for i in range(Ocur_Rock):
                speed = random.randint(Rock_Speed, Max_Speed)
                rock = Rock(random.randint(30, SCREEN_WIDTH - 30), 0, speed)
                self.rocks.add(rock)

        for fire in self.fires:
            rock = fire.colide(self.rocks)
            if rock:
                self.destroied_rock += 1
                fire.kill()
                rock.kill()

        for rock in self.rocks:
            if rock.Count_miss_rock():
                rock.kill()
                self.count_miss += 1

    def draw_text(self, screen, text, font, x, y, color):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = x, y
        screen.blit(text_obj, text_rect)

    def display_menu(self, screen):
        screen.blit(self.menu_image, [0, 0])
        draw_x = int(SCREEN_WIDTH / 2)
        draw_y = int(SCREEN_HEIGHT / 4)
        self.draw_text(screen, 'Save The Earth', self.default_font, draw_x, draw_y, YELLOW)
        self.draw_text(screen, 'Press Space Button', self.default_font, draw_x, draw_y + 200, WHITE)
        self.draw_text(screen, 'Start Game', self.default_font, draw_x, draw_y + 250, WHITE)

    def display_frame(self, screen):

        screen.blit(self.background_image, self.background_image.get_rect())
        self.draw_text(screen, 'Destroyed Meteorite: {}'.format(self.destroied_rock),
                       self.default_font, 110, 20, YELLOW)
        self.draw_text(screen, 'Missed Meteorite: {}'.format(self.count_miss),
                       self.default_font, 340, 20, RED)
        self.rocks.update()
        self.rocks.draw(screen)
        self.fires.update()
        self.fires.draw(screen)
        self.battleship.update()
        self.battleship.draw(screen)




def main():
    pygame.init()
    pygame.display.set_caption('Space_Guardian')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    done = False

    while not done:

        done = game.process_events()
        if game.menu_on:
            game.display_menu(screen)
        else:
            game.game_logic(screen)
            game.display_frame(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()



