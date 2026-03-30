# Iterator Pattern — Question 2 (Medium)

## Problem: Tree Traversal Iterators (BFS, DFS, In-Order)

A binary tree needs multiple traversal strategies, each exposed as a Python iterator.

### Requirements

- `TreeNode`: `value`, `left`, `right`
- Iterators (each implements `__iter__` + `__next__`):
  - `BFSIterator(root)` — level-by-level (breadth-first)
  - `DFSIterator(root)` — pre-order depth-first
  - `InOrderIterator(root)` — in-order (left → root → right)

- `BinaryTree`: holds root, exposes `.bfs()`, `.dfs()`, `.inorder()` methods that return iterators

### Expected Usage

```python
#         1
#        / \
#       2   3
#      / \   \
#     4   5   6

tree = BinaryTree()
tree.root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, None, TreeNode(6)))

print(list(tree.bfs()))      # → [1, 2, 3, 4, 5, 6]
print(list(tree.dfs()))      # → [1, 2, 4, 5, 3, 6]
print(list(tree.inorder()))  # → [4, 2, 5, 1, 3, 6]

# Lazy iteration
for node in tree.bfs():
    if node == 3:
        break
    print(node)  # → 1, 2
```

### Constraints

- BFS uses a queue (`collections.deque`).
- DFS uses a stack (list).
- InOrder uses a stack with current-node tracking.
- All iterators are **lazy** — they don't build a list upfront.

### Think About

- Why is the iterator pattern better than tree.get_all_bfs() returning a list?
- How does Python's generator (`yield`) simplify this? Try rewriting one iterator as a generator.
