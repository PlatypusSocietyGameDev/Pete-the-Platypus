import pygame.image as image
import pygame.transform as transform
import pygame.mask as mask
from pygame import Surface
import UDim2
import Vector2
import collide


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
        self.lookRight = True

        topLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.imageRect = self.imageSurface.get_rect(topleft=topLeft.tuple)
        self.imageMask = mask.from_surface(self.imageSurface)

    def xFlip(self):
        self.imageSurface = transform.flip(self.imageSurface, True, False)
        self.imageMask = mask.from_surface(self.imageSurface)
        self.lookRight = not self.lookRight

        topLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.imageRect = self.imageSurface.get_rect(topleft=topLeft.tuple)

    def getSurface(self):
        return self.imageSurface

    def getMask(self):
        return self.imageMask

    def getRect(self):
        return self.imageRect

    def getTopLeft(self) -> Vector2.New:
        return UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)

    def setTopLeft(self, newPosition: Vector2.New):
        size = Vector2.New(*self.imageSurface.get_size())
        offset = self.anchorVector * size * Vector2.New(1, -1)

        self.imageRect.topleft = newPosition.tuple
        self.imageUDim2Pos = UDim2.fromVector2(newPosition + offset)

    def offScreen(self, threshold: int = 4):
        size = self.getSurface().get_size()

        # Pygame World
        topLeft = self.getTopLeft()
        topRight = topLeft + Vector2.New(size[0], 0)
        bottomRight = topRight + Vector2.New(0, size[1])
        bottomLeft = topLeft + Vector2.New(0, size[1])

        corners = [topLeft, topRight, bottomLeft, bottomRight]
        cornerIn = [Vector2.inScreen(coord) for coord in corners]

        return cornerIn.count(False) >= threshold

    def changeSize(self, UDim2Scale: UDim2.New):
        absoluteSize = UDim2.absoluteUDim2(UDim2Scale)
        self.imageSurface = transform.scale(self.imageSurface,
                                            absoluteSize.tuple
                                            )

        topLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.imageRect = self.imageSurface.get_rect(topleft=topLeft.tuple)
        self.imageMask = mask.from_surface(self.imageSurface)

    def draw(self):
        newPosition = UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.imageRect.topleft = newPosition.tuple

        self.windowScreen.blit(self.imageSurface, newPosition.tuple)

    def setPosition(self, newPos: Vector2.New):
        newPosUDim2 = UDim2.fromVector2(newPos)
        newTopLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, newPosUDim2, toPygame=True)

        self.imageRect.topleft = newTopLeft.tuple

    def willCollide(self, newPos: Vector2.New, colliders: list) -> tuple:
        oldTopLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)

        newPosUDim2 = UDim2.fromVector2(newPos)
        newTopLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, newPosUDim2, toPygame=True)

        self.imageRect.topleft = newTopLeft.tuple

        offset, image = collide.isTouching(self, colliders)

        self.imageRect.topleft = oldTopLeft.tuple

        return offset, image



