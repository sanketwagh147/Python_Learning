"""
Leet code 45
https://www.youtube.com/watch?v=CsDI-yQuGeM
"""

from typing import List


class Solution:
    """
    nums:list =
    p1 = nums[0]
    n = len(nums)


    # constraints
    j is gte o
    j is lte nums[i]

    return min number of jumps to reach nums[n-1] (i.e the endk)
    """

    def jump(self, nums: List[int]) -> int:

        jumps = 0
        n = len(nums)
        end, far = 0, 0

        for i in range(n - 1):

            far = max(far, i + nums[i])
            if i == end:
                jumps += 1
                end = far

        return jumps

    def jump_brute(self, nums: List[int]) -> int:
        """
        Brute force
        """
        n = len(nums)
        smallest = [float("inf")]

        def backtrack(i=0, jumps=0):

            if i == n - 1:
                smallest[0] = min(smallest[0], jumps)
                return

            max_jumps = nums[i]

            max_reachable_idx = min(i + max_jumps, n - 1)

            for j in range(max_reachable_idx, i, -1):
                backtrack(j, jumps + 1)

        backtrack()
        return smallest[0]


if __name__ == "__main__":
    s = Solution()
    print(s.jump([2, 3, 1, 1, 4]))
