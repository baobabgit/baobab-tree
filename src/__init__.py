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
    AVLError,
    InvalidBalanceFactorError,
    RotationError,
    HeightMismatchError,
    AVLNodeError,
    HeightCalculationError,
    BTreeError,
    InvalidOrderError,
    NodeFullError,
    NodeUnderflowError,
    SplitError,
    MergeError,
    RedistributionError,
    BalancingError,
    ImbalanceDetectionError,
    CorrectionApplicationError,
    ValidationError,
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
from .avl_node import AVLNode
from .avl_tree import AVLTree
from .avl_rotations import AVLRotations
from .avl_balancing import AVLBalancing
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

# Classes d'opérations sur les arbres
from .tree_operations import TreeOperations
from .binary_tree_operations import BinaryTreeOperations
from .bst_operations import BSTOperations
from .avl_operations import AVLOperations
from .search_operations import SearchOperations
from .utility_operations import UtilityOperations

# Classes B-tree
from .btree import BTree
from .btree_node import BTreeNode

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
    "AVLError",
    "InvalidBalanceFactorError",
    "RotationError",
    "HeightMismatchError",
    "AVLNodeError",
    "HeightCalculationError",
    "BTreeError",
    "InvalidOrderError",
    "NodeFullError",
    "NodeUnderflowError",
    "SplitError",
    "MergeError",
    "RedistributionError",
    "BalancingError",
    "ImbalanceDetectionError",
    "CorrectionApplicationError",
    "ValidationError",
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
    "AVLNode",
    "AVLTree",
    "AVLRotations",
    "AVLBalancing",
    # Classes B-tree
    "BTree",
    "BTreeNode",
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
    # Classes d'opérations sur les arbres
    "TreeOperations",
    "BinaryTreeOperations",
    "BSTOperations",
    "AVLOperations",
    "SearchOperations",
    "UtilityOperations",
]
