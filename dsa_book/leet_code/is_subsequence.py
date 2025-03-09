"""
Leet code 392
"""


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:

        len_s = len(s)
        len_t = len(t)

        if s == "":
            return True

        # if len of substring is gt the it will be false as all char won't be present in the string
        if len_s > len_t:
            return False

        j = 0
        for i in range(len_t):
            if t[i] == s[j]:

                # If j is at the last position
                # Else i.e when i will reach end postion it wil be false
                if j == len_s - 1:
                    return True

                j += 1

        return False


if __name__ == "__main__":
    s = "acb"
    t = "ahbgdc"

    s = Solution().isSubsequence(s, t)
    print(f"Op ={s} : Expected = false")
