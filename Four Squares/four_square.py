from typing import Tuple, Self

class GaussianInt:
    def __init__(self, real: int, imag: int) -> None:
        self.real = real
        self.imag = imag
    
    def __add__(self, other: Self) -> "GaussianInt": return GaussianInt(self.real + other.real, self.imag + self.real)
    def __iadd__(self, other: Self) -> Self:
        self.real += other.real
        self.imag += other.imag
        return self
    
    def __sub__(self, other: Self) -> "GaussianInt": return GaussianInt(self.real - other.real, self.imag - other.imag)
    def __isub__(self, other: Self) -> Self:    
        self.real -= other.real
        self.imag -= other.imag
        return self
    
    def __mul__(self, other: Self) -> "GaussianInt":
        real = self.real*other.real - self.imag*other.imag
        imag = self.real*other.imag + self.imag*other.real
        return GaussianInt(real, imag)

    def __divmod__(self, divisor: Self) -> Tuple["GaussianInt", "GaussianInt"]:
        # divides by divisor using normal complex division then floors the real and imaginary parts
        conjugate = divisor.conj()
        numerator = self*conjugate
        norm = abs(divisor)
        # print(numerator, norm)
        quotient = GaussianInt(int(round(numerator.real/norm)), int(round(numerator.imag/norm)))
        remainder = self - (quotient*divisor)
        return (quotient, remainder)

    def __abs__(self) -> int:
        return self.real*self.real + self.imag*self.imag

    def __repr__(self):
        return f"{self.real} + {self.imag}j" if self.imag >= 0 else f"{self.real} - {-self.imag}j"

    def conj(self): return GaussianInt(self.real, -self.imag)

def gaussian_gcd(a: GaussianInt, b: GaussianInt) -> GaussianInt:
    if (a.real == 0 and a.imag==0): return b
    if (b.real == 0 and b.imag==0): return a
    if abs(a) >= abs(b):
        _, r = divmod(a, b) # we must calculate the quotient anyway when computing the remainder
        # print(a, "//", b, r)
        return gaussian_gcd(b, r)
    else:
        _, r = divmod(b, a) # we must calculate the quotient anyway when computing the remainder
        # print(b, "//", a , r)
        return gaussian_gcd(a, r)

print(gaussian_gcd(GaussianInt(30, 54), GaussianInt(2, 64)))
# print(divmod(GaussianInt(1, 45), GaussianInt(-4, 24)))
# def four_squares(n: int) -> Tuple[int, int, int, int]:
#     pass