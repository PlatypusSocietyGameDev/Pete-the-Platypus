import Image
import UDim2
import Enums
import Vector2


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
            Enums.AnchorType.MiddleMiddle
        )

    def refresh(self):
        self.Image.imageUDim2Pos = UDim2.New(0, self.Position.X, 0, self.Position.Y)

    def draw(self):
        self.Image.draw()

    def move(self, dt, moveDict:dict):
        newSpeed = self.pixelsPerSecond * dt / 1000

        movements = {
            "W": lambda position: Vector2.New(position.X, position.Y + newSpeed),
            "S": lambda position: Vector2.New(position.X, position.Y - newSpeed),
            "A": lambda position: Vector2.New(position.X - newSpeed, position.Y),
            "D": lambda position: Vector2.New(position.X + newSpeed, position.Y),
        }

        for key, isPressed in moveDict.items():
            if isPressed:
                self.Position = movements[key](self.Position)
