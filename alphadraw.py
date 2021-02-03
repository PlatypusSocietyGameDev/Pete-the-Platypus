import pygame.draw as draw
from pygame import Surface, SRCALPHA, Rect


def rect(surface: Surface, colour: tuple, rectPositions: tuple):
    shape_surf = Surface(Rect(rectPositions).size, SRCALPHA)
    draw.rect(shape_surf, colour, shape_surf.get_rect())
    surface.blit(shape_surf, rectPositions)
