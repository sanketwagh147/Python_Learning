"""
Leet code 16 3 sum closest
"""


class Solution:
    def threeSumClosest(self, nums, target):

        nums.sort()
        n = len(nums)

        closest_sum = float("inf")
        min_distance = float("inf")

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1

            while left < right:
                total = nums[i] + nums[left] + nums[right]
                diff = abs(total - target)

                if diff < min_distance:
                    min_distance = diff
                    closest_sum = total

                if total < target:
                    left += 1
                elif total > target:
                    right -= 1
                else:
                    return total

        return closest_sum
