"""
Leet code 242
"""


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:

        n, m = [len(_) for _ in [s, t]]

        if n != m:
            return False

        chr_count = {}

        # for chr in s:
        # chr_count[chr] = chr_count.get(chr,0) + 1

        for chr in s:
            if chr in chr_count:
                chr_count[chr] += 1
            else:
                chr_count[chr] = 1

        for chr in t:
            if chr in chr_count:
                chr_count[chr] -= 1
            else:
                return False

        return all(val == 0 for val in chr_count.values())


if __name__ == "__main__":

    s = Solution()
    print(s.isAnagram("aa", "bb"))
