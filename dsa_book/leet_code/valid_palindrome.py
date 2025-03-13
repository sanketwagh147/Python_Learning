"""
Leet code 125 valid palindrome
"""

import re
from string import ascii_letters, digits


# @lc code=start
class Solution:
    # def isPalindrome(self, s: str) -> bool:

    # clean_s = ""
    # for each in s:
    #     if each in ascii_letters + digits:
    #         temp = each.lower()
    #         clean_s +=temp
    # print(clean_s)

    # return clean_s == clean_s[::-1]

    # sol 2
    def isPalindrome_2(self, s: str) -> bool:
        s = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
        return s == s[::-1]

    # solution 3 : 2 pointer approach
    def isPalindrome_3(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
