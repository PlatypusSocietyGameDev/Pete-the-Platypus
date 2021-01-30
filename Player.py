import Image
import UDim2
import Vector2
import collide


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

    def refresh(self):
        self.Image.imageUDim2Pos = UDim2.New(0, self.Position.X, 0, self.Position.Y)

    def draw(self):
        self.Image.draw()

    def move(self, dt, moveDict: dict, imageList: list):
        newSpeed = self.pixelsPerSecond * dt / 1000

        movements = {
            "W": lambda position: Vector2.New(position.X, position.Y + newSpeed),
            "S": lambda position: Vector2.New(position.X, position.Y - newSpeed),
            "A": lambda position: Vector2.New(position.X - newSpeed, position.Y),
            "D": lambda position: Vector2.New(position.X + newSpeed, position.Y),
        }

        oldPos = self.Position

        offset = Vector2.New(0, 0)
        for key, isPressed in moveDict.items():
            if isPressed:
                offset = movements[key](offset)

        newPos = oldPos + offset
        newPosUDim2 = UDim2.New(0, newPos.X, 0, newPos.Y)
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
                newDirectionalPosUDim2 = UDim2.New(0, newDirectionalPos.X, 0, newDirectionalPos.Y)
                newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newDirectionalPosUDim2, toPygame=True)

                self.Image.imageRect.topleft = newTopLeft.tuple

                if collide.isTouching(self.Image, imageList):
                    offset = newVectorFunction[direction]()

            newPos = oldPos + offset
            newPosUDim2 = UDim2.New(0, newPos.X, 0, newPos.Y)
            newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newPosUDim2, toPygame=True)

            self.Image.imageRect.topleft = newTopLeft.tuple
            self.Position = newPos
        else:
            self.Position = newPos
