"""
Leet code 31 next permutation
"""


class Solution:

    # Swap in place
    def swap(self, nums, idx1, idx2):
        temp = nums[idx1]
        nums[idx1] = nums[idx2]
        nums[idx2] = temp

    def reverse(self, nums, start, end):
        while start < end:
            self.swap(nums, start, end)
            start += 1
            end -= 1

    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        if len(nums) == 1:
            return
        #
        if len(nums) == 2:
            return self.swap(nums, 0, 1)

        dec = len(nums) - 2

        while dec >= 0 and nums[dec] >= nums[dec + 1]:
            dec -= 1

        self.reverse(nums, dec + 1, len(nums) - 1)

        if dec == -1:
            return

        next_num = dec + 1
        while next_num < len(nums) and nums[next_num] <= nums[dec]:
            next_num += 1

        self.swap(nums, next_num, dec)
