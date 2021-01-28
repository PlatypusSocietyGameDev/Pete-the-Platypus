import pygame
import constants
import Image
import UDim2
import Enums
import Player
import Vector2
from miscellaneous import drawtext


pygame.init()
pygame.display.set_caption('Pete the Platypus')
WindowIcon = pygame.image.load(r"assets/images/Petebetter1.png")


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
    Enums.AnchorType.BottomLeft
)

player = Player.New(windowScreen, Vector2.New(500, 100))

clock = pygame.time.Clock()

while running:
    dt = clock.tick(60)
    gameFPS = round(1000 / dt, 2)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    windowScreen.fill(background_colour)

    Background.draw()
    player.refresh()
    player.draw()

    player.move(dt, {
        "W": keys[pygame.K_w],
        "A": keys[pygame.K_a],
        "S": keys[pygame.K_s],
        "D": keys[pygame.K_d],
    })
    
    drawtext(windowScreen, (0, 0, 0), (10, 10), f"Current FPS {gameFPS}")
    drawtext(windowScreen, (0, 0, 0), (10, 40), f"Target FPS {60}")

    pygame.display.flip()
