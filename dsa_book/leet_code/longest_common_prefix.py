"""
Leet code 14
Longest Common Prefix
"""

from typing import List

import pytest

from dsa_book.common.builders import TestCase


class Solution:

    def longestCommonPrefix(self, strs: List[str]) -> str:

        # 1️⃣ The minimum length amongst all strings in strs
        min_length = float("inf")

        for curr_word in strs:
            if len(curr_word) < min_length:
                min_length = len(curr_word)

        i = 0
        first_word = strs[0]
        # i = 0 : check if first word is common prefix
        # i = 0 : check if first_word is common prefix
        while i < min_length:
            for curr_word in strs:

                if curr_word[i] != first_word[i]:
                    return curr_word[:i]
            i += 1

        return first_word[:i]


tc = [
    # Basic cases
    TestCase(
        "tc1",
        {"strs": ["flower", "flow", "flight"]},
        expected="fl",
        description="Basic case with a common prefix",
    ),
    TestCase(
        "tc2",
        {"strs": ["dog", "racecar", "car"]},
        expected="",
        description="No common prefix",
    ),
    # Edge cases
    TestCase(
        "tc3",
        {"strs": [""]},
        expected="",
        description="Single empty string",
    ),
    TestCase(
        "tc4",
        {"strs": ["a"]},
        expected="a",
        description="Single character string",
    ),
    TestCase(
        "tc5",
        {"strs": ["aa", "ab"]},
        expected="a",
        description="Common prefix is a single character",
    ),
    TestCase(
        "tc6",
        {"strs": ["abc", "abc", "abc"]},
        expected="abc",
        description="All strings are identical",
    ),
    # Large cases
    TestCase(
        "tc7",
        {"strs": ["abcdefgh", "abcdef", "abcde", "abcd"]},
        expected="abcd",
        description="Gradual shortening of common prefix",
    ),
    TestCase(
        "tc8",
        {"strs": ["prefix", "pretest", "precompute", "preview"]},
        expected="pre",
        description="Common prefix of multiple words",
    ),
    # Special characters and case sensitivity
    TestCase(
        "tc9",
        {"strs": ["Case", "Casing", "Casual"]},
        expected="Cas",
        description="Case-sensitive prefix",
    ),
    TestCase(
        "tc10",
        {"strs": ["12345", "123", "123abc"]},
        expected="123",
        description="Numeric and alphanumeric strings",
    ),
]


@pytest.mark.parametrize("name, input_data, expected, description", tc)
def test_longest_common_prefix(name, input_data, expected, description):
    solution = Solution().longestCommonPrefix(input_data["strs"])
    assert (
        solution == expected
    ), f"Test Case {name}: Expected {expected}, got {solution}. Details: {description}"
