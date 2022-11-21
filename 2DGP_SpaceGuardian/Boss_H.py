import pygame
from Fire_H import Fire
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.Boss01 = pygame.image.load('sprite/Boss_rock.png')
        self.image = self.Boss01
        self.rect = self.Boss01.get_rect()
        self.rect.x = 100
        self.rect.y = 10
        self.speed = 1
        self.HP = 30

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


