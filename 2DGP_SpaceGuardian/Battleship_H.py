import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60

class BattleShip(pygame.sprite.Sprite):
    def __init__(self):
        super(BattleShip, self).__init__()
        self.images = []
        # 0 가만히 있는 상태
        self.images.append(pygame.image.load('sprite/Battleship.png'))
        # 1 ~ 2 오른쪽 움직임
        self.images.append(pygame.image.load('sprite/Battleship_R1.png'))
        self.images.append(pygame.image.load('sprite/Battleship_R2.png'))
        # 3 ~ 4 왼쪽 움직임
        self.images.append(pygame.image.load('sprite/Battleship_L1.png'))
        self.images.append(pygame.image.load('sprite/Battleship_L2.png'))
        # 5 ~ 6 위쪽 움직임
        self.images.append(pygame.image.load('sprite/Battleship_U1.png'))
        self.images.append(pygame.image.load('sprite/Battleship_U2.png'))
        # 7 ~ 8 아래쪽 움직임
        self.images.append(pygame.image.load('sprite/Battleship_D1.png'))
        self.images.append(pygame.image.load('sprite/Battleship_D2.png'))

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

    def collide_boss(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

