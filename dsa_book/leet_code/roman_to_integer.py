"""
LeetCode 13 : Roman to integer
"""

import unittest

from parameterized import parameterized

from dsa_book.common.builders import TestCase


class Solution:
    """
    I (before) -> (-1 )
    X (before) -> (-10)
    C (before) -> (-100)
    """

    def romanToInt(self, s: str) -> int:
        r_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

        result: int = 0
        i: int = 0

        while i < len(s):

            # Check for subtractive pairs
            if i < len(s) - 1 and r_map[s[i]] < r_map[s[i + 1]]:
                result += r_map[s[i + 1]] - r_map[s[i]]
                i += 2
            else:
                result += r_map[s[i]]
                i += 1

        return result


class TestRomanToInt(unittest.TestCase):

    test_cases = [
        # 🟢 Basic Cases
        TestCase("tc1", inp=dict(s="III"), op=3, details="basic case"),
        TestCase("tc4", inp=dict(s="MDC"), op=1600, details="basic case"),
        TestCase("tc5", inp=dict(s="MLI"), op=1051, details="basic case"),
        TestCase("tc7", inp=dict(s="XII"), op=12, details="basic case"),
        TestCase("tc8", inp=dict(s="CXL"), op=140, details="basic case"),
        # 🟡 Intermediate Cases
        TestCase("tc2", inp=dict(s="LVIII"), op=58, details="intermediate case"),
        TestCase("tc9", inp=dict(s="DCCC"), op=800, details="intermediate case"),
        TestCase("tc10", inp=dict(s="CMXC"), op=990, details="intermediate case"),
        # 🔴 Edge Cases
        TestCase("tc6", inp=dict(s=""), op=0, details="edge case - empty string"),
        TestCase(
            "tc11", inp=dict(s="I"), op=1, details="edge case - smallest valid input"
        ),
        TestCase(
            "tc12",
            inp=dict(s="MMMCMXCIX"),
            op=3999,
            details="edge case - largest valid Roman numeral",
        ),
        # 🏆 Complex Cases
        TestCase("tc3", inp=dict(s="MCMXCIV"), op=1994, details="complex case"),
        TestCase(
            "tc13", inp=dict(s="MMMDCCCLXXXVIII"), op=3888, details="complex case"
        ),
    ]

    @parameterized.expand(
        [(each.name, each.inp["s"], each.op, each.details) for each in test_cases]
    )
    def test_generic(self, name, s: str, op: int, description: str = ""):
        solution = Solution().romanToInt(s)
        self.assertEqual(
            solution,
            op,
            f"Test Case {name=} {solution=} is not equal to {op=}\n{description=}",
        )


if __name__ == "__main__":
    unittest.main()
