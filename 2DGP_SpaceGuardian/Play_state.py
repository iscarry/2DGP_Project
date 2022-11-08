import pygame
import os
import sys
import random
from time import sleep
import game_framework
import title_state
import Pause_state

# 정의
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)
FPS = 60
battleship = None
fires = None
rocks = None
items = None
Ocur_Rock = 1
Rock_Speed = 1
Max_Speed = 2
destroied_rock = 0
count_miss = 0
fire_num = 1

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

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite



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
            if random.randint(1, 2) == 1:
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

class Item(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos, speed):
        super(Item, self).__init__()
        self.Item01 = pygame.image.load('item.png')
        self.image = self.Item01
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    # def collide(self, sprites):
    #     for sprite in sprites:
    #         if pygame.sprite.collide_rect(self, battleship):
    #             fire_num += 1
    #             return sprite

def draw_text(screen, text, font, x, y, color):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = x, y
    screen.blit(text_obj, text_rect)


def occur_explosion(screen, x, y):

    explosion_image = []
    explosion_image.append(pygame.image.load('explosion01.png'))
    explosion_image.append(pygame.image.load('explosion02.png'))
    explosion_image.append(pygame.image.load('explosion03.png'))
    explosion_image.append(pygame.image.load('explosion04.png'))
    explosion_image.append(pygame.image.load('explosion05.png'))
    explosion_image.append(pygame.image.load('explosion06.png'))
    explosion_image.append(pygame.image.load('explosion07.png'))
    explosion_image.append(pygame.image.load('explosion08.png'))
    explosion_image.append(pygame.image.load('explosion09.png'))
    explosion_image.append(pygame.image.load('explosion10.png'))
    explosion_image.append(pygame.image.load('explosion11.png'))
    explosion_image.append(pygame.image.load('explosion12.png'))
    explosion_image.append(pygame.image.load('explosion13.png'))
    explosion_image.append(pygame.image.load('explosion14.png'))
    explosion_image.append(pygame.image.load('explosion15.png'))

    current_time = 0
    clock = pygame.time.Clock()
    frame = round(100 / len(explosion_image * 100), 2)
    current_time += clock.tick(FPS)
    index = 0
    count = 15

    if current_time >= frame:
        current_time = 0
        index = (index % count)
        image = explosion_image[index]
        index += 1

        if index >= len(explosion_image):
            index = 0

    explosion_rect = image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    screen.blit(image, explosion_rect)
    pygame.display.flip()




def game_logic():
    global Ocur_Rock, Rock_Speed, Max_Speed, destroied_rock, count_miss, fire_num
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 암석이 랜덤으로 뿌려줌
    if random.randint(1, 60) == 1:
        for i in range(Ocur_Rock):
            speed = random.randint(Rock_Speed, Max_Speed)
            rock = Rock(random.randint(30, SCREEN_WIDTH - 30), 0, speed)
            rocks.add(rock)


# 미사일과 돌이 충돌시 돌과 미사일을 지워줌
    for fire in fires:
        rock = fire.colide(rocks)
        if rock:
            occur_explosion(screen, rock.rect.x, rock.rect.y)
            destroied_rock += 1
            fire.kill()
            rock.kill()
            if rock.image == rock.G_rock:
                speed = 2
                item = Item(rock.rect.x, rock.rect.y, speed)
                items.add(item)



#화면 밖으로 나간돌의 처리
    for rock in rocks:
        if rock.Count_miss_rock():
            rock.kill()
            count_miss += 1

# 운석과 충돌 하거나 운석을 3번 놓치면 게임 오버
    if battleship.collide(rocks) or count_miss >= 3:
        occur_explosion(screen, battleship.rect.x, battleship.rect.y)
        rocks.empty()
        battleship.reset()
        destroied_rock = 0
        count_miss = 0
        fire_num = 1
        game_framework.change_state(title_state)
        sleep(1)
# 아이템을 먹었을 때 발사체 수 증가
    for item in items:
        if battleship.collide(items):
            if fire_num < 5:
                fire_num += 1
            item.kill()

pygame.init()

def enter():
    global battleship, fires, rocks, items

    battleship = BattleShip()
    fires = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    items = pygame.sprite.Group()

def exit():
    global battleship, fires, rocks
    del battleship
    del fires
    del rocks

def handle_events():
    global fire_num

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_framework.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                battleship.direction = "left"
                battleship.state = 2
            elif event.key == pygame.K_RIGHT:
                battleship.direction = "right"
                battleship.state = 1
            elif event.key == pygame.K_UP:
                battleship.direction = "up"
                battleship.state = 3
            elif event.key == pygame.K_DOWN:
                battleship.direction = "down"
                battleship.state = 4
            elif event.key == pygame.K_SPACE:
                if fire_num == 1:
                    fire = Fire(battleship.rect.centerx - 10, battleship.rect.y, 10)
                    fires.add(fire)
                elif fire_num == 2:
                    fire01 = Fire(battleship.rect.centerx - 25, battleship.rect.y, 10)
                    fire02 = Fire(battleship.rect.centerx + 5, battleship.rect.y, 10)
                    fires.add(fire01)
                    fires.add(fire02)
                elif fire_num == 3:
                    fire01 = Fire(battleship.rect.centerx + 5, battleship.rect.y, 10)
                    fire02 = Fire(battleship.rect.centerx - 15, battleship.rect.y, 10)
                    fire03 = Fire(battleship.rect.centerx - 35, battleship.rect.y, 10)
                    fires.add(fire01)
                    fires.add(fire02)
                    fires.add(fire03)
                elif fire_num == 4:
                    fire01 = Fire(battleship.rect.centerx + 15, battleship.rect.y, 10)
                    fire02 = Fire(battleship.rect.centerx - 5, battleship.rect.y, 10)
                    fire03 = Fire(battleship.rect.centerx - 25, battleship.rect.y, 10)
                    fire04 = Fire(battleship.rect.centerx - 45, battleship.rect.y, 10)
                    fires.add(fire01)
                    fires.add(fire02)
                    fires.add(fire03)
                    fires.add(fire04)
                elif fire_num == 5:
                    fire01 = Fire(battleship.rect.centerx + 25, battleship.rect.y, 10)
                    fire02 = Fire(battleship.rect.centerx + 5, battleship.rect.y, 10)
                    fire03 = Fire(battleship.rect.centerx - 15, battleship.rect.y, 10)
                    fire04 = Fire(battleship.rect.centerx - 35, battleship.rect.y, 10)
                    fire05 = Fire(battleship.rect.centerx - 55, battleship.rect.y, 10)
                    fires.add(fire01)
                    fires.add(fire02)
                    fires.add(fire03)
                    fires.add(fire04)
                    fires.add(fire05)


            elif event.key == pygame.K_ESCAPE:
                game_framework.push_state(Pause_state)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                battleship.direction = "stay"
                battleship.state = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                battleship.direction = "stay"
                battleship.state = 0

    return False


def update():
    battleship.update()
    fires.update()
    rocks.update()
    items.update()
    game_logic()


def draw_world():
    global destroied_rock, count_miss
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Space_Guardian')
    background_image = pygame.image.load('background.png')
    default_font = pygame.font.Font(None, 28)
    clock = pygame.time.Clock()
    screen.blit(background_image, background_image.get_rect())
    draw_text(screen, 'Destroyed Meteorite: {}'.format(destroied_rock),
              default_font, 110, 20, YELLOW)
    draw_text(screen, 'Missed Meteorite: {}'.format(count_miss),
              default_font, 340, 20, RED)

    rocks.draw(screen)
    fires.draw(screen)
    items.draw(screen)
    battleship.draw(screen)
    clock.tick(FPS)
def draw():
    draw_world()
    pygame.display.flip()

def pause():
    pass

def resume():
    pass





