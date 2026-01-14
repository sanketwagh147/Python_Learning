def disable_print(func):
    """Decorator that suppresses all print statements in the decorated function"""
    def wrapper(*args, **kwargs):
        original_print = globals()['print']
        
        globals()['print'] = lambda *args, **kwargs: None
        
        try:
            result = func(*args, **kwargs)
        finally:
            globals()['print'] = original_print
        
        return result
    return wrapper


class Solution:
    def isPalindrome_debug(self, x: int) -> bool:
        """Full implementation with detailed debugging output"""
        print(f"========== PALINDROME CHECK START ==========")
        print(f"Input number: {x}")
        print()
        
        # Negative numbers cannot be palindrome coz -ve sign
        # as -> -123 != 321-
        print(f"[CHECK] Is number negative?")
        if x < 0:
            print(f"  ✗ YES: {x} < 0 → Negative numbers cannot be palindromes (minus sign breaks symmetry)")
            print(f"  Result: False")
            print(f"========== RESULT: NOT PALINDROME ✗ ==========\n")
            return False
        
        print(f"  ✓ NO: {x} >= 0 → Proceed with reversal check\n")

        # Will store reversed number
        rev = 0
        # modify num in loop but compare with original x
        num = x
        
        print(f"[INIT] Starting reversal process:")
        print(f"  original = {x}")
        print(f"  reversed = {rev}")
        print(f"  remaining = {num}")
        print()

        iteration = 0
        while num != 0:
            iteration += 1
            print(f"  --- Iteration {iteration} ---")
            
            # mod original by 10
            mod_10 = num % 10
            print(f"    [EXTRACT] Last digit of {num}: {num} % 10 = {mod_10}")

            # multiply rev by 10 to get reversed number
            rev_x_10 = rev * 10
            print(f"    [SHIFT] Shift reversed left: {rev} * 10 = {rev_x_10}")
            
            rev = rev_x_10 + mod_10
            print(f"    [ADD] Append digit: {rev_x_10} + {mod_10} = {rev}")

            # divides num by 10 to remove last digit
            num = num // 10
            print(f"    [REMOVE] Drop last digit: {num} (remaining digits)")
            print(f"    State: reversed = {rev}, remaining = {num}")
            print()

        result = rev == x
        
        print(f"[FINAL COMPARISON]")
        print(f"  Original: {x}")
        print(f"  Reversed: {rev}")
        print(f"  Are they equal? {x} == {rev} → {result}")
        print(f"========== RESULT: {'PALINDROME ✓' if result else 'NOT PALINDROME ✗'} ==========\n")
        
        return result
    
    # @disable_print
    def isPalindrome(self, x: int) -> bool:
        """Clean version - same function but prints are suppressed by decorator"""
        return self.isPalindrome_debug(x)




if __name__ == "__main__":
    sol = Solution()
    
    # Test cases with debug output
    # sol.isPalindrome_debug(121)
    # sol.isPalindrome_debug(-121)
    # sol.isPalindrome_debug(10)
    # sol.isPalindrome_debug(12321)
    
    # Test cases without debug output
    print(sol.isPalindrome(121))     # True
    # print(sol.isPalindrome(-121))    # False
    # print(sol.isPalindrome(10))      # False
    # print(sol.isPalindrome(12321))   # True
        

