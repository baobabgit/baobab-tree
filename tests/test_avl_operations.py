"""
Tests unitaires pour la classe AVLOperations.

Ce module contient les tests unitaires pour la classe AVLOperations
et ses méthodes spécialisées pour les arbres AVL.
"""

import pytest
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.balanced.avl_operations import AVLOperations


class TestAVLOperations:
    """Tests pour la classe AVLOperations."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.operations = AVLOperations[int]()

        # Créer un AVL de test (équilibré)
        self.root = BinaryTreeNode(4)
        self.left = BinaryTreeNode(2)
        self.right = BinaryTreeNode(6)
        self.left_left = BinaryTreeNode(1)
        self.left_right = BinaryTreeNode(3)
        self.right_left = BinaryTreeNode(5)
        self.right_right = BinaryTreeNode(7)

        self.root.set_left(self.left)
        self.root.set_right(self.right)
        self.left.set_left(self.left_left)
        self.left.set_right(self.left_right)
        self.right.set_left(self.right_left)
        self.right.set_right(self.right_right)

    def test_insert_empty_tree(self):
        """Test d'insertion dans un arbre vide."""
        new_root, inserted = self.operations.insert(None, 10)
        assert inserted is True
        assert new_root is not None
        assert new_root.value == 10

    def test_insert_new_value(self):
        """Test d'insertion d'une nouvelle valeur."""
        new_root, inserted = self.operations.insert(self.root, 8)
        assert inserted is True
        assert new_root is self.root

        # Vérifier que le nouveau nœud a été ajouté
        result = self.operations.search(new_root, 8)
        assert result is not None
        assert result.value == 8

    def test_insert_duplicate_value(self):
        """Test d'insertion d'une valeur dupliquée."""
        new_root, inserted = self.operations.insert(self.root, 4)
        assert inserted is False
        assert new_root is self.root

    def test_insert_with_rotation(self):
        """Test d'insertion nécessitant une rotation."""
        # Créer un arbre qui nécessitera une rotation
        unbalanced_root = BinaryTreeNode(3)
        left = BinaryTreeNode(2)
        left_left = BinaryTreeNode(1)

        unbalanced_root.set_left(left)
        left.set_left(left_left)

        # Insérer une valeur qui nécessitera une rotation
        new_root, inserted = self.operations.insert(unbalanced_root, 0)
        assert inserted is True

        # Vérifier que l'arbre est équilibré
        assert self.operations.is_avl_tree(new_root) is True

    def test_delete_existing_value(self):
        """Test de suppression d'une valeur existante."""
        new_root, deleted = self.operations.delete(self.root, 1)
        assert deleted is True
        assert new_root is self.root

        # Vérifier que la valeur a été supprimée
        result = self.operations.search(new_root, 1)
        assert result is None

    def test_delete_non_existing_value(self):
        """Test de suppression d'une valeur inexistante."""
        new_root, deleted = self.operations.delete(self.root, 8)
        assert deleted is False
        assert new_root is self.root

    def test_delete_with_rotation(self):
        """Test de suppression nécessitant une rotation."""
        # Créer un arbre qui nécessitera une rotation après suppression
        unbalanced_root = BinaryTreeNode(3)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(4)
        right_right = BinaryTreeNode(5)

        unbalanced_root.set_left(left)
        unbalanced_root.set_right(right)
        right.set_right(right_right)

        # Supprimer une valeur qui nécessitera une rotation
        new_root, deleted = self.operations.delete(unbalanced_root, 2)
        assert deleted is True

        # Vérifier que l'arbre est équilibré
        assert self.operations.is_avl_tree(new_root) is True

    def test_rotate_left(self):
        """Test de rotation à gauche."""
        # Créer un arbre nécessitant une rotation à gauche
        root = BinaryTreeNode(2)
        right = BinaryTreeNode(3)
        right_right = BinaryTreeNode(4)

        root.set_right(right)
        right.set_right(right_right)

        # Effectuer la rotation
        new_root = self.operations._rotate_left(root)

        # Vérifier la structure après rotation
        assert new_root.value == 3
        assert new_root.left.value == 2
        assert new_root.right.value == 4

    def test_rotate_right(self):
        """Test de rotation à droite."""
        # Créer un arbre nécessitant une rotation à droite
        root = BinaryTreeNode(3)
        left = BinaryTreeNode(2)
        left_left = BinaryTreeNode(1)

        root.set_left(left)
        left.set_left(left_left)

        # Effectuer la rotation
        new_root = self.operations._rotate_right(root)

        # Vérifier la structure après rotation
        assert new_root.value == 2
        assert new_root.left.value == 1
        assert new_root.right.value == 3

    def test_balance_node(self):
        """Test d'équilibrage d'un nœud."""
        # Créer un nœud déséquilibré
        unbalanced_node = BinaryTreeNode(3)
        left = BinaryTreeNode(2)
        left_left = BinaryTreeNode(1)

        unbalanced_node.set_left(left)
        left.set_left(left_left)

        # Équilibrer le nœud
        balanced_node = self.operations._balance_node(unbalanced_node)

        # Vérifier que le nœud est équilibré
        balance_factor = self.operations.get_balance_factor(balanced_node)
        assert abs(balance_factor) <= 1

    def test_get_balance_factor(self):
        """Test de get_balance_factor."""
        balance_factor = self.operations.get_balance_factor(self.root)
        assert balance_factor == 0  # Arbre équilibré

        balance_factor = self.operations.get_balance_factor(self.left)
        assert balance_factor == 0  # Arbre équilibré

    def test_is_avl_tree(self):
        """Test de is_avl_tree."""
        assert self.operations.is_avl_tree(self.root) is True
        assert self.operations.is_avl_tree(self.left) is True
        assert self.operations.is_avl_tree(self.left_left) is True
        assert self.operations.is_avl_tree(None) is True

    def test_is_avl_tree_invalid_bst(self):
        """Test de is_avl_tree avec un BST invalide."""
        # Créer un arbre qui viole les propriétés BST
        invalid_root = BinaryTreeNode(4)
        invalid_left = BinaryTreeNode(6)  # Plus grand que la racine
        invalid_right = BinaryTreeNode(2)  # Plus petit que la racine

        invalid_root.set_left(invalid_left)
        invalid_root.set_right(invalid_right)

        assert self.operations.is_avl_tree(invalid_root) is False

    def test_is_avl_tree_unbalanced(self):
        """Test de is_avl_tree avec un arbre déséquilibré."""
        # Créer un arbre déséquilibré
        unbalanced_root = BinaryTreeNode(1)
        left = BinaryTreeNode(2)
        left_left = BinaryTreeNode(3)
        left_left_left = BinaryTreeNode(4)

        unbalanced_root.set_left(left)
        left.set_left(left_left)
        left_left.set_left(left_left_left)

        assert self.operations.is_avl_tree(unbalanced_root) is False

    def test_insert_with_avl_validation(self):
        """Test de insert_with_avl_validation."""
        new_root, inserted = self.operations.insert_with_avl_validation(self.root, 8)
        assert inserted is True
        assert new_root is self.root

        # Vérifier que l'arbre reste un AVL valide
        assert self.operations.is_avl_tree(new_root) is True

    def test_get_avl_height(self):
        """Test de get_avl_height."""
        height = self.operations.get_avl_height(self.root)
        assert height == 2

        height_empty = self.operations.get_avl_height(None)
        assert height_empty == -1

    def test_get_min_avl_height(self):
        """Test de get_min_avl_height."""
        height = self.operations.get_min_avl_height(7)
        assert height == 2  # Pour 7 nœuds, hauteur minimale = 2

        height = self.operations.get_min_avl_height(1)
        assert height == 0  # Pour 1 nœud, hauteur minimale = 0

        height = self.operations.get_min_avl_height(0)
        assert height == -1  # Pour 0 nœud, hauteur = -1

    def test_get_max_avl_height(self):
        """Test de get_max_avl_height."""
        height = self.operations.get_max_avl_height(7)
        assert height >= 2  # Pour 7 nœuds, hauteur maximale >= 2

        height = self.operations.get_max_avl_height(1)
        assert height >= 0  # Pour 1 nœud, hauteur maximale >= 0

        height = self.operations.get_max_avl_height(0)
        assert height == -1  # Pour 0 nœud, hauteur = -1

    def test_balance_tree(self):
        """Test de balance_tree."""
        # Créer un BST déséquilibré
        unbalanced_bst = BinaryTreeNode(1)
        right = BinaryTreeNode(2)
        right_right = BinaryTreeNode(3)
        right_right_right = BinaryTreeNode(4)

        unbalanced_bst.set_right(right)
        right.set_right(right_right)
        right_right.set_right(right_right_right)

        # Équilibrer l'arbre
        balanced_tree = self.operations.balance_tree(unbalanced_bst)

        # Vérifier que l'arbre est équilibré
        assert self.operations.is_avl_tree(balanced_tree) is True

    def test_collect_nodes_inorder(self):
        """Test de _collect_nodes_inorder."""
        nodes = []
        self.operations._collect_nodes_inorder(self.root, nodes)

        # Vérifier que tous les nœuds ont été collectés
        assert len(nodes) == 7
        assert nodes == [1, 2, 3, 4, 5, 6, 7]

    def test_build_balanced_avl(self):
        """Test de _build_balanced_avl."""
        values = [1, 2, 3, 4, 5, 6, 7]
        balanced_tree = self.operations._build_balanced_avl(values, 0, len(values) - 1)

        # Vérifier que l'arbre est équilibré
        assert self.operations.is_avl_tree(balanced_tree) is True

        # Vérifier que toutes les valeurs sont présentes
        collected_values = []
        self.operations._collect_nodes_inorder(balanced_tree, collected_values)
        assert collected_values == values

    def test_inheritance_from_bst_operations(self):
        """Test que AVLOperations hérite bien de BSTOperations."""
        from src.baobab_tree.binary.bst_operations import BSTOperations

        assert issubclass(AVLOperations, BSTOperations)

        # Vérifier que les méthodes de BSTOperations sont disponibles
        assert hasattr(self.operations, "search_recursive")
        assert hasattr(self.operations, "search_iterative")
        assert hasattr(self.operations, "insert_recursive")
        assert hasattr(self.operations, "insert_iterative")
        assert hasattr(self.operations, "delete_recursive")
        assert hasattr(self.operations, "delete_iterative")
        assert hasattr(self.operations, "is_valid_bst")
        assert hasattr(self.operations, "get_balance_factor")

    def test_custom_comparator(self):
        """Test avec un comparateur personnalisé."""

        def reverse_comparator(a, b):
            if a > b:
                return -1
            elif a == b:
                return 0
            else:
                return 1

        operations = AVLOperations(reverse_comparator)

        # Test avec le comparateur inversé
        assert operations._comparator(1, 2) == 1
        assert operations._comparator(2, 2) == 0
        assert operations._comparator(3, 2) == -1
