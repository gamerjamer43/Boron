from decimal import Decimal
from typing import Union
import math

@staticmethod
def sqrt(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.sqrt(value))

@staticmethod
def sin(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.sin(float(value)))

@staticmethod
def cos(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.cos(float(value)))

@staticmethod
def tan(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.tan(float(value)))

@staticmethod
def log(value: Union[int, Decimal], base: Union[int, Decimal] = math.e) -> Decimal:
    return Decimal(math.log(float(value), float(base)))

@staticmethod
def ln(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.log(float(value)))

@staticmethod
def exp(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.exp(float(value)))

@staticmethod
def ceil(value: Union[int, Decimal]) -> int:
    return math.ceil(float(value))

@staticmethod
def rounded(value: Union[int, Decimal], ndigits: int = 0) -> Decimal:
    return Decimal(round(float(value), ndigits))

@staticmethod
def asin(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.asin(float(value)))

@staticmethod
def acos(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.acos(float(value)))

@staticmethod
def atan(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.atan(float(value)))