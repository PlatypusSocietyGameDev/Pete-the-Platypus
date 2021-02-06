import Vector2


def isTouching(mainSurface, obstacleImages) -> tuple:
    mainMask = mainSurface.getMask()
    mainRect = mainSurface.getRect()

    for image in obstacleImages:
        obstacleRect = image.getRect()

        if mainRect.colliderect(obstacleRect):
            obstacleMask = image.getMask()

            offset = obstacleRect[0] - mainRect[0], obstacleRect[1] - mainRect[1]
            collideOffset = mainMask.overlap(obstacleMask, offset)

            if collideOffset:
                return collideOffset, image

    return None, None


def getClosestIndex(image, pos: Vector2.New) -> int:
    corners = image.getWorldCorners()
    # topLeft, topRight, bottomRight, bottomLeft

    cornerDist = [(corner - pos).magnitude for corner in corners]

    cornerClosestDist = min(cornerDist)
    cornerClosestI = cornerDist.index(cornerClosestDist)
    cornerClosest = corners[cornerClosestI]

    # 0 Top
    # 1 Right
    # 2 Bottom
    # 3 Left

    cornerData = []

    if cornerClosestI == 0:  # Top Left
        cornerData.append([cornerClosest + Vector2.New(5, 0), 0])
        cornerData.append([cornerClosest + Vector2.New(0, -5), 3])

    elif cornerClosestI == 1:  # Top Right
        cornerData.append([cornerClosest + Vector2.New(-5, 0), 0])
        cornerData.append([cornerClosest + Vector2.New(0, -5), 1])

    elif cornerClosestI == 2:  # Bottom Right
        cornerData.append([cornerClosest + Vector2.New(-5, 0), 2])
        cornerData.append([cornerClosest + Vector2.New(0, 5), 1])

    elif cornerClosestI == 3:  # Bottom Left
        cornerData.append([cornerClosest + Vector2.New(5, 0), 2])
        cornerData.append([cornerClosest + Vector2.New(0, 5), 3])

    newCornerSideDistances = [(cornerInfo[0] - pos).magnitude for cornerInfo in cornerData]
    closestCornerDist = min(newCornerSideDistances)
    closestCornerSideIndex = newCornerSideDistances.index(closestCornerDist)
    closestI = cornerData[closestCornerSideIndex][1]

    return closestI


def repositionAfterCollision(newCentrePosition: Vector2.New, hitImage, targetImage, forceSideIndex: int = None):
    targetImageSize = Vector2.New(*targetImage.getSurface().get_size())
    hitImageSize = Vector2.New(*hitImage.getSurface().get_size())

    hitTopLeft = hitImage.getTopLeft()
    hitTopLeftWorld = Vector2.ToWorld(hitTopLeft, isVector=True)

    closestI = getClosestIndex(hitImage, newCentrePosition)

    if forceSideIndex is not None:
        closestI = forceSideIndex

    if closestI == 1 or closestI == 3:  # Left/Right
        for _ in range(2):
            multiplier = 1 if closestI == 1 else -1
            topRightImage = hitTopLeftWorld + Vector2.New(hitImageSize.X, 0) * multiplier
            newPos = Vector2.New(topRightImage.X, newCentrePosition.Y + targetImageSize.Y/2)
            targetImage.setTopLeft(newPos)
            if targetImage.offScreen():
                closestI = 1 if closestI == 3 else 3
            else:
                break

    if closestI == 2 or closestI == 0:  # Left/Right
        for _ in range(2):
            multiplier = 1 if closestI == 0 else -1

            topRightImage = hitTopLeftWorld + Vector2.New(0, hitImageSize.Y) * multiplier
            newPos = Vector2.New(newCentrePosition.X - targetImageSize.X/2, topRightImage.Y)
            targetImage.setTopLeft(newPos)

            if targetImage.offScreen():
                closestI = 2 if closestI == 0 else 0
            else:
                break
