from errors import UDimError
from dataclasses import dataclass


@dataclass()
class New:
    def __init__(self, Scale, Offset):
        if not isinstance(Scale, (int, float)):
            raise UDimError("Scale Has To Be Of Class int/float")
        if not isinstance(Offset, (int, float)):
            raise UDimError("Offset Has To Be Of Class int/float")

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
        raise UDimError("Scale Cannot Be Reassigned")

    @Offset.setter
    def Offset(self, newVal):
        raise UDimError("Offset Cannot Be Reassigned")

    def __add__(self, other):
        if isinstance(other, New):
            return New(self._Scale + other._Scale, self._Offset + other._Offset)
        else:
            raise UDimError(f"{type(other)} Not Supported For Addition")

    def __sub__(self, other):
        if isinstance(other, New):
            return New(self._Scale - other._Scale, self._Offset - other._Offset)
        else:
            raise UDimError(f"{type(other)} Not Supported For Subtraction")