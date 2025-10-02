"""
Tests unitaires pour la classe BSTOperations.

Ce module contient les tests unitaires pour la classe BSTOperations
et ses méthodes spécialisées pour les arbres binaires de recherche.
"""

import pytest
from src.binary_tree_node import BinaryTreeNode
from src.bst_operations import BSTOperations


class TestBSTOperations:
    """Tests pour la classe BSTOperations."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.operations = BSTOperations[int]()
        
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
        assert comparator(10, 5) == 1
        assert comparator(5, 10) == -1
    
    def test_search_existing_value(self):
        """Test de search avec une valeur existante."""
        result = self.operations.search(self.root, 4)
        assert result is not None
        assert result.value == 4
        
        result = self.operations.search(self.root, 2)
        assert result is not None
        assert result.value == 2
        
        result = self.operations.search(self.root, 7)
        assert result is not None
        assert result.value == 7
    
    def test_search_non_existing_value(self):
        """Test de search avec une valeur inexistante."""
        result = self.operations.search(self.root, 8)
        assert result is None
        
        result = self.operations.search(self.root, 0)
        assert result is None
        
        result = self.operations.search(None, 1)
        assert result is None
    
    def test_search_invalid_root_type(self):
        """Test de search avec un type de racine invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.search("invalid", 1)
    
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
    
    def test_insert_invalid_root_type(self):
        """Test d'insertion avec un type de racine invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.insert("invalid", 1)
    
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
    
    def test_delete_root(self):
        """Test de suppression de la racine."""
        new_root, deleted = self.operations.delete(self.root, 4)
        assert deleted is True
        # La racine devrait être remplacée par son successeur (5)
        assert new_root.value == 5
    
    def test_delete_invalid_root_type(self):
        """Test de suppression avec un type de racine invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.delete("invalid", 1)
    
    def test_get_min_node(self):
        """Test de get_min_node."""
        min_node = self.operations.get_min_node(self.root)
        assert min_node is not None
        assert min_node.value == 1  # Le minimum dans notre BST
    
    def test_get_max_node(self):
        """Test de get_max_node."""
        max_node = self.operations.get_max_node(self.root)
        assert max_node is not None
        assert max_node.value == 7  # Le maximum dans notre BST
    
    def test_get_min_max_invalid_root_type(self):
        """Test de get_min_node et get_max_node avec un type invalide."""
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.get_min_node("invalid")
        
        with pytest.raises(TypeError, match="Root must be a BinaryTreeNode"):
            self.operations.get_max_node("invalid")
    
    def test_search_recursive(self):
        """Test de search_recursive."""
        result = self.operations.search_recursive(self.root, 4)
        assert result is not None
        assert result.value == 4
        
        result = self.operations.search_recursive(self.root, 3)
        assert result is not None
        assert result.value == 3
        
        result = self.operations.search_recursive(self.root, 8)
        assert result is None
        
        result = self.operations.search_recursive(None, 1)
        assert result is None
    
    def test_search_iterative(self):
        """Test de search_iterative."""
        result = self.operations.search_iterative(self.root, 4)
        assert result is not None
        assert result.value == 4
        
        result = self.operations.search_iterative(self.root, 6)
        assert result is not None
        assert result.value == 6
        
        result = self.operations.search_iterative(self.root, 8)
        assert result is None
        
        result = self.operations.search_iterative(None, 1)
        assert result is None
    
    def test_insert_recursive(self):
        """Test de insert_recursive."""
        new_root, inserted = self.operations.insert_recursive(None, 10)
        assert inserted is True
        assert new_root is not None
        assert new_root.value == 10
        
        new_root, inserted = self.operations.insert_recursive(self.root, 8)
        assert inserted is True
        assert new_root is self.root
    
    def test_insert_iterative(self):
        """Test de insert_iterative."""
        new_root, inserted = self.operations.insert_iterative(None, 10)
        assert inserted is True
        assert new_root is not None
        assert new_root.value == 10
        
        new_root, inserted = self.operations.insert_iterative(self.root, 8)
        assert inserted is True
        assert new_root is self.root
    
    def test_delete_recursive(self):
        """Test de delete_recursive."""
        new_root, deleted = self.operations.delete_recursive(None, 1)
        assert deleted is False
        assert new_root is None
        
        new_root, deleted = self.operations.delete_recursive(self.root, 3)
        assert deleted is True
        assert new_root is self.root
    
    def test_delete_iterative(self):
        """Test de delete_iterative."""
        new_root, deleted = self.operations.delete_iterative(None, 1)
        assert deleted is False
        assert new_root is None
        
        new_root, deleted = self.operations.delete_iterative(self.root, 5)
        assert deleted is True
        assert new_root is self.root
    
    def test_insert_with_validation(self):
        """Test de insert_with_validation."""
        new_root, inserted = self.operations.insert_with_validation(self.root, 8)
        assert inserted is True
        assert new_root is self.root
        
        # Vérifier que l'arbre reste valide
        assert self.operations.is_valid_bst(new_root) is True
    
    def test_insert_with_duplicates(self):
        """Test de insert_with_duplicates."""
        new_root, inserted = self.operations.insert_with_duplicates(self.root, 4)
        assert inserted is True
        assert new_root is self.root
        
        # Vérifier que le doublon a été ajouté
        result = self.operations.search(new_root, 4)
        assert result is not None
    
    def test_is_valid_bst(self):
        """Test de is_valid_bst."""
        assert self.operations.is_valid_bst(self.root) is True
        assert self.operations.is_valid_bst(self.left) is True
        assert self.operations.is_valid_bst(self.left_left) is True
        assert self.operations.is_valid_bst(None) is True
    
    def test_is_valid_bst_invalid(self):
        """Test de is_valid_bst avec un arbre invalide."""
        # Créer un arbre invalide
        invalid_root = BinaryTreeNode(4)
        invalid_left = BinaryTreeNode(6)  # Plus grand que la racine
        invalid_right = BinaryTreeNode(2)  # Plus petit que la racine
        
        invalid_root.set_left(invalid_left)
        invalid_root.set_right(invalid_right)
        
        assert self.operations.is_valid_bst(invalid_root) is False
    
    def test_get_balance_factor(self):
        """Test de get_balance_factor."""
        balance_factor = self.operations.get_balance_factor(self.root)
        assert balance_factor == 0  # Arbre équilibré
        
        balance_factor = self.operations.get_balance_factor(self.left)
        assert balance_factor == 0  # Arbre équilibré
    
    def test_inheritance_from_binary_tree_operations(self):
        """Test que BSTOperations hérite bien de BinaryTreeOperations."""
        from src.binary_tree_operations import BinaryTreeOperations
        assert issubclass(BSTOperations, BinaryTreeOperations)
        
        # Vérifier que les méthodes de BinaryTreeOperations sont disponibles
        assert hasattr(self.operations, 'search_recursive')
        assert hasattr(self.operations, 'search_iterative')
        assert hasattr(self.operations, 'insert_recursive')
        assert hasattr(self.operations, 'insert_iterative')
        assert hasattr(self.operations, 'delete_recursive')
        assert hasattr(self.operations, 'delete_iterative')
    
    def test_custom_comparator(self):
        """Test avec un comparateur personnalisé."""
        def reverse_comparator(a, b):
            if a > b:
                return -1
            elif a == b:
                return 0
            else:
                return 1
        
        operations = BSTOperations(reverse_comparator)
        
        # Test avec le comparateur inversé
        assert operations._comparator(1, 2) == 1
        assert operations._comparator(2, 2) == 0
        assert operations._comparator(3, 2) == -1