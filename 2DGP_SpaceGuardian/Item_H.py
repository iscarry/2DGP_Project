import pygame

class Item(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos, speed):
        super(Item, self).__init__()
        self.Item01 = pygame.image.load('sprite/item.png')
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
