import Image
import UDim2
import Vector2
import collide
from pygame import K_q, K_e
from pygame.draw import circle, lines
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

        self.dead = False

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
                closeEnough = wall.closeEnough(self.Position,
                                               self.placeRangeRadius + UDim2.absoluteUDim2(self.placeSize).X/2,
                                               1)

                if not closeEnough:
                    continue

                wall.drawWall()

                #alphadraw.rect(self.windowScreen, (80, 220, 100, 100), (*topLeft.tuple, *size))

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
        mouseWorld = Vector2.ToWorld(mouseVec, isVector=True)

        image = self.tempWoodImage if self.woodToggle else self.tempBrickImage
        image.imageUDim2Pos = UDim2.fromVector2(mouseWorld)

        if self.placingBlocks:
            offset, hitImage = image.willCollide(mouseWorld, self.walls)
            hits = 0
            if hitImage:
                hits = collide.countTouchers(image, self.walls)
                if False:
                    topLeft = image.getTopLeft()
                    hitPos = topLeft + Vector2.New(*offset)
                    circle(self.windowScreen, (0, 0, 0), hitPos.tuple, 10)

                collide.repositionAfterCollision(mouseWorld, hitImage, image)

            image.draw()

            dist = (UDim2.absoluteUDim2(image.imageUDim2Pos) - self.Position).magnitude
            hitPlayerOffset, _ = collide.isTouching(self.Image, [image], self.placeRangeRadius)

            if dist > self.placeRangeRadius or not hitImage or hitPlayerOffset or hits > 1 or hits == 0:
                self.windowScreen.blit(self.badHighlight, image.getTopLeft().tuple)

            elif mouseDown and hitImage and not hitPlayerOffset and hits == 1:
                newImage = Image.New(
                    self.windowScreen,
                    image.imagePath,

                    image.imageUDim2Pos,
                    self.placeSize,
                    image.anchorVector
                )

                self.addObstacle(newImage)
                self.addWall(newImage)

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
        repositionFlip = False
        repositionHitImage = None

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

                tempObstacles = self.walls.copy()
                del tempObstacles[0]  # Ground

                hitPlayerOffset, hitImage = collide.isTouching(self.Image, tempObstacles, self.Image.bestTouch)

                if hitPlayerOffset:
                    repositionFlip = True
                    repositionHitImage = hitImage

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

        if repositionFlip:
            origTopLeft = Vector2.ToWorld(self.Image.getTopLeft(), isVector=True)
            if not self.movingRight:
                hitImageTopLeft = Vector2.ToWorld(repositionHitImage.getTopLeft(), isVector=True)
                imageSize = self.Image.getSize()
                self.Image.setTopLeft(Vector2.New(hitImageTopLeft.X-imageSize.X, origTopLeft.Y))
            else:
                imageSize = repositionHitImage.getSize()
                hitImageTopRight = Vector2.ToWorld(repositionHitImage.getTopLeft(), isVector=True) + Vector2.New(imageSize.X, 0)
                self.Image.setTopLeft(Vector2.New(hitImageTopRight.X, origTopLeft.Y))

            self.Position = UDim2.absoluteUDim2(self.Image.imageUDim2Pos)
