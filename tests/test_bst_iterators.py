"""
Tests unitaires pour les itérateurs BST.

Ce module contient tous les tests unitaires pour valider le bon fonctionnement
des itérateurs d'arbres binaires de recherche.
"""

from __future__ import annotations

import unittest
from typing import List

from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.binary.bst_iterators import (
    InorderIterator,
    LevelOrderIterator,
    PostorderIterator,
    PreorderIterator,
)


class TestBSTIterators(unittest.TestCase):
    """
    Classe de tests pour les itérateurs BST.
    """

    def create_test_tree(self) -> BinaryTreeNode[int]:
        """
        Crée un arbre de test pour les tests.

        :return: Arbre de test
        :rtype: BinaryTreeNode[int]
        """
        # Créer l'arbre suivant :
        #       50
        #      /  \
        #     30   70
        #    / \   / \
        #   20 40 60 80
        root = BinaryTreeNode(50)
        left = BinaryTreeNode(30)
        right = BinaryTreeNode(70)
        root.set_left(left)
        root.set_right(right)

        left_left = BinaryTreeNode(20)
        left_right = BinaryTreeNode(40)
        left.set_left(left_left)
        left.set_right(left_right)

        right_left = BinaryTreeNode(60)
        right_right = BinaryTreeNode(80)
        right.set_left(right_left)
        right.set_right(right_right)

        return root

    def test_preorder_iterator(self):
        """Test de l'itérateur préfixe."""
        root = self.create_test_tree()
        iterator = PreorderIterator(root)

        expected = [50, 30, 20, 40, 70, 60, 80]
        result = list(iterator)
        assert result == expected

        # Test de la longueur
        assert len(iterator) == len(expected)

    def test_inorder_iterator(self):
        """Test de l'itérateur infixe."""
        root = self.create_test_tree()
        iterator = InorderIterator(root)

        expected = [20, 30, 40, 50, 60, 70, 80]
        result = list(iterator)
        assert result == expected

        # Test de la longueur
        assert len(iterator) == len(expected)

    def test_postorder_iterator(self):
        """Test de l'itérateur postfixe."""
        root = self.create_test_tree()
        iterator = PostorderIterator(root)

        expected = [20, 40, 30, 60, 80, 70, 50]
        result = list(iterator)
        assert result == expected

        # Test de la longueur
        assert len(iterator) == len(expected)

    def test_level_order_iterator(self):
        """Test de l'itérateur par niveaux."""
        root = self.create_test_tree()
        iterator = LevelOrderIterator(root)

        expected = [50, 30, 70, 20, 40, 60, 80]
        result = list(iterator)
        assert result == expected

        # Test de la longueur
        assert len(iterator) == len(expected)

    def test_empty_tree_iterators(self):
        """Test des itérateurs sur un arbre vide."""
        # Test avec None
        for iterator_class in [
            PreorderIterator,
            InorderIterator,
            PostorderIterator,
            LevelOrderIterator,
        ]:
            iterator = iterator_class(None)
            assert list(iterator) == []
            assert len(iterator) == 0

    def test_single_node_iterators(self):
        """Test des itérateurs sur un arbre à un seul nœud."""
        root = BinaryTreeNode(42)

        # Test préfixe
        iterator = PreorderIterator(root)
        assert list(iterator) == [42]
        assert len(iterator) == 1

        # Test infixe
        iterator = InorderIterator(root)
        assert list(iterator) == [42]
        assert len(iterator) == 1

        # Test postfixe
        iterator = PostorderIterator(root)
        assert list(iterator) == [42]
        assert len(iterator) == 1

        # Test par niveaux
        iterator = LevelOrderIterator(root)
        assert list(iterator) == [42]
        assert len(iterator) == 1

    def test_left_skewed_tree(self):
        """Test des itérateurs sur un arbre penché à gauche."""
        # Créer un arbre penché à gauche : 1 -> 2 -> 3 -> 4
        root = BinaryTreeNode(1)
        node2 = BinaryTreeNode(2)
        root.set_left(node2)
        node3 = BinaryTreeNode(3)
        node2.set_left(node3)
        node4 = BinaryTreeNode(4)
        node3.set_left(node4)

        # Test préfixe
        iterator = PreorderIterator(root)
        assert list(iterator) == [1, 2, 3, 4]

        # Test infixe
        iterator = InorderIterator(root)
        assert list(iterator) == [4, 3, 2, 1]

        # Test postfixe
        iterator = PostorderIterator(root)
        assert list(iterator) == [4, 3, 2, 1]

        # Test par niveaux
        iterator = LevelOrderIterator(root)
        assert list(iterator) == [1, 2, 3, 4]

    def test_right_skewed_tree(self):
        """Test des itérateurs sur un arbre penché à droite."""
        # Créer un arbre penché à droite : 1 -> 2 -> 3 -> 4
        root = BinaryTreeNode(1)
        node2 = BinaryTreeNode(2)
        root.set_right(node2)
        node3 = BinaryTreeNode(3)
        node2.set_right(node3)
        node4 = BinaryTreeNode(4)
        node3.set_right(node4)

        # Test préfixe
        iterator = PreorderIterator(root)
        assert list(iterator) == [1, 2, 3, 4]

        # Test infixe
        iterator = InorderIterator(root)
        assert list(iterator) == [1, 2, 3, 4]

        # Test postfixe
        iterator = PostorderIterator(root)
        assert list(iterator) == [4, 3, 2, 1]

        # Test par niveaux
        iterator = LevelOrderIterator(root)
        assert list(iterator) == [1, 2, 3, 4]

    def test_iterator_consumption(self):
        """Test de la consommation des itérateurs."""
        root = self.create_test_tree()
        iterator = InorderIterator(root)

        # Consommer partiellement l'itérateur
        first_value = next(iterator)
        assert first_value == 20

        # Vérifier que l'itérateur continue correctement
        remaining_values = list(iterator)
        assert remaining_values == [30, 40, 50, 60, 70, 80]

    def test_iterator_exhaustion(self):
        """Test de l'épuisement des itérateurs."""
        root = BinaryTreeNode(42)
        iterator = InorderIterator(root)

        # Consommer l'itérateur
        value = next(iterator)
        assert value == 42

        # Vérifier que l'itérateur est épuisé
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_iterator_reuse(self):
        """Test de la réutilisation des itérateurs."""
        root = self.create_test_tree()

        # Créer deux itérateurs identiques
        iterator1 = InorderIterator(root)
        iterator2 = InorderIterator(root)

        # Vérifier qu'ils produisent les mêmes résultats
        values1 = list(iterator1)
        values2 = list(iterator2)
        assert values1 == values2

    def test_complex_tree_iterators(self):
        """Test des itérateurs sur un arbre complexe."""
        # Créer un arbre plus complexe
        #        100
        #       /   \
        #      50    150
        #     / \    /  \
        #    25  75 125 175
        #   /  \    \    \
        #  10  30   90   200
        root = BinaryTreeNode(100)

        # Sous-arbre gauche
        left = BinaryTreeNode(50)
        root.set_left(left)

        left_left = BinaryTreeNode(25)
        left_right = BinaryTreeNode(75)
        left.set_left(left_left)
        left.set_right(left_right)

        left_left_left = BinaryTreeNode(10)
        left_left_right = BinaryTreeNode(30)
        left_left.set_left(left_left_left)
        left_left.set_right(left_left_right)

        left_right_right = BinaryTreeNode(90)
        left_right.set_right(left_right_right)

        # Sous-arbre droit
        right = BinaryTreeNode(150)
        root.set_right(right)

        right_left = BinaryTreeNode(125)
        right_right = BinaryTreeNode(175)
        right.set_left(right_left)
        right.set_right(right_right)

        right_right_right = BinaryTreeNode(200)
        right_right.set_right(right_right_right)

        # Test des itérateurs
        preorder_expected = [100, 50, 25, 10, 30, 75, 90, 150, 125, 175, 200]
        inorder_expected = [10, 25, 30, 50, 75, 90, 100, 125, 150, 175, 200]
        postorder_expected = [10, 30, 25, 90, 75, 50, 125, 200, 175, 150, 100]
        level_order_expected = [100, 50, 150, 25, 75, 125, 175, 10, 30, 90, 200]

        assert list(PreorderIterator(root)) == preorder_expected
        assert list(InorderIterator(root)) == inorder_expected
        assert list(PostorderIterator(root)) == postorder_expected
        assert list(LevelOrderIterator(root)) == level_order_expected
