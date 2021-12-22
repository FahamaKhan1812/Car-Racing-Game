import pygame
import math
import time

from otherFunc import scale_image, blitRotateCenter


GRASS = scale_image(pygame.image.load('imgs/grass.jpg'), 2)
TRACK = scale_image(pygame.image.load('imgs/track.png'), .71)

TRACK_BORDER = scale_image(pygame.image.load('imgs/track-border.png'), .71)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = scale_image(pygame.image.load('imgs/finish.png'), .6)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (110, 205)

RED_CAR = scale_image(pygame.image.load('imgs/red-car.png'), 0.45)
GREEN_CAR = RED_CAR = scale_image(pygame.image.load('imgs/grey-car.png'), 0.45)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

GAME_WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Racing Game')

# Game FPS:
FPS = 20


class AbstractCar:
    IMG = RED_CAR

    def __init__(self, max_vel, rotation_vel):
        self.max_val = max_vel
        self.rotation_vel = rotation_vel
        self.vel = 0
        self.angle = 0
        self.img = self.IMG
        self.x, self.y = self.startPOS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blitRotateCenter(win, self.img, (self.x, self.y), self.angle)

    def moveForward(self):
        self.vel = min(self.vel + self.acceleration, self.max_val)
        self.move()

    def moveBackward(self):
        self.vel = min(self.vel - self.acceleration, -self.max_val/2, 0)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.x -= horizontal
        self.y -= vertical

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.startPOS
        self.vel = 0
        self.angle = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    startPOS = (130, 170)  # => Car Initial Position

    def reduceSpeed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.vel = - self.vel
        self.move()


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

class ComputerCar(AbstractCar):
    IMG = RED_CAR
    startPOS = (130, 170)

    def __init__(self, ):


run = True
clock = pygame.time.Clock()
player_car = PlayerCar(4, 4)

images = [
    (GRASS, (0, 0)),
    (TRACK, (0, 0)),
    (FINISH, FINISH_POSITION),
]

while run:
    clock.tick(FPS)
    draw(GAME_WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        moved = True
        player_car.moveForward()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        moved = True
        player_car.moveBackward()

    if not moved:
        player_car.reduceSpeed()

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide != None:
        if finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()


pygame.quit()
