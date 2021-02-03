from pygame.font import Font
from pygame import Color


def fillSurface(oldSurface, color):
    surface = oldSurface.copy()

    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), Color(r, g, b, a))

    return surface


def fillSurfaceTransparency(oldSurface, color):
    surface = oldSurface.copy()

    w, h = surface.get_size()
    r, g, b, customA = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), Color(r, g, b, customA if a != 0 else a))

    return surface


def drawtext(window, colour, pos, text="", font=20, fontlocation=""):
    if fontlocation == "":
        textSettings = Font('freesansbold.ttf', font)
    else:
        textSettings = Font(fontlocation, font)

    Text = textSettings.render(text, True, colour)
    TextRect = Text.get_rect()
    TextRect.x, TextRect.y = pos
    window.blit(Text, TextRect)
