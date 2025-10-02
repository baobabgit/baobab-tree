"""
Tests unitaires pour les exceptions personnalisées.

Ce module contient tous les tests unitaires pour les classes d'exceptions
définies dans le module exceptions.
"""

import unittest

from src.exceptions import (
    TreeNodeError,
    InvalidNodeOperationError,
    CircularReferenceError,
    NodeValidationError,
    BSTError,
    DuplicateValueError,
    ValueNotFoundError,
    InvalidOperationError,
)


class TestTreeNodeError(unittest.TestCase):
    """Tests pour la classe TreeNodeError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec seulement un message."""
        error = TreeNodeError("Test error message")
        self.assertEqual(str(error), "Test error message")
        self.assertEqual(error.message, "Test error message")
        self.assertIsNone(error.node)

    def test_init_with_message_and_node(self):
        """Test de l'initialisation avec message et nœud."""
        mock_node = "mock_node"
        error = TreeNodeError("Test error message", mock_node)
        self.assertEqual(str(error), "Test error message (Node: mock_node)")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.node, mock_node)

    def test_inheritance(self):
        """Test que TreeNodeError hérite bien d'Exception."""
        error = TreeNodeError("Test")
        self.assertIsInstance(error, Exception)


class TestInvalidNodeOperationError(unittest.TestCase):
    """Tests pour la classe InvalidNodeOperationError."""

    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        mock_node = "mock_node"
        error = InvalidNodeOperationError(
            "Test error message", "test_operation", mock_node
        )
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.operation, "test_operation")
        self.assertEqual(error.node, mock_node)
        self.assertIn("Operation: test_operation", str(error))

    def test_init_without_node(self):
        """Test de l'initialisation sans nœud."""
        error = InvalidNodeOperationError("Test error message", "test_operation")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.operation, "test_operation")
        self.assertIsNone(error.node)
        self.assertIn("Operation: test_operation", str(error))

    def test_inheritance(self):
        """Test que InvalidNodeOperationError hérite bien de TreeNodeError."""
        error = InvalidNodeOperationError("Test", "operation")
        self.assertIsInstance(error, TreeNodeError)
        self.assertIsInstance(error, Exception)


class TestCircularReferenceError(unittest.TestCase):
    """Tests pour la classe CircularReferenceError."""

    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        mock_node1 = "mock_node1"
        mock_node2 = "mock_node2"
        error = CircularReferenceError("Test error message", mock_node1, mock_node2)
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.node1, mock_node1)
        self.assertEqual(error.node2, mock_node2)
        self.assertIn("Node1: mock_node1", str(error))
        self.assertIn("Node2: mock_node2", str(error))

    def test_inheritance(self):
        """Test que CircularReferenceError hérite bien de TreeNodeError."""
        error = CircularReferenceError("Test", "node1", "node2")
        self.assertIsInstance(error, TreeNodeError)
        self.assertIsInstance(error, Exception)


class TestNodeValidationError(unittest.TestCase):
    """Tests pour la classe NodeValidationError."""

    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        mock_node = "mock_node"
        error = NodeValidationError("Test error message", "test_rule", mock_node)
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.validation_rule, "test_rule")
        self.assertEqual(error.node, mock_node)
        self.assertIn("Validation rule: test_rule", str(error))

    def test_init_without_node(self):
        """Test de l'initialisation sans nœud."""
        error = NodeValidationError("Test error message", "test_rule")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.validation_rule, "test_rule")
        self.assertIsNone(error.node)
        self.assertIn("Validation rule: test_rule", str(error))

    def test_inheritance(self):
        """Test que NodeValidationError hérite bien de TreeNodeError."""
        error = NodeValidationError("Test", "rule")
        self.assertIsInstance(error, TreeNodeError)
        self.assertIsInstance(error, Exception)


class TestBSTError(unittest.TestCase):
    """Tests pour la classe BSTError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec seulement un message."""
        error = BSTError("Test error message")
        self.assertEqual(str(error), "Test error message")
        self.assertEqual(error.message, "Test error message")
        self.assertIsNone(error.operation)

    def test_init_with_message_and_operation(self):
        """Test de l'initialisation avec message et opération."""
        error = BSTError("Test error message", "test_operation")
        self.assertEqual(str(error), "Test error message (Operation: test_operation)")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.operation, "test_operation")

    def test_inheritance(self):
        """Test que BSTError hérite bien d'Exception."""
        error = BSTError("Test")
        self.assertIsInstance(error, Exception)


class TestDuplicateValueError(unittest.TestCase):
    """Tests pour la classe DuplicateValueError."""

    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        error = DuplicateValueError(
            "Test error message", "test_value", "test_operation"
        )
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.value, "test_value")
        self.assertEqual(error.operation, "test_operation")
        self.assertIn("Value: test_value", str(error))

    def test_init_with_default_operation(self):
        """Test de l'initialisation avec opération par défaut."""
        error = DuplicateValueError("Test error message", "test_value")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.value, "test_value")
        self.assertEqual(error.operation, "insert")
        self.assertIn("Value: test_value", str(error))

    def test_inheritance(self):
        """Test que DuplicateValueError hérite bien de BSTError."""
        error = DuplicateValueError("Test", "value")
        self.assertIsInstance(error, BSTError)
        self.assertIsInstance(error, Exception)


class TestValueNotFoundError(unittest.TestCase):
    """Tests pour la classe ValueNotFoundError."""

    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        error = ValueNotFoundError("Test error message", "test_value", "test_operation")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.value, "test_value")
        self.assertEqual(error.operation, "test_operation")
        self.assertIn("Value: test_value", str(error))

    def test_init_with_default_operation(self):
        """Test de l'initialisation avec opération par défaut."""
        error = ValueNotFoundError("Test error message", "test_value")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.value, "test_value")
        self.assertEqual(error.operation, "search")
        self.assertIn("Value: test_value", str(error))

    def test_inheritance(self):
        """Test que ValueNotFoundError hérite bien de BSTError."""
        error = ValueNotFoundError("Test", "value")
        self.assertIsInstance(error, BSTError)
        self.assertIsInstance(error, Exception)


class TestInvalidOperationError(unittest.TestCase):
    """Tests pour la classe InvalidOperationError."""

    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        error = InvalidOperationError("Test error message", "test_operation")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.operation, "test_operation")
        self.assertIn("Operation: test_operation", str(error))

    def test_inheritance(self):
        """Test que InvalidOperationError hérite bien de BSTError."""
        error = InvalidOperationError("Test", "operation")
        self.assertIsInstance(error, BSTError)
        self.assertIsInstance(error, Exception)


if __name__ == "__main__":
    unittest.main()
