"""
Librairie d'arbres - Module principal.

Ce module expose les classes et interfaces principales de la librairie d'arbres.
"""

from .exceptions import (
    TreeNodeError,
    InvalidNodeOperationError,
    CircularReferenceError,
    NodeValidationError,
    BSTError,
    DuplicateValueError,
    ValueNotFoundError,
    InvalidOperationError,
)

from .interfaces import (
    Comparable,
    TreeInterface,
    TreeTraversalInterface,
    TreeOperationInterface,
    T,
)

from .tree_node import TreeNode
from .binary_tree_node import BinaryTreeNode
from .binary_search_tree import BinarySearchTree
from .bst_iterators import (
    PreorderIterator,
    InorderIterator,
    PostorderIterator,
    LevelOrderIterator,
)

# Classes de parcours
from .tree_traversal import TreeTraversal
from .preorder_traversal import PreorderTraversal
from .inorder_traversal import InorderTraversal
from .postorder_traversal import PostorderTraversal
from .level_order_traversal import LevelOrderTraversal

# Itérateurs de parcours
from .tree_iterator import TreeIterator
from .traversal_iterators import (
    PreorderIterator as TraversalPreorderIterator,
    InorderIterator as TraversalInorderIterator,
    PostorderIterator as TraversalPostorderIterator,
    LevelOrderIterator as TraversalLevelOrderIterator,
    LevelOrderWithLevelIterator,
)

__version__ = "0.1.0"
__author__ = "Tree Library Team"

__all__ = [
    # Exceptions
    "TreeNodeError",
    "InvalidNodeOperationError",
    "CircularReferenceError",
    "NodeValidationError",
    "BSTError",
    "DuplicateValueError",
    "ValueNotFoundError",
    "InvalidOperationError",
    # Interfaces
    "Comparable",
    "TreeInterface",
    "TreeTraversalInterface",
    "TreeOperationInterface",
    "T",
    # Classes principales
    "TreeNode",
    "BinaryTreeNode",
    "BinarySearchTree",
    # Classes de parcours
    "TreeTraversal",
    "PreorderTraversal",
    "InorderTraversal",
    "PostorderTraversal",
    "LevelOrderTraversal",
    # Itérateurs BST
    "PreorderIterator",
    "InorderIterator",
    "PostorderIterator",
    "LevelOrderIterator",
    # Itérateurs de parcours
    "TreeIterator",
    "TraversalPreorderIterator",
    "TraversalInorderIterator",
    "TraversalPostorderIterator",
    "TraversalLevelOrderIterator",
    "LevelOrderWithLevelIterator",
]
