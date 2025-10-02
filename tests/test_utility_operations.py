"""
Tests unitaires pour la classe UtilityOperations.

Ce module contient les tests unitaires pour la classe UtilityOperations
et ses méthodes utilitaires.
"""

import pytest
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.utility_operations import UtilityOperations


class TestUtilityOperations:
    """Tests pour la classe UtilityOperations."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.operations = UtilityOperations()

        # Créer un arbre de test
        self.root = BinaryTreeNode(1)
        self.left = BinaryTreeNode(2)
        self.right = BinaryTreeNode(3)
        self.left_left = BinaryTreeNode(4)
        self.left_right = BinaryTreeNode(5)

        self.root.set_left(self.left)
        self.root.set_right(self.right)
        self.left.set_left(self.left_left)
        self.left.set_right(self.left_right)

    def test_get_height(self):
        """Test de get_height."""
        assert self.operations.get_height(self.root) == 2
        assert self.operations.get_height(self.left) == 1
        assert self.operations.get_height(self.left_left) == 0
        assert self.operations.get_height(None) == -1

    def test_get_depth(self):
        """Test de get_depth."""
        assert self.operations.get_depth(self.root) == 0
        assert self.operations.get_depth(self.left) == 1
        assert self.operations.get_depth(self.right) == 1
        assert self.operations.get_depth(self.left_left) == 2
        assert self.operations.get_depth(self.left_right) == 2

    def test_get_size(self):
        """Test de get_size."""
        assert self.operations.get_size(self.root) == 5
        assert self.operations.get_size(self.left) == 3
        assert self.operations.get_size(self.left_left) == 1
        assert self.operations.get_size(None) == 0

    def test_get_balance_factor(self):
        """Test de get_balance_factor."""
        balance_factor = self.operations.get_balance_factor(self.root)
        assert balance_factor == -1  # Arbre déséquilibré (pas d'enfant droit)

        balance_factor = self.operations.get_balance_factor(self.left)
        assert balance_factor == 0  # Arbre équilibré

    def test_is_balanced(self):
        """Test de is_balanced."""
        assert self.operations.is_balanced(self.root) is True  # Arbre équilibré
        assert self.operations.is_balanced(self.left) is True
        assert self.operations.is_balanced(self.left_left) is True
        assert self.operations.is_balanced(None) is True

    def test_is_balanced_unbalanced(self):
        """Test de is_balanced avec un arbre déséquilibré."""
        # Créer un arbre déséquilibré
        unbalanced_root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        left_left = BinaryTreeNode(3)
        left_left_left = BinaryTreeNode(4)

        unbalanced_root.set_left(left)
        left.set_left(left_left)
        left_left.set_left(left_left_left)

        assert self.operations.is_balanced(unbalanced_root) is False

    def test_is_complete(self):
        """Test de is_complete."""
        assert self.operations.is_complete(self.root) is True
        assert self.operations.is_complete(self.left) is True
        assert self.operations.is_complete(self.left_left) is True
        assert self.operations.is_complete(None) is True

    def test_is_complete_incomplete(self):
        """Test de is_complete avec un arbre incomplet."""
        # Créer un arbre incomplet
        incomplete_root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)
        right_left = BinaryTreeNode(6)
        # Pas de right_right, ce qui rend l'arbre incomplet

        incomplete_root.set_left(left)
        incomplete_root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)
        right.set_left(right_left)

        # Cet arbre devrait être complet car il respecte la propriété
        assert self.operations.is_complete(incomplete_root) is True

    def test_is_full(self):
        """Test de is_full."""
        assert self.operations.is_full(self.root) is True
        assert self.operations.is_full(self.left) is True
        assert self.operations.is_full(self.left_left) is True
        assert self.operations.is_full(None) is True

    def test_is_perfect(self):
        """Test de is_perfect."""
        # Créer un arbre parfait
        perfect_root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        left_left = BinaryTreeNode(4)
        left_right = BinaryTreeNode(5)
        right_left = BinaryTreeNode(6)
        right_right = BinaryTreeNode(7)

        perfect_root.set_left(left)
        perfect_root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)
        right.set_left(right_left)
        right.set_right(right_right)

        assert self.operations.is_perfect(perfect_root) is True
        assert self.operations.is_perfect(self.root) is False
        assert self.operations.is_perfect(None) is True

    def test_get_leaf_nodes(self):
        """Test de get_leaf_nodes."""
        leaves = self.operations.get_leaf_nodes(self.root)
        assert len(leaves) == 3
        assert self.right in leaves
        assert self.left_left in leaves
        assert self.left_right in leaves

        leaves_empty = self.operations.get_leaf_nodes(None)
        assert leaves_empty == []

    def test_get_internal_nodes(self):
        """Test de get_internal_nodes."""
        internal = self.operations.get_internal_nodes(self.root)
        assert len(internal) == 2
        assert self.root in internal
        assert self.left in internal

        internal_empty = self.operations.get_internal_nodes(None)
        assert internal_empty == []

        internal_leaf = self.operations.get_internal_nodes(self.left_left)
        assert internal_leaf == []

    def test_get_nodes_at_level(self):
        """Test de get_nodes_at_level."""
        # Niveau 0 (racine)
        nodes = self.operations.get_nodes_at_level(self.root, 0)
        assert len(nodes) == 1
        assert self.root in nodes

        # Niveau 1
        nodes = self.operations.get_nodes_at_level(self.root, 1)
        assert len(nodes) == 2
        assert self.left in nodes
        assert self.right in nodes

        # Niveau 2
        nodes = self.operations.get_nodes_at_level(self.root, 2)
        assert len(nodes) == 2
        assert self.left_left in nodes
        assert self.left_right in nodes

        # Niveau inexistant
        nodes = self.operations.get_nodes_at_level(self.root, 3)
        assert len(nodes) == 0

        # Arbre vide
        nodes = self.operations.get_nodes_at_level(None, 0)
        assert len(nodes) == 0

    def test_get_width(self):
        """Test de get_width."""
        width = self.operations.get_width(self.root)
        assert width == 2  # Largeur maximale au niveau 1

        width_empty = self.operations.get_width(None)
        assert width_empty == 0

    def test_get_diameter(self):
        """Test de get_diameter."""
        diameter = self.operations.get_diameter(self.root)
        assert diameter == 3  # Chemin de 4 -> 2 -> 1 -> 3

        diameter_empty = self.operations.get_diameter(None)
        assert diameter_empty == 0

        diameter_single = self.operations.get_diameter(self.left_left)
        assert diameter_single == 0

    def test_count_nodes_with_value(self):
        """Test de count_nodes_with_value."""
        count = self.operations.count_nodes_with_value(self.root, 1)
        assert count == 1

        count = self.operations.count_nodes_with_value(self.root, 2)
        assert count == 1

        count = self.operations.count_nodes_with_value(self.root, 6)
        assert count == 0

        count_empty = self.operations.count_nodes_with_value(None, 1)
        assert count_empty == 0

    def test_get_path_to_node(self):
        """Test de get_path_to_node."""
        # Chemin vers la racine
        path = self.operations.get_path_to_node(self.root, self.root)
        assert len(path) == 1
        assert path[0] is self.root

        # Chemin vers un nœud interne
        path = self.operations.get_path_to_node(self.root, self.left)
        assert len(path) == 2
        assert path[0] is self.root
        assert path[1] is self.left

        # Chemin vers une feuille
        path = self.operations.get_path_to_node(self.root, self.left_left)
        assert len(path) == 3
        assert path[0] is self.root
        assert path[1] is self.left
        assert path[2] is self.left_left

        # Nœud non trouvé
        other_node = BinaryTreeNode(10)
        path = self.operations.get_path_to_node(self.root, other_node)
        assert len(path) == 0

        # Arbre vide
        path = self.operations.get_path_to_node(None, self.root)
        assert len(path) == 0

    def test_get_common_ancestor(self):
        """Test de get_common_ancestor."""
        # Ancêtre commun de deux feuilles
        ancestor = self.operations.get_common_ancestor(
            self.root, self.left_left, self.left_right
        )
        assert ancestor is self.left

        # Ancêtre commun de la racine et d'une feuille
        ancestor = self.operations.get_common_ancestor(
            self.root, self.root, self.left_left
        )
        assert ancestor is self.root

        # Ancêtre commun de deux nœuds du même niveau
        ancestor = self.operations.get_common_ancestor(self.root, self.left, self.right)
        assert ancestor is self.root

        # Nœuds non trouvés
        other_node = BinaryTreeNode(10)
        ancestor = self.operations.get_common_ancestor(
            self.root, other_node, self.left_left
        )
        assert ancestor is None

        # Arbre vide
        ancestor = self.operations.get_common_ancestor(
            None, self.left_left, self.left_right
        )
        assert ancestor is None

    def test_is_subtree(self):
        """Test de is_subtree."""
        # Sous-arbre valide
        assert self.operations.is_subtree(self.root, self.left) is True
        assert self.operations.is_subtree(self.root, self.left_left) is True

        # Sous-arbre invalide
        other_tree = BinaryTreeNode(10)
        assert self.operations.is_subtree(self.root, other_tree) is False

        # Arbre vide comme sous-arbre
        assert self.operations.is_subtree(self.root, None) is True

        # Arbre vide comme arbre principal
        assert self.operations.is_subtree(None, self.left) is False

        # Deux arbres vides
        assert self.operations.is_subtree(None, None) is True

    def test_are_trees_identical(self):
        """Test de _are_trees_identical."""
        # Arbres identiques
        assert self.operations._are_trees_identical(self.root, self.root) is True
        assert self.operations._are_trees_identical(self.left, self.left) is True

        # Arbres différents
        other_tree = BinaryTreeNode(10)
        assert self.operations._are_trees_identical(self.root, other_tree) is False

        # Arbres vides
        assert self.operations._are_trees_identical(None, None) is True

        # Un arbre vide et un non vide
        assert self.operations._are_trees_identical(None, self.root) is False
        assert self.operations._are_trees_identical(self.root, None) is False
