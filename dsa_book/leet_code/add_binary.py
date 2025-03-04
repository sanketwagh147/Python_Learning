"""
Leet code 67 add binary
"""


class Solution:

    def addBinary(self, a: str, b: str) -> str:
        """Two pointer solution no need to reverse"""
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        result = []

        while i >= 0 or j >= 0 or carry:

            # consider carry
            total = carry

            if i >= 0:
                total += int(a[i])
                i -= 1

            if j >= 0:
                total += int(b[j])
                j -= 1

            result.append(str(total % 2))
            carry = total // 2

        return "".join(result[::-1])

    # def addBinary(self, a: str, b: str) -> str:
    #     res = ""
    #     carry = 0

    #     # reverse strings
    #     a,b=a[::-1], b[::-1]
    #     m,n = len(a), len(b)

    #     # calculate max length
    #     mx_ln = max(len(a),len(b))

    #     for i in range(mx_ln):

    #         # handle out of bounds
    #         first = int(a[i]) if i < m else 0
    #         second = int(b[i]) if i < n else 0

    #         total = first + second + carry

    #         char = str(total % 2) # % 2 will return remainder

    #         res = char + res

    #         carry = total // 2

    #     if carry:
    #         res = "1" + res

    #     return res


if __name__ == "__main__":
    s = Solution()
    r = s.addBinary("1010", "1011")
    print(r)
