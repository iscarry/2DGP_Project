import pygame
from Fire_H import Fire
class Boss(pygame.sprite.Sprite):
    def __init__(self, xpos,  ypos, speed):
        super(Boss, self).__init__()
        self.image = pygame.image.load('sprite/Boss_rock.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.HP = 30

    def update(self):
        self.rect.y += self.speed


    # def draw(self, screen):
    #     screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


