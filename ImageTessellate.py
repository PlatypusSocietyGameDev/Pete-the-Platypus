import pygame.image as image
import pygame.transform as transform
from pygame import Surface
import UDim2
import Vector2


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

        self.imageUDim2Pos = UDim2Pos
        self.anchorVector = anchorVector

        self.setImageSurfaceData()

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

    def changeBaseSize(self, UDim2Scale: UDim2.New):
        self.baseAbsoluteSize = UDim2.absoluteUDim2(UDim2Scale)

        self.tessellatedImageSurface = Surface(self.totalAbsoluteSize.tuple)
        self.imageSurface = transform.scale(self.imageSurface,
                                            self.baseAbsoluteSize.tuple
                                            )
        self.setImageSurfaceData()

    def draw(self):
        newPosition = UDim2.getTopLeft(self.tessellatedImageSurface, self.anchorVector, self.imageUDim2Pos, toPygame=True)
        self.windowScreen.blit(self.tessellatedImageSurface, newPosition.tuple)
