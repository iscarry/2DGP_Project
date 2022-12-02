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


    def update(self):
        self.rect.y += self.speed


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
    def collide_battleship(self, sprite):

            if pygame.sprite.collide_rect(self, sprite):
                return sprite


    def occur_explosion(screen, x, y):

        explosion_image = pygame.image.load('sprite/Boss_explosion.png')

        explosion_rect = explosion_image.get_rect()
        explosion_rect.x = x
        explosion_rect.y = y
        screen.blit(explosion_image, explosion_rect)
        pygame.display.flip()
