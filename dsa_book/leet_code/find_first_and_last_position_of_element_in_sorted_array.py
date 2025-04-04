"""
Leet code 34
"""

from typing import List


class Solution:
    # def searchRange(self, nums: List[int], target: int) -> List[int]:

    #     n = len(nums)
    #     matches  =[]
    #     for i in range(n):
    #         if nums[i] == target:
    #             matches.append(i)

    #     if len(matches) == 0:
    #         return [-1,-1]

    #     if len(matches) == 1:
    #         return [matches[0],matches[0]]
    #     return [matches[0],matches[-1]]

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)

        def binary_search_left(nums, target):
            left, right = 0, n - 1
            first = -1

            while left <= right:
                mid = (left + right) // 2

                if nums[mid] == target:
                    first = mid
                    right = mid - 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1

            return first

        def binary_search_right(nums, target):
            left, right = 0, n - 1
            last = -1

            while left <= right:
                mid = (left + right) // 2

                if nums[mid] == target:
                    last = mid
                    left = mid + 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1

            return last

        return [binary_search_left(nums, target), binary_search_right(nums, target)]


if __name__ == "__main__":
    li = [1, 2, 2, 2, 5, 1]
    s = Solution()
    print(s.searchRange(li, 2))
