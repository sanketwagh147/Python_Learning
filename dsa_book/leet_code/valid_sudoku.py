"""
Leet code 36
"""

from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        n = len(board)

        # Validate cols

        for i in range(n):
            s = set()

            for j in range(n):
                item = board[i][j]

                if item in s:
                    return False
                elif item != ".":
                    s.add(item)

        # Validate rows
        for i in range(n):
            s = set()

            for j in range(n):
                item = board[j][i]

                if item in s:
                    return False
                elif item != ".":
                    s.add(item)

        # Validate boxes
        starts = [
            (0, 0),
            (0, 3),
            (0, 6),
            (3, 0),
            (3, 3),
            (3, 6),
            (6, 0),
            (6, 3),
            (6, 6),
        ]

        for i, j in starts:
            s = set()

            for row in range(i, i + 3):
                for col in range(j, j + 3):
                    item = board[row][col]
                    if item in s:
                        return False

                    elif item != ".":
                        s.add(item)

        return True
