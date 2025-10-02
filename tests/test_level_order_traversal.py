"""
Tests unitaires pour la classe LevelOrderTraversal.

Ce module contient tous les tests unitaires pour la classe LevelOrderTraversal
et ses fonctionnalités de parcours par niveaux.
"""

import pytest

from src.level_order_traversal import LevelOrderTraversal
from src.binary_tree_node import BinaryTreeNode
from src.exceptions import NodeValidationError


class TestLevelOrderTraversal:
    """Tests pour la classe LevelOrderTraversal."""

    def test_init_default_name(self):
        """Test de l'initialisation avec nom par défaut."""
        traversal = LevelOrderTraversal()
        assert traversal.get_traversal_name() == "LevelOrder"

    def test_init_custom_name(self):
        """Test de l'initialisation avec nom personnalisé."""
        traversal = LevelOrderTraversal("CustomLevelOrder")
        assert traversal.get_traversal_name() == "CustomLevelOrder"

    def test_traverse_empty_tree(self):
        """Test du parcours sur un arbre vide."""
        traversal = LevelOrderTraversal()
        result = traversal.traverse(None)
        assert result == []

    def test_traverse_single_node(self):
        """Test du parcours sur un nœud unique."""
        traversal = LevelOrderTraversal()
        node = BinaryTreeNode(42)
        result = traversal.traverse(node)
        assert result == [42]

    def test_traverse_simple_tree(self):
        """Test du parcours sur un arbre simple."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal.traverse(root)
        assert result == [1, 2, 3]

    def test_traverse_complex_tree(self):
        """Test du parcours sur un arbre complexe."""
        traversal = LevelOrderTraversal()
        
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
        
        result = traversal.traverse(root)
        assert result == [1, 2, 3, 4, 5]

    def test_traverse_iter_empty_tree(self):
        """Test du parcours itératif sur un arbre vide."""
        traversal = LevelOrderTraversal()
        result = list(traversal.traverse_iter(None))
        assert result == []

    def test_traverse_iter_single_node(self):
        """Test du parcours itératif sur un nœud unique."""
        traversal = LevelOrderTraversal()
        node = BinaryTreeNode(42)
        result = list(traversal.traverse_iter(node))
        assert result == [42]

    def test_traverse_iter_simple_tree(self):
        """Test du parcours itératif sur un arbre simple."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = list(traversal.traverse_iter(root))
        assert result == [1, 2, 3]

    def test_traverse_iter_complex_tree(self):
        """Test du parcours itératif sur un arbre complexe."""
        traversal = LevelOrderTraversal()
        
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
        
        result = list(traversal.traverse_iter(root))
        assert result == [1, 2, 3, 4, 5]

    def test_traverse_by_level_empty_tree(self):
        """Test de traverse_by_level sur un arbre vide."""
        traversal = LevelOrderTraversal()
        result = traversal.traverse_by_level(None)
        assert result == []

    def test_traverse_by_level_single_node(self):
        """Test de traverse_by_level sur un nœud unique."""
        traversal = LevelOrderTraversal()
        node = BinaryTreeNode(42)
        result = traversal.traverse_by_level(node)
        assert result == [[42]]

    def test_traverse_by_level_simple_tree(self):
        """Test de traverse_by_level sur un arbre simple."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal.traverse_by_level(root)
        assert result == [[1], [2, 3]]

    def test_traverse_by_level_complex_tree(self):
        """Test de traverse_by_level sur un arbre complexe."""
        traversal = LevelOrderTraversal()
        
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
        
        result = traversal.traverse_by_level(root)
        assert result == [[1], [2, 3], [4, 5]]

    def test_traverse_with_level_info_empty_tree(self):
        """Test de traverse_with_level_info sur un arbre vide."""
        traversal = LevelOrderTraversal()
        result = traversal.traverse_with_level_info(None)
        assert result == []

    def test_traverse_with_level_info_single_node(self):
        """Test de traverse_with_level_info sur un nœud unique."""
        traversal = LevelOrderTraversal()
        node = BinaryTreeNode(42)
        result = traversal.traverse_with_level_info(node)
        assert result == [(42, 0)]

    def test_traverse_with_level_info_simple_tree(self):
        """Test de traverse_with_level_info sur un arbre simple."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal.traverse_with_level_info(root)
        assert result == [(1, 0), (2, 1), (3, 1)]

    def test_traverse_with_level_info_complex_tree(self):
        """Test de traverse_with_level_info sur un arbre complexe."""
        traversal = LevelOrderTraversal()
        
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
        
        result = traversal.traverse_with_level_info(root)
        assert result == [(1, 0), (2, 1), (3, 1), (4, 2), (5, 2)]

    def test_traverse_depth_limited(self):
        """Test du parcours limité par profondeur."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre
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
        
        # Limiter à la profondeur 1
        result = traversal.traverse_depth_limited(root, 1)
        assert result == [1]

        # Limiter à la profondeur 2
        result = traversal.traverse_depth_limited(root, 2)
        assert result == [1, 2, 3]

    def test_traverse_right_to_left(self):
        """Test du parcours de droite à gauche."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal.traverse_right_to_left(root)
        assert result == [1, 3, 2]

    def test_traverse_with_callback(self):
        """Test du parcours avec callback."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        callback_calls = []
        
        def callback(value):
            callback_calls.append(value)
        
        traversal.traverse_with_callback(root, callback)
        assert callback_calls == [1, 2, 3]

    def test_traverse_with_condition(self):
        """Test du parcours avec condition."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        def condition(value):
            return value > 1
        
        result = traversal.traverse_with_condition(root, condition)
        assert result == [2, 3]

    def test_traverse_count_limited(self):
        """Test du parcours limité par count."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal.traverse_count_limited(root, 2)
        assert result == [1, 2]

    def test_traverse_reverse(self):
        """Test du parcours inversé."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal.traverse_reverse(root)
        assert result == [3, 2, 1]

    def test_get_tree_statistics(self):
        """Test des statistiques d'arbre."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        stats = traversal.get_tree_statistics(root)
        
        assert stats["node_count"] == 3
        assert stats["height"] == 1
        assert stats["leaf_count"] == 2
        assert stats["internal_node_count"] == 1
        assert stats["is_valid"] is True

    def test_validate_tree_invalid(self):
        """Test de validation d'arbre invalide."""
        traversal = LevelOrderTraversal()
        root = BinaryTreeNode(1)
        child = BinaryTreeNode(2)
        
        # Créer une référence circulaire en utilisant set_left
        root.set_left(child)
        # Créer manuellement une référence circulaire pour tester la validation
        child._left = root
        
        with pytest.raises(NodeValidationError):
            traversal.traverse(root)

    def test_traverse_with_queue_method(self):
        """Test de la méthode _traverse_with_queue."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal._traverse_with_queue(root)
        assert result == [1, 2, 3]

    def test_traverse_iterative_method(self):
        """Test de la méthode _traverse_iterative."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = list(traversal._traverse_iterative(root))
        assert result == [1, 2, 3]

    def test_traverse_depth_limited_recursive_method(self):
        """Test de la méthode _traverse_depth_limited_recursive."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre
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
        
        result = traversal._traverse_depth_limited_recursive(root, 2, 0)
        assert result == [1, 2, 3]

    def test_traverse_right_to_left_recursive_method(self):
        """Test de la méthode _traverse_right_to_left_recursive."""
        traversal = LevelOrderTraversal()
        
        # Créer un arbre simple
        #     1
        #    / \
        #   2   3
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)
        
        result = traversal._traverse_right_to_left_recursive(root)
        assert result == [1, 3, 2]

    def test_str_representation(self):
        """Test de la représentation string."""
        traversal = LevelOrderTraversal("TestLevelOrder")
        str_repr = str(traversal)
        assert "LevelOrderTraversal" in str_repr
        assert "TestLevelOrder" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        traversal = LevelOrderTraversal("TestLevelOrder")
        repr_str = repr(traversal)
        assert "LevelOrderTraversal" in repr_str
        assert "TestLevelOrder" in repr_str