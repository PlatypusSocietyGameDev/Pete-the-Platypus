import pygame
import constants
import Image
import UDim2
import Enums
import Player
import Vector2
from miscellaneous import drawtext
import ImageTessellate
from time import time


pygame.init()
pygame.display.set_caption('Pete the Platypus')
WindowIcon = pygame.image.load(r"assets/images/smallicon.png")


background_colour = (135, 206, 235)

pygame.display.set_icon(WindowIcon)
windowScreen = pygame.display.set_mode((constants.SCREENWIDTH, constants.SCREENHEIGHT))
windowScreen.fill(background_colour)
pygame.display.flip()

running = True

Background = Image.New(
    windowScreen,
    r"assets/images/background.jpg",

    UDim2.New(0, 0, 0, 0),
    UDim2.New(1, 0, 1, 0),
    Vector2.New(0, 0)
)

DirtWalls = [
    ImageTessellate.New(
        windowScreen,
        r"assets/images/DirtWalls1.png",

        UDim2.New(0, 0, 0, 0),

        UDim2.New(0, 200, 1, 0),
        UDim2.New(0, 150, 0, 150),

        Vector2.New(0, 0)
    ),

    ImageTessellate.New(
        windowScreen,
        r"assets/images/DirtWalls1.png",

        UDim2.New(1, -200, 0, 0),

        UDim2.New(0, 200, 1, 0),
        UDim2.New(0, 150, 0, 150),

        Vector2.New(0, 0)
    ),

    Image.New(
        windowScreen,
        r"assets/images/obstacleMaskTest.png",
        UDim2.New(.5, 0, .5, 0),
        UDim2.New(0, 500, 0, 500),
        Vector2.New(.5, .5)
    ),
]


DirtGround = ImageTessellate.New(
    windowScreen,
    r"assets/images/GrassBlock.png",

    UDim2.New(0.5, 0, 0, 0),

    UDim2.New(1, 0, 0, 75),
    UDim2.New(0, 75, 0, 75),

    Vector2.New(0.5, 0)
)

# Comment the line below, if you want to test the mask collision
#del DirtWalls[-1]

player = Player.New(windowScreen, Vector2.New(500, 1000))

clock = pygame.time.Clock()
gameFPS = 60

while running:
    s = time()

    dt = clock.tick(60)
    pygame.display.set_caption(f'Pete the Platypus {gameFPS}')

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    #windowScreen.fill(background_colour)

    Background.draw()
    for wall in DirtWalls:
        wall.draw()
    DirtGround.draw()

    player.refresh()
    player.draw()

    player.move(dt, {
        "W": keys[pygame.K_w],
        "A": keys[pygame.K_a],
        #"S": keys[pygame.K_s],
        "D": keys[pygame.K_d],
    }, *DirtWalls, DirtGround)

    pygame.display.flip()

    e = time()
    gameFPS = round(1 / (e - s), 2)
