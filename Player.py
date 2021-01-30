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
        oldPosUDim2 = UDim2.New(0, oldPos.X, 0, oldPos.Y)
        oldTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, oldPosUDim2, toPygame=True)

        newPos = Vector2.New(oldPos.X, oldPos.Y)
        for key, isPressed in moveDict.items():
            if isPressed:
                newPos = movements[key](newPos)

        newPosUDim2 = UDim2.New(0, newPos.X, 0, newPos.Y)
        newTopLeft = UDim2.getTopLeft(self.Image.imageSurface, self.Image.anchorVector, newPosUDim2, toPygame=True)

        self.Image.imageRect.topleft = newTopLeft.tuple

        isTouching = collide.isTouching(self.Image, imageList)

        if isTouching:
            self.Image.imageRect.topleft = oldTopLeft.tuple
        else:
            self.Position = newPos
