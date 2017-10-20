import pygame, math, sys 
import sendCommand
from pygame.locals import *

screen = pygame.display.set_mode((1024,768))

clock = pygame.time.Clock()

BLUE = (50,50,235)

boat_position = 0;

class BoatSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        boat_position = self.position

    def update(self, direction):
        self.image = pygame.transform.rotate(self.src_image, direction)
        self.rect = self.image.get_rect(center=rect.center)

class CompSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect(center=rect.center)

class WindSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect()

rect = screen.get_rect()
boat = BoatSprite('../../../Downloads/boat.png', rect.center)
compass = CompSprite('../../../Downloads/compass.png', boat_position)
wind = WindSprite('../../../Downloads/wind.png', (50,50))
render_wind = pygame.sprite.RenderPlain(wind)
render_boat = pygame.sprite.RenderPlain(boat)
render_compass = pygame.sprite.RenderPlain(compass)
angle = 0
while 1:
    # this section gets the user input
    clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue

        elif event.key == K_LEFT: angle = angle + 1
        if event.key == K_RIGHT and event.type == KEYDOWN: angle = angle - 1
        elif event.key == K_LEFT: angle = angle + 1
        # servo control
        elif event.key == K_q: sendCommand.sendCommand('7')
        elif event.key == K_ESCAPE: sys.exit(0)

    screen.fill(BLUE)
    render_compass.draw(screen)
    render_wind.draw(screen)
    render_boat.update(angle)
    render_boat.draw(screen)
    pygame.display.flip()
