import Image
import UDim2
import Vector2
import collide
from pygame.draw import circle


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
        self.jumping = False

    def refresh(self):
        self.Image.imageUDim2Pos = UDim2.Vector2ToUDim2(self.Position)

    def draw(self):
        self.Image.draw()

    def gravity(self, imageList: list):
        self.gravitySpeed = min(self.gravitySpeed, 20)

        oldPos = self.Position

        newPos = oldPos + Vector2.New(0, -self.gravitySpeed)
        newPosUDim2 = UDim2.Vector2ToUDim2(newPos)
        newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newPosUDim2, toPygame=True)

        self.Image.imageRect.topleft = newTopLeft.tuple
        offsetPos = collide.isTouching(self.Image, imageList)

        if offsetPos:
            self.jumping = False

            offsetPos = Vector2.New(*offsetPos)
            playerSize = self.Image.imageSurface.get_size()
            distToBottom = playerSize[1] - offsetPos.Y
            collidePos = self.Position + offsetPos
            newBottom = collidePos + Vector2.New(0, distToBottom)
            newPos = Vector2.New(oldPos.X, newBottom.Y - playerSize[1])

            newPosUDim2 = UDim2.Vector2ToUDim2(newPos)
            newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newPosUDim2, toPygame=True)

            self.Position = newPos

            #circle(self.windowScreen, (0, 0, 0), newTopLeft.tuple, 10)
            self.Image.imageRect.topleft = newTopLeft.tuple
            self.gravitySpeed = 0
            self.gravityIncreasePF = 0.5
        else:
            self.Position = oldPos + Vector2.New(0, -self.gravitySpeed)
            self.gravitySpeed += self.gravityIncreasePF

    def move(self, dt, moveDict: dict, *imageList: list):
        self.gravity(imageList)

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
                self.gravityIncreasePF = -1.5
                continue

            if isPressed and key in movements:
                offset = movements[key](offset)

        if self.gravitySpeed < -20:
            self.gravityIncreasePF = 1.5

        newPos = oldPos + offset
        newPosUDim2 = UDim2.Vector2ToUDim2(newPos)
        newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newPosUDim2, toPygame=True)

        self.Image.imageRect.topleft = newTopLeft.tuple

        isTouching = collide.isTouching(self.Image, imageList)

        if isTouching:
            xOffset = Vector2.New(offset.X, 0)
            yOffset = Vector2.New(0, offset.Y)

            movementDirs = {"X": xOffset, "Y": yOffset}
            newVectorFunction = {"X": lambda *a: Vector2.New(0, offset.Y),
                                 "Y": lambda *a: Vector2.New(offset.X, 0)
                                 }

            for direction, newOffset in movementDirs.items():
                newDirectionalPos = oldPos + newOffset
                newDirectionalPosUDim2 = UDim2.Vector2ToUDim2(newDirectionalPos)
                newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newDirectionalPosUDim2, toPygame=True)

                self.Image.imageRect.topleft = newTopLeft.tuple

                if collide.isTouching(self.Image, imageList):
                    offset = newVectorFunction[direction]()

            newPos = oldPos + offset
            newPosUDim2 = UDim2.Vector2ToUDim2(newPos)
            newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newPosUDim2, toPygame=True)

            self.Image.imageRect.topleft = newTopLeft.tuple
            self.Position = newPos
        else:
            self.Position = newPos
