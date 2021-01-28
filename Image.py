import pygame.image as image
import pygame.transform as transform
from miscellaneous import *
from pygame import surface
import Enums
import UDim2


class New:
    def __init__(self, windowScreen: surface, imagePath: str, UDim2Pos: UDim2.New, UDim2Scale: UDim2.New, anchorType: Enums.AnchorType):
        self.windowScreen = windowScreen

        self.imagePath = imagePath
        self.imageSurface = image.load(self.imagePath)

        absoluteSize = absoluteUDim2(UDim2Scale)
        self.imageSurface = transform.scale(self.imageSurface,
                                            absoluteSize.tuple
                                            )

        self.imageUDim2Pos = UDim2Pos
        self.anchorType = anchorType

    def changeSize(self, UDim2Scale: UDim2.New):
        absoluteSize = absoluteUDim2(UDim2Scale)
        self.imageSurface = transform.scale(self.imageSurface,
                                            absoluteSize.tuple
                                            )

    def draw(self):
        newPosition = getTopLeft(self.imageSurface, self.anchorType, self.imageUDim2Pos, toPygame=True)
        self.windowScreen.blit(self.imageSurface, newPosition.tuple)
