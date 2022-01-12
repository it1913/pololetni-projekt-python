import math
import pygame

FPS = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800


bg = pygame.image.load('assets/background.jpg')
spaceShip = pygame.image.load('assets/spaceship.jpg')

pygame.display.set_caption('Asteroids')
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

gameover = False



class Ship(object):
    def __init__(self):
        self.img = spaceShip
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_HEIGHT//2
        self.angle = 0
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians((self.angle + 90)))
        self.head = (self.x + self.cosine + self.w//2, self.y - self.sine * self.h//2)

    def draw(self, window):
        window.blit(self.rotationSurf, self.rotationRect)

    def turnLeft(self):
        self.angle += 5
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head= (self.x + self.cosine + self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head= (self.x + self.cosine + self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self):
        self.x += self.cosine *6
        self.y -= self.sine *6
        self.rotationSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotationRect = self.rotationSurf.get_rect()
        self.rotationRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine + self.w // 2, self.y - self.sine * self.h // 2)


player= Ship()

def redrawGameWindow():
    window.blit(bg, (0,0))
    player.draw(window)
    pygame.display.update()

run= True

while run:
    clock.tick(FPS)
    if not gameover:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
                player.moveForward()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()
pygame.quit()