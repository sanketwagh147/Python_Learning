"""
Leet code 33 Binary search
"""


class Solution:
    def search(self, nums, target: int) -> int:

        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:  # Target in left half
                if nums[left] <= target < nums[mid]:  # Target in right half
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:  # Target in right half
                    left = mid + 1
                else:
                    right = mid - 1

        return -1

    # def search(self, nums: List[int], target: int) -> int:
    #     """Linear Search"""

    #     n = len(nums)

    #     for i in range(n):
    #         if nums[i] == target:
    #             return i

    #     return -1


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    s = Solution()
    idx = s.search(a, 3)
    print(idx)
