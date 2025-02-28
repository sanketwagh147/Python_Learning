"""
Leet code 27 
Remove element 
"""

import unittest
from typing import List

from parameterized import parameterized

from dsa_book.common.builders import TestCase


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """ """

        # 1️⃣ i points to the start of lst
        i = 0
        n = len(nums)
        # 2️⃣ j points to the end of lst
        j = n - 1
        num_swaps = 0

        # 3️⃣ find no of swaps
        for i in range(n):
            if nums[i] == val:
                num_swaps += 1

        # 4️⃣ reset i
        i = 0

        # REVIEW : Two pointer first and last

        # 5️⃣ main while till run only till i and j intersect
        while i < j:

            # increment i only item at i is not eq to val
            while nums[i] != val and i < j:
                i += 1

            # decrement j only item at j is equal to val
            while nums[j] == val and i < j:
                j -= 1

            # Break main while if i and j meet
            if i >= j:
                break

            # swap
            nums[i], nums[j] = nums[j], nums[i]

        return n - num_swaps


class TestRemoveElement(unittest.TestCase):

    _ = None

    @parameterized.expand(
        [
            TestCase(
                "tc1",
                {"nums": [3, 2, 2, 3], "val": 3},
                {"nums": [2, 2, _, _], "k": 2},
                "Basic test case",
            ),
            TestCase(
                "tc2",
                {"nums": [0, 1, 2, 2, 3, 0, 4, 2], "val": 2},
                {"nums": [0, 1, 4, 0, 3, _, _, _], "k": 5},
                "Multiple occurrences of val",
            ),
            TestCase(
                "tc3",
                {"nums": [1, 2, 3, 4, 5], "val": 6},
                {"nums": [1, 2, 3, 4, 5], "k": 5},
                "No occurrences of val",
            ),
            TestCase(
                "tc4",
                {"nums": [2, 2, 2, 2], "val": 2},
                {"nums": [_, _, _, _], "k": 0},
                "All elements are val",
            ),
            TestCase("tc5", {"nums": [], "val": 1}, {"nums": [], "k": 0}, "Empty list"),
        ]
    )
    def test_remove_element(self, name, input, output, description):
        solution = Solution()
        nums = input["nums"]
        val = input["val"]
        res = solution.removeElement(nums=nums, val=val)

        self.assertEqual(
            res,
            output["k"],
            f"{name} failed: Expected k={output['k']}, but got {res}. Description: {description}. "
            f"Final nums: {nums}",
        )


if __name__ == "__main__":
    unittest.main()
