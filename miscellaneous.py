import Vector2
from pygame import surface
import Enums
import UDim2
import constants

screenWidth, screenHeight = constants.SCREENWIDTH, constants.SCREENHEIGHT
flipVector = Vector2.New(0, screenHeight)

anchorOffsetFunctions = {
    Enums.AnchorType.BottomLeft: lambda width, height: (0, height),
    Enums.AnchorType.BottomMiddle: lambda width, height: (-width/2, height),
    Enums.AnchorType.BottomRight: lambda width, height: (-width, height),

    Enums.AnchorType.MiddleLeft: lambda width, height: (0, height/2),
    Enums.AnchorType.MiddleMiddle: lambda width, height: (-width/2, height/2),
    Enums.AnchorType.MiddleRight: lambda width, height: (-width, height/2),

    Enums.AnchorType.TopLeft: lambda width, height: (0, 0),
    Enums.AnchorType.TopMiddle: lambda width, height: (-width/2, 0),
    Enums.AnchorType.TopRight: lambda width, height: (-width, 0),
}


def absoluteUDim2(UDim2Pos: UDim2.New) -> Vector2.New:
    return Vector2.New(screenWidth * UDim2Pos.X.Scale + UDim2Pos.X.Offset,
                       screenHeight * UDim2Pos.Y.Scale + UDim2Pos.Y.Offset
                       )


def getTopLeft(imageSurface: surface, anchorType: Enums.AnchorType, anchorUDim2Pos: UDim2.New, toPygame: bool = False) -> Vector2.New:
    width, height = imageSurface.get_size()

    anchorOffset = Vector2.New(*anchorOffsetFunctions[anchorType](width, height))
    absolutePosition = absoluteUDim2(anchorUDim2Pos)
    newPosition = absolutePosition + anchorOffset

    if toPygame:
        newPosition = flipVector - newPosition

    return newPosition
