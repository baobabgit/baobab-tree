"""
Tests unitaires pour les itérateurs de parcours spécialisés.

Ce module contient tous les tests unitaires pour les classes d'itérateurs
spécialisés : PreorderIterator, InorderIterator, PostorderIterator,
LevelOrderIterator et LevelOrderWithLevelIterator.
"""

import pytest

from src.baobab_tree.search.traversal_iterators import (
    PreorderIterator,
    InorderIterator,
    PostorderIterator,
    LevelOrderIterator,
    LevelOrderWithLevelIterator,
)
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode


class TestPreorderIterator:
    """Tests pour la classe PreorderIterator."""

    def test_init_with_root(self):
        """Test de l'initialisation avec racine."""
        node = BinaryTreeNode(42)
        iterator = PreorderIterator(node)
        assert iterator._root == node
        assert len(iterator._stack) == 1
        assert iterator._stack[0] == node

    def test_init_without_root(self):
        """Test de l'initialisation sans racine."""
        iterator = PreorderIterator(None)
        assert iterator._root is None
        assert len(iterator._stack) == 0

    def test_iter_empty_tree(self):
        """Test de l'itération sur un arbre vide."""
        iterator = PreorderIterator(None)
        result = list(iterator)
        assert result == []

    def test_iter_single_node(self):
        """Test de l'itération sur un nœud unique."""
        node = BinaryTreeNode(42)
        iterator = PreorderIterator(node)
        result = list(iterator)
        assert result == [42]

    def test_iter_simple_tree(self):
        """Test de l'itération sur un arbre simple."""
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)

        iterator = PreorderIterator(root)
        result = list(iterator)
        assert result == [1, 2, 3]

    def test_iter_complex_tree(self):
        """Test de l'itération sur un arbre complexe."""
        # Créer un arbre plus complexe
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)

        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        iterator = PreorderIterator(root)
        result = list(iterator)
        assert result == [1, 2, 4, 5, 3]

    def test_next_empty_iterator(self):
        """Test de __next__ sur un itérateur vide."""
        iterator = PreorderIterator(None)
        with pytest.raises(StopIteration):
            iterator.__next__()

    def test_next_single_node(self):
        """Test de __next__ sur un nœud unique."""
        node = BinaryTreeNode(42)
        iterator = PreorderIterator(node)
        assert iterator.__next__() == 42
        with pytest.raises(StopIteration):
            iterator.__next__()


class TestInorderIterator:
    """Tests pour la classe InorderIterator."""

    def test_init_with_root(self):
        """Test de l'initialisation avec racine."""
        node = BinaryTreeNode(42)
        iterator = InorderIterator(node)
        assert iterator._root == node
        assert iterator._current == node
        assert len(iterator._stack) == 0
        assert len(iterator._visited) == 0

    def test_init_without_root(self):
        """Test de l'initialisation sans racine."""
        iterator = InorderIterator(None)
        assert iterator._root is None
        assert iterator._current is None

    def test_iter_empty_tree(self):
        """Test de l'itération sur un arbre vide."""
        iterator = InorderIterator(None)
        result = list(iterator)
        assert result == []

    def test_iter_single_node(self):
        """Test de l'itération sur un nœud unique."""
        node = BinaryTreeNode(42)
        iterator = InorderIterator(node)
        result = list(iterator)
        assert result == [42]

    def test_iter_simple_tree(self):
        """Test de l'itération sur un arbre simple."""
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)

        iterator = InorderIterator(root)
        result = list(iterator)
        assert result == [2, 1, 3]

    def test_iter_complex_tree(self):
        """Test de l'itération sur un arbre complexe."""
        # Créer un arbre plus complexe
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)

        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        iterator = InorderIterator(root)
        result = list(iterator)
        assert result == [4, 2, 5, 1, 3]

    def test_next_empty_iterator(self):
        """Test de __next__ sur un itérateur vide."""
        iterator = InorderIterator(None)
        with pytest.raises(StopIteration):
            iterator.__next__()


class TestPostorderIterator:
    """Tests pour la classe PostorderIterator."""

    def test_init_with_root(self):
        """Test de l'initialisation avec racine."""
        node = BinaryTreeNode(42)
        iterator = PostorderIterator(node)
        assert iterator._root == node
        assert iterator._current == node
        assert len(iterator._stack) == 0
        assert iterator._last_visited is None

    def test_init_without_root(self):
        """Test de l'initialisation sans racine."""
        iterator = PostorderIterator(None)
        assert iterator._root is None
        assert iterator._current is None

    def test_iter_empty_tree(self):
        """Test de l'itération sur un arbre vide."""
        iterator = PostorderIterator(None)
        result = list(iterator)
        assert result == []

    def test_iter_single_node(self):
        """Test de l'itération sur un nœud unique."""
        node = BinaryTreeNode(42)
        iterator = PostorderIterator(node)
        result = list(iterator)
        assert result == [42]

    def test_iter_simple_tree(self):
        """Test de l'itération sur un arbre simple."""
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)

        iterator = PostorderIterator(root)
        result = list(iterator)
        assert result == [2, 3, 1]

    def test_iter_complex_tree(self):
        """Test de l'itération sur un arbre complexe."""
        # Créer un arbre plus complexe
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)

        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        iterator = PostorderIterator(root)
        result = list(iterator)
        assert result == [4, 5, 2, 3, 1]

    def test_next_empty_iterator(self):
        """Test de __next__ sur un itérateur vide."""
        iterator = PostorderIterator(None)
        with pytest.raises(StopIteration):
            iterator.__next__()


class TestLevelOrderIterator:
    """Tests pour la classe LevelOrderIterator."""

    def test_init_with_root(self):
        """Test de l'initialisation avec racine."""
        node = BinaryTreeNode(42)
        iterator = LevelOrderIterator(node)
        assert iterator._root == node
        assert len(iterator._queue) == 1
        assert iterator._queue[0] == node

    def test_init_without_root(self):
        """Test de l'initialisation sans racine."""
        iterator = LevelOrderIterator(None)
        assert iterator._root is None
        assert len(iterator._queue) == 0

    def test_iter_empty_tree(self):
        """Test de l'itération sur un arbre vide."""
        iterator = LevelOrderIterator(None)
        result = list(iterator)
        assert result == []

    def test_iter_single_node(self):
        """Test de l'itération sur un nœud unique."""
        node = BinaryTreeNode(42)
        iterator = LevelOrderIterator(node)
        result = list(iterator)
        assert result == [42]

    def test_iter_simple_tree(self):
        """Test de l'itération sur un arbre simple."""
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)

        iterator = LevelOrderIterator(root)
        result = list(iterator)
        assert result == [1, 2, 3]

    def test_iter_complex_tree(self):
        """Test de l'itération sur un arbre complexe."""
        # Créer un arbre plus complexe
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)

        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        iterator = LevelOrderIterator(root)
        result = list(iterator)
        assert result == [1, 2, 3, 4, 5]

    def test_next_empty_iterator(self):
        """Test de __next__ sur un itérateur vide."""
        iterator = LevelOrderIterator(None)
        with pytest.raises(StopIteration):
            iterator.__next__()


class TestLevelOrderWithLevelIterator:
    """Tests pour la classe LevelOrderWithLevelIterator."""

    def test_init_with_root(self):
        """Test de l'initialisation avec racine."""
        node = BinaryTreeNode(42)
        iterator = LevelOrderWithLevelIterator(node)
        assert iterator._root == node
        assert len(iterator._queue) == 1
        assert iterator._queue[0] == (node, 0)

    def test_init_without_root(self):
        """Test de l'initialisation sans racine."""
        iterator = LevelOrderWithLevelIterator(None)
        assert iterator._root is None
        assert len(iterator._queue) == 0

    def test_iter_empty_tree(self):
        """Test de l'itération sur un arbre vide."""
        iterator = LevelOrderWithLevelIterator(None)
        result = list(iterator)
        assert result == []

    def test_iter_single_node(self):
        """Test de l'itération sur un nœud unique."""
        node = BinaryTreeNode(42)
        iterator = LevelOrderWithLevelIterator(node)
        result = list(iterator)
        assert result == [(42, 0)]

    def test_iter_simple_tree(self):
        """Test de l'itération sur un arbre simple."""
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)

        iterator = LevelOrderWithLevelIterator(root)
        result = list(iterator)
        assert result == [(1, 0), (2, 1), (3, 1)]

    def test_iter_complex_tree(self):
        """Test de l'itération sur un arbre complexe."""
        # Créer un arbre plus complexe
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)

        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        iterator = LevelOrderWithLevelIterator(root)
        result = list(iterator)
        assert result == [(1, 0), (2, 1), (3, 1), (4, 2), (5, 2)]

    def test_next_empty_iterator(self):
        """Test de __next__ sur un itérateur vide."""
        iterator = LevelOrderWithLevelIterator(None)
        with pytest.raises(StopIteration):
            iterator.__next__()

    def test_str_representation(self):
        """Test de la représentation string."""
        node = BinaryTreeNode(42)
        iterator = LevelOrderWithLevelIterator(node)
        str_repr = str(iterator)
        assert "LevelOrderWithLevelIterator" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        node = BinaryTreeNode(42)
        iterator = LevelOrderWithLevelIterator(node)
        repr_str = repr(iterator)
        assert "LevelOrderWithLevelIterator" in repr_str
