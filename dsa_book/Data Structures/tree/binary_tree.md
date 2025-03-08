# Binary Tree

A binary tree is a hierarchical data structure where each node has at most two children(left and right) and it is commonly used in searching sorting and hierarchical data representation in computer science

## Key Terminology

**Root** - The topmost node of the tree.  
**Parent Node** - A node that has children.  
**Child Node** - A node that descends from another node.  
**Leaf Node** - A node that has no children.  
**Height of Tree** - The longest path from the root to a leaf.  
**Depth of Node** - The number of edges from the root to the node.  

## Types of Binary Trees

**Full Binary Tree** - Each node has either 0 or 2 children.  
**Complete Binary Tree** - All levels are filled except possibly the last, which is filled from left to right.  
**Perfect Binary Tree** - All internal nodes have 2 children, and all leaf nodes are at the same level.  
**Balanced Binary Tree** - The height difference between the left and right subtree is at most 1.  
**Binary Search Tree (BST)** A binary tree where left child < parent < right child.  

## Illustration of a binary Tree

        A
       / \
      B   C
     / \   \
    D   E   F

A is the root node.  
B and C are children of A.
D and E are children of B.  
F is the child of C.  
D, E, and F are leaf nodes.  

Binary trees are useful in searching algorithms, expression trees, hierarchical databases, and file system structures.  
  
## Edge of a binary tree

In a binary tree, an edge is the connection (or link) between two nodes. It represents the relationship between a parent node and a child node.

### Key Points About Edges in a Binary Tree

Each edge connects a parent to its child (left or right).  
**Number of edges in a tree** = Number of nodes - 1 (since every node except the root has one incoming edge).
**Path length** is measured in edges (e.g., the distance between two nodes is the number of edges between them).  
**Height of a tree** is defined as the number of edges on the longest path from the root to a leaf.  

### Example Binary Tree and Edges  

        A
       / \
      B   C
     / \   \
    D   E   F
Edges:

A → B  
A → C  
B → D  
B → E  
C → F  
(Total 5 edges for 6 nodes)  
