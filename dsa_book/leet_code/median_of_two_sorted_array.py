""""
Leetcode no : 4
Give: 
nums1 
"""

from typing import List

from dsa_book.common.builders import TestCase_


class Solution:

    def merge_two_sorted_array(self, arr1: List[int], arr2: List[int]) -> List[int]:
        """
        Merge two sorted arrays
        """

        i = j = 0
        merged_arr = []

        while i < len(arr1) and j < len(arr2):

            arr1_item = arr1[i]
            arr2_item = arr2[j]

            if arr1_item < arr2_item:
                merged_arr.append(arr1_item)
                i += 1
            else:
                merged_arr.append(arr2_item)
                j += 1

        # add remaining
        merged_arr.extend(arr1[i:])
        merged_arr.extend(arr2[j:])
        print(merged_arr)
        return merged_arr

    # REVIEW
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:

        # always make nums1 and smaller array
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums2

        x_partition, y_partition = len(nums1), len(nums2)
        low, high = 0, x_partition

        return 0.0


if __name__ == "__main__":
    nums1 = [1, 3]
    nums2 = [2]
    tc1 = TestCase_(inp=dict(nums1=nums1, nums2=nums2), op=2.00)

    def test_merge_sorted_array():
        nums1 = [1, 3]
        nums2 = [2]
        tc1 = TestCase_(inp=dict(arr1=nums1, arr2=nums2), op=[1, 2, 3])
        s = Solution()
        assert s.merge_two_sorted_array(**tc1.inp) == tc1.op

    test_merge_sorted_array()
