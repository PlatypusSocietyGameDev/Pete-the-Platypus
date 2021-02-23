import Image
import Vector2
import UDim2
import ImageTessellate
import collide


class New:
    def __init__(self, windowScreen, yHeight: int, player):
        self.windowScreen = windowScreen
        self.pixelsPerSecond = 20
        self.yHeight = yHeight
        self.Player = player
        self.framePassed = 0

        self.LavaMain = ImageTessellate.New(
            windowScreen,
            r"assets/images/Lavabuildupbase.png",

            UDim2.New(0, 0, 0, self.yHeight),

            UDim2.New(1, 0, 1, 0),
            UDim2.New(0, 273.333, 0, 146.6666),

            Vector2.New(0, 1)
        )

        self.LavaTop = ImageTessellate.New(
            windowScreen,
            r"assets/images/Lavabuilduptop2.png",

            UDim2.New(0, 0, 0, self.yHeight),

            UDim2.New(1, 0, 0, 30),
            UDim2.New(0, 270, 0, 30),

            Vector2.New(0, 0)
        )

    def touchPlayer(self):
        self.Player.dead = True if collide.isTouching(self.Player.Image, [self.LavaTop, self.LavaMain])[0] else False

    def draw(self, dt):
        self.framePassed += 1

        if self.framePassed >= 60:
            newSpeed = self.pixelsPerSecond * dt / 1000
            self.yHeight += newSpeed

        newUDim2 = UDim2.New(0, 0, 0, self.yHeight)
        self.LavaMain.imageUDim2Pos = newUDim2
        self.LavaTop.imageUDim2Pos = newUDim2

        self.LavaMain.draw()
        self.LavaTop.draw()
    