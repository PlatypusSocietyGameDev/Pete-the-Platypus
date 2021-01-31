import Image
import ImageTessellate
from typing import Union, List, TypeVar

ImageType = TypeVar('ImageType', ImageTessellate.New, Image.New)


def isTouching(mainSurface: Union[ImageType], obstacleImages: List[ImageType]) -> tuple:
    isMainImage = isinstance(mainSurface, Image.New)
    mainMask = mainSurface.imageMask if isMainImage else mainSurface.tessellatedImageMask
    mainRect = mainSurface.imageRect if isMainImage else mainSurface.tessellatedImageRect

    for image in obstacleImages:
        isImage = isinstance(image, Image.New)
        obstacleRect = image.imageRect if isImage else image.tessellatedImageRect

        if mainRect.colliderect(obstacleRect):
            obstacleMask = image.imageMask if isImage else image.tessellatedImageMask

            offset = obstacleRect[0] - mainRect[0], obstacleRect[1] - mainRect[1]
            collideOffset = mainMask.overlap(obstacleMask, offset)

            if collideOffset:
                return collideOffset
