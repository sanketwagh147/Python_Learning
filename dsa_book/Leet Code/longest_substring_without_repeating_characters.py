"""Leet Code problem 3"""


# 🌟 Uses Sliding window pattern
class Solution:

    def lengthOfLongestSubstring(self, s: str) -> int:
        chrs = set()
        left = 0
        max_length = 0

        for right in range(len(s)):

            # checks chr on right side
            while s[right] in chrs:
                chrs.remove(s[left])
                left += 1

            chrs.add(s[right])
            max_length = max(max_length, right - left + 1)

        return max_length
