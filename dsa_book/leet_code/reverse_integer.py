"""Leet code 7 Reverse Integer"""


class Solution:
    def reverse(self, x: int) -> int:

        is_negative = x < 0

        s = str(abs(x))[::-1]
        result = int(s) * (-1 if is_negative else 1)

        # Check if the result is within the 32-bit signed integer range
        return result if -(2**31) <= result <= (2**31) - 1 else 0

    # def reverse(self, x: int) -> int:
    #     is_negative  = x < 0

    #     s = str(abs(x))[::-1]

    #     if is_negative:
    #         s = int("-" + s)
    #     else:
    #         s= int(s)

    #     if (s <= -2 ** 31) or (s >= (2 ** 31) -1):
    #         return 0
    #     return s
