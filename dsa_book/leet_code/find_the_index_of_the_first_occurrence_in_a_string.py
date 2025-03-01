"""
Leet code 28
Find the index of first occurence in a string
"""


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        n = len(haystack)
        m = len(needle)

        # loop through the haystack
        for i in range(n):

            # reset needle index
            j = 0

            # Loop from i to end of haystack
            for k in range(i, n):
                if haystack[k] == needle[j]:
                    # incremen j if match
                    j += 1

                else:
                    break

                # when len match means from i index the matcheing sbustring starts
                if j == m:

                    return i

        return -1


if __name__ == "__main__":
    s = Solution()
    resu1 = s.strStr(haystack="sabsad", needle="sad")
    assert resu1 == 4
