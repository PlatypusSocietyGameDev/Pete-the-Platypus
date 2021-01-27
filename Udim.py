from errors import UDim2Error
from dataclasses import dataclass


@dataclass()
class New:
    def __init__(self, Scale, Offset):
        if not isinstance(Scale, (int, float)):
            raise UDim2Error("Scale Has To Be Of Class int/float")
        if not isinstance(Offset, (int, float)):
            raise UDim2Error("Offset Has To Be Of Class int/float")

        self._Scale = Scale
        self._Offset = Offset

    @property
    def Scale(self):
        return self._Scale

    @property
    def Offset(self):
        return self._Offset

    @Scale.setter
    def Scale(self, newVal):
        raise UDim2Error("ScaleX Cannot Be Reassigned")

    @Offset.setter
    def Offset(self, newVal):
        raise UDim2Error("OffsetX Cannot Be Reassigned")