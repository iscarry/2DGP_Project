import pygame
import random
from time import sleep
import game_framework
import title_state
import Pause_state
from Battleship_H import BattleShip
from Fire_H import Fire
from Rock_H import Rock
from Item_H import Item
from Boss_H import Boss

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
boss = None
Occur_Rock = 1
Rock_Speed = 1
Max_Speed = 2
destroyed_rock = 0
count_miss = 0
fire_num = 1
unit_fall = True
rocks_count = 0


def draw_text(screen, text, font, x, y, color):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = x, y
    screen.blit(text_obj, text_rect)





def game_logic():
    global battleship, Occur_Rock, Rock_Speed, Max_Speed, destroyed_rock, count_miss, fire_num, unit_fall, boss, rocks_count
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 암석이 랜덤으로 뿌려줌
    if unit_fall == True:
        if random.randint(1, 60) == 1:
            for i in range(Occur_Rock):
                speed = random.randint(Rock_Speed, Max_Speed)
                rock = Rock(random.randint(30, SCREEN_WIDTH - 30), 0, speed)
                rocks.add(rock)
                rocks_count += 1
# 보스 등장

# 미사일과 돌이 충돌시 돌과 미사일을 지워줌
    for fire in fires:
        rock = fire.colide(rocks)

        if rock:
            #Fire.occur_explosion(screen, rock.rect.x, rock.rect.y)
            destroyed_rock += 1
            fire.kill()
            rock.kill()
            rocks_count -= 1
            if rock.image == rock.G_rock:
                speed = 2
                item = Item(rock.rect.x, rock.rect.y, speed)
                items.add(item)


#화면 밖으로 나간돌의 처리
    for rock in rocks:
        if rock.Count_miss_rock():
            rock.kill()
            rocks_count -= 1
            count_miss += 1
# 회면 밖으로 나간 미사일 처리
    for fire in fires:
        if fire.miss_fire():
            fire.kill()

# 운석과 충돌 하거나 운석을 3번 놓치면 게임 오버
    if battleship.collide(rocks) or count_miss >= 3:
        Fire.occur_explosion(screen, battleship.rect.x, battleship.rect.y)
        rocks.empty()
        battleship.reset()
        destroyed_rock = 0
        rocks_count = 0
        count_miss = 0
        fire_num = 1
        game_framework.change_state(title_state)
        sleep(1)

    if destroyed_rock >= 10 and rocks_count == 0:
        if boss.collide(fires):
            fire.kill()

        if battleship.collide_boss(boss):
            Fire.occur_explosion(screen, battleship.rect.x, battleship.rect.y)
            rocks.empty()
            battleship.reset()
            destroyed_rock = 0
            rocks_count = 0
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
    global battleship, fires, rocks, items, boss

    battleship = BattleShip()
    fires = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    items = pygame.sprite.Group()
    boss = pygame.sprite.Group()

def exit():
    global battleship, fires, rocks, boss
    del battleship
    del fires
    del rocks
    del boss

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
    if destroyed_rock >= 10 and rocks_count == 0:
        boss.update()


def draw_world():
    global destroyed_rock, count_miss, unit_fall
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Space_Guardian')
    background_image = pygame.image.load('sprite/background.png')
    default_font = pygame.font.Font(None, 28)
    clock = pygame.time.Clock()
    screen.blit(background_image, background_image.get_rect())
    draw_text(screen, 'Destroyed Meteorite: {}'.format(destroyed_rock),
              default_font, 110, 20, YELLOW)
    draw_text(screen, 'Missed Meteorite: {}'.format(count_miss),
              default_font, 340, 20, RED)

    if destroyed_rock >= 10:
        unit_fall = False
        if rocks_count == 0:
            boss.draw(screen)

    rocks.draw(screen)
    fires.draw(screen)
    items.draw(screen)
    battleship.draw(screen)
    #boss.draw(screen)
    clock.tick(FPS)
def draw():
    draw_world()
    pygame.display.flip()

def pause():
    pass

def resume():
    pass





