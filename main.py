import pygame
import ctypes


pygame.init()
pygame.display.set_caption('Pete the Platypus')
WindowIcon = pygame.image.load(r"assets/images/icon.png")

user32 = ctypes.windll.user32
screenWidth, screenHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 60

background_colour = (135, 206, 235)

windowScreen = pygame.display.set_mode((screenWidth, screenHeight))
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
