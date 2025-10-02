"""
Tests unitaires pour la classe AVLBalancingStrategy.

Ce module contient tous les tests unitaires pour la classe AVLBalancingStrategy
et ses fonctionnalités spécifiques.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_tree.balanced.avl_balancing_strategy import AVLBalancingStrategy
from src.baobab_tree.core.exceptions import BalancingStrategyError, StrategyApplicationError
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode


class MockAVLNode(BinaryTreeNode[int]):
    """Nœud AVL mock pour les tests."""
    
    def __init__(self, value: int, balance_factor: int = 0, height: int = 1):
        super().__init__(value)
        self.balance_factor = balance_factor
        self.height = height


class TestAVLBalancingStrategy:
    """Tests pour la classe AVLBalancingStrategy."""
    
    def test_init(self):
        """Test de l'initialisation."""
        strategy = AVLBalancingStrategy()
        
        assert strategy._rotation_count == 0
        assert strategy._balance_factor_cache == {}
    
    def test_balance_with_balanced_node(self):
        """Test d'équilibrage avec nœud déjà équilibré."""
        strategy = AVLBalancingStrategy()
        node = MockAVLNode(5, balance_factor=0)
        
        result = strategy.balance(node)
        
        assert result == node
    
    def test_balance_with_left_heavy_node(self):
        """Test d'équilibrage avec nœud déséquilibré à gauche."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5, balance_factor=2)
        left = MockAVLNode(3, balance_factor=1)
        right = MockAVLNode(7, balance_factor=0)
        
        root.left_child = left
        root.right_child = right
        left.parent = root
        right.parent = root
        
        with patch.object(strategy, '_calculate_balance_factor') as mock_calc:
            mock_calc.side_effect = [2, 1, 0]  # root, left, right
            with patch.object(strategy, '_rotate_right') as mock_rotate:
                mock_rotate.return_value = left
                
                result = strategy.balance(root)
                
                assert result == left
                mock_rotate.assert_called_once_with(root)
    
    def test_balance_with_right_heavy_node(self):
        """Test d'équilibrage avec nœud déséquilibré à droite."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5, balance_factor=-2)
        left = MockAVLNode(3, balance_factor=0)
        right = MockAVLNode(7, balance_factor=-1)
        
        root.left_child = left
        root.right_child = right
        left.parent = root
        right.parent = root
        
        with patch.object(strategy, '_calculate_balance_factor') as mock_calc:
            mock_calc.side_effect = [-2, 0, -1]  # root, left, right
            with patch.object(strategy, '_rotate_left') as mock_rotate:
                mock_rotate.return_value = right
                
                result = strategy.balance(root)
                
                assert result == right
                mock_rotate.assert_called_once_with(root)
    
    def test_balance_with_left_right_case(self):
        """Test d'équilibrage avec cas gauche-droite."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5, balance_factor=2)
        left = MockAVLNode(3, balance_factor=-1)
        right = MockAVLNode(7, balance_factor=0)
        
        root.left_child = left
        root.right_child = right
        left.parent = root
        right.parent = root
        
        with patch.object(strategy, '_calculate_balance_factor') as mock_calc:
            mock_calc.side_effect = [2, -1, 0]  # root, left, right
            with patch.object(strategy, '_rotate_left_right') as mock_rotate:
                mock_rotate.return_value = left
                
                result = strategy.balance(root)
                
                assert result == left
                mock_rotate.assert_called_once_with(root)
    
    def test_balance_with_right_left_case(self):
        """Test d'équilibrage avec cas droite-gauche."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5, balance_factor=-2)
        left = MockAVLNode(3, balance_factor=0)
        right = MockAVLNode(7, balance_factor=1)
        
        root.left_child = left
        root.right_child = right
        left.parent = root
        right.parent = root
        
        with patch.object(strategy, '_calculate_balance_factor') as mock_calc:
            mock_calc.side_effect = [-2, 0, 1]  # root, left, right
            with patch.object(strategy, '_rotate_right_left') as mock_rotate:
                mock_rotate.return_value = right
                
                result = strategy.balance(root)
                
                assert result == right
                mock_rotate.assert_called_once_with(root)
    
    def test_balance_with_exception(self):
        """Test d'équilibrage avec exception."""
        strategy = AVLBalancingStrategy()
        node = MockAVLNode(5)
        
        with patch.object(strategy, 'validate_before_balancing', return_value=False):
            with pytest.raises(BalancingStrategyError):
                strategy.balance(node)
    
    def test_can_balance_with_valid_node(self):
        """Test de can_balance avec nœud valide."""
        strategy = AVLBalancingStrategy()
        node = MockAVLNode(5)
        
        result = strategy.can_balance(node)
        
        assert result is True
    
    def test_can_balance_with_invalid_node(self):
        """Test de can_balance avec nœud invalide."""
        strategy = AVLBalancingStrategy()
        node = BinaryTreeNode(5)  # Pas de balance_factor
        
        result = strategy.can_balance(node)
        
        assert result is False
    
    def test_can_balance_with_none_node(self):
        """Test de can_balance avec nœud None."""
        strategy = AVLBalancingStrategy()
        
        result = strategy.can_balance(None)
        
        assert result is False
    
    def test_get_description(self):
        """Test de récupération de la description."""
        strategy = AVLBalancingStrategy()
        
        description = strategy.get_description()
        
        assert description == "Stratégie d'équilibrage AVL basée sur les facteurs d'équilibre"
    
    def test_get_complexity(self):
        """Test de récupération de la complexité."""
        strategy = AVLBalancingStrategy()
        
        complexity = strategy.get_complexity()
        
        assert complexity == "O(log n)"
    
    def test_validate_strategy_specific_with_valid_node(self):
        """Test de validation spécifique avec nœud valide."""
        strategy = AVLBalancingStrategy()
        node = MockAVLNode(5, balance_factor=1)
        
        result = strategy._validate_strategy_specific(node)
        
        assert result is True
    
    def test_validate_strategy_specific_with_invalid_node(self):
        """Test de validation spécifique avec nœud invalide."""
        strategy = AVLBalancingStrategy()
        node = BinaryTreeNode(5)  # Pas de balance_factor
        
        result = strategy._validate_strategy_specific(node)
        
        assert result is False
    
    def test_validate_strategy_specific_with_extreme_balance_factor(self):
        """Test de validation spécifique avec facteur d'équilibre extrême."""
        strategy = AVLBalancingStrategy()
        node = MockAVLNode(5, balance_factor=3)  # Trop élevé
        
        result = strategy._validate_strategy_specific(node)
        
        assert result is False
    
    def test_validate_resulting_structure_with_valid_structure(self):
        """Test de validation de structure résultante avec structure valide."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5, balance_factor=0)
        left = MockAVLNode(3, balance_factor=0)
        right = MockAVLNode(7, balance_factor=0)
        
        root.left_child = left
        root.right_child = right
        
        result = strategy._validate_resulting_structure(root)
        
        assert result is True
    
    def test_validate_resulting_structure_with_invalid_structure(self):
        """Test de validation de structure résultante avec structure invalide."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5, balance_factor=2)  # Facteur invalide
        
        result = strategy._validate_resulting_structure(root)
        
        assert result is False
    
    def test_calculate_balance_factor(self):
        """Test de calcul du facteur d'équilibre."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5, height=3)
        left = MockAVLNode(3, height=2)
        right = MockAVLNode(7, height=1)
        
        root.left_child = left
        root.right_child = right
        
        with patch.object(strategy, '_get_height') as mock_height:
            mock_height.side_effect = [2, 1]  # left_height, right_height
            
            balance_factor = strategy._calculate_balance_factor(root)
            
            assert balance_factor == 1  # 2 - 1 = 1
    
    def test_calculate_balance_factor_with_cache(self):
        """Test de calcul du facteur d'équilibre avec cache."""
        strategy = AVLBalancingStrategy()
        node = MockAVLNode(5)
        
        # Premier calcul
        strategy._balance_factor_cache[node] = 1
        balance_factor = strategy._calculate_balance_factor(node)
        
        assert balance_factor == 1
    
    def test_get_height_with_cached_height(self):
        """Test de récupération de hauteur avec cache."""
        strategy = AVLBalancingStrategy()
        node = MockAVLNode(5, height=3)
        
        height = strategy._get_height(node)
        
        assert height == 3
    
    def test_get_height_with_calculated_height(self):
        """Test de récupération de hauteur avec calcul."""
        strategy = AVLBalancingStrategy()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(3)
        right = BinaryTreeNode(7)
        
        root.left_child = left
        root.right_child = right
        
        height = strategy._get_height(root)
        
        assert height == 2  # 1 + max(1, 1) = 2
    
    def test_rotate_left_with_valid_structure(self):
        """Test de rotation gauche avec structure valide."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        right = MockAVLNode(7)
        right_left = MockAVLNode(6)
        
        root.right_child = right
        right.left_child = right_left
        right.parent = root
        right_left.parent = right
        
        with patch.object(strategy, '_update_avl_properties') as mock_update:
            with patch.object(strategy, '_invalidate_cache') as mock_invalidate:
                result = strategy._rotate_left(root)
                
                assert result == right
                assert right.left_child == root
                assert root.parent == right
                assert root.right_child == right_left
                assert right_left.parent == root
                assert strategy._rotation_count == 1
                mock_update.assert_called()
                mock_invalidate.assert_called()
    
    def test_rotate_left_with_missing_right_child(self):
        """Test de rotation gauche avec enfant droit manquant."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        
        with pytest.raises(StrategyApplicationError):
            strategy._rotate_left(root)
    
    def test_rotate_right_with_valid_structure(self):
        """Test de rotation droite avec structure valide."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        left = MockAVLNode(3)
        left_right = MockAVLNode(4)
        
        root.left_child = left
        left.right_child = left_right
        left.parent = root
        left_right.parent = left
        
        with patch.object(strategy, '_update_avl_properties') as mock_update:
            with patch.object(strategy, '_invalidate_cache') as mock_invalidate:
                result = strategy._rotate_right(root)
                
                assert result == left
                assert left.right_child == root
                assert root.parent == left
                assert root.left_child == left_right
                assert left_right.parent == root
                assert strategy._rotation_count == 1
                mock_update.assert_called()
                mock_invalidate.assert_called()
    
    def test_rotate_right_with_missing_left_child(self):
        """Test de rotation droite avec enfant gauche manquant."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        
        with pytest.raises(StrategyApplicationError):
            strategy._rotate_right(root)
    
    def test_rotate_left_right(self):
        """Test de rotation gauche-droite."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        
        with patch.object(strategy, '_rotate_left') as mock_left:
            with patch.object(strategy, '_rotate_right') as mock_right:
                mock_left.return_value = root
                mock_right.return_value = root
                
                result = strategy._rotate_left_right(root)
                
                mock_left.assert_called_once()
                mock_right.assert_called_once_with(root)
                assert result == root
    
    def test_rotate_right_left(self):
        """Test de rotation droite-gauche."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        
        with patch.object(strategy, '_rotate_right') as mock_right:
            with patch.object(strategy, '_rotate_left') as mock_left:
                mock_right.return_value = root
                mock_left.return_value = root
                
                result = strategy._rotate_right_left(root)
                
                mock_right.assert_called_once()
                mock_left.assert_called_once_with(root)
                assert result == root
    
    def test_update_avl_properties(self):
        """Test de mise à jour des propriétés AVL."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        left = MockAVLNode(3)
        right = MockAVLNode(7)
        
        root.left_child = left
        root.right_child = right
        
        with patch.object(strategy, '_get_height') as mock_height:
            mock_height.side_effect = [1, 1]  # left_height, right_height
            
            strategy._update_avl_properties(root)
            
            assert root.height == 2  # 1 + max(1, 1)
            assert root.balance_factor == 0  # 1 - 1
            assert root in strategy._balance_factor_cache
            assert strategy._balance_factor_cache[root] == 0
    
    def test_invalidate_cache(self):
        """Test d'invalidation du cache."""
        strategy = AVLBalancingStrategy()
        root = MockAVLNode(5)
        left = MockAVLNode(3)
        
        root.left_child = left
        left.parent = root
        
        # Ajouter au cache
        strategy._balance_factor_cache[root] = 1
        strategy._balance_factor_cache[left] = 0
        
        # Invalider le cache
        strategy._invalidate_cache(left)
        
        # Vérifier que le cache a été invalidé pour left et root
        assert left not in strategy._balance_factor_cache
        assert root not in strategy._balance_factor_cache