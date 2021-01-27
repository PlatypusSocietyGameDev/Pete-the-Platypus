import pygame.image as image
from pygame import surface
import Vector2


class Background:
    def __init__(self, windowScreen: surface):
        self.imagePath = r"assets/images/background"
        self.imageSurface = image.load(self.imagePath)
        self.windowScreen = windowScreen
        self.bottomCentre = ()

    def draw(self):
        self.windowScreen.blit(self.imageSurface, )

