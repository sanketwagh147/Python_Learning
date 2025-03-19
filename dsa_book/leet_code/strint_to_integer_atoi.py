"""
Leet code 8
"""


class Solution:
    def myAtoi(self, s: str) -> int:

        sign = 1
        result = 0

        s = s.lstrip(" ")

        if not s:
            return 0

        if s[0] in ("-", "+"):
            if s[0] == "-":
                sign = -1

            s = s[1:]

        for chr in s:

            if not chr.isdigit():
                break
            result = result * 10 + int(chr)

        result = result * sign

        if result < -(2**31):
            return -(2**31)
        elif result > 2**31 - 1:
            return 2**31 - 1
        return result

    # def myAtoi(self, s: str) -> int:
    #     sign = 1
    #     result = 0
    #     i = 0
    #     n = len(s)

    #     # Ignore leading whitespace
    #     while i < n and s[i] == " ":
    #         i += 1

    #     if i < n and s[i] in ("-", "+"):
    #         if s[i] == "-":
    #             sign = -1
    #         i += 1  # Move past the sign character

    #     while i < n and s[i].isdigit():
    #         result = result * 10 + int(s[i])
    #         i += 1

    #     result *= sign

    #     int_min, int_max = -(2**31), 2**31 - 1
    #     return max(int_min, min(result, int_max))
