"""
LeetCode 9
Palindrome number
"""

from decorators.disable_print_decorator import DisablePrint, disable_print


class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        return str(x)[::-1] == str(x)


class Solution2(DisablePrint):

    def isPalindrome(self, x: int) -> bool:
        """
        Instead of converting it to string we can reverser the second half of number and compare to first half
        """

        # 1️⃣ return non palindromic first
        # x < 0 as -ve numbers will never be palindromic
        # ( x % 10 == 0 and x != 0) numbers ending with 0 except 0 itself
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reversed_half = 0

        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            print(f"{reversed_half * 10 =} + {x % 10=}")
            print(f"{reversed_half}")
            x //= 10
            print(f"x= x//10 = {x}")

        # For even-length palindromes (1221): x == reversed_half → 12 == 12 → True.
        # For odd-length palindromes (12321): x == reversed_half // 10 → 12 == 123 // 10 (which is 12) → True.
        return x == reversed_half or x == reversed_half // 10


if __name__ == "__main__":
    s2 = Solution2()
    # s2.isPalindrome(1221)
    print(s2.__dict__)
    s2.isPalindrome(123123123123, disable_print=True)
    # print(disable_print(s2.isPalindrome)(121))
