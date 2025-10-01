"""
Tests unitaires pour les exceptions personnalisées.

Ce module contient tous les tests unitaires pour les classes d'exceptions
définies dans le module exceptions.
"""

import pytest

from src.exceptions import (
    TreeNodeError,
    InvalidNodeOperationError,
    CircularReferenceError,
    NodeValidationError
)


class TestTreeNodeError:
    """Tests pour la classe TreeNodeError."""
    
    def test_init_with_message_only(self):
        """Test de l'initialisation avec seulement un message."""
        error = TreeNodeError("Test error message")
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.node is None
    
    def test_init_with_message_and_node(self):
        """Test de l'initialisation avec message et nœud."""
        mock_node = "mock_node"
        error = TreeNodeError("Test error message", mock_node)
        assert str(error) == "Test error message (Node: mock_node)"
        assert error.message == "Test error message"
        assert error.node == mock_node
    
    def test_inheritance(self):
        """Test que TreeNodeError hérite bien d'Exception."""
        error = TreeNodeError("Test")
        assert isinstance(error, Exception)


class TestInvalidNodeOperationError:
    """Tests pour la classe InvalidNodeOperationError."""
    
    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        mock_node = "mock_node"
        error = InvalidNodeOperationError(
            "Test error message",
            "test_operation",
            mock_node
        )
        assert error.message == "Test error message"
        assert error.operation == "test_operation"
        assert error.node == mock_node
        assert "Operation: test_operation" in str(error)
    
    def test_init_without_node(self):
        """Test de l'initialisation sans nœud."""
        error = InvalidNodeOperationError(
            "Test error message",
            "test_operation"
        )
        assert error.message == "Test error message"
        assert error.operation == "test_operation"
        assert error.node is None
        assert "Operation: test_operation" in str(error)
    
    def test_inheritance(self):
        """Test que InvalidNodeOperationError hérite bien de TreeNodeError."""
        error = InvalidNodeOperationError("Test", "operation")
        assert isinstance(error, TreeNodeError)
        assert isinstance(error, Exception)


class TestCircularReferenceError:
    """Tests pour la classe CircularReferenceError."""
    
    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        mock_node1 = "mock_node1"
        mock_node2 = "mock_node2"
        error = CircularReferenceError(
            "Test error message",
            mock_node1,
            mock_node2
        )
        assert error.message == "Test error message"
        assert error.node1 == mock_node1
        assert error.node2 == mock_node2
        assert "Node1: mock_node1" in str(error)
        assert "Node2: mock_node2" in str(error)
    
    def test_inheritance(self):
        """Test que CircularReferenceError hérite bien de TreeNodeError."""
        error = CircularReferenceError("Test", "node1", "node2")
        assert isinstance(error, TreeNodeError)
        assert isinstance(error, Exception)


class TestNodeValidationError:
    """Tests pour la classe NodeValidationError."""
    
    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        mock_node = "mock_node"
        error = NodeValidationError(
            "Test error message",
            "test_rule",
            mock_node
        )
        assert error.message == "Test error message"
        assert error.validation_rule == "test_rule"
        assert error.node == mock_node
        assert "Validation rule: test_rule" in str(error)
    
    def test_init_without_node(self):
        """Test de l'initialisation sans nœud."""
        error = NodeValidationError(
            "Test error message",
            "test_rule"
        )
        assert error.message == "Test error message"
        assert error.validation_rule == "test_rule"
        assert error.node is None
        assert "Validation rule: test_rule" in str(error)
    
    def test_inheritance(self):
        """Test que NodeValidationError hérite bien de TreeNodeError."""
        error = NodeValidationError("Test", "rule")
        assert isinstance(error, TreeNodeError)
        assert isinstance(error, Exception)