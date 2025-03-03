"""
Leet code 61 : plus one

"""

# class Solution:
#     def plusOne(self, digits: List[int]) -> List[int]:

#         int_digits:str = ""

#         for each in digits:
#             int_digits+= str(each)

#         int_val = int(int_digits)

#         int_val += 1

#         str_val = str(int_val)
#         res = []
#         for each in str_val:
#             res.append(int(each))

# return res


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:

        digits = digits[::-1]
        carry, i = 1, 0

        while carry:

            # to keep i  in bound
            if i < len(digits):

                # handle if + 1 leads in a carry
                if digits[i] == 9:
                    digits[i] = 0
                else:
                    digits[i] += 1
                    carry = 0
            else:
                digits.append(1)
                carry = 0

            i += 1

        return digits[::-1]
