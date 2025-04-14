"""
Leet code 49
https://www.youtube.com/watch?v=eDmxPfVa81k
"""

from collections import defaultdict
from typing import List


# @lc code=start
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Pattern creates immutable tuple as key
        """
        anagrams_dict = defaultdict(list)

        for word in strs:

            count = [0] * 26

            for chr in word:

                count[ord(chr) - ord("a")] += 1

            key = tuple(count)
            anagrams_dict[key].append(word)
            # print(key)

        for k, v in anagrams_dict.items():
            print(k, v)
        ans = anagrams_dict.values()
        # print(ans)

        return list(ans)


if __name__ == "__main__":
    # Example 1:
    # Input:
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    # Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

    s = Solution()
    print(s.groupAnagrams(strs))
