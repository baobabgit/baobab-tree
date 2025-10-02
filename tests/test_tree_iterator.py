"""
Tests unitaires pour la classe TreeIterator.

Ce module contient tous les tests unitaires pour la classe abstraite TreeIterator
et ses fonctionnalités de base.
"""

import pytest
from unittest.mock import Mock

from src.tree_iterator import TreeIterator
from src.binary_tree_node import BinaryTreeNode


class ConcreteTreeIterator(TreeIterator):
    """Classe concrète pour tester TreeIterator."""
    
    def __init__(self, root):
        super().__init__(root)
        self._values = [root.value] if root else []
        self._index = 0
        self._peeked_value = None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._peeked_value is not None:
            value = self._peeked_value
            self._peeked_value = None
            return value
        
        if self._index >= len(self._values):
            raise StopIteration
        value = self._values[self._index]
        self._index += 1
        return value
    
    def _put_back(self, value):
        """Remet une valeur en place pour la prochaine itération."""
        self._peeked_value = value


class TestTreeIterator:
    """Tests pour la classe TreeIterator."""

    def test_init_with_root(self):
        """Test de l'initialisation avec racine."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        assert iterator._root == node
        assert iterator._initialized is False

    def test_init_without_root(self):
        """Test de l'initialisation sans racine."""
        iterator = ConcreteTreeIterator(None)
        assert iterator._root is None
        assert iterator._initialized is False

    def test_iter_empty_iterator(self):
        """Test de l'itération sur un itérateur vide."""
        iterator = ConcreteTreeIterator(None)
        result = list(iterator)
        assert result == []

    def test_iter_single_value(self):
        """Test de l'itération sur un itérateur avec une valeur."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        result = list(iterator)
        assert result == [42]

    def test_next_empty_iterator(self):
        """Test de __next__ sur un itérateur vide."""
        iterator = ConcreteTreeIterator(None)
        with pytest.raises(StopIteration):
            iterator.__next__()

    def test_next_single_value(self):
        """Test de __next__ sur un itérateur avec une valeur."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        assert iterator.__next__() == 42
        with pytest.raises(StopIteration):
            iterator.__next__()

    def test_has_next_empty_iterator(self):
        """Test de has_next sur un itérateur vide."""
        iterator = ConcreteTreeIterator(None)
        assert iterator.has_next() is False

    def test_has_next_with_values(self):
        """Test de has_next sur un itérateur avec des valeurs."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        assert iterator.has_next() is True
        iterator.__next__()
        assert iterator.has_next() is False

    def test_peek_empty_iterator(self):
        """Test de peek sur un itérateur vide."""
        iterator = ConcreteTreeIterator(None)
        assert iterator.peek() is None

    def test_peek_with_values(self):
        """Test de peek sur un itérateur avec des valeurs."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        assert iterator.peek() == 42
        # peek ne doit pas consommer la valeur
        assert iterator.__next__() == 42

    def test_to_list_empty_iterator(self):
        """Test de to_list sur un itérateur vide."""
        iterator = ConcreteTreeIterator(None)
        result = iterator.to_list()
        assert result == []

    def test_to_list_with_values(self):
        """Test de to_list sur un itérateur avec des valeurs."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        result = iterator.to_list()
        assert result == [42]

    def test_str_representation(self):
        """Test de la représentation string."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        str_repr = str(iterator)
        assert "ConcreteTreeIterator" in str_repr
        assert "42" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        repr_str = repr(iterator)
        assert "ConcreteTreeIterator" in repr_str
        assert "42" in repr_str

    def test_put_back_default_implementation(self):
        """Test de _put_back avec implémentation par défaut."""
        node = BinaryTreeNode(42)
        iterator = ConcreteTreeIterator(node)
        # _put_back ne doit pas lever d'exception
        iterator._put_back(42)