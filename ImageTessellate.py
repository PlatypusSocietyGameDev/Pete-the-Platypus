import pygame.image as image
import pygame.transform as transform
import pygame.mask as mask
from pygame import Surface
import UDim2
import Vector2
import collide


class New:
    def __init__(self, windowScreen: Surface, imagePath: str, UDim2Pos: UDim2.New, TotalUDim2Scale: UDim2.New, BaseImageUDim2Scale: UDim2.New, anchorVector: Vector2.New):
        self.windowScreen = windowScreen

        self.imagePath = imagePath
        self.imageSurface = image.load(self.imagePath)

        self.totalAbsoluteSize = UDim2.absoluteUDim2(TotalUDim2Scale)
        self.baseAbsoluteSize = UDim2.absoluteUDim2(BaseImageUDim2Scale)

        self.imageSurface = transform.scale(self.imageSurface,
                                            self.baseAbsoluteSize.tuple
                                            )

        self.tessellatedImageSurface = Surface(self.totalAbsoluteSize.tuple)
        self.setImageSurfaceData()

        self.imageUDim2Pos = UDim2Pos
        self.anchorVector = anchorVector

        topLeft = UDim2.getTopLeft(self.tessellatedImageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.tessellatedImageRect = self.tessellatedImageSurface.get_rect(topleft=topLeft.tuple)
        self.tessellatedImageMask = mask.from_surface(self.tessellatedImageSurface)

    def getSurface(self):
        return self.tessellatedImageSurface

    def getMask(self):
        return self.tessellatedImageMask

    def getRect(self):
        return self.tessellatedImageRect

    def getTopLeft(self) -> Vector2.New:
        return UDim2.getTopLeft(self.tessellatedImageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)

    def cropImage(self, image: Surface, areaSize: tuple) -> Surface:
        croppedImage = Surface(areaSize)
        croppedImage.blit(image, (0, 0), (0, 0, *areaSize))

        return croppedImage

    def setImageSurfaceData(self):
        xBigger = self.baseAbsoluteSize.X > self.totalAbsoluteSize.X
        yBigger = self.baseAbsoluteSize.Y > self.totalAbsoluteSize.Y
        if xBigger or yBigger:
            self.baseAbsoluteSize = Vector2.New(self.totalAbsoluteSize.X if xBigger else self.baseAbsoluteSize.X,
                                                self.totalAbsoluteSize.Y if yBigger else self.baseAbsoluteSize.Y
                                                )

            croppedImage = self.cropImage(self.baseAbsoluteSize.tuple)

            self.tessellatedImageSurface = croppedImage
            return

        xMaxFit = self.totalAbsoluteSize.X // self.baseAbsoluteSize.X + 2
        yMaxFit = self.totalAbsoluteSize.Y // self.baseAbsoluteSize.Y + 2

        newScreen = Surface(self.totalAbsoluteSize.tuple)

        for xTimes in range(xMaxFit):
            for yTimes in range(yMaxFit):
                offset = self.baseAbsoluteSize * Vector2.New(xTimes, yTimes)
                newScreen.blit(self.imageSurface, offset.tuple)

        self.tessellatedImageSurface = self.cropImage(newScreen, self.totalAbsoluteSize.tuple)

    def changeTotalSize(self, UDim2Scale: UDim2.New):
        self.totalAbsoluteSize = UDim2.absoluteUDim2(UDim2Scale)

        self.tessellatedImageSurface = Surface(self.totalAbsoluteSize.tuple)
        self.setImageSurfaceData()

        topLeft = UDim2.getTopLeft(self.tessellatedImageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.tessellatedImageRect = self.tessellatedImageSurface.get_rect(topleft=topLeft.tuple)
        self.tessellatedImageMask = mask.from_surface(self.tessellatedImageSurface)

    def changeBaseSize(self, UDim2Scale: UDim2.New):
        self.baseAbsoluteSize = UDim2.absoluteUDim2(UDim2Scale)

        self.tessellatedImageSurface = Surface(self.totalAbsoluteSize.tuple)
        self.imageSurface = transform.scale(self.imageSurface,
                                            self.baseAbsoluteSize.tuple
                                            )
        self.setImageSurfaceData()

        topLeft = UDim2.getTopLeft(self.tessellatedImageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.tessellatedImageRect = self.tessellatedImageSurface.get_rect(topleft=topLeft.tuple)
        self.tessellatedImageMask = mask.from_surface(self.tessellatedImageSurface)

    def draw(self):
        newPosition = UDim2.getTopLeft(self.tessellatedImageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.tessellatedImageRect.topleft = newPosition.tuple
        self.windowScreen.blit(self.tessellatedImageSurface, newPosition.tuple)

    def willCollide(self, newPos: Vector2.New, colliders: list) -> tuple:
        oldTopLeft = UDim2.getTopLeft(self.tessellatedImageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)

        newPosUDim2 = UDim2.fromVector2(newPos)
        newTopLeft = UDim2.getTopLeft(self.imageSurface, self.anchorVector, newPosUDim2, toPygame=True)

        self.tessellatedImageRect.topleft = newTopLeft.tuple
        offset, hitImage = collide.isTouching(self, colliders)
        self.tessellatedImageRect.topleft = oldTopLeft.tuple

        return offset, image