import pygame
import constants
import Image
import UDim2
import Enums


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
    UDim2.New(0.5, 0, 1, 0),
    Enums.AnchorType.BottomLeft
)

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    windowScreen.fill(background_colour)

    Background.draw()

    pygame.display.flip()
