import Vector2
from pygame import surface
import ctypes
import Enums
import UDim2


user32 = ctypes.windll.user32
screenWidth, screenHeight = (1920, 1020)

anchorOffsetFunctions = {
    Enums.AnchorType.BottomLeft: lambda height, width: (-height, 0),
    Enums.AnchorType.BottomMiddle: lambda height, width: (-height, -width/2),
    Enums.AnchorType.BottomRight: lambda height, width: (-height, -width),

    Enums.AnchorType.MiddleLeft: lambda height, width: (-height/2, 0),
    Enums.AnchorType.MiddleMiddle: lambda height, width: (-height/2, -width/2),
    Enums.AnchorType.MiddleRight: lambda height, width: (-height/2, -width),

    Enums.AnchorType.TopLeft: lambda height, width: (0, 0),
    Enums.AnchorType.TopMiddle: lambda height, width: (0, -width/2),
    Enums.AnchorType.TopRight: lambda height, width: (0, -width),
}


def absoluteUDim2(UDim2Pos: UDim2.New) -> Vector2.New:
    return Vector2.New(screenWidth*UDim2Pos.X.Scale + UDim2Pos.X.Offset,
                       screenHeight*UDim2Pos.Y.Scale + UDim2Pos.Y.Offset
                       )


def setScreenData(width, height):
    global screenWidth, screenHeight

    screenWidth, screenHeight = width, height


def getTopLeft(imageSurface: surface, anchorType: Enums.AnchorType, anchorUDim2Pos: UDim2.New) -> Vector2.New:
    height, width = imageSurface.get_size()
    anchorOffset = Vector2.New(*anchorOffsetFunctions[anchorType](height, width))
    absolutePosition = absoluteUDim2(anchorUDim2Pos)

    return absolutePosition + anchorOffset
