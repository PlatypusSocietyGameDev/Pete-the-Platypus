import Vector2
from pygame import surface
import ctypes

user32 = ctypes.windll.user32
screenWidth, screenHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 60


def reposition(imageSurface: surface, anchorType) -> Vector2.New:
    pass