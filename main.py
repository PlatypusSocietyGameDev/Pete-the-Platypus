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

        UDim2.New(0, 0, 0, 75),

        UDim2.New(0, 200, 1, -75),
        UDim2.New(0, 150, 0, 150),

        Vector2.New(0, 0)
    ),

    ImageTessellate.New(
        windowScreen,
        r"assets/images/DirtWalls1.png",

        UDim2.New(1, -200, 0, 75),

        UDim2.New(0, 200, 1, -75),
        UDim2.New(0, 150, 0, 150),

        Vector2.New(0, 0)
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

TestDirtBlock = Image.New(
    windowScreen,
    r"assets/images/GrassBlock.png",

    UDim2.New(.5, 0, .5, 0),
    UDim2.New(0, 100, 0, 100),
    Vector2.New(.5, .5) 
)

player = Player.New(windowScreen, Vector2.New(500, 1000))
player.addObstacle(DirtGround, *DirtWalls)
player.addWall(*DirtWalls)

clock = pygame.time.Clock()
gameFPS = 60
fps = []

while running:
    s = time()

    dt = clock.tick(60)
    fps.append(gameFPS)
    pygame.display.set_caption(f'Pete the Platypus, Average: {gameFPS}')
    
    keys = pygame.key.get_pressed()

    eventKeys = []
    mouseDown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

        elif event.type == pygame.KEYDOWN:
            eventKeys.append(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True

    #windowScreen.fill(background_colour)

    Background.draw()
    player.drawRadius()

    player.drawWalls()
    player.drawObstacles()
    player.drawValidWalls()

    TestDirtBlock.draw()

    player.refresh()
    player.draw()
    player.placeBlock(eventKeys, pygame.mouse.get_pos(), mouseDown)

    player.move(dt, {
        "W": keys[pygame.K_w],
        "A": keys[pygame.K_a],
        #"S": keys[pygame.K_s],
        "D": keys[pygame.K_d],
    })

    pygame.display.flip()

    e = time()
    gameFPS = round(1 / (e - s), 2)
