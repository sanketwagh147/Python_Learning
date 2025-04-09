"""
Leet code 40
https://www.youtube.com/watch?v=FOyRpNUSFeA
"""

from typing import List


class Solution:
    # def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

    #     res, sol = [], []
    #     n = len(candidates)
    #     candidates.sort()

    #     def backtrack(i, curr_sum):

    #         if curr_sum == target:

    #             res.append(sol[:])

    #             return

    #         if curr_sum > target or i == n :
    #             return

    #         # include canditates

    #         for j in range(i, n):
    #             # Skip duplicates
    #             if j > i and candidates[j] == candidates[j - 1]:
    #                 continue

    #             sol.append(candidates[j])
    #             backtrack(j + 1, curr_sum + candidates[j])  # Move to next index (no reuse)
    #             sol.pop()

    #     backtrack(0, 0)

    #     return res

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        res = []
        candidates.sort()

        def backtrack(start, path, curr_sum):

            if curr_sum == target:
                res.append(path[:])
                return

            if curr_sum > target:
                return

            # include canditates
            prev = -1

            for i in range(start, len(candidates)):
                # Skip duplicates
                if candidates[i] == prev:
                    continue

                path.append(candidates[i])
                backtrack(i + 1, path, curr_sum + candidates[i])
                path.pop()
                prev = candidates[i]

        backtrack(0, [], 0)

        return res


if __name__ == "__main__":

    candidates = [10, 1, 2, 7, 6, 1, 5]
    target = 8
    s = Solution()
    res = s.combinationSum2(candidates, target)
    print(res)
