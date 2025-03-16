"""
Leet code 238
"""

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        n = len(nums)
        res = [1] * (n)

        prefix = 1

        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]

        postfix = 1

        for i in range(n - 1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]

        return res

    # def productExceptSelf(self, nums: List[int]) -> List[int]:

    #     n = len(nums)
    #     r_mul = 1
    #     l_mul = 1

    #     l_arr = [0] * n
    #     r_arr = [0] * n

    #     for i in range(n):
    #         j = -i - 1

    #         l_arr[i] = l_mul
    #         r_arr[j] = r_mul
    #         l_mul *= nums[i]
    #         r_mul *= nums[j]

    #     return [l*r for l,r in zip(l_arr,r_arr)]

    # def productExceptSelf(self, nums: List[int]) -> List[int]:

    #     n = len(nums)

    #     arr = [1] * n
    #     left_product = 1

    #     for i in range(n):
    #         arr[i] = left_product
    #         left_product *= nums[i]
    #         # print(arr)

    #     # print("-----------")

    #     right_product = 1

    #     for i in range(n-1,-1,-1):
    #         arr[i] *= right_product
    #         right_product *= nums[i]

    #         # print(arr)

    #     return arr


if __name__ == "__main__":

    s = Solution()
    print(s.productExceptSelf([1, 2, 3, 4]))

    print(s.productExceptSelf([-1, 1, 0, -3, 3]))
