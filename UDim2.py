from errors import UDim2Error
from dataclasses import dataclass
import UDim
from miscellaneous import absoluteUDim2


@dataclass()
class New:
    def __init__(self, scaleX, offsetX, scaleY=None, offsetY=None):
        if not isinstance(scaleX, (int, float, UDim.New)):
            raise UDim2Error("scaleX Has To Be Of Class int/float/UDim.New")
        if not isinstance(offsetX, (int, float, UDim.New)):
            raise UDim2Error("offsetX Has To Be Of Class int/float/UDim.New")
        if scaleY and not isinstance(scaleY, (int, float)):
            raise UDim2Error("scaleY Has To Be Of Class int/float")
        if offsetY and not isinstance(offsetY, (int, float)):
            raise UDim2Error("offsetY Has To Be Of Class int/float")

        if scaleY is not None and offsetY is not None:
            self._X = UDim.New(scaleX, offsetX)
            self._Y = UDim.New(scaleY, offsetY)
        else:
            self._X = scaleX
            self._Y = offsetX

    def __repr__(self):
        return f"UDim2 XScale: {self._X._Scale}, XOffset: {self._X._Offset}, YScale: {self._Y._Scale}, YOffset: {self._Y._Offset}"

    @property
    def AbsoluteSize(self):
        return absoluteUDim2(self)

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @X.setter
    def X(self, newVal):
        raise UDim2Error("X Cannot Be Reassigned")

    @Y.setter
    def Y(self, newVal):
        raise UDim2Error("Y Cannot Be Reassigned")

    def __add__(self, other):
        if isinstance(other, New):
            return New(self._X + other._X, self._Y + other._Y)
        else:
            raise UDim2Error(f"{type(other)} Not Supported For Addition")

    def __sub__(self, other):
        if isinstance(other, New):
            return New(self._X - other._X, self._Y - other._Y)
        else:
            raise UDim2Error(f"{type(other)} Not Supported For Subtraction")
