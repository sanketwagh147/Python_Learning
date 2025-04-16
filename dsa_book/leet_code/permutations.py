"""
Leet code 46

https://www.youtube.com/watch?v=gFm1lEfnzUQ

"""

from itertools import permutations
from typing import List


# @lc code=start
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        n = len(nums)

        res, sol = [], []

        def backtrack():
            if len(sol) == n:
                res.append(sol[:])
                return

            for i in nums:

                if i not in sol:

                    sol.append(i)
                    backtrack()
                    sol.pop()

        backtrack()
        return res

        # def permute(self, nums: List[int]) -> List[List[int]]:
        #     return list(permutations(nums))
        # def permute(self, nums: List[int]) -> List[List[int]]:

        #     result = []
        #     n = len(nums)

        #     def backtrack(path,used):

        #         if len(path) == n:
        #             result.append(path[:])
        #             return

        #         for i in range(n):
        #             if used[i]:
        #                 continue

        #             used[i] = True
        #             path.append(nums[i])
        #             backtrack(path,used)
        #             path.pop()
        #             used[i] = False

        #     backtrack([],[False]*n)

        return result


if __name__ == "__main__":

    s = Solution()
    print(s.permute([1, 2, 3]))
