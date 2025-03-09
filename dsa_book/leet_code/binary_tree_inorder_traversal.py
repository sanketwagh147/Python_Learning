"""
Leet code 94 Binary Tree in order traversal

"""

from typing import List, Optional

from dsa_book.common.nodes import TreeNode


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        # Guard Clause
        if root is None:
            return []
        return (
            self.inorderTraversal(root.left)
            + [root.val]
            + self.inorderTraversal(root.right)
        )


if __name__ == "__main__":
    s = Solution()
    root = TreeNode(1, None, TreeNode(2, TreeNode(3)))
    tl = s.inorderTraversal(root)
    print(tl)
