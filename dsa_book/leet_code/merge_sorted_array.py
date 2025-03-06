"""
Leet code 88
"""

from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        x_idx, y_idx = m - 1, n - 1

        for i in range(m + n - 1, -1, -1):

            # If x index is out of bounds
            if x_idx < 0:
                nums1[i] = nums2[y_idx]

            # If y index is out of bounds
            elif y_idx < 0:
                break
            # if item at x index is gt item at y idx
            elif nums1[x_idx] > nums2[y_idx]:
                nums1[i] = nums1[x_idx]
                x_idx -= 1
            else:
                nums1[i] = nums2[y_idx]
                y_idx -= 1
