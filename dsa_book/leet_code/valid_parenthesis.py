"""
Leet Code 20 valid parenthesis
"""


class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_map = {")": "(", "}": "{", "]": "["}  # Matching pairs

        for char in s:
            # 1️⃣ Check if it is a closing bracket
            if char in bracket_map:

                # pop last element else set it to any other char if stack not empty
                top = stack.pop() if stack else "X"

                # Check if top matches opening bracket
                if top != bracket_map[char]:
                    return False
            else:
                # Push opening brackets onto the stack
                stack.append(char)

        # Stack should be empty if valid
        return not stack
