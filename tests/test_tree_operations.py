"""
Tests unitaires pour la classe TreeOperations.

Ce module contient les tests unitaires pour la classe abstraite TreeOperations
et ses méthodes communes.
"""

import pytest
from src.binary_tree_node import BinaryTreeNode
from src.tree_operations import TreeOperations


class ConcreteTreeOperations(TreeOperations[int]):
    """Implémentation concrète de TreeOperations pour les tests."""
    
    def search(self, root, value):
        """Implémentation simple pour les tests."""
        if root is None:
            return None
        if root.value == value:
            return root
        for child in root.get_children():
            result = self.search(child, value)
            if result is not None:
                return result
        return None
    
    def insert(self, root, value):
        """Implémentation simple pour les tests."""
        if root is None:
            new_node = BinaryTreeNode(value)
            return new_node, True
        return root, False
    
    def delete(self, root, value):
        """Implémentation simple pour les tests."""
        if root is None:
            return None, False
        if root.value == value:
            return None, True
        return root, False
    
    def get_min_node(self, root):
        """Implémentation simple pour les tests."""
        return root
    
    def get_max_node(self, root):
        """Implémentation simple pour les tests."""
        return root


class TestTreeOperations:
    """Tests pour la classe TreeOperations."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.operations = ConcreteTreeOperations()
        
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
    
    def test_contains_existing_value(self):
        """Test de contains avec une valeur existante."""
        assert self.operations.contains(self.root, 1) is True
        assert self.operations.contains(self.root, 2) is True
        assert self.operations.contains(self.root, 3) is True
        assert self.operations.contains(self.root, 4) is True
        assert self.operations.contains(self.root, 5) is True
    
    def test_contains_non_existing_value(self):
        """Test de contains avec une valeur inexistante."""
        assert self.operations.contains(self.root, 6) is False
        assert self.operations.contains(self.root, 0) is False
        assert self.operations.contains(None, 1) is False
    
    def test_get_min(self):
        """Test de get_min."""
        assert self.operations.get_min(self.root) == 1
        assert self.operations.get_min(None) is None
    
    def test_get_max(self):
        """Test de get_max."""
        assert self.operations.get_max(self.root) == 1
        assert self.operations.get_max(None) is None
    
    def test_get_height(self):
        """Test de get_height."""
        assert self.operations.get_height(self.root) == 2
        assert self.operations.get_height(self.left) == 1
        assert self.operations.get_height(self.left_left) == 0
        assert self.operations.get_height(None) == -1
    
    def test_get_size(self):
        """Test de get_size."""
        assert self.operations.get_size(self.root) == 5
        assert self.operations.get_size(self.left) == 3
        assert self.operations.get_size(self.left_left) == 1
        assert self.operations.get_size(None) == 0
    
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
    
    def test_get_depth(self):
        """Test de get_depth."""
        assert self.root.get_depth() == 0
        assert self.left.get_depth() == 1
        assert self.right.get_depth() == 1
        assert self.left_left.get_depth() == 2
        assert self.left_right.get_depth() == 2
    
    def test_is_balanced(self):
        """Test de is_balanced."""
        assert self.operations.is_balanced(self.root) is True
        assert self.operations.is_balanced(self.left) is True
        assert self.operations.is_balanced(self.left_left) is True
        assert self.operations.is_balanced(None) is True
    
    def test_is_complete(self):
        """Test de is_complete."""
        assert self.operations.is_complete(self.root) is True
        assert self.operations.is_complete(self.left) is True
        assert self.operations.is_complete(self.left_left) is True
        assert self.operations.is_complete(None) is True
    
    def test_is_full(self):
        """Test de is_full."""
        assert self.operations.is_full(self.root) is True
        assert self.operations.is_full(self.left) is True
        assert self.operations.is_full(self.left_left) is True
        assert self.operations.is_full(None) is True
    
    def test_abstract_methods(self):
        """Test que les méthodes abstraites sont bien définies."""
        # Ces méthodes doivent être implémentées par les classes concrètes
        assert hasattr(self.operations, 'search')
        assert hasattr(self.operations, 'insert')
        assert hasattr(self.operations, 'delete')
        assert hasattr(self.operations, 'get_min_node')
        assert hasattr(self.operations, 'get_max_node')
        
        # Vérifier que ce sont bien des méthodes
        assert callable(self.operations.search)
        assert callable(self.operations.insert)
        assert callable(self.operations.delete)
        assert callable(self.operations.get_min_node)
        assert callable(self.operations.get_max_node)
    
    def test_concrete_methods(self):
        """Test que les méthodes concrètes sont bien définies."""
        # Ces méthodes doivent être disponibles directement
        assert hasattr(self.operations, 'contains')
        assert hasattr(self.operations, 'get_min')
        assert hasattr(self.operations, 'get_max')
        assert hasattr(self.operations, 'get_height')
        assert hasattr(self.operations, 'get_size')
        assert hasattr(self.operations, 'get_leaf_nodes')
        assert hasattr(self.operations, 'get_internal_nodes')
        assert hasattr(self.operations, 'get_depth')
        assert hasattr(self.operations, 'is_balanced')
        assert hasattr(self.operations, 'is_complete')
        assert hasattr(self.operations, 'is_full')
        
        # Vérifier que ce sont bien des méthodes
        assert callable(self.operations.contains)
        assert callable(self.operations.get_min)
        assert callable(self.operations.get_max)
        assert callable(self.operations.get_height)
        assert callable(self.operations.get_size)
        assert callable(self.operations.get_leaf_nodes)
        assert callable(self.operations.get_internal_nodes)
        assert callable(self.operations.get_depth)
        assert callable(self.operations.is_balanced)
        assert callable(self.operations.is_complete)
        assert callable(self.operations.is_full)