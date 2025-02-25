"""
Leet code problem 5
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:

        if not s or len(s) == 1:
            return s

        def expand_around_center(left, right):

            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1

            return s[left + 1 : right]

        longest = ""

        for i in range(len(s)):

            # odd len string
            p1 = expand_around_center(i, i)

            # even len string
            p2 = expand_around_center(i, i + 1)

            # Check the longes palindrome

            if len(p1) > len(longest):
                longest = p1

            if len(p2) > len(longest):
                longest = p2

        return longest


if __name__ == "__main__":
    s = "cbbd"

    s = Solution().longestPalindrome(s)
    print(s)
