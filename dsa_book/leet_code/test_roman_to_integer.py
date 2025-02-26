import pytest

from dsa_book.common.builders import TestCase
from dsa_book.leet_code.roman_to_integer import Solution

test_cases = [
    # 🟢 Basic Cases
    TestCase("tc1", {"s": "III"}, 3, "basic case"),
    TestCase("tc4", {"s": "MDC"}, 1600, "basic case"),
    TestCase("tc5", {"s": "MLI"}, 1051, "basic case"),
    TestCase("tc7", {"s": "XII"}, 12, "basic case"),
    TestCase("tc8", {"s": "CXL"}, 140, "basic case"),
    # 🟡 Intermediate Cases
    TestCase("tc2", {"s": "LVIII"}, 58, "intermediate case"),
    TestCase("tc9", {"s": "DCCC"}, 800, "intermediate case"),
    TestCase("tc10", {"s": "CMXC"}, 990, "intermediate case"),
    # 🔴 Edge Cases
    TestCase("tc6", {"s": ""}, 0, "edge case - empty string"),
    TestCase("tc11", {"s": "I"}, 1, "edge case - smallest valid input"),
    TestCase(
        "tc12",
        {"s": "MMMCMXCIX"},
        3999,
        "edge case - largest valid Roman numeral",
    ),
    # 🏆 Complex Cases
    TestCase("tc3", {"s": "MCMXCIV"}, 1994, "complex case"),
    TestCase("tc13", {"s": "MMMDCCCLXXXVIII"}, 3888, "complex case"),
]


@pytest.mark.parametrize("name, input_data, expected, description", test_cases)
def test_roman_to_int(name, input_data, expected, description):
    solution = Solution().romanToInt(input_data["s"])
    assert (
        solution == expected
    ), f"Test Case {name}: Expected {expected}, got {solution}. Details: {description}"
