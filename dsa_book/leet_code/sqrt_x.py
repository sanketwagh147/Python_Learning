"""Leet code 69 square root"""

from math import floor


class Solution:
    #  def mySqrt(self, x: int) -> int:
    #      """"using floor"""
    #      x = x ** (1 / 2)
    #      return floor(x)

    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x  # sqrt(0) = 0, sqrt(1) = 1

        left, right = 0, x
        while left <= right:
            mid = (left + right) // 2
            print(f"{left=} {mid=} {right=}")
            if mid * mid == x:
                return mid
            elif mid * mid < x:
                left = mid + 1
            else:
                right = mid - 1

        return right  # `right` is the truncated sqrt(x)


if __name__ == "__main__":
    s = Solution().mySqrt(16)
    print(s)
