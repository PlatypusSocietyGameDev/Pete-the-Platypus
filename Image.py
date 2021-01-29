import pygame.image as image
import pygame.transform as transform
from pygame import Surface
import UDim2
import Vector2


class New:
    def __init__(self, windowScreen: Surface, imagePath: str, UDim2Pos: UDim2.New, UDim2Scale: UDim2.New, anchorVector: Vector2.New):
        self.windowScreen = windowScreen

        self.imagePath = imagePath
        self.imageSurface = image.load(self.imagePath)

        absoluteSize = UDim2.absoluteUDim2(UDim2Scale)
        self.imageSurface = transform.scale(self.imageSurface,
                                            absoluteSize.tuple
                                            )

        self.imageUDim2Pos = UDim2Pos
        self.anchorVector = anchorVector

    def changeSize(self, UDim2Scale: UDim2.New):
        absoluteSize = UDim2.absoluteUDim2(UDim2Scale)
        self.imageSurface = transform.scale(self.imageSurface,
                                            absoluteSize.tuple
                                            )

    def draw(self):
        newPosition = UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.windowScreen.blit(self.imageSurface, newPosition.tuple)
