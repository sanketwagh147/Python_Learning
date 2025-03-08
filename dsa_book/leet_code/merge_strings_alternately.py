"""
Leet code 1768
"""


class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        n = len(word1)
        m = len(word2)
        min_ = min(m, n)
        max_ = max(m, n)

        res = ""
        # iterate through common lower indexex
        for i in range(min_):
            res += word1[i]
            res += word2[i]

        # iterate through remaining
        for i in range(min_, max_):

            # only add if not out of bounds
            if n >= min_ and n >= max_:
                res += word1[i]
            if m >= min_ and m >= max_:
                res += word2[i]

        return res
