from pygame.font import Font


def drawtext(window, colour, pos, text="", font=20, fontlocation=""):
    if fontlocation == "":
        textSettings = Font('freesansbold.ttf', font)
    else:
        textSettings = Font(fontlocation, font)

    Text = textSettings.render(text, True, colour)
    TextRect = Text.get_rect()
    TextRect.x, TextRect.y = pos
    window.blit(Text, TextRect)
