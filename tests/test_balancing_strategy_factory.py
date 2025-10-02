"""
Tests unitaires pour la classe BalancingStrategyFactory.

Ce module contient tous les tests unitaires pour la classe BalancingStrategyFactory
et ses fonctionnalités de création de stratégies.
"""

import pytest

from src.baobab_tree.balanced.balancing_strategy_factory import BalancingStrategyFactory
from src.baobab_tree.balanced.balancing_strategy import BalancingStrategy
from src.baobab_tree.core.exceptions import InvalidStrategyError


class TestBalancingStrategyFactory:
    """Tests pour la classe BalancingStrategyFactory."""
    
    def test_create_strategy_avl(self):
        """Test de création de stratégie AVL."""
        strategy = BalancingStrategyFactory.create_strategy("avl")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_create_strategy_red_black(self):
        """Test de création de stratégie rouge-noir."""
        strategy = BalancingStrategyFactory.create_strategy("red_black")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "RedBlackBalancingStrategy"
    
    def test_create_strategy_redblack(self):
        """Test de création de stratégie rouge-noir avec alias."""
        strategy = BalancingStrategyFactory.create_strategy("redblack")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "RedBlackBalancingStrategy"
    
    def test_create_strategy_rb(self):
        """Test de création de stratégie rouge-noir avec alias court."""
        strategy = BalancingStrategyFactory.create_strategy("rb")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "RedBlackBalancingStrategy"
    
    def test_create_strategy_splay(self):
        """Test de création de stratégie Splay."""
        strategy = BalancingStrategyFactory.create_strategy("splay")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "SplayBalancingStrategy"
    
    def test_create_strategy_treap(self):
        """Test de création de stratégie Treap."""
        strategy = BalancingStrategyFactory.create_strategy("treap")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "TreapBalancingStrategy"
    
    def test_create_strategy_case_insensitive(self):
        """Test de création de stratégie insensible à la casse."""
        strategy = BalancingStrategyFactory.create_strategy("AVL")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_create_strategy_with_whitespace(self):
        """Test de création de stratégie avec espaces."""
        strategy = BalancingStrategyFactory.create_strategy("  avl  ")
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_create_strategy_invalid_type(self):
        """Test de création de stratégie avec type invalide."""
        with pytest.raises(InvalidStrategyError) as exc_info:
            BalancingStrategyFactory.create_strategy("invalid")
        
        assert "Type de stratégie invalide" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)
    
    def test_create_strategy_empty_type(self):
        """Test de création de stratégie avec type vide."""
        with pytest.raises(InvalidStrategyError):
            BalancingStrategyFactory.create_strategy("")
    
    def test_create_strategy_none_type(self):
        """Test de création de stratégie avec type None."""
        with pytest.raises(InvalidStrategyError):
            BalancingStrategyFactory.create_strategy(None)
    
    def test_get_available_strategies(self):
        """Test de récupération des stratégies disponibles."""
        strategies = BalancingStrategyFactory.get_available_strategies()
        
        assert isinstance(strategies, list)
        assert "avl" in strategies
        assert "red_black" in strategies
        assert "redblack" in strategies
        assert "rb" in strategies
        assert "splay" in strategies
        assert "treap" in strategies
    
    def test_is_strategy_available_valid(self):
        """Test de vérification de disponibilité avec stratégie valide."""
        assert BalancingStrategyFactory.is_strategy_available("avl") is True
        assert BalancingStrategyFactory.is_strategy_available("red_black") is True
        assert BalancingStrategyFactory.is_strategy_available("splay") is True
        assert BalancingStrategyFactory.is_strategy_available("treap") is True
    
    def test_is_strategy_available_invalid(self):
        """Test de vérification de disponibilité avec stratégie invalide."""
        assert BalancingStrategyFactory.is_strategy_available("invalid") is False
        assert BalancingStrategyFactory.is_strategy_available("") is False
        assert BalancingStrategyFactory.is_strategy_available(None) is False
    
    def test_is_strategy_available_case_insensitive(self):
        """Test de vérification de disponibilité insensible à la casse."""
        assert BalancingStrategyFactory.is_strategy_available("AVL") is True
        assert BalancingStrategyFactory.is_strategy_available("  avl  ") is True
    
    def test_register_strategy_valid(self):
        """Test d'enregistrement de stratégie valide."""
        class CustomStrategy(BalancingStrategy):
            def balance(self, node):
                return node
            
            def can_balance(self, node):
                return True
            
            def get_description(self):
                return "Custom Strategy"
            
            def get_complexity(self):
                return "O(1)"
        
        BalancingStrategyFactory.register_strategy("custom", CustomStrategy)
        
        assert BalancingStrategyFactory.is_strategy_available("custom") is True
        
        strategy = BalancingStrategyFactory.create_strategy("custom")
        assert isinstance(strategy, CustomStrategy)
        
        # Nettoyer
        BalancingStrategyFactory.unregister_strategy("custom")
    
    def test_register_strategy_invalid_class(self):
        """Test d'enregistrement de stratégie avec classe invalide."""
        class InvalidClass:
            pass
        
        with pytest.raises(InvalidStrategyError) as exc_info:
            BalancingStrategyFactory.register_strategy("invalid", InvalidClass)
        
        assert "Classe de stratégie invalide" in str(exc_info.value)
    
    def test_unregister_strategy_valid(self):
        """Test de désenregistrement de stratégie valide."""
        # Enregistrer d'abord
        class CustomStrategy(BalancingStrategy):
            def balance(self, node):
                return node
            
            def can_balance(self, node):
                return True
            
            def get_description(self):
                return "Custom Strategy"
            
            def get_complexity(self):
                return "O(1)"
        
        BalancingStrategyFactory.register_strategy("temp", CustomStrategy)
        assert BalancingStrategyFactory.is_strategy_available("temp") is True
        
        # Désenregistrer
        BalancingStrategyFactory.unregister_strategy("temp")
        assert BalancingStrategyFactory.is_strategy_available("temp") is False
    
    def test_unregister_strategy_invalid(self):
        """Test de désenregistrement de stratégie invalide."""
        with pytest.raises(InvalidStrategyError) as exc_info:
            BalancingStrategyFactory.unregister_strategy("nonexistent")
        
        assert "Stratégie non enregistrée" in str(exc_info.value)
    
    def test_get_strategy_info_valid(self):
        """Test de récupération d'informations sur stratégie valide."""
        info = BalancingStrategyFactory.get_strategy_info("avl")
        
        assert isinstance(info, dict)
        assert info['type'] == 'avl'
        assert info['class_name'] == 'AVLBalancingStrategy'
        assert 'description' in info
        assert 'complexity' in info
        assert "AVL" in info['description']
    
    def test_get_strategy_info_invalid(self):
        """Test de récupération d'informations sur stratégie invalide."""
        with pytest.raises(InvalidStrategyError):
            BalancingStrategyFactory.get_strategy_info("invalid")
    
    def test_create_all_strategies(self):
        """Test de création de toutes les stratégies."""
        strategies = BalancingStrategyFactory.create_all_strategies()
        
        assert isinstance(strategies, dict)
        assert len(strategies) > 0
        
        for strategy_type, strategy in strategies.items():
            assert isinstance(strategy_type, str)
            assert isinstance(strategy, BalancingStrategy)
        
        # Vérifier que les stratégies principales sont présentes
        assert "avl" in strategies
        assert "red_black" in strategies
        assert "splay" in strategies
        assert "treap" in strategies