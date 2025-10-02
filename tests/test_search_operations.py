"""
Tests unitaires pour la classe SearchOperations.

Ce module contient les tests unitaires pour la classe SearchOperations
et ses méthodes de recherche avancées.
"""

import pytest
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.binary.search_operations import SearchOperations


class TestSearchOperations:
    """Tests pour la classe SearchOperations."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.operations = SearchOperations[int]()

        # Créer un BST de test
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

    def test_default_comparator(self):
        """Test du comparateur par défaut."""
        comparator = self.operations._default_comparator

        assert comparator(1, 2) == -1
        assert comparator(2, 2) == 0
        assert comparator(3, 2) == 1

    def test_find_successor(self):
        """Test de find_successor."""
        # Successeur de 1 (feuille gauche)
        successor = self.operations.find_successor(self.left_left)
        assert successor is not None
        assert successor.value == 2

        # Successeur de 2 (nœud interne)
        successor = self.operations.find_successor(self.left)
        assert successor is not None
        assert successor.value == 3

        # Successeur de 4 (racine)
        successor = self.operations.find_successor(self.root)
        assert successor is not None
        assert successor.value == 5

        # Successeur de 7 (feuille droite, pas de successeur)
        successor = self.operations.find_successor(self.right_right)
        assert successor is None

    def test_find_predecessor(self):
        """Test de find_predecessor."""
        # Prédécesseur de 7 (feuille droite)
        predecessor = self.operations.find_predecessor(self.right_right)
        assert predecessor is not None
        assert predecessor.value == 6

        # Prédécesseur de 6 (nœud interne)
        predecessor = self.operations.find_predecessor(self.right)
        assert predecessor is not None
        assert predecessor.value == 5

        # Prédécesseur de 4 (racine)
        predecessor = self.operations.find_predecessor(self.root)
        assert predecessor is not None
        assert predecessor.value == 3

        # Prédécesseur de 1 (feuille gauche, pas de prédécesseur)
        predecessor = self.operations.find_predecessor(self.left_left)
        assert predecessor is None

    def test_find_floor(self):
        """Test de find_floor."""
        # Floor de 4 (valeur existante)
        floor = self.operations.find_floor(self.root, 4)
        assert floor == 4

        # Floor de 3.5 (entre 3 et 4)
        floor = self.operations.find_floor(self.root, 3.5)
        assert floor == 3

        # Floor de 0.5 (plus petit que le minimum)
        floor = self.operations.find_floor(self.root, 0.5)
        assert floor is None

        # Floor de 8 (plus grand que le maximum)
        floor = self.operations.find_floor(self.root, 8)
        assert floor == 7

        # Floor dans un arbre vide
        floor = self.operations.find_floor(None, 5)
        assert floor is None

    def test_find_ceiling(self):
        """Test de find_ceiling."""
        # Ceiling de 4 (valeur existante)
        ceiling = self.operations.find_ceiling(self.root, 4)
        assert ceiling == 4

        # Ceiling de 3.5 (entre 3 et 4)
        ceiling = self.operations.find_ceiling(self.root, 3.5)
        assert ceiling == 4

        # Ceiling de 0.5 (plus petit que le minimum)
        ceiling = self.operations.find_ceiling(self.root, 0.5)
        assert ceiling == 1

        # Ceiling de 8 (plus grand que le maximum)
        ceiling = self.operations.find_ceiling(self.root, 8)
        assert ceiling is None

        # Ceiling dans un arbre vide
        ceiling = self.operations.find_ceiling(None, 5)
        assert ceiling is None

    def test_range_search(self):
        """Test de range_search."""
        # Plage complète
        result = self.operations.range_search(self.root, 1, 7)
        assert len(result) == 7
        assert set(result) == {1, 2, 3, 4, 5, 6, 7}

        # Plage partielle
        result = self.operations.range_search(self.root, 2, 5)
        assert len(result) == 4
        assert set(result) == {2, 3, 4, 5}

        # Plage d'une seule valeur
        result = self.operations.range_search(self.root, 4, 4)
        assert len(result) == 1
        assert result[0] == 4

        # Plage vide
        result = self.operations.range_search(self.root, 8, 10)
        assert len(result) == 0

        # Plage invalide (min > max)
        result = self.operations.range_search(self.root, 5, 3)
        assert len(result) == 0

        # Plage dans un arbre vide
        result = self.operations.range_search(None, 1, 5)
        assert len(result) == 0

    def test_count_range(self):
        """Test de count_range."""
        # Compter dans la plage complète
        count = self.operations.count_range(self.root, 1, 7)
        assert count == 7

        # Compter dans une plage partielle
        count = self.operations.count_range(self.root, 2, 5)
        assert count == 4

        # Compter une seule valeur
        count = self.operations.count_range(self.root, 4, 4)
        assert count == 1

        # Compter dans une plage vide
        count = self.operations.count_range(self.root, 8, 10)
        assert count == 0

        # Compter dans une plage invalide
        count = self.operations.count_range(self.root, 5, 3)
        assert count == 0

        # Compter dans un arbre vide
        count = self.operations.count_range(None, 1, 5)
        assert count == 0

    def test_find_kth_smallest(self):
        """Test de find_kth_smallest."""
        # 1er plus petit
        result = self.operations.find_kth_smallest(self.root, 1)
        assert result == 1

        # 3ème plus petit
        result = self.operations.find_kth_smallest(self.root, 3)
        assert result == 3

        # 7ème plus petit (dernier)
        result = self.operations.find_kth_smallest(self.root, 7)
        assert result == 7

        # k invalide (trop grand)
        result = self.operations.find_kth_smallest(self.root, 8)
        assert result is None

        # k invalide (négatif)
        result = self.operations.find_kth_smallest(self.root, 0)
        assert result is None

        # Dans un arbre vide
        result = self.operations.find_kth_smallest(None, 1)
        assert result is None

    def test_find_kth_largest(self):
        """Test de find_kth_largest."""
        # 1er plus grand
        result = self.operations.find_kth_largest(self.root, 1)
        assert result == 7

        # 3ème plus grand
        result = self.operations.find_kth_largest(self.root, 3)
        assert result == 5

        # 7ème plus grand (dernier)
        result = self.operations.find_kth_largest(self.root, 7)
        assert result == 1

        # k invalide (trop grand)
        result = self.operations.find_kth_largest(self.root, 8)
        assert result is None

        # k invalide (négatif)
        result = self.operations.find_kth_largest(self.root, 0)
        assert result is None

        # Dans un arbre vide
        result = self.operations.find_kth_largest(None, 1)
        assert result is None

    def test_find_closest_value(self):
        """Test de find_closest_value."""
        # Valeur existante
        result = self.operations.find_closest_value(self.root, 4)
        assert result == 4

        # Valeur proche
        result = self.operations.find_closest_value(self.root, 3.5)
        assert result == 4  # Plus proche de 4 que de 3

        result = self.operations.find_closest_value(self.root, 2.5)
        assert result in [2, 3, 4]  # Plus proche de 2, 3 ou 4

        # Valeur très petite
        result = self.operations.find_closest_value(self.root, 0)
        assert result in [1, 4]  # Plus proche de 1 ou 4

        # Valeur très grande
        result = self.operations.find_closest_value(self.root, 10)
        assert result in [7, 4]  # Plus proche de 7 ou 4

        # Dans un arbre vide
        result = self.operations.find_closest_value(None, 5)
        assert result is None

    def test_find_all_values(self):
        """Test de find_all_values."""
        # Créer un BST avec des doublons
        root_with_duplicates = BinaryTreeNode(4)
        left = BinaryTreeNode(2)
        right = BinaryTreeNode(6)
        left_left = BinaryTreeNode(2)  # Doublon
        left_right = BinaryTreeNode(3)
        right_left = BinaryTreeNode(5)
        right_right = BinaryTreeNode(6)  # Doublon

        root_with_duplicates.set_left(left)
        root_with_duplicates.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)
        right.set_left(right_left)
        right.set_right(right_right)

        # Trouver tous les nœuds avec la valeur 2
        result = self.operations.find_all_values(root_with_duplicates, 2)
        assert len(result) == 2
        assert all(node.value == 2 for node in result)

        # Trouver tous les nœuds avec la valeur 6
        result = self.operations.find_all_values(root_with_duplicates, 6)
        assert len(result) == 2
        assert all(node.value == 6 for node in result)

        # Trouver une valeur unique
        result = self.operations.find_all_values(root_with_duplicates, 3)
        assert len(result) == 1
        assert result[0].value == 3

        # Trouver une valeur inexistante
        result = self.operations.find_all_values(root_with_duplicates, 8)
        assert len(result) == 0

        # Dans un arbre vide
        result = self.operations.find_all_values(None, 5)
        assert len(result) == 0

    def test_custom_comparator(self):
        """Test avec un comparateur personnalisé."""

        def reverse_comparator(a, b):
            if a > b:
                return -1
            elif a == b:
                return 0
            else:
                return 1

        operations = SearchOperations(reverse_comparator)

        # Test avec le comparateur inversé
        assert operations._comparator(1, 2) == 1
        assert operations._comparator(2, 2) == 0
        assert operations._comparator(3, 2) == -1
