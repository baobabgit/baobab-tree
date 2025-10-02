"""
Module nary - Arbres n-aires.

Ce module contient les implémentations d'arbres n-aires,
notamment les B-trees.
"""

from .btree import BTree
from .btree_node import BTreeNode

__all__ = [
    "BTree",
    "BTreeNode",
]