#
# @lc app=leetcode id=1 lang=python3
#
# [1] Two Sum
nums = [3,2,4]
target = 6
#

# @lc code=start
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        a_dict = {}  # val:index
        
        for i,n in enumerate(nums):
            diff = target -n
            if diff in a_dict:
                return [ a_dict[diff], i]
            a_dict[n] = i
            
            
            

               
            

        
# @lc code=end

