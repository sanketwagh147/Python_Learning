"""
Generate parenthesis leet code 22
"""


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans, sol = [], []

        def backtrack(open_, close):

            print(sol)

            if len(sol) == 2 * n:
                ans.append("".join(sol))
                print("----------------------")
                return

            if open_ < n:
                sol.append("(")
                backtrack(open_ + 1, close)
                sol.pop()

            if open_ > close:
                sol.append(")")
                backtrack(open_, close + 1)
                sol.pop()

        backtrack(0, 0)

        return ans


if __name__ == "__main__":
    s = Solution()
    s.generateParenthesis(3)
    """
    Example 1:

    Input: n = 3
    Output: ["((()))","(()())","(())()","()(())","()()()"]
    Example 2:

    Input: n = 1
    Output: ["()"]
    """
