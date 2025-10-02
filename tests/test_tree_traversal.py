"""
Tests unitaires pour la classe TreeTraversal.

Ce module contient tous les tests unitaires pour la classe abstraite TreeTraversal
et ses fonctionnalités de base.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_tree.spatial.tree_traversal import TreeTraversal
from src.baobab_tree.core.tree_node import TreeNode
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.exceptions import NodeValidationError


class ConcreteTreeTraversal(TreeTraversal):
    """Classe concrète pour tester TreeTraversal."""

    def traverse(self, root):
        """Implémentation concrète du parcours."""
        if root is None:
            return []
        result = [root.value]
        for child in root.get_children():
            result.extend(self.traverse(child))
        return result

    def traverse_iter(self, root):
        """Implémentation concrète du parcours itératif."""
        if root is None:
            return iter([])
        result = [root.value]
        for child in root.get_children():
            result.extend(self.traverse(child))
        return iter(result)


class TestTreeTraversal:
    """Tests pour la classe TreeTraversal."""

    def test_init_default_name(self):
        """Test de l'initialisation avec nom par défaut."""
        traversal = ConcreteTreeTraversal()
        assert traversal.get_traversal_name() == "ConcreteTreeTraversal"

    def test_init_custom_name(self):
        """Test de l'initialisation avec nom personnalisé."""
        traversal = ConcreteTreeTraversal("CustomTraversal")
        assert traversal.get_traversal_name() == "CustomTraversal"

    def test_traverse_empty_tree(self):
        """Test du parcours sur un arbre vide."""
        traversal = ConcreteTreeTraversal()
        result = traversal.traverse(None)
        assert result == []

    def test_traverse_iter_empty_tree(self):
        """Test du parcours itératif sur un arbre vide."""
        traversal = ConcreteTreeTraversal()
        result = list(traversal.traverse_iter(None))
        assert result == []

    def test_traverse_single_node(self):
        """Test du parcours sur un nœud unique."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        result = traversal.traverse(node)
        assert result == [42]

    def test_traverse_iter_single_node(self):
        """Test du parcours itératif sur un nœud unique."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        result = list(traversal.traverse_iter(node))
        assert result == [42]

    def test_is_empty_none_root(self):
        """Test de is_empty avec racine None."""
        traversal = ConcreteTreeTraversal()
        assert traversal.is_empty(None) is True

    def test_is_empty_valid_root(self):
        """Test de is_empty avec racine valide."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        assert traversal.is_empty(node) is False

    def test_validate_tree_none_root(self):
        """Test de validation d'arbre vide."""
        traversal = ConcreteTreeTraversal()
        assert traversal.validate_tree(None) is True

    def test_validate_tree_valid_tree(self):
        """Test de validation d'arbre valide."""
        traversal = ConcreteTreeTraversal()
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)

        assert traversal.validate_tree(root) is True

    def test_validate_tree_circular_reference(self):
        """Test de validation d'arbre avec référence circulaire."""
        traversal = ConcreteTreeTraversal()
        root = BinaryTreeNode(1)
        child = BinaryTreeNode(2)

        # Créer une référence circulaire en utilisant set_left
        root.set_left(child)
        # Créer manuellement une référence circulaire pour tester la validation
        child._left = root

        with pytest.raises(NodeValidationError):
            traversal.validate_tree(root)

    def test_traverse_with_callback_none_callback(self):
        """Test de traverse_with_callback avec callback None."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)

        with pytest.raises(ValueError, match="Callback function cannot be None"):
            traversal.traverse_with_callback(node, None)

    def test_traverse_with_callback_valid(self):
        """Test de traverse_with_callback avec callback valide."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        callback_calls = []

        def callback(value):
            callback_calls.append(value)

        traversal.traverse_with_callback(node, callback)
        assert callback_calls == [42]

    def test_traverse_with_callback_empty_tree(self):
        """Test de traverse_with_callback sur arbre vide."""
        traversal = ConcreteTreeTraversal()
        callback_calls = []

        def callback(value):
            callback_calls.append(value)

        traversal.traverse_with_callback(None, callback)
        assert callback_calls == []

    def test_traverse_with_condition_none_condition(self):
        """Test de traverse_with_condition avec condition None."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)

        with pytest.raises(ValueError, match="Condition function cannot be None"):
            traversal.traverse_with_condition(node, None)

    def test_traverse_with_condition_valid(self):
        """Test de traverse_with_condition avec condition valide."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)

        def condition(value):
            return value > 40

        result = traversal.traverse_with_condition(node, condition)
        assert result == [42]

    def test_traverse_with_condition_filtered(self):
        """Test de traverse_with_condition avec filtrage."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)

        def condition(value):
            return value < 40

        result = traversal.traverse_with_condition(node, condition)
        assert result == []

    def test_traverse_with_condition_empty_tree(self):
        """Test de traverse_with_condition sur arbre vide."""
        traversal = ConcreteTreeTraversal()

        def condition(value):
            return True

        result = traversal.traverse_with_condition(None, condition)
        assert result == []

    def test_traverse_depth_limited_negative_depth(self):
        """Test de traverse_depth_limited avec profondeur négative."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)

        with pytest.raises(ValueError, match="Max depth must be non-negative"):
            traversal.traverse_depth_limited(node, -1)

    def test_traverse_depth_limited_empty_tree(self):
        """Test de traverse_depth_limited sur arbre vide."""
        traversal = ConcreteTreeTraversal()
        result = traversal.traverse_depth_limited(None, 5)
        assert result == []

    def test_traverse_count_limited_negative_count(self):
        """Test de traverse_count_limited avec count négatif."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)

        with pytest.raises(ValueError, match="Max count must be non-negative"):
            traversal.traverse_count_limited(node, -1)

    def test_traverse_count_limited_empty_tree(self):
        """Test de traverse_count_limited sur arbre vide."""
        traversal = ConcreteTreeTraversal()
        result = traversal.traverse_count_limited(None, 5)
        assert result == []

    def test_traverse_count_limited_valid(self):
        """Test de traverse_count_limited avec count valide."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        result = traversal.traverse_count_limited(node, 1)
        assert result == [42]

    def test_traverse_reverse_empty_tree(self):
        """Test de traverse_reverse sur arbre vide."""
        traversal = ConcreteTreeTraversal()
        result = traversal.traverse_reverse(None)
        assert result == []

    def test_traverse_reverse_valid(self):
        """Test de traverse_reverse sur arbre valide."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        result = traversal.traverse_reverse(node)
        assert result == [42]

    def test_traverse_right_to_left_empty_tree(self):
        """Test de traverse_right_to_left sur arbre vide."""
        traversal = ConcreteTreeTraversal()
        result = traversal.traverse_right_to_left(None)
        assert result == []

    def test_traverse_right_to_left_valid(self):
        """Test de traverse_right_to_left sur arbre valide."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        result = traversal.traverse_right_to_left(node)
        assert result == [42]

    def test_get_tree_statistics_empty_tree(self):
        """Test de get_tree_statistics sur arbre vide."""
        traversal = ConcreteTreeTraversal()
        stats = traversal.get_tree_statistics(None)

        expected = {
            "node_count": 0,
            "height": -1,
            "leaf_count": 0,
            "internal_node_count": 0,
            "is_valid": True,
        }
        assert stats == expected

    def test_get_tree_statistics_single_node(self):
        """Test de get_tree_statistics sur nœud unique."""
        traversal = ConcreteTreeTraversal()
        node = BinaryTreeNode(42)
        stats = traversal.get_tree_statistics(node)

        assert stats["node_count"] == 1
        assert stats["height"] == 0
        assert stats["leaf_count"] == 1
        assert stats["internal_node_count"] == 0
        assert stats["is_valid"] is True

    def test_get_tree_statistics_complex_tree(self):
        """Test de get_tree_statistics sur arbre complexe."""
        traversal = ConcreteTreeTraversal()

        # Créer un arbre simple
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

    def test_str_representation(self):
        """Test de la représentation string."""
        traversal = ConcreteTreeTraversal("TestTraversal")
        str_repr = str(traversal)
        assert "ConcreteTreeTraversal" in str_repr
        assert "TestTraversal" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        traversal = ConcreteTreeTraversal("TestTraversal")
        repr_str = repr(traversal)
        assert "ConcreteTreeTraversal" in repr_str
        assert "TestTraversal" in repr_str

    def test_validate_node_recursive_circular_reference(self):
        """Test de _validate_node_recursive avec référence circulaire."""
        traversal = ConcreteTreeTraversal()
        root = BinaryTreeNode(1)
        child = BinaryTreeNode(2)

        # Créer une référence circulaire en utilisant set_left
        root.set_left(child)
        # Créer manuellement une référence circulaire pour tester la validation
        child._left = root

        with pytest.raises(NodeValidationError):
            traversal._validate_node_recursive(root, set())

    def test_validate_node_recursive_valid_tree(self):
        """Test de _validate_node_recursive avec arbre valide."""
        traversal = ConcreteTreeTraversal()
        root = BinaryTreeNode(1)
        child = BinaryTreeNode(2)
        root.set_left(child)

        result = traversal._validate_node_recursive(root, set())
        assert result is True

    def test_count_nodes_recursive(self):
        """Test de _count_nodes_recursive."""
        traversal = ConcreteTreeTraversal()
        root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        root.set_left(left)
        root.set_right(right)

        stats = {
            "node_count": 0,
            "height": 0,
            "leaf_count": 0,
            "internal_node_count": 0,
            "is_valid": True,
        }

        traversal._count_nodes_recursive(root, stats)

        assert stats["leaf_count"] == 2
        assert stats["internal_node_count"] == 1
