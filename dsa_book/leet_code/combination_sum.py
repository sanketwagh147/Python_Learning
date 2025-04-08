"""
Leet code 39
https://www.youtube.com/watch?v=utBw5FbYswk
"""

from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        res, sol = [], []
        n = len(candidates)

        def backtrack(i, curr_sum):

            if curr_sum == target:
                res.append(sol[:])
                return

            if curr_sum > target or i == n:
                return

            backtrack(i + 1, curr_sum)

            sol.append(candidates[i])
            backtrack(i, curr_sum + candidates[i])
            sol.pop()

        backtrack(0, 0)

        return res


if __name__ == "__main__":
    candidates = [2, 3, 6, 7]
    target = 7
    s = Solution()
    res = s.combinationSum(candidates, target)
    print(res)
