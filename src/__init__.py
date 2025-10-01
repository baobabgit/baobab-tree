"""
Librairie d'arbres - Module principal.

Ce module expose les classes et interfaces principales de la librairie d'arbres.
"""

from .exceptions import (
    TreeNodeError,
    InvalidNodeOperationError,
    CircularReferenceError,
    NodeValidationError,
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

__version__ = "0.1.0"
__author__ = "Tree Library Team"

__all__ = [
    # Exceptions
    "TreeNodeError",
    "InvalidNodeOperationError",
    "CircularReferenceError",
    "NodeValidationError",
    # Interfaces
    "Comparable",
    "TreeInterface",
    "TreeTraversalInterface",
    "TreeOperationInterface",
    "T",
    # Classes principales
    "TreeNode",
    "BinaryTreeNode",
]
