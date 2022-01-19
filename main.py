import math
import random
import pygame

FPS = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
playerBullet = []
asteroid = []
count = 0
MIN_ASTEROID_SPEED = 2
MAX_ASTEROID_SPEED = 3

bg = pygame.image.load('assets/background.jpg')
spaceShip = pygame.image.load('assets/spaceship.png')
rocket = pygame.image.load('assets/rocket.png')
midAsteroid = pygame.image.load('assets/midAsteroid.png')

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
    #Ničení střel, které letí pryč z hracího pole
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
        self.img = midAsteroid
        self.aWidth = self.img.get_width()
        self.aHeight = self.img.get_height()
        self.randomPoint = random.choice([(random.randrange(0, SCREEN_WIDTH-self.aWidth), random.choice([-1*self.aHeight - 5, SCREEN_HEIGHT + 5])), (random.choice([-1*self.aWidth - 5, SCREEN_WIDTH + 5]), random.randrange(0, SCREEN_HEIGHT - self.aHeight))])
        self.x, self.y = self.randomPoint

        if self.x < SCREEN_WIDTH//2:
            self.xDirection = random.random()
        else:
            self.xDirection = random.random() * -1

        if self.x < SCREEN_HEIGHT//2:
            self.yDirection = random.random()
        else:
            self.yDirection = random.random() * -1
        self.xVelocity = self.xDirection * random.randrange(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED)
        if self.xVelocity > 1:
            self.xVelocity = 2
        elif self.xVelocity < -1:
            self.xVelocity = -2
        self.yVelocity = self.yDirection * random.randrange(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED)
        if self.yVelocity > 1:
            self.yVelocity = 2
        elif self.yVelocity < -1:
            self.yVelocity = -2


    def draw(self, window):
        window.blit(self.img,(self.x, self.y))

    def borderCollision(self):
        if self.x < 0 - self.aWidth:
            return True
        elif self.x > SCREEN_WIDTH + self.aWidth:
            return True

        if self.y < 0 - self.aHeight:
            return True
        elif self.y > SCREEN_HEIGHT + self.aHeight:
            return True

player = Ship()

def redrawGameWindow():
    window.blit(bg, (0, 0))
    player.draw(window)
    for a in asteroid:
        a.draw(window)
    for b in playerBullet:
        b.draw(window)
    pygame.display.update()

run = True



while run:
    clock.tick(FPS)
    count += 1
    # print(len(playerBullet))
    # print(len(asteroid))
    player.moveForward()
    if not gameover:
        if count % 50 == 0:
            asteroid.append(Asteroid())

        for b in playerBullet:
            b.move()
            if b.borderCollision():
                playerBullet.pop(playerBullet.index(b))

        for a in asteroid:
            a.x += a.xVelocity
            a.y += a.yVelocity
            if a.borderCollision():
                asteroid.pop(asteroid.index(a))

            #Kolize střel a asteroidů
            for b in playerBullet:
                if(b.x >= a.x and b.x <= a.x + a.aWidth) or b.x + b.bWidth >= a.x and b.x + b.bWidth <= a.x + a.aWidth:
                    if(b.y >= a.y and b.y <= a.y + a.aHeight) or b.y + b.bHeight >= a.y and b.y + b.bHeight <= a.y + a.aHeight:
                        playerBullet.pop(playerBullet.index(b))
                        asteroid.pop(asteroid.index(a))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.movement = True

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playerBullet.append(Bullet())
            elif event.type == pygame.QUIT:
                run = False

    redrawGameWindow()
pygame.quit()