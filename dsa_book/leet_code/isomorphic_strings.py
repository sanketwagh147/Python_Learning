"""
Isomorphic strings
"""


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        n = len(s)
        m = len(t)

        # isomorphic strings have equal length
        if n != m:
            return False

        s_map = {}
        t_map = {}

        for i in range(n):
            s_chr = s[i]
            t_chr = t[i]

            if s_chr in s_map:

                if s_map[s_chr] != t_chr:
                    return False
            else:
                s_map[s_chr] = t_chr

            if t_chr in t_map:
                if t_map[t_chr] != s_chr:
                    return False
            else:
                t_map[t_chr] = s_chr

        return True


if __name__ == "__main__":
    s = Solution()
    print(s.isIsomorphic("egg", "add"))
