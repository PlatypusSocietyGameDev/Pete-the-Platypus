import Vector2
from pygame import surface
import ctypes
import Enums
import UDim2


user32 = ctypes.windll.user32
screenWidth, screenHeight = (1920, 1020)


def setScreenData(width, height):
    global screenWidth, screenHeight

    screenWidth, screenHeight = width, height


def getTopLeft(imageSurface: surface, anchorType: Enums.AnchorType, anchorUDim2: UDim2) -> Vector2.New:
    pass