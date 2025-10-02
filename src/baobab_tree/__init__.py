"""
Baobab Tree - Librairie d'arbres Python.

Cette librairie fournit une collection complète d'implémentations d'arbres
en Python, organisée de manière modulaire pour une utilisation facile et
une maintenance simplifiée.

Structure:
- core: Structures de base et interfaces
- binary: Arbres binaires et BST
- balanced: Arbres auto-équilibrés (AVL, etc.)
- nary: Arbres n-aires (B-trees, etc.)
- spatial: Arbres spatiaux et parcours
- search: Arbres de recherche et itérateurs
- specialized: Arbres spécialisés
"""

__version__ = "1.0.0"
__author__ = "Baobab Tree Team"
__email__ = "contact@baobab-tree.org"

# Imports principaux pour faciliter l'utilisation
from .core.interfaces import Comparable, TreeInterface, TreeTraversalInterface, TreeOperationInterface
from .core.exceptions import (
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
    RedBlackTreeError,
    ColorViolationError,
    PathViolationError,
    RedBlackBalancingError,
    TreeRotationError,
    InvalidRotationError,
    MissingChildError,
    RotationValidationError,
    BalancingStrategyError,
    InvalidStrategyError,
    StrategyApplicationError,
    StrategyValidationError,
)
from .core.tree_node import TreeNode

# Arbres binaires
from .binary.binary_tree_node import BinaryTreeNode
from .binary.binary_search_tree import BinarySearchTree

# Arbres équilibrés
from .balanced.avl_tree import AVLTree
from .balanced.avl_node import AVLNode
from .balanced.red_black_tree import RedBlackTree
from .balanced.red_black_node import RedBlackNode, Color
from .balanced.rotations import (
    TreeRotation,
    LeftRotation,
    RightRotation,
    LeftRightRotation,
    RightLeftRotation,
    RotationFactory,
    RotationSelector,
)
from .balanced.balancing_strategy import BalancingStrategy
from .balanced.avl_balancing_strategy import AVLBalancingStrategy
from .balanced.red_black_balancing_strategy import RedBlackBalancingStrategy
from .balanced.splay_balancing_strategy import SplayBalancingStrategy
from .balanced.treap_balancing_strategy import TreapBalancingStrategy
from .balanced.balancing_strategy_factory import BalancingStrategyFactory
from .balanced.balancing_strategy_selector import BalancingStrategySelector

# Arbres n-aires
from .nary.btree import BTree
from .nary.btree_node import BTreeNode

# Opérations utilitaires
from .core.utility_operations import UtilityOperations

__all__ = [
    # Version et métadonnées
    "__version__",
    "__author__",
    "__email__",
    
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
    "RedBlackTreeError",
    "ColorViolationError",
    "PathViolationError",
    "RedBlackBalancingError",
    "TreeRotationError",
    "InvalidRotationError",
    "MissingChildError",
    "RotationValidationError",
    "BalancingStrategyError",
    "InvalidStrategyError",
    "StrategyApplicationError",
    "StrategyValidationError",
    
    # Classes principales
    "TreeNode",
    "BinaryTreeNode",
    "BinarySearchTree",
    "AVLTree",
    "AVLNode",
    "RedBlackTree",
    "RedBlackNode",
    "Color",
    "TreeRotation",
    "LeftRotation",
    "RightRotation",
    "LeftRightRotation",
    "RightLeftRotation",
    "RotationFactory",
    "RotationSelector",
    "BalancingStrategy",
    "AVLBalancingStrategy",
    "RedBlackBalancingStrategy",
    "SplayBalancingStrategy",
    "TreapBalancingStrategy",
    "BalancingStrategyFactory",
    "BalancingStrategySelector",
    "BTree",
    "BTreeNode",
    "UtilityOperations",
]