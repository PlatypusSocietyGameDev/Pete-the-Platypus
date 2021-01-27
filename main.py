import pygame
import constants


pygame.init()
pygame.display.set_caption('Pete the Platypus')
WindowIcon = pygame.image.load(r"assets/images/Petebetter1.png")


background_colour = (135, 206, 235)

pygame.display.set_icon(WindowIcon)
windowScreen = pygame.display.set_mode((constants.SCREENWIDTH, constants.SCREENHEIGHT))
windowScreen.fill(background_colour)

pygame.display.flip()

running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    windowScreen.fill(background_colour)

    pygame.display.flip()
