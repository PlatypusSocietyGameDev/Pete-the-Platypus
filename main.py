import pygame

pygame.init()
pygame.display.set_caption('Pete the Platypus')
WindowIcon = pygame.image.load("assets\icon.png")
screenWidth, screenHeight = (1920, 1080)
background_colour = (135, 206, 235)

windowScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
windowScreen.fill(background_colour)

pygame.display.set_icon(WindowIcon)
pygame.display.flip()

running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    windowScreen.fill(background_colour)

    pygame.display.flip()
