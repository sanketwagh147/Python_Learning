"""
Leet code 50
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        """Iterative solution"""

        if n < 0:
            x = 1 / x
            n = -n

        result = 1

        while n:

            # if not even
            if n % 2:
                result *= x

            x *= x
            n //= 2

        return result

    # def myPow(self, x: float, n: int) -> float:

    #     def pow(x, n):
    #         if n == 0:
    #             return 1

    #         # find power of half n
    #         half = pow(x, n // 2)

    #         # if n is even
    #         if n % 2 == 0:
    #             return half * half
    #         else:
    #             return half * half * x

    #     if n < 0:
    #         x = 1 / x
    #         n = -n

    #     return pow(x, n)


if __name__ == "__main__":
    s = Solution()
    print(s.myPow(2.00, 10))
