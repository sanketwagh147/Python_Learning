"""
Leet code 43

"""


class Solution:
    # def multiply(self, num1: str, num2: str) -> str:

    #     return str(int(num1) * int(num2))

    def multiply(self, num1: str, num2: str) -> str:

        if num1 == 0 or num2 == 0:
            return "0"

        n, m = len(num1), len(num2)

        # in multiplication n *m their product can have almost n+m digits
        result = [0] * (n + m)

        for i in reversed(range(n)):
            for j in reversed(range(m)):
                mul = int(num1[i]) * int(num2[j])
                p1, p2 = i + j, i + j + 1
                total = mul + result[p2]

                result[p2] = total % 10
                result[p1] += total // 10

        result_str = "".join(map(str, result)).lstrip("0")
        return result_str or "0"


if __name__ == "__main__":

    s = Solution()
    print(s.multiply("2", "3"))
