from functools import cache
from typing import Protocol


class MaxSubArrayStrategy(Protocol):
    def solve(self, nums: list[int]) -> int:
        ...


class KadaneStrategy:
    def solve(self, nums: list[int]) -> int:
        if not nums:
            return 0

        global_max = nums[0]
        best_ending_here = nums[0]

        for i in range(1, len(nums)):
            num = nums[i]
            best_ending_here = max(num, best_ending_here + num)
            global_max = max(global_max, best_ending_here)

        return global_max


class BruteForceStrategy:
    def solve(self, nums: list[int]) -> int:
        ans = float("-inf")
        for i in range(len(nums)):
            cur_sum = 0
            for j in range(i, len(nums)):
                cur_sum += nums[j]
                ans = max(ans, cur_sum)
        return 0 if ans == float("-inf") else int(ans)


class MemoizationStrategy:
    def solve(self, nums: list[int]) -> int:
        @cache
        def dp(i: int, must_pick: bool) -> int:
            if i >= len(nums):
                return 0 if must_pick else int(-float("inf"))

            return max(
                nums[i] + dp(i + 1, True),
                0 if must_pick else dp(i + 1, False),
            )

        return int(dp(0, False))


class Solution:
    def __init__(self, strategy: MaxSubArrayStrategy | None = None) -> None:
        self.strategy = strategy or KadaneStrategy()

    def maxSubArray(self, nums: list[int]) -> int:
        return self.strategy.solve(nums)


if __name__ == "__main__":
    s = Solution(strategy=BruteForceStrategy())
    s1 = Solution(strategy=MemoizationStrategy())
    s2 = Solution(strategy=KadaneStrategy())
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(s.maxSubArray(nums))
    print(s1.maxSubArray(nums))
    print(s2.maxSubArray(nums))