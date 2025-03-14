"""
Leet Code Excel Sheet column Number 171
"""

from string import ascii_uppercase


class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        h_map = {each[0]: each[1] for each in zip(ascii_uppercase, range(1, 27))}
        print(h_map)
        multiplier = 1
        total = 0

        for each in columnTitle[::-1]:
            val = h_map[each] * multiplier
            total += val
            multiplier *= 26

        return total


if __name__ == "__main__":

    print(Solution().titleToNumber("ABCD"))
