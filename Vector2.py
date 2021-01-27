from errors import VectorError
from math import sqrt
from dataclasses import dataclass


@dataclass()
class New:
    def __init__(self, X, Y):
        if not isinstance(X, (int, float)):
            raise VectorError("X Has To Be Of Class int/float")
        if not isinstance(Y, (int, float)):
            raise VectorError("Y Has To Be Of Class int/float")

        self._X = X
        self._Y = Y

        self.list = [self.X, self.Y]
        self.tuple = tuple(self.list)

        self.magnitude = sqrt(sum(map(lambda num: num ** 2, self.list)))

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @X.setter
    def X(self, newVal):
        raise VectorError("X Cannot Be Reassigned")

    @Y.setter
    def Y(self, newVal):
        raise VectorError("X Cannot Be Reassigned")

    def operationHandler(self, other, operation):
        """
        Returns a New Vector Which is Adjusted

        Parameters
        ----------
        other : any
            The new type that is adjusted to the Vector2

        operation : str
            The str that is used for the function adjustment

        Returns
        -------
        Vector2
        """

        functionDict = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

        operationText = {
            "+": ["Added", "Addition"],
            "-": ["Subtracted", "Subtraction"],
            "*": ["Multiplied", "Multiplication"],
            "/": ["Divided", "Division"],
        }

        if type(other) == int or type(other) == float:
            return New(functionDict[operation](self.X, other), functionDict[operation](self.Y, other))

        elif type(other) == New:
            return New(functionDict[operation](self.X, other.X), functionDict[operation](self.Y, other.Y))

        else:
            raise VectorError(f"{type(other)} Is Not Supported For Vector {operationText[operation][1]}")

    def __add__(self, other):
        return self.operationHandler(other, "+")

    def __sub__(self, other):
        return self.operationHandler(other, "-")

    def __mul__(self, other):
        return self.operationHandler(other, "*")

    def __truediv__(self, other):
        return self.operationHandler(other, "/")

    def __repr__(self):
        return f"Vector2 X:{self.X} Y:{self.Y}"
