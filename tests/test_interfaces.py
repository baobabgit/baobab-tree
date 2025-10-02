"""
Tests unitaires pour les interfaces et types.

Ce module contient tous les tests unitaires pour les interfaces et types
définis dans le module interfaces.
"""

import pytest
from typing import Any

from src.interfaces import (
    Comparable,
    TreeInterface,
    TreeTraversalInterface,
    TreeOperationInterface,
)


class TestComparable:
    """Tests pour l'interface Comparable."""

    def test_comparable_protocol(self):
        """Test que l'interface Comparable est bien définie."""
        # Vérifier que l'interface a les bonnes méthodes
        assert hasattr(Comparable, "__lt__")
        assert hasattr(Comparable, "__le__")
        assert hasattr(Comparable, "__gt__")
        assert hasattr(Comparable, "__ge__")
        assert hasattr(Comparable, "__eq__")
        assert hasattr(Comparable, "__ne__")

    def test_comparable_with_int(self):
        """Test que int implémente l'interface Comparable."""
        # int implémente naturellement toutes les méthodes de comparaison
        assert isinstance(1, Comparable)
        assert 1 < 2
        assert 1 <= 2
        assert 2 > 1
        assert 2 >= 1
        assert 1 == 1
        assert 1 != 2

    def test_comparable_with_str(self):
        """Test que str implémente l'interface Comparable."""
        # str implémente naturellement toutes les méthodes de comparaison
        assert isinstance("a", Comparable)
        assert "a" < "b"
        assert "a" <= "b"
        assert "b" > "a"
        assert "b" >= "a"
        assert "a" == "a"
        assert "a" != "b"

    def test_comparable_with_float(self):
        """Test que float implémente l'interface Comparable."""
        # float implémente naturellement toutes les méthodes de comparaison
        assert isinstance(1.0, Comparable)
        assert 1.0 < 2.0
        assert 1.0 <= 2.0
        assert 2.0 > 1.0
        assert 2.0 >= 1.0
        assert 1.0 == 1.0
        assert 1.0 != 2.0


class TestTreeInterface:
    """Tests pour l'interface TreeInterface."""

    def test_tree_interface_protocol(self):
        """Test que l'interface TreeInterface est bien définie."""
        # Vérifier que l'interface a les bonnes méthodes
        assert hasattr(TreeInterface, "is_empty")
        assert hasattr(TreeInterface, "size")
        assert hasattr(TreeInterface, "height")
        assert hasattr(TreeInterface, "clear")


class TestTreeTraversalInterface:
    """Tests pour l'interface TreeTraversalInterface."""

    def test_tree_traversal_interface_protocol(self):
        """Test que l'interface TreeTraversalInterface est bien définie."""
        # Vérifier que l'interface a les bonnes méthodes
        assert hasattr(TreeTraversalInterface, "traverse")
        assert hasattr(TreeTraversalInterface, "__iter__")


class TestTreeOperationInterface:
    """Tests pour l'interface TreeOperationInterface."""

    def test_tree_operation_interface_protocol(self):
        """Test que l'interface TreeOperationInterface est bien définie."""
        # Vérifier que l'interface a les bonnes méthodes
        assert hasattr(TreeOperationInterface, "insert")
        assert hasattr(TreeOperationInterface, "delete")
        assert hasattr(TreeOperationInterface, "search")
