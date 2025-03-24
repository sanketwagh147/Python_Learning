"""
Leet Code 17
"""


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
            if index == len(digits):
                res.append("".join(path))
                return

            for letter in key_map[digits[index]]:
                backtrack(index + 1, path + [letter])

        backtrack(0, [])

        return res
