"""
Leet code 58 length of last word
"""


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        li = s.split(" ")
        temp = []
        for each in li:
            if each:
                # print(each)
                temp.append(each)

        return len(temp[-1]) if temp else 0


test_cases = [" take me to the moon  "]

if __name__ == "__main__":
    s = Solution().lengthOfLastWord(test_cases[0])
    print(s)
