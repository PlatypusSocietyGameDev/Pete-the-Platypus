import Image
import UDim2
import Vector2
import collide
from pygame import K_q, K_e
from pygame.draw import circle
from miscellaneous import drawtext, fillSurfaceTransparency
import alphadraw


class New:
    def __init__(self, windowScreen, origPos: Vector2.New):
        self.windowScreen = windowScreen
        self.Position = origPos
        self.pixelsPerSecond = 200

        self.Image = Image.New(
            windowScreen,
            r"assets/images/Petebetter1.png",
            UDim2.New(0, self.Position.X, 0, self.Position.Y),
            UDim2.New(0, 100, 0, 100),
            Vector2.New(0.5, 0.5)
        )

        self.gravitySpeed = 0
        self.gravityIncreasePF = .5
        self.movingRight = True

        self.jumping = True
        
        self.placingBlocks = False
        self.woodToggle = False
        self.brickToggle = False

        self.placeSize = UDim2.New(0, 200, 0, 40)
        self.placeRangeRadius = 300

        self.tempBrickImage = Image.New(
            self.windowScreen,
            r"assets/images/brickslab1.png",

            UDim2.New(0, 0, 0, 0),
            self.placeSize,
            Vector2.New(.5, .5)
        )

        self.tempWoodImage = Image.New(
            self.windowScreen,
            r"assets/images/Woodbar1.png",

            UDim2.New(0, 0, 0, 0),
            self.placeSize,
            Vector2.New(.5, .5)
        )

        self.badHighlight = fillSurfaceTransparency(self.tempWoodImage.getSurface(), (179, 58, 58, 200))

        self.obstacles = []
        self.walls = []
        self.lastMousePos = (0, 0)

    def drawRadius(self):
        if self.placingBlocks:
            circle(self.windowScreen, (100, 255, 100), Vector2.ToPygame(self.Position, isVector=True).tuple, self.placeRangeRadius, 5)

    def addObstacle(self, *obstacles):
        self.obstacles += obstacles

    def addWall(self, *walls):
        self.walls += walls

    def drawWalls(self):
        for wall in self.walls:
            wall.draw()

    def drawObstacles(self):
        for obstacle in self.obstacles:
            if obstacle not in self.walls:
                obstacle.draw()

    def drawValidWalls(self):
        # Directions are either left or right of a block
        if self.placingBlocks:
            for wall in self.walls:
                size = wall.getSurface().get_size()
                topLeft = wall.getTopLeft()
                topRight = topLeft + Vector2.New(size[0], 0)

                xLength = self.placeSize.X.Offset
                alphadraw.rect(self.windowScreen, (80, 220, 100, 200), (*topRight.tuple, xLength, size[1]))
                alphadraw.rect(self.windowScreen, (80, 220, 100, 200), (*(topLeft - Vector2.New(xLength, 0)).tuple, self.placeSize.X.Offset, size[1]))

    def refresh(self):
        self.Image.imageUDim2Pos = UDim2.fromVector2(self.Position)

    def draw(self):
        self.Image.draw()

    def placeBlock(self, eventKeys: list, mousePosition: tuple, mouseDown):
        if K_q in eventKeys:
            self.woodToggle = not self.woodToggle

            if self.woodToggle:
                self.brickToggle = False

        elif K_e in eventKeys:
            self.brickToggle = not self.brickToggle

            if self.brickToggle:
                self.woodToggle = False

        self.placingBlocks = self.woodToggle or self.brickToggle
        mouseVec = Vector2.New(*mousePosition)

        image = self.tempWoodImage if self.woodToggle else self.tempBrickImage
        size = image.getSurface().get_size()
        sizeVec = Vector2.New(*size)

        if self.placingBlocks:
            newPosition = Vector2.ToWorld(mousePosition)
            offset, hitImage = image.willCollide(newPosition, self.walls)

            image.imageUDim2Pos = UDim2.fromVector2(newPosition)

            if offset:
                origTopLeft = hitImage.getTopLeft()
                imageSize = hitImage.getSurface().get_size()

                topLeft = Vector2.ToWorld(origTopLeft, isVector=True)
                topRight = Vector2.ToWorld(origTopLeft + Vector2.New(imageSize[0], 0), isVector=True)

                leftDist = (topLeft - newPosition).magnitude
                rightDist = (topRight - newPosition).magnitude

                #print(leftDist, rightDist)
                #print(topLeft, topRight)

                leftFurther = leftDist > rightDist
                adjustedPosition = newPosition

                for _ in range(2):
                    if leftFurther:
                        adjustedPosition = Vector2.New(topRight.X, newPosition.Y + size[1]/2)
                    else:
                        adjustedPosition = Vector2.New(topLeft.X - size[0], newPosition.Y + size[1]/2)

                    image.setTopLeft(adjustedPosition)

                    if image.offScreen():
                        leftFurther = not leftFurther
                    else:
                        break

                if mouseDown:
                    newImage = Image.New(image.windowScreen,
                                         image.imagePath,
                                         UDim2.fromVector2(adjustedPosition),
                                         self.placeSize,
                                         Vector2.New(0, 1))

                    self.addWall(newImage)
                    self.addObstacle(newImage)

            image.draw()

            if not offset:
                self.windowScreen.blit(self.badHighlight, (mouseVec - sizeVec / 2).tuple)

    def gravity(self):
        self.gravitySpeed = min(self.gravitySpeed, 20)

        oldPos = self.Position

        newPos = oldPos + Vector2.New(0, -self.gravitySpeed)
        offsetPos, _ = self.Image.willCollide(newPos, self.obstacles)

        if offsetPos:
            self.jumping = False

            playerSize = self.Image.imageSurface.get_size()

            offsetPos = Vector2.New(*offsetPos)
            distToBottom = playerSize[1] - offsetPos.Y

            collidePos = self.Position + offsetPos

            newBottom = collidePos + Vector2.New(0, distToBottom)
            newPos = Vector2.New(oldPos.X, newBottom.Y - playerSize[1])

            self.Image.setPosition(newPos)

            self.Position = newPos
            self.gravitySpeed = 0
            self.gravityIncreasePF = 0.5
        else:
            self.Position = oldPos + Vector2.New(0, -self.gravitySpeed)
            self.gravitySpeed += self.gravityIncreasePF

    def move(self, dt, moveDict: dict):
        self.gravity()

        newSpeed = self.pixelsPerSecond * dt / 1000

        movements = {
            "S": lambda position: Vector2.New(position.X, position.Y - newSpeed),
            "A": lambda position: Vector2.New(position.X - newSpeed, position.Y),
            "D": lambda position: Vector2.New(position.X + newSpeed, position.Y),
        }

        oldPos = self.Position

        offset = Vector2.New(0, 0)
        for key, isPressed in moveDict.items():
            if key == "W" and isPressed and not self.jumping:
                self.jumping = True
                self.gravityIncreasePF = -2
                continue

            if isPressed and key in movements:
                if key == "A":
                    self.movingRight = False
                elif key == "D":
                    self.movingRight = True

                offset = movements[key](offset)

            if self.movingRight != self.Image.lookRight:
                self.Image.xFlip()

        if self.gravitySpeed < -15:
            self.gravityIncreasePF = 2

        newPos = oldPos + offset
        offsetPos, _ = self.Image.willCollide(newPos, self.obstacles)

        if offsetPos:
            xOffset = Vector2.New(offset.X, 0)
            yOffset = Vector2.New(0, offset.Y)

            movementDirs = {"X": xOffset, "Y": yOffset}
            newVectorFunction = {"X": lambda *a: Vector2.New(0, offset.Y),
                                 "Y": lambda *a: Vector2.New(offset.X, 0)
                                 }

            for direction, newOffset in movementDirs.items():
                newDirectionalPos = oldPos + newOffset

                offsetPos, _ = self.Image.willCollide(newDirectionalPos, self.obstacles)
                if offsetPos:
                    offset = newVectorFunction[direction]()

            newPos = oldPos + offset
            self.Image.setPosition(newPos)
            self.Position = newPos
        else:
            self.Position = newPos
