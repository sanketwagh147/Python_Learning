"""
Leet code 2239
"""


class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        """ """

        # Assume closest number to be the  first number
        closest = nums[0]
        for each in nums:

            # compare each closet
            if abs(each) < abs(closest):
                closest = each

        # if  closest is -ve  then check if same exists in nums
        if closest < 0 and abs(closest) in nums:
            return abs(closest)

        return closest
