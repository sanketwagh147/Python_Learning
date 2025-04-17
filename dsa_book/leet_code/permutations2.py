"""
Leet code 47
https://www.youtube.com/watch?v=qhBVWf0YafA
"""


class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        """
        using a dictionary
        """

        res, sol = [], []

        count = {n: 0 for n in nums}

        for each in nums:
            count[each] += 1

        def dfs():

            if len(sol) == len(nums):
                res.append(sol[:])
                return

            for n in count:

                if count[n] > 0:
                    sol.append(n)
                    count[n] -= 1

                    dfs()
                    count[n] += 1
                    sol.pop()

        dfs()

        return res

    # def permuteUnique(self, nums: list[int]) -> list[list[int]]:

    #     n = len(nums)
    #     nums = sorted(nums)

    #     res, sol = [], []
    #     used = [False] * n

    #     def backtrack():

    #         # Base case
    #         if len(sol) == n:
    #             res.append(sol[:])
    #             return

    #         for i in range(n):

    #             # if already used skip it
    #             if used[i]:
    #                 continue

    #             # avoids duplicates
    #             if  i>0 and nums[i] == nums[i -1 ] and not used[i-1]:
    #                 continue

    #             used[i] = True
    #             sol.append(nums[i])
    #             backtrack()
    #             sol.pop()
    #             used[i] = False

    #     backtrack()
    #     return res


if __name__ == "__main__":

    arr = [1, 1, 2]
    s = Solution()
    print(s.permuteUnique(arr))
