"""
Leet Code 17
"""

from typing import List

from icecream import ic


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        res = []
        if not digits:
            return res

        key_map = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        def backtrack(index, path):
            ic(index)
            ic(path)
            ic("END".center(40, "-"))
            if index == len(digits):
                res.append("".join(path))
                return

            for letter in key_map[digits[index]]:
                backtrack(index + 1, path + [letter])

            ic(res)
            ic("END".center(60, "-"))

        backtrack(0, [])

        return res


if __name__ == "__main__":
    s = Solution()
    s.letterCombinations("23")
