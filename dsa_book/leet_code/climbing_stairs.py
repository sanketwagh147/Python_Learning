"""
Leet code 70 : Climbing Stairs
"""


class Solution:
    cache = {}

    def climbStairs(self, n: int) -> int:

        if n in Solution.cache:
            return Solution.cache[n]

        # Base Case

        if n == 1:
            return 1

        if n == 2:
            return 2

        res = self.climbStairs(n - 2) + self.climbStairs(n - 1)

        Solution.cache[n] = res
        return res
