"""
Leet code 168
Excel sheet Column title
"""


class Solution:
    def convertToTitle(self, columnNumber: int) -> str:

        ord_a = ord("A")

        res = []
        while columnNumber > 0:

            remainder = (columnNumber - 1) % 26
            res.append(chr(ord_a + remainder))

            columnNumber = (columnNumber - 1) // 26
        return "".join(res)[::-1]


if __name__ == "__main__":
    s = Solution()

    print(s.convertToTitle(28))
    print(s.convertToTitle(701))
    # print(s.convertToTitle())
