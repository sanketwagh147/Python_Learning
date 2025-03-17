"""Leetcode 6 Zig Zag Conversation"""


class Solution:

    def convert(self, s: str, numRows: int) -> str:

        if numRows == 1:
            return s

        i = 0

        # positive means going down
        direction = 1

        matrix = [[] for _ in range(numRows)]

        for chr in s:

            matrix[i].append(chr)

            if i == 0:
                direction = 1
            elif i == numRows - 1:  # Last index (3 - 1) = 2
                direction = -1

            i += direction

        res = ""

        for i in range(numRows):
            res += "".join(matrix[i])

        return res

    # Optimized approach
    # def convert(self, s: str, numRows: int) -> str:
    #     if numRows == 1 or numRows >= len(s):
    #         return s

    #     rows = [""] * numRows
    #     i, direction = 0, 1

    #     for ch in s:
    #         rows[i] += ch
    #         if i == 0:
    #             direction = 1
    #         elif i == numRows - 1:
    #             direction = -1
    #         i += direction

    #     return "".join(rows)


if __name__ == "__main__":
    s = "PAYPALISHIRING"
    sol = Solution().convert(s, 3)
    print(sol)
    print(sol == "PAHNAPLIIGYIR")
