"""
Tests unitaires pour la classe BinarySearchTree.

Ce module contient tous les tests unitaires pour valider le bon fonctionnement
de la classe BinarySearchTree et de ses méthodes.
"""

import unittest
from typing import List

from src.baobab_tree.binary.binary_search_tree import BinarySearchTree
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.exceptions import (
    BSTError,
    DuplicateValueError,
    ValueNotFoundError,
    InvalidOperationError,
)


class TestBinarySearchTree(unittest.TestCase):
    """
    Classe de tests pour BinarySearchTree.
    """

    def test_init_empty(self):
        """Test de l'initialisation d'un BST vide."""
        bst = BinarySearchTree()
        self.assertIsNone(bst.root)
        self.assertEqual(bst.size, 0)
        self.assertTrue(bst.is_empty())
        self.assertEqual(bst.get_height(), -1)

    def test_init_with_comparator(self):
        """Test de l'initialisation avec un comparateur personnalisé."""

        def reverse_comparator(a: int, b: int) -> int:
            if a > b:
                return -1
            elif a == b:
                return 0
            else:
                return 1

        bst = BinarySearchTree(reverse_comparator)
        self.assertEqual(bst.comparator, reverse_comparator)

    def test_insert_single(self):
        """Test de l'insertion d'un seul élément."""
        bst = BinarySearchTree()
        self.assertTrue(bst.insert(5))
        self.assertEqual(bst.size, 1)
        self.assertFalse(bst.is_empty())
        self.assertIsNotNone(bst.root)
        self.assertEqual(bst.root.value, 5)
        self.assertEqual(bst.get_height(), 0)

    def test_insert_multiple(self):
        """Test de l'insertion de plusieurs éléments."""
        bst = BinarySearchTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            self.assertTrue(bst.insert(value))

        self.assertEqual(bst.size, len(values))
        self.assertEqual(bst.get_height(), 2)

    def test_insert_duplicate(self):
        """Test de l'insertion d'une valeur dupliquée."""
        bst = BinarySearchTree()
        bst.insert(5)
        self.assertFalse(bst.insert(5))  # Doit retourner False

    def test_search_existing(self):
        """Test de la recherche d'une valeur existante."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        result = bst.search(30)
        self.assertIsNotNone(result)
        self.assertEqual(result.value, 30)

    def test_search_non_existing(self):
        """Test de la recherche d'une valeur inexistante."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        result = bst.search(25)
        self.assertIsNone(result)

    def test_contains(self):
        """Test de la méthode contains."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        self.assertTrue(bst.contains(50))
        self.assertTrue(bst.contains(30))
        self.assertTrue(bst.contains(70))
        self.assertFalse(bst.contains(25))

    def test_delete_leaf(self):
        """Test de la suppression d'une feuille."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)

        self.assertTrue(bst.delete(20))
        self.assertEqual(bst.size, 3)
        self.assertFalse(bst.contains(20))

    def test_delete_single_child(self):
        """Test de la suppression d'un nœud avec un seul enfant."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)

        self.assertTrue(bst.delete(30))
        self.assertEqual(bst.size, 4)
        self.assertFalse(bst.contains(30))
        self.assertTrue(bst.contains(20))
        self.assertTrue(bst.contains(40))

    def test_delete_two_children(self):
        """Test de la suppression d'un nœud avec deux enfants."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        self.assertTrue(bst.delete(50))
        self.assertEqual(bst.size, 6)
        self.assertFalse(bst.contains(50))
        # Vérifier que les autres valeurs sont toujours présentes
        self.assertTrue(bst.contains(30))
        self.assertTrue(bst.contains(70))
        self.assertTrue(bst.contains(20))
        self.assertTrue(bst.contains(40))
        self.assertTrue(bst.contains(60))
        self.assertTrue(bst.contains(80))

    def test_delete_non_existing(self):
        """Test de la suppression d'une valeur inexistante."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        self.assertFalse(bst.delete(25))
        self.assertEqual(bst.size, 3)

    def test_clear(self):
        """Test de la méthode clear."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        bst.clear()
        self.assertEqual(bst.size, 0)
        self.assertTrue(bst.is_empty())
        self.assertIsNone(bst.root)

    def test_get_min_max(self):
        """Test des méthodes get_min et get_max."""
        bst = BinarySearchTree()
        self.assertIsNone(bst.get_min())
        self.assertIsNone(bst.get_max())

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        self.assertEqual(bst.get_min(), 20)
        self.assertEqual(bst.get_max(), 80)

    def test_get_height(self):
        """Test du calcul de la hauteur."""
        bst = BinarySearchTree()
        self.assertEqual(bst.get_height(), -1)

        bst.insert(50)
        self.assertEqual(bst.get_height(), 0)

        bst.insert(30)
        self.assertEqual(bst.get_height(), 1)

        bst.insert(70)
        self.assertEqual(bst.get_height(), 1)

        bst.insert(20)
        self.assertEqual(bst.get_height(), 2)

    def test_is_valid(self):
        """Test de la validation des propriétés BST."""
        bst = BinarySearchTree()
        self.assertTrue(bst.is_valid())

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        self.assertTrue(bst.is_valid())

    def test_is_balanced(self):
        """Test de la vérification d'équilibre."""
        bst = BinarySearchTree()
        self.assertTrue(bst.is_balanced())

        # Arbre équilibré
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        self.assertTrue(bst.is_balanced())

        # Arbre déséquilibré
        bst2 = BinarySearchTree()
        for i in range(1, 6):
            bst2.insert(i)

        self.assertFalse(bst2.is_balanced())

    def test_get_balance_factor(self):
        """Test du calcul du facteur d'équilibre."""
        bst = BinarySearchTree()
        self.assertEqual(bst.get_balance_factor(), 0)

        bst.insert(50)
        self.assertEqual(bst.get_balance_factor(), 0)

        bst.insert(30)
        self.assertEqual(bst.get_balance_factor(), -1)

        bst.insert(70)
        self.assertEqual(bst.get_balance_factor(), 0)

    def test_preorder_traversal(self):
        """Test du parcours préfixe."""
        bst = BinarySearchTree()
        self.assertEqual(bst.preorder_traversal(), [])

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        expected = [50, 30, 20, 40, 70, 60, 80]
        self.assertEqual(bst.preorder_traversal(), expected)

    def test_inorder_traversal(self):
        """Test du parcours infixe."""
        bst = BinarySearchTree()
        self.assertEqual(bst.inorder_traversal(), [])

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        expected = [20, 30, 40, 50, 60, 70, 80]
        self.assertEqual(bst.inorder_traversal(), expected)

    def test_postorder_traversal(self):
        """Test du parcours postfixe."""
        bst = BinarySearchTree()
        self.assertEqual(bst.postorder_traversal(), [])

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        expected = [20, 40, 30, 60, 80, 70, 50]
        self.assertEqual(bst.postorder_traversal(), expected)

    def test_level_order_traversal(self):
        """Test du parcours par niveaux."""
        bst = BinarySearchTree()
        self.assertEqual(bst.level_order_traversal(), [])

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        expected = [50, 30, 70, 20, 40, 60, 80]
        self.assertEqual(bst.level_order_traversal(), expected)

    def test_iterators(self):
        """Test des itérateurs."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        # Test itérateur préfixe
        preorder_values = list(bst.preorder_iter())
        self.assertEqual(preorder_values, [50, 30, 20, 40, 70, 60, 80])

        # Test itérateur infixe
        inorder_values = list(bst.inorder_iter())
        self.assertEqual(inorder_values, [20, 30, 40, 50, 60, 70, 80])

        # Test itérateur postfixe
        postorder_values = list(bst.postorder_iter())
        self.assertEqual(postorder_values, [20, 40, 30, 60, 80, 70, 50])

        # Test itérateur par niveaux
        level_order_values = list(bst.level_order_iter())
        self.assertEqual(level_order_values, [50, 30, 70, 20, 40, 60, 80])

    def test_find_successor(self):
        """Test de la recherche du successeur."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        self.assertEqual(bst.find_successor(20), 30)
        self.assertEqual(bst.find_successor(30), 40)
        self.assertEqual(bst.find_successor(40), 50)
        self.assertEqual(bst.find_successor(50), 60)
        self.assertEqual(bst.find_successor(60), 70)
        self.assertEqual(bst.find_successor(70), 80)
        self.assertIsNone(bst.find_successor(80))

    def test_find_predecessor(self):
        """Test de la recherche du prédécesseur."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        self.assertIsNone(bst.find_predecessor(20))
        self.assertEqual(bst.find_predecessor(30), 20)
        self.assertEqual(bst.find_predecessor(40), 30)
        self.assertEqual(bst.find_predecessor(50), 40)
        self.assertEqual(bst.find_predecessor(60), 50)
        self.assertEqual(bst.find_predecessor(70), 60)
        self.assertEqual(bst.find_predecessor(80), 70)

    def test_find_floor_ceiling(self):
        """Test des méthodes find_floor et find_ceiling."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        # Test find_floor
        self.assertEqual(bst.find_floor(25), 20)
        self.assertEqual(bst.find_floor(30), 30)
        self.assertEqual(bst.find_floor(35), 30)
        self.assertEqual(bst.find_floor(50), 50)
        self.assertEqual(bst.find_floor(75), 70)
        self.assertEqual(bst.find_floor(90), 80)
        self.assertIsNone(bst.find_floor(10))

        # Test find_ceiling
        self.assertEqual(bst.find_ceiling(10), 20)
        self.assertEqual(bst.find_ceiling(25), 30)
        self.assertEqual(bst.find_ceiling(30), 30)
        self.assertEqual(bst.find_ceiling(35), 40)
        self.assertEqual(bst.find_ceiling(50), 50)
        self.assertEqual(bst.find_ceiling(75), 80)
        self.assertIsNone(bst.find_ceiling(90))

    def test_range_query(self):
        """Test de la requête de plage."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        # Test plage normale
        result = bst.range_query(30, 60)
        self.assertEqual(sorted(result), [30, 40, 50, 60])

        # Test plage vide
        result = bst.range_query(10, 15)
        self.assertEqual(result, [])

        # Test plage invalide
        result = bst.range_query(60, 30)
        self.assertEqual(result, [])

        # Test plage complète
        result = bst.range_query(0, 100)
        self.assertEqual(sorted(result), [20, 30, 40, 50, 60, 70, 80])

    def test_count_range(self):
        """Test du comptage dans une plage."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        # Test comptage normal
        self.assertEqual(bst.count_range(30, 60), 4)

        # Test plage vide
        self.assertEqual(bst.count_range(10, 15), 0)

        # Test plage invalide
        self.assertEqual(bst.count_range(60, 30), 0)

        # Test plage complète
        self.assertEqual(bst.count_range(0, 100), 7)

    def test_magic_methods(self):
        """Test des méthodes magiques."""
        bst = BinarySearchTree()
        self.assertEqual(len(bst), 0)
        self.assertFalse(bool(bst))

        bst.insert(50)
        self.assertEqual(len(bst), 1)
        self.assertTrue(bool(bst))

        # Test __str__ et __repr__
        str_repr = str(bst)
        repr_repr = repr(bst)
        self.assertIn("BinarySearchTree", str_repr)
        self.assertIn("BinarySearchTree", repr_repr)

    def test_exceptions(self):
        """Test des exceptions."""
        bst = BinarySearchTree()

        # Test ValueNotFoundError
        with self.assertRaises(ValueNotFoundError):
            bst.find_successor(50)

        with self.assertRaises(ValueNotFoundError):
            bst.find_predecessor(50)

    def test_complex_scenario(self):
        """Test d'un scénario complexe avec plusieurs opérations."""
        bst = BinarySearchTree()

        # Insertion de valeurs
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        for value in values:
            self.assertTrue(bst.insert(value))

        self.assertEqual(bst.size, len(values))
        self.assertTrue(bst.is_valid())

        # Test des parcours
        inorder = bst.inorder_traversal()
        self.assertEqual(inorder, sorted(values))

        # Test des opérations de recherche
        self.assertEqual(bst.get_min(), min(values))
        self.assertEqual(bst.get_max(), max(values))

        # Test des suppressions
        to_delete = [20, 50, 70]
        for value in to_delete:
            self.assertTrue(bst.delete(value))

        self.assertEqual(bst.size, len(values) - len(to_delete))
        self.assertTrue(bst.is_valid())

        # Test des requêtes de plage
        range_result = bst.range_query(30, 60)
        self.assertGreater(len(range_result), 0)

        # Test du comptage de plage
        count = bst.count_range(30, 60)
        self.assertGreater(count, 0)


if __name__ == "__main__":
    unittest.main()
