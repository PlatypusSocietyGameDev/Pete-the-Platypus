import pygame.image as image
import pygame.transform as transform
import pygame.mask as mask
from pygame import Surface, SRCALPHA
import UDim2
import Vector2
import collide
from pygame.draw import lines


class New:
    def __init__(self, windowScreen: Surface, imagePath: str, UDim2Pos: UDim2.New, UDim2Scale: UDim2.New, anchorVector: Vector2.New):
        self.windowScreen = windowScreen

        self.imagePath = imagePath
        self.imageSurface = image.load(self.imagePath).convert_alpha()

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

        self.wall = Surface(absoluteSize.tuple, SRCALPHA)
        lines(self.wall, (80, 220, 100), True, (
            (0, 0), (absoluteSize.X, 0), absoluteSize.tuple, (0, absoluteSize.Y)
        ), 3)

        self.bestTouch = absoluteSize.magnitude / 2

    def getSize(self):
        return Vector2.New(*self.imageSurface.get_size())

    def drawWall(self):
        topLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.windowScreen.blit(self.wall, topLeft.tuple)

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

        self.imageRect.topleft = Vector2.ToPygame(newPosition, isVector=True).tuple
        self.imageUDim2Pos = UDim2.fromVector2(newPosition + offset)

    def closeEnough(self, newPoint: Vector2.New, distRange: int, threshold: int = 4):
        distances = [(point - newPoint).magnitude for point in self.getWorldCorners()]
        inRange = [dist < distRange for dist in distances]

        return inRange.count(True) >= threshold

    def getWorldCorners(self):
        size = self.getSurface().get_size()

        topLeft = self.getTopLeft()
        topLeft = Vector2.ToWorld(topLeft, isVector=True)
        topRight = topLeft + Vector2.New(size[0], 0)

        bottomLeft = topLeft + Vector2.New(0, -size[1])
        bottomRight = topRight + Vector2.New(0, -size[1])

        return topLeft, topRight, bottomRight, bottomLeft

    def getPygameCorners(self):
        corners = self.getWorldCorners()
        newCorners = [Vector2.ToPygame(cornerPos, isVector=True) for cornerPos in corners]

        return newCorners

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
        
        self.wall = Surface(absoluteSize.tuple, SRCALPHA)
        lines(self.wall, (80, 220, 100), True, (
            (0, 0), (absoluteSize.X, 0), absoluteSize.tuple, (0, absoluteSize.Y)
        ), 3)

        self.bestTouch = absoluteSize.magnitude / 2

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
        oldPosUDim2 = self.imageUDim2Pos

        newPosUDim2 = UDim2.fromVector2(newPos)
        newTopLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, newPosUDim2, toPygame=True)

        self.imageRect.topleft = newTopLeft.tuple
        self.imageUDim2Pos = newPosUDim2

        offset, image = collide.isTouching(self, colliders, self.bestTouch)

        self.imageRect.topleft = oldTopLeft.tuple
        self.imageUDim2Pos = oldPosUDim2

        return offset, image



