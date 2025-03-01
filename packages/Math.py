from decimal import Decimal
from typing import Union
import math

def sqrt(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.sqrt(value))

def sin(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.sin(float(value)))

def cos(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.cos(float(value)))

def tan(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.tan(float(value)))

def log(value: Union[int, Decimal], base: Union[int, Decimal] = math.e) -> Decimal:
    return Decimal(math.log(float(value), float(base)))

def ln(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.log(float(value)))

def exp(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.exp(float(value)))

def ceil(value: Union[int, Decimal]) -> int:
    return math.ceil(float(value))

def rounded(value: Union[int, Decimal], ndigits: int = 0) -> Decimal:
    return Decimal(round(float(value), ndigits))

def asin(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.asin(float(value)))

def acos(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.acos(float(value)))

def atan(value: Union[int, Decimal]) -> Decimal:
    return Decimal(math.atan(float(value)))