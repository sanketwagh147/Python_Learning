"""
Leet code 35 : Search insert position

"""

import unittest
from typing import List
from unittest import TestCase

from parameterized import parameterized


class Solution:

    def searchInsert(self, nums: List[int], target: int) -> int:
        n = len(nums)
        for i in range(n):
            curr = nums[i]

            if curr >= target:
                return i

        return n


cases = [
    ("tc1", {"arr": [1, 2, 3, 5], "t": 5}, 3, "Contains an item"),
    ("tc1", {"arr": [1, 3, 5, 6], "t": 7}, 4, "Contains an item"),
]


class TestSearchInsert(TestCase):
    @parameterized.expand(cases)
    def test_search_insert(self, name, input: dict, op: int, description: str):

        print(name, input, op, description)

        s = Solution()
        res = s.searchInsert(input["arr"], input["t"])
        self.assertEqual(res, op, f"{name} case ({description} failed")
        print(f"{name} ran successfully")


if __name__ == "__main__":
    unittest.main()
