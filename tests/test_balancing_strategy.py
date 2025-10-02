"""
Tests unitaires pour la classe BalancingStrategy.

Ce module contient tous les tests unitaires pour la classe abstraite BalancingStrategy
et ses fonctionnalités communes.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_tree.balanced.balancing_strategy import BalancingStrategy
from src.baobab_tree.core.exceptions import BalancingStrategyError, StrategyApplicationError
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode


class ConcreteBalancingStrategy(BalancingStrategy):
    """Implémentation concrète pour les tests."""
    
    def balance(self, node: BinaryTreeNode) -> BinaryTreeNode | None:
        """Implémentation de test."""
        return node
    
    def can_balance(self, node: BinaryTreeNode) -> bool:
        """Implémentation de test."""
        return node is not None
    
    def get_description(self) -> str:
        """Implémentation de test."""
        return "Test Strategy"
    
    def get_complexity(self) -> str:
        """Implémentation de test."""
        return "O(1)"


class TestBalancingStrategy:
    """Tests pour la classe BalancingStrategy."""
    
    def test_init(self):
        """Test de l'initialisation."""
        strategy = ConcreteBalancingStrategy()
        
        assert strategy._performance_metrics is not None
        assert strategy._operation_count == 0
        assert strategy._success_count == 0
        assert strategy._failure_count == 0
    
    def test_balance_abstract_method(self):
        """Test que balance est une méthode abstraite."""
        with pytest.raises(TypeError):
            BalancingStrategy()
    
    def test_can_balance_abstract_method(self):
        """Test que can_balance est une méthode abstraite."""
        with pytest.raises(TypeError):
            BalancingStrategy()
    
    def test_get_description_abstract_method(self):
        """Test que get_description est une méthode abstraite."""
        with pytest.raises(TypeError):
            BalancingStrategy()
    
    def test_get_complexity_abstract_method(self):
        """Test que get_complexity est une méthode abstraite."""
        with pytest.raises(TypeError):
            BalancingStrategy()
    
    def test_validate_before_balancing_with_valid_node(self):
        """Test de validation pré-équilibrage avec nœud valide."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        result = strategy.validate_before_balancing(node)
        
        assert result is True
    
    def test_validate_before_balancing_with_none_node(self):
        """Test de validation pré-équilibrage avec nœud None."""
        strategy = ConcreteBalancingStrategy()
        
        result = strategy.validate_before_balancing(None)
        
        assert result is False
    
    def test_validate_before_balancing_with_invalid_node(self):
        """Test de validation pré-équilibrage avec nœud invalide."""
        strategy = ConcreteBalancingStrategy()
        
        # Mock can_balance pour retourner False
        with patch.object(strategy, 'can_balance', return_value=False):
            result = strategy.validate_before_balancing(BinaryTreeNode(5))
            assert result is False
    
    def test_validate_after_balancing_with_valid_node(self):
        """Test de validation post-équilibrage avec nœud valide."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        result = strategy.validate_after_balancing(node)
        
        assert result is True
    
    def test_validate_after_balancing_with_none_node(self):
        """Test de validation post-équilibrage avec nœud None."""
        strategy = ConcreteBalancingStrategy()
        
        result = strategy.validate_after_balancing(None)
        
        assert result is False
    
    def test_get_performance_metrics(self):
        """Test de récupération des métriques de performance."""
        strategy = ConcreteBalancingStrategy()
        
        metrics = strategy.get_performance_metrics()
        
        assert 'strategy_type' in metrics
        assert 'description' in metrics
        assert 'complexity' in metrics
        assert 'total_operations' in metrics
        assert 'successful_operations' in metrics
        assert 'failed_operations' in metrics
        assert 'success_rate' in metrics
        assert 'performance_metrics' in metrics
        
        assert metrics['strategy_type'] == 'ConcreteBalancingStrategy'
        assert metrics['description'] == 'Test Strategy'
        assert metrics['complexity'] == 'O(1)'
    
    def test_analyze_strategy_with_valid_node(self):
        """Test d'analyse de stratégie avec nœud valide."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        analysis = strategy.analyze_strategy(node)
        
        assert 'node_value' in analysis
        assert 'can_balance' in analysis
        assert 'strategy_type' in analysis
        assert 'complexity' in analysis
        assert 'current_state' in analysis
        assert 'predicted_effect' in analysis
        assert 'performance_impact' in analysis
        
        assert analysis['node_value'] == 5
        assert analysis['can_balance'] is True
        assert analysis['strategy_type'] == 'ConcreteBalancingStrategy'
    
    def test_analyze_strategy_with_none_node(self):
        """Test d'analyse de stratégie avec nœud None."""
        strategy = ConcreteBalancingStrategy()
        
        analysis = strategy.analyze_strategy(None)
        
        assert 'error' in analysis
        assert analysis['error'] == 'Node is None'
    
    def test_get_strategy_stats_with_valid_node(self):
        """Test de récupération des statistiques avec nœud valide."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        stats = strategy.get_strategy_stats(node)
        
        assert 'subtree_size' in stats
        assert 'operation_types' in stats
        assert 'performance_metrics' in stats
        assert 'strategy_efficiency' in stats
        
        assert stats['subtree_size'] == 1
    
    def test_get_strategy_stats_with_none_node(self):
        """Test de récupération des statistiques avec nœud None."""
        strategy = ConcreteBalancingStrategy()
        
        stats = strategy.get_strategy_stats(None)
        
        assert 'error' in stats
        assert stats['error'] == 'Node is None'
    
    def test_validate_consistency_with_valid_node(self):
        """Test de validation de cohérence avec nœud valide."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        result = strategy.validate_consistency(node)
        
        assert result is True
    
    def test_validate_consistency_with_none_node(self):
        """Test de validation de cohérence avec nœud None."""
        strategy = ConcreteBalancingStrategy()
        
        result = strategy.validate_consistency(None)
        
        assert result is True
    
    def test_validate_properties_with_valid_node(self):
        """Test de validation des propriétés avec nœud valide."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        properties = strategy.validate_properties(node)
        
        assert 'basic_properties' in properties
        assert 'balance_properties' in properties
        assert 'specific_properties' in properties
        
        assert properties['basic_properties'] is True
        assert properties['balance_properties'] is True
        assert properties['specific_properties'] is True
    
    def test_validate_properties_with_none_node(self):
        """Test de validation des propriétés avec nœud None."""
        strategy = ConcreteBalancingStrategy()
        
        properties = strategy.validate_properties(None)
        
        assert 'error' in properties
        assert properties['error'] == 'Node is None'
    
    def test_validate_references_with_valid_tree(self):
        """Test de validation des références avec arbre valide."""
        strategy = ConcreteBalancingStrategy()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(3)
        right = BinaryTreeNode(7)
        
        root.set_left(left)
        root.set_right(right)
        
        result = strategy._validate_references(root)
        
        assert result is True
    
    def test_validate_references_with_invalid_tree(self):
        """Test de validation des références avec arbre invalide."""
        strategy = ConcreteBalancingStrategy()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(3)
        
        root.set_left(left)
        # left.parent n'est pas défini (violation)
        
        result = strategy._validate_references(root)
        
        assert result is False
    
    def test_validate_tree_properties_with_valid_bst(self):
        """Test de validation des propriétés avec BST valide."""
        strategy = ConcreteBalancingStrategy()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(3)
        right = BinaryTreeNode(7)
        
        root.left_child = left
        root.right_child = right
        
        result = strategy._validate_tree_properties(root)
        
        assert result is True
    
    def test_validate_tree_properties_with_invalid_bst(self):
        """Test de validation des propriétés avec BST invalide."""
        strategy = ConcreteBalancingStrategy()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(7)  # Violation: 7 > 5
        
        root.left_child = left
        
        result = strategy._validate_tree_properties(root)
        
        assert result is False
    
    def test_count_subtree_nodes(self):
        """Test de comptage des nœuds du sous-arbre."""
        strategy = ConcreteBalancingStrategy()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(3)
        right = BinaryTreeNode(7)
        
        root.set_left(left)
        root.set_right(right)
        
        count = strategy._count_subtree_nodes(root)
        
        assert count == 3
    
    def test_count_subtree_nodes_with_none(self):
        """Test de comptage des nœuds avec nœud None."""
        strategy = ConcreteBalancingStrategy()
        
        count = strategy._count_subtree_nodes(None)
        
        assert count == 0
    
    def test_analyze_current_state(self):
        """Test d'analyse de l'état actuel."""
        strategy = ConcreteBalancingStrategy()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(3)
        
        root.set_left(left)
        
        state = strategy._analyze_current_state(root)
        
        assert state['has_left_child'] is True
        assert state['has_right_child'] is False
        assert state['has_parent'] is False
        assert state['node_type'] == 'BinaryTreeNode'
    
    def test_predict_effect(self):
        """Test de prédiction de l'effet."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        effect = strategy._predict_effect(node)
        
        assert 'will_balance' in effect
        assert 'estimated_operations' in effect
        assert 'complexity' in effect
        
        assert effect['will_balance'] is True
        assert effect['estimated_operations'] == 1
        assert effect['complexity'] == 'O(1)'
    
    def test_analyze_performance_impact(self):
        """Test d'analyse de l'impact sur les performances."""
        strategy = ConcreteBalancingStrategy()
        node = BinaryTreeNode(5)
        
        impact = strategy._analyze_performance_impact(node)
        
        assert 'current_metrics' in impact
        assert 'operation_count' in impact
        assert 'success_rate' in impact
        
        assert impact['operation_count'] == 0
        assert impact['success_rate'] == 0.0