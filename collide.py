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