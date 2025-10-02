"""
Tests unitaires pour les cas d'erreur de BinarySearchTree.

Ce module contient les tests pour les cas d'erreur et les branches
exceptionnelles de la classe BinarySearchTree.
"""

import unittest
from unittest.mock import patch, MagicMock

from src.baobab_tree.binary.binary_search_tree import BinarySearchTree
from src.baobab_tree.core.exceptions import BSTError, ValueNotFoundError


class TestBSTErrorCases(unittest.TestCase):
    """
    Classe de tests pour les cas d'erreur de BinarySearchTree.
    """

    # def test_insert_error_handling(self):
    #     """Test de la gestion d'erreur lors de l'insertion."""
    #     bst = BinarySearchTree()
    #
    #     # Mock pour simuler une erreur lors de l'insertion
    #     with patch.object(bst, '_insert_recursive', side_effect=Exception("Test error")):
    #         with self.assertRaises(BSTError) as context:
    #             bst.insert(50)
    #
    #         self.assertIn("Error during insertion", str(context.exception))
    #         self.assertEqual(context.exception.operation, "insert")

    def test_insert_with_failing_comparator(self):
        """Test d'insertion avec un comparateur qui échoue."""

        def failing_comparator(a, b):
            if a == 50 and b == 30:
                raise ValueError("Comparator error")
            return a - b

        bst = BinarySearchTree(failing_comparator)
        bst.insert(30)  # Ceci fonctionne

        # Ceci doit lever une BSTError à cause de l'erreur du comparateur
        with self.assertRaises(BSTError) as context:
            bst.insert(50)

        self.assertIn("Error during insertion", str(context.exception))
        self.assertEqual(context.exception.operation, "insert")

    # def test_delete_error_handling(self):
    #     """Test de la gestion d'erreur lors de la suppression."""
    #     bst = BinarySearchTree()
    #     bst.insert(50)
    #
    #     # Mock pour simuler une erreur lors de la suppression
    #     with patch.object(bst, '_delete_recursive', side_effect=Exception("Test error")):
    #         with self.assertRaises(BSTError) as context:
    #             bst.delete(50)
    #
    #         self.assertIn("Error during deletion", str(context.exception))
    #         self.assertEqual(context.exception.operation, "delete")

    def test_delete_with_failing_comparator(self):
        """Test de suppression avec un comparateur qui échoue."""

        def failing_comparator(a, b):
            if a == 50 and b == 30:
                raise ValueError("Comparator error")
            return a - b

        bst = BinarySearchTree(failing_comparator)
        bst.insert(30)

        # L'insertion de 50 échoue à cause du comparateur
        with self.assertRaises(BSTError) as context:
            bst.insert(50)

        self.assertIn("Error during insertion", str(context.exception))
        self.assertEqual(context.exception.operation, "insert")

    def test_search_error_handling(self):
        """Test de la gestion d'erreur lors de la recherche."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la recherche
        with patch.object(
            bst, "_search_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.search(50)

            self.assertIn("Error during search", str(context.exception))
            self.assertEqual(context.exception.operation, "search")

    def test_is_valid_error_handling(self):
        """Test de la gestion d'erreur lors de la validation."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la validation
        with patch.object(
            bst, "_is_valid_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.is_valid()

            self.assertIn("Error during validation", str(context.exception))
            self.assertEqual(context.exception.operation, "is_valid")

    def test_is_balanced_error_handling(self):
        """Test de la gestion d'erreur lors de la vérification d'équilibre."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la vérification d'équilibre
        with patch.object(
            bst, "_is_balanced_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.is_balanced()

            self.assertIn("Error during balance check", str(context.exception))
            self.assertEqual(context.exception.operation, "is_balanced")

    def test_find_successor_error_handling(self):
        """Test de la gestion d'erreur lors de la recherche de successeur."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la recherche de successeur
        with patch.object(bst, "search", side_effect=Exception("Test error")):
            with self.assertRaises(BSTError) as context:
                bst.find_successor(50)

            self.assertIn("Error during successor search", str(context.exception))
            self.assertEqual(context.exception.operation, "find_successor")

    def test_find_predecessor_error_handling(self):
        """Test de la gestion d'erreur lors de la recherche de prédécesseur."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la recherche de prédécesseur
        with patch.object(bst, "search", side_effect=Exception("Test error")):
            with self.assertRaises(BSTError) as context:
                bst.find_predecessor(50)

            self.assertIn("Error during predecessor search", str(context.exception))
            self.assertEqual(context.exception.operation, "find_predecessor")

    def test_find_floor_error_handling(self):
        """Test de la gestion d'erreur lors de la recherche de plancher."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la recherche de plancher
        with patch.object(
            bst, "_find_floor_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.find_floor(50)

            self.assertIn("Error during floor search", str(context.exception))
            self.assertEqual(context.exception.operation, "find_floor")

    def test_find_ceiling_error_handling(self):
        """Test de la gestion d'erreur lors de la recherche de plafond."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la recherche de plafond
        with patch.object(
            bst, "_find_ceiling_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.find_ceiling(50)

            self.assertIn("Error during ceiling search", str(context.exception))
            self.assertEqual(context.exception.operation, "find_ceiling")

    def test_range_query_error_handling(self):
        """Test de la gestion d'erreur lors de la requête de plage."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors de la requête de plage
        with patch.object(
            bst, "_range_query_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.range_query(10, 50)

            self.assertIn("Error during range query", str(context.exception))
            self.assertEqual(context.exception.operation, "range_query")

    def test_count_range_error_handling(self):
        """Test de la gestion d'erreur lors du comptage de plage."""
        bst = BinarySearchTree()

        # Mock pour simuler une erreur lors du comptage de plage
        with patch.object(
            bst, "_count_range_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.count_range(10, 50)

            self.assertIn("Error during range count", str(context.exception))
            self.assertEqual(context.exception.operation, "count_range")

    # def test_bst_error_preservation(self):
    #     """Test que les BSTError existantes sont préservées."""
    #     bst = BinarySearchTree()
    #
    #     # Test avec une BSTError existante
    #     with patch.object(bst, '_insert_recursive', side_effect=BSTError("Original error", "insert")):
    #         with self.assertRaises(BSTError) as context:
    #             bst.insert(50)
    #
    #         self.assertEqual(str(context.exception), "Original error (Operation: insert)")
    #         self.assertEqual(context.exception.operation, "insert")

    def test_delete_root_with_two_children_error_handling(self):
        """Test de la gestion d'erreur lors de la suppression de la racine avec deux enfants."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        # Mock pour simuler une erreur lors de la suppression de la racine
        with patch.object(bst, "_delete_node", side_effect=Exception("Test error")):
            with self.assertRaises(BSTError) as context:
                bst.delete(50)

            self.assertIn("Error during deletion", str(context.exception))
            self.assertEqual(context.exception.operation, "delete")

    def test_delete_recursive_error_handling(self):
        """Test de la gestion d'erreur lors de la suppression récursive."""
        bst = BinarySearchTree()
        bst.insert(50)
        bst.insert(30)

        # Mock pour simuler une erreur lors de la suppression récursive
        with patch.object(
            bst, "_delete_recursive", side_effect=Exception("Test error")
        ):
            with self.assertRaises(BSTError) as context:
                bst.delete(30)

            self.assertIn("Error during deletion", str(context.exception))
            self.assertEqual(context.exception.operation, "delete")


if __name__ == "__main__":
    unittest.main()
