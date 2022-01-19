import math
import pygame

FPS = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
playerBullet = []

bg = pygame.image.load('assets/background.jpg')
spaceShip = pygame.image.load('assets/spaceship.png')
rocket = pygame.image.load('assets/rocket.png')

pygame.display.set_caption('Asteroids')
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

gameover = False

class Game():
    pass

class Ship():
    def __init__(self):
        self.img = spaceShip
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_HEIGHT//2
        self.movement = False
        self.xx = 0
        self.yy = 0
        self.angle = 0
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians((self.angle + 90)))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, window):
        window.blit(self.rotationSurf, self.rotationRect)

    def turnLeft(self):
        self.angle += 5
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head= (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head= (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self):
        # Akcelerace a tření/zpomalování lodě
        if self.movement is True:
            self.xx += self.cosine * 0.1
            self.yy -= self.sine * 0.1
        elif self.movement is False and (self.xx < 0.0 or self.yy < 0.0):
            self.xx -= self.xx * 0.05
            self.yy -= self.yy * 0.05
        elif self.movement is False and (self.xx > 0.0 or self.yy > 0.0):
            self.xx -= self.xx * 0.05
            self.yy -= self.yy * 0.05
        # print(self.xx)
        # print(self.yy)
        self.x += self.xx
        self.y += self.yy
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)
        # Ošetření okrajů
        if self.x < 0 - self.w:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH + self.w:
            self.x = 0 - self.w

        if self.y < 0 - self.h:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT + self.h:
            self.y = 0 - self.h


class Bullet():
    def __init__(self):
        self.img = rocket
        self.shipPoint = player.head
        self.x, self.y = self.shipPoint
        self.shipRotation = pygame.transform.rotate(self.img, player.angle)
        self.shipRotationRect = self.shipRotation.get_rect()
        self.bWidth = self.img.get_width()
        self.bHeight = self.img.get_height()
        self.c = 0.8
        self.s = 0.8
        self.xVelocity = self.c * 10 * player.cosine
        self.yVelocity = self.c * 10 * player.sine

    def move(self):
        self.x += self.xVelocity
        self.y -= self.yVelocity
        self.shipRotationRect.center = (self.x, self.y)

    def draw(self, window):
        window.blit(self.shipRotation, self.shipRotationRect)

    def borderCollision(self):
        if self.x < 0 - self.bWidth:
            return True
        elif self.x > SCREEN_WIDTH + self.bWidth:
            return True

        if self.y < 0 - self.bHeight:
            return True
        elif self.y > SCREEN_HEIGHT + self.bHeight:
            return True

class Asteroid():
    def __init__(self):
        pass


player = Ship()

def redrawGameWindow():
    window.blit(bg, (0,0))
    player.draw(window)
    for b in playerBullet:
        b.draw(window)
    pygame.display.update()

run= True



while run:
    clock.tick(FPS)
    player.moveForward()
    if not gameover:
        for b in playerBullet:
            b.move()
            if b.borderCollision():
                playerBullet.pop(playerBullet.index(b))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.movement = True
            # print(player.movement)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playerBullet.append(Bullet())

                    # print(player.movement)
            elif event.type == pygame.QUIT:
                run = False
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     player.turnLeft()
        # if keys[pygame.K_RIGHT]:
        #     player.turnRight()







    redrawGameWindow()
pygame.quit()