import pygame

FPS = 60
SCREEN_HEIGHT = 640
class Fire(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Fire, self).__init__()
        self.image = pygame.image.load('sprite/Fire.png')
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

    def occur_explosion(screen, x, y):

        explosion_image = []
        explosion_image.append(pygame.image.load('sprite/explosion01.png'))
        explosion_image.append(pygame.image.load('sprite/explosion02.png'))
        explosion_image.append(pygame.image.load('sprite/explosion03.png'))
        explosion_image.append(pygame.image.load('sprite/explosion04.png'))
        explosion_image.append(pygame.image.load('sprite/explosion05.png'))
        explosion_image.append(pygame.image.load('sprite/explosion06.png'))
        explosion_image.append(pygame.image.load('sprite/explosion07.png'))
        explosion_image.append(pygame.image.load('sprite/explosion08.png'))
        explosion_image.append(pygame.image.load('sprite/explosion09.png'))
        explosion_image.append(pygame.image.load('sprite/explosion10.png'))
        explosion_image.append(pygame.image.load('sprite/explosion11.png'))
        explosion_image.append(pygame.image.load('sprite/explosion12.png'))
        explosion_image.append(pygame.image.load('sprite/explosion13.png'))
        explosion_image.append(pygame.image.load('sprite/explosion14.png'))
        explosion_image.append(pygame.image.load('sprite/explosion15.png'))

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


    def miss_fire(self):
        if self.rect.y > SCREEN_HEIGHT:
            return True
