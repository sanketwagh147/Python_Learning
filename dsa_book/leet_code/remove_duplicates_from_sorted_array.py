"""
Leet Code 26
Remove duplicates from sorted array
"""

import unittest

from parameterized import parameterized

from dsa_book.common.builders import TestCase


class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0

        ln_nums = len(nums)
        fp = 1

        # REVIEW Previous and next pointer comparison

        for i in range(1, ln_nums):
            prev_item = nums[i - 1]
            curr_item = nums[i]

            if curr_item != prev_item:
                nums[fp] = curr_item
                fp += 1

        return fp


class TestRemoveDuplicates(unittest.TestCase):
    @parameterized.expand(
        [
            TestCase("tc1", {"nums": [1, 1, 2]}, 2, "Removes one duplicate"),
            TestCase(
                "tc2",
                {"nums": [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]},
                5,
                "Removes multiple duplicates",
            ),
            TestCase("tc3", {"nums": [1, 2, 3, 4, 5]}, 5, "Already unique elements"),
            TestCase("tc4", {"nums": []}, 0, "Empty list case"),
            TestCase("tc5", {"nums": [1, 1, 1, 1]}, 1, "All elements are the same"),
            TestCase(
                "tc6",
                {"nums": [-1, 0, 0, 1, 1, 2, 3, 3, 4]},
                6,
                "Handles negative and positive numbers",
            ),
            TestCase(
                "tc7",
                {"nums": [1, 1, 1, 2, 2, 3, 3, 3, 4, 4]},
                4,
                "Handles multiple grouped duplicates",
            ),
            TestCase("tc8", {"nums": [2, 2, 2, 2, 2]}, 1, "Only one unique element"),
            TestCase(
                "tc9",
                {"nums": [-5, -4, -3, -3, -2, -2, -1, 0, 1, 2]},
                8,
                "Includes negative numbers",
            ),
            TestCase(
                "tc10",
                {"nums": [100, 200, 200, 300, 400, 500, 500, 600]},
                6,
                "Larger numbers with gaps",
            ),
        ]
    )
    def test_remove_duplicates(self, name, params, expected, description):
        solution = Solution()
        nums_copy = params["nums"][:]  # Create a copy to check mutation
        result = solution.removeDuplicates(nums_copy)

        self.assertEqual(result, expected, f"Failed {name}: k mismatch: {description=}")


if __name__ == "__main__":
    unittest.main()
