"""
Tests unitaires pour la classe BinaryTreeOperations.

Ce module contient les tests unitaires pour la classe BinaryTreeOperations
et ses méthodes spécialisées pour les arbres binaires.
"""

import pytest
from src.binary_tree_node import BinaryTreeNode
from src.binary_tree_operations import BinaryTreeOperations


class TestBinaryTreeOperations:
    """Tests pour la classe BinaryTreeOperations."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.operations = BinaryTreeOperations[int]()

        # Créer un arbre binaire de test
        self.root = BinaryTreeNode(1)
        self.left = BinaryTreeNode(2)
        self.right = BinaryTreeNode(3)
        self.left_left = BinaryTreeNode(4)
        self.left_right = BinaryTreeNode(5)

        self.root.set_left(self.left)
        self.root.set_right(self.right)
        self.left.set_left(self.left_left)
        self.left.set_right(self.left_right)

    def test_search_existing_value(self):
        """Test de search avec une valeur existante."""
        result = self.operations.search(self.root, 1)
        assert result is not None
        assert result.value == 1

        result = self.operations.search(self.root, 2)
        assert result is not None
        assert result.value == 2

        result = self.operations.search(self.root, 4)
        assert result is not None
        assert result.value == 4

    def test_search_non_existing_value(self):
        """Test de search avec une valeur inexistante."""
        result = self.operations.search(self.root, 6)
        assert result is None

        result = self.operations.search(None, 1)
        assert result is None

    def test_search_invalid_root_type(self):
        """Test de search avec un type de racine invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.search("invalid", 1)

    def test_insert_empty_tree(self):
        """Test d'insertion dans un arbre vide."""
        new_root, inserted = self.operations.insert(None, 10)
        assert inserted is True
        assert new_root is not None
        assert new_root.value == 10

    def test_insert_existing_tree(self):
        """Test d'insertion dans un arbre existant."""
        new_root, inserted = self.operations.insert(self.root, 6)
        assert inserted is True
        assert new_root is self.root

        # Vérifier que le nouveau nœud a été ajouté
        result = self.operations.search(new_root, 6)
        assert result is not None
        assert result.value == 6

    def test_insert_invalid_root_type(self):
        """Test d'insertion avec un type de racine invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.insert("invalid", 1)

    def test_delete_existing_value(self):
        """Test de suppression d'une valeur existante."""
        new_root, deleted = self.operations.delete(self.root, 4)
        assert deleted is True
        assert new_root is self.root

        # Vérifier que la valeur a été supprimée
        result = self.operations.search(new_root, 4)
        assert result is None

    def test_delete_non_existing_value(self):
        """Test de suppression d'une valeur inexistante."""
        new_root, deleted = self.operations.delete(self.root, 6)
        assert deleted is False
        assert new_root is self.root

    def test_delete_root(self):
        """Test de suppression de la racine."""
        new_root, deleted = self.operations.delete(self.root, 1)
        assert deleted is True
        # La racine devrait être remplacée par son enfant droit
        assert new_root is self.right

    def test_delete_invalid_root_type(self):
        """Test de suppression avec un type de racine invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.delete("invalid", 1)

    def test_get_min_node(self):
        """Test de get_min_node."""
        min_node = self.operations.get_min_node(self.root)
        assert min_node is not None
        assert (
            min_node.value == 4
        )  # Dans notre arbre de test, 4 est le minimum (left_left)

    def test_get_max_node(self):
        """Test de get_max_node."""
        max_node = self.operations.get_max_node(self.root)
        assert max_node is not None
        assert max_node.value == 3  # Dans notre arbre de test, 3 est le maximum

    def test_get_min_max_invalid_root_type(self):
        """Test de get_min_node et get_max_node avec un type invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.get_min_node("invalid")

        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.get_max_node("invalid")

    def test_search_recursive(self):
        """Test de search_recursive."""
        result = self.operations.search_recursive(self.root, 1)
        assert result is not None
        assert result.value == 1

        result = self.operations.search_recursive(self.root, 5)
        assert result is not None
        assert result.value == 5

        result = self.operations.search_recursive(self.root, 6)
        assert result is None

        result = self.operations.search_recursive(None, 1)
        assert result is None

    def test_search_iterative(self):
        """Test de search_iterative."""
        result = self.operations.search_iterative(self.root, 1)
        assert result is not None
        assert result.value == 1

        result = self.operations.search_iterative(self.root, 3)
        assert result is not None
        assert result.value == 3

        result = self.operations.search_iterative(self.root, 6)
        assert result is None

        result = self.operations.search_iterative(None, 1)
        assert result is None

    def test_insert_recursive(self):
        """Test de insert_recursive."""
        new_root, inserted = self.operations.insert_recursive(None, 10)
        assert inserted is True
        assert new_root is not None
        assert new_root.value == 10

        new_root, inserted = self.operations.insert_recursive(self.root, 6)
        assert inserted is True
        assert new_root is self.root

    def test_insert_iterative(self):
        """Test de insert_iterative."""
        new_root, inserted = self.operations.insert_iterative(None, 10)
        assert inserted is True
        assert new_root is not None
        assert new_root.value == 10

        new_root, inserted = self.operations.insert_iterative(self.root, 6)
        assert inserted is True
        assert new_root is self.root

    def test_delete_recursive(self):
        """Test de delete_recursive."""
        new_root, deleted = self.operations.delete_recursive(None, 1)
        assert deleted is False
        assert new_root is None

        new_root, deleted = self.operations.delete_recursive(self.root, 4)
        assert deleted is True
        assert new_root is self.root

    def test_delete_iterative(self):
        """Test de delete_iterative."""
        new_root, deleted = self.operations.delete_iterative(None, 1)
        assert deleted is False
        assert new_root is None

        new_root, deleted = self.operations.delete_iterative(self.root, 5)
        assert deleted is True
        assert new_root is self.root

    def test_find_insertion_point(self):
        """Test de _find_insertion_point."""
        insertion_point = self.operations._find_insertion_point(self.root)
        assert insertion_point is not None
        # Le point d'insertion devrait être un nœud qui n'a pas d'enfant gauche

        # Créer un arbre où tous les nœuds ont des enfants
        full_root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)

        full_root.set_left(left)
        full_root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        insertion_point = self.operations._find_insertion_point(full_root)
        assert insertion_point is not None

    def test_delete_recursive_internal(self):
        """Test de _delete_recursive."""
        new_root, deleted = self.operations._delete_recursive(self.root, 4)
        assert deleted is True
        assert new_root is self.root

        new_root, deleted = self.operations._delete_recursive(self.root, 6)
        assert deleted is False
        assert new_root is self.root

    def test_inheritance_from_tree_operations(self):
        """Test que BinaryTreeOperations hérite bien de TreeOperations."""
        from src.tree_operations import TreeOperations

        assert issubclass(BinaryTreeOperations, TreeOperations)

        # Vérifier que les méthodes de TreeOperations sont disponibles
        assert hasattr(self.operations, "contains")
        assert hasattr(self.operations, "get_min")
        assert hasattr(self.operations, "get_max")
        assert hasattr(self.operations, "get_height")
        assert hasattr(self.operations, "get_size")
        assert hasattr(self.operations, "get_leaf_nodes")
        assert hasattr(self.operations, "get_internal_nodes")
        assert hasattr(self.operations, "get_depth")
        assert hasattr(self.operations, "is_balanced")
        assert hasattr(self.operations, "is_complete")
        assert hasattr(self.operations, "is_full")
