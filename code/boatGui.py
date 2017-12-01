import pygame, math, sys 
import sendCommand
from pygame.locals import *

screen = pygame.display.set_mode((1024,750))

clock = pygame.time.Clock()

BLUE = (50,50,235)

class BoatSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position

    def update(self, direction):
        self.image = pygame.transform.rotate(self.src_image, direction)
        self.rect = self.image.get_rect(center=rect.center)

class CompSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect(center=position)

class WindSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect(center=position)

class RudderSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.rect = self.src_image.get_rect(center=position)

    def update(self, direction):
        self.image = pygame.transform.rotate(self.src_image, direction)
        self.rect = self.image.get_rect(center=(800,600))

class MainSailSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.rect = self.src_image.get_rect(center=position)

    def update(self, direction):
        self.image = pygame.transform.rotate(self.src_image, direction)
        self.rect = self.image.get_rect(center=(800,105))

class AftSailSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.rect = self.src_image.get_rect(center=position)

    def update(self, direction, coords):
        self.image = pygame.transform.rotate(self.src_image, direction)
        self.rect = self.image.get_rect(center=coords)

#sendCommand.readPIInput()
rect = screen.get_rect()
boat = BoatSprite('../../../Downloads/boat.png', rect.center)
compass = CompSprite('../../../Downloads/compass.png', rect.center)
wind = WindSprite('../../../Downloads/wind.png', (200,200))
rudder = RudderSprite('../../../Downloads/rudder.png', (800,600))
mainsail = MainSailSprite('../../../Downloads/sail.png',(800,105))
aftsail = AftSailSprite('../../../Downloads/sail.png',(800,200))
render_rudder = pygame.sprite.RenderPlain(rudder)
render_wind = pygame.sprite.RenderPlain(wind)
render_boat = pygame.sprite.RenderPlain(boat)
render_compass = pygame.sprite.RenderPlain(compass)
render_mainsail = pygame.sprite.RenderPlain(mainsail)
render_aftsail = pygame.sprite.RenderPlain(aftsail)
boat_angle = 0
rudder_angle = 0
mainsail_angle = 360
aftsail_angle = 360
aftsail_coords = (800,200)
while 1:
    # this section gets the user input
    clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue

        #elif event.key == K_LEFT: boat_angle = angle + 1
        #if event.key == K_RIGHT and event.type == KEYDOWN: angle = angle - 1
        #elif event.key == K_LEFT: angle = angle + 1
        # servo control
        elif event.key == K_q and event.type == KEYDOWN: #rudder left
            sendCommand.sendCommand('7')
            rudder_angle = rudder_angle + 1
        elif event.key == K_e and event.type == KEYDOWN: #rudder right
            rudder_angle = rudder_angle - 1
        elif event.key == K_s and event.type == KEYDOWN: #main center
            mainsail_angle = 0
            sendCommand.sendCommand('2')
        elif event.key == K_a and event.type == KEYDOWN: #main right
            mainsail_angle = mainsail_angle - 1
            sendCommand.sendCommand('3')
        elif event.key == K_d and event.type == KEYDOWN: #main left
            mainsail_angle = mainsail_angle + 1
            sendCommand.sendCommand('1')
        elif event.key == K_z and event.type == KEYDOWN: #aft right
            aftsail_angle = aftsail_angle - 1
            sendCommand.sendCommand('6')
        elif event.key == K_x and event.type == KEYDOWN: #aft center
            aftsail_angle = 0
            sendCommand.sendCommand('5')
        elif event.key == K_c and event.type == KEYDOWN: #aft left
            aftsail_angle = aftsail_angle + 1
            sendCommand.sendCommand('4')
        elif event.key == K_ESCAPE: sys.exit(0)

    screen.fill(BLUE)
    render_compass.draw(screen)
    render_wind.draw(screen)
    render_boat.update(0)
    render_boat.draw(screen)
    render_rudder.update(rudder_angle)
    render_rudder.draw(screen)
    render_mainsail.update(mainsail_angle)
    render_mainsail.draw(screen)
    render_aftsail.update(aftsail_angle, aftsail_coords)
    render_aftsail.draw(screen)
    pygame.display.flip()


# calculates the new coords the aftsail will be at
# when main sail moves.
# must use angle movement based on counterclockwise movement
#def computeAftPosition(oldCoords, offsetCoords, angleMov):


