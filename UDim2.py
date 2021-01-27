from errors import UDim2Error
from dataclasses import dataclass
import Udim


@dataclass()
class New:
    def __init__(self, scaleX, offsetX, scaleY, offsetY):
        if not isinstance(scaleX, (int, float)):
            raise UDim2Error("scaleX Has To Be Of Class int/float")
        if not isinstance(offsetX, (int, float)):
            raise UDim2Error("offsetX Has To Be Of Class int/float")
        if not isinstance(scaleY, (int, float)):
            raise UDim2Error("scaleY Has To Be Of Class int/float")
        if not isinstance(offsetY, (int, float)):
            raise UDim2Error("offsetY Has To Be Of Class int/float")

        self._X = Udim.New(scaleX, offsetX)
        self._Y = Udim.New(scaleY, offsetY)

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