"""
Module core - Structures de base pour la librairie d'arbres.

Ce module contient les interfaces, exceptions et classes de base
utilisées dans toute la librairie d'arbres.
"""

from .interfaces import Comparable, TreeInterface, TreeTraversalInterface, TreeOperationInterface
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
    BTreeError,
    InvalidOrderError,
    NodeFullError,
    NodeUnderflowError,
)
from .tree_node import TreeNode
from .utility_operations import UtilityOperations

__all__ = [
    # Interfaces
    "Comparable",
    "TreeInterface",
    "TreeTraversalInterface", 
    "TreeOperationInterface",
    
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
    "BTreeError",
    "InvalidOrderError",
    "NodeFullError",
    "NodeUnderflowError",
    
    # Classes principales
    "TreeNode",
    "UtilityOperations",
]