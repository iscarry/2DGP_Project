import pygame
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        self.rock01 = pygame.image.load('sprite/Rock01.png')
        self.G_rock = pygame.image.load('sprite/G_Rock.png')
        self.U_Rock = pygame.image.load('sprite/unique_rock.png')

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
