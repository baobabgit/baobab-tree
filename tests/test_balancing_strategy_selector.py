"""
Tests unitaires pour la classe BalancingStrategySelector.

Ce module contient tous les tests unitaires pour la classe BalancingStrategySelector
et ses fonctionnalités de sélection automatique.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_tree.balanced.balancing_strategy_selector import BalancingStrategySelector
from src.baobab_tree.balanced.balancing_strategy import BalancingStrategy
from src.baobab_tree.core.exceptions import InvalidStrategyError
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode


class MockAVLNode(BinaryTreeNode):
    """Nœud AVL mock pour les tests."""
    
    def __init__(self, value: int):
        super().__init__(value)


class MockRedBlackNode(BinaryTreeNode):
    """Nœud rouge-noir mock pour les tests."""
    
    def __init__(self, value: int):
        super().__init__(value)


class TestBalancingStrategySelector:
    """Tests pour la classe BalancingStrategySelector."""
    
    def test_init(self):
        """Test de l'initialisation."""
        selector = BalancingStrategySelector()
        
        assert selector._selection_cache == {}
        assert selector._context_weights is not None
        assert len(selector._context_weights) == 5
    
    def test_select_strategy_static_method(self):
        """Test de la méthode statique select_strategy."""
        node = BinaryTreeNode(5)
        context = {'tree_type': 'avl'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy is not None
        assert isinstance(strategy, BalancingStrategy)
    
    def test_select_strategy_with_avl_context(self):
        """Test de sélection avec contexte AVL."""
        node = BinaryTreeNode(5)
        context = {'tree_type': 'avl'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_select_strategy_with_red_black_context(self):
        """Test de sélection avec contexte rouge-noir."""
        node = BinaryTreeNode(5)
        context = {'tree_type': 'red_black'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "RedBlackBalancingStrategy"
    
    def test_select_strategy_with_splay_context(self):
        """Test de sélection avec contexte Splay."""
        node = BinaryTreeNode(5)
        context = {'tree_type': 'splay'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "SplayBalancingStrategy"
    
    def test_select_strategy_with_treap_context(self):
        """Test de sélection avec contexte Treap."""
        node = BinaryTreeNode(5)
        context = {'tree_type': 'treap'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "TreapBalancingStrategy"
    
    def test_select_strategy_with_access_pattern_recent(self):
        """Test de sélection avec modèle d'accès récent."""
        node = BinaryTreeNode(5)
        context = {'access_pattern': 'recent'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "SplayBalancingStrategy"
    
    def test_select_strategy_with_memory_constraint_low(self):
        """Test de sélection avec contrainte mémoire faible."""
        node = BinaryTreeNode(5)
        context = {'memory_constraint': 'low'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "RedBlackBalancingStrategy"
    
    def test_select_strategy_with_performance_requirement_guaranteed(self):
        """Test de sélection avec exigence de performance garantie."""
        node = BinaryTreeNode(5)
        context = {'performance_requirement': 'guaranteed'}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_select_strategy_with_small_tree(self):
        """Test de sélection avec petit arbre."""
        node = BinaryTreeNode(5)
        context = {'node_count': 50}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_select_strategy_with_large_tree(self):
        """Test de sélection avec grand arbre."""
        node = BinaryTreeNode(5)
        context = {'node_count': 10000}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "RedBlackBalancingStrategy"
    
    def test_select_strategy_with_avl_node(self):
        """Test de sélection avec nœud AVL."""
        node = MockAVLNode(5)
        context = {}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_select_strategy_with_red_black_node(self):
        """Test de sélection avec nœud rouge-noir."""
        node = MockRedBlackNode(5)
        context = {}
        
        strategy = BalancingStrategySelector.select_strategy(node, context)
        
        assert strategy.__class__.__name__ == "RedBlackBalancingStrategy"
    
    def test_select_strategy_with_none_node(self):
        """Test de sélection avec nœud None."""
        context = {'tree_type': 'avl'}
        
        strategy = BalancingStrategySelector.select_strategy(None, context)
        
        assert strategy.__class__.__name__ == "AVLBalancingStrategy"
    
    def test_select_strategy_caching(self):
        """Test de mise en cache des sélections."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context = {'tree_type': 'avl'}
        
        # Première sélection
        strategy1 = selector._select_strategy_internal(node, context)
        
        # Deuxième sélection (devrait utiliser le cache)
        strategy2 = selector._select_strategy_internal(node, context)
        
        assert strategy1 is strategy2  # Même instance
        assert len(selector._selection_cache) == 1
    
    def test_generate_cache_key(self):
        """Test de génération de clé de cache."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context = {'tree_type': 'avl', 'node_count': 100}
        
        key1 = selector._generate_cache_key(node, context)
        key2 = selector._generate_cache_key(node, context)
        
        assert key1 == key2
        assert isinstance(key1, str)
        assert "BinaryTreeNode" in key1
    
    def test_generate_cache_key_different_contexts(self):
        """Test de génération de clé de cache avec contextes différents."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context1 = {'tree_type': 'avl'}
        context2 = {'tree_type': 'red_black'}
        
        key1 = selector._generate_cache_key(node, context1)
        key2 = selector._generate_cache_key(node, context2)
        
        assert key1 != key2
    
    def test_analyze_context(self):
        """Test d'analyse du contexte."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context = {
            'tree_type': 'avl',
            'node_count': 1000,
            'access_pattern': 'random',
            'memory_constraint': 'normal',
            'performance_requirement': 'balanced'
        }
        
        analysis = selector._analyze_context(node, context)
        
        assert isinstance(analysis, dict)
        assert 'tree_type' in analysis
        assert 'node_count' in analysis
        assert 'access_pattern' in analysis
        assert 'memory_constraint' in analysis
        assert 'performance_requirement' in analysis
        
        assert analysis['tree_type'] == 'avl'
        assert analysis['node_count'] == 1000
        assert analysis['access_pattern'] == 'random'
    
    def test_analyze_tree_type_from_context(self):
        """Test d'analyse du type d'arbre depuis le contexte."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context = {'tree_type': 'splay'}
        
        tree_type = selector._analyze_tree_type(node, context)
        
        assert tree_type == 'splay'
    
    def test_analyze_tree_type_from_node(self):
        """Test d'analyse du type d'arbre depuis le nœud."""
        selector = BalancingStrategySelector()
        node = MockAVLNode(5)
        context = {}
        
        tree_type = selector._analyze_tree_type(node, context)
        
        assert tree_type == 'avl'
    
    def test_analyze_tree_type_unknown(self):
        """Test d'analyse du type d'arbre inconnu."""
        selector = BalancingStrategySelector()
        node = None
        context = {}
        
        tree_type = selector._analyze_tree_type(node, context)
        
        assert tree_type == 'unknown'
    
    def test_analyze_node_count_from_context(self):
        """Test d'analyse du nombre de nœuds depuis le contexte."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context = {'node_count': 500}
        
        node_count = selector._analyze_node_count(node, context)
        
        assert node_count == 500
    
    def test_analyze_node_count_from_tree(self):
        """Test d'analyse du nombre de nœuds depuis l'arbre."""
        selector = BalancingStrategySelector()
        root = BinaryTreeNode(5)
        left = BinaryTreeNode(3)
        right = BinaryTreeNode(7)
        
        root.set_left(left)
        root.set_right(right)
        
        node_count = selector._analyze_node_count(root, {})
        
        assert node_count == 3
    
    def test_analyze_access_pattern(self):
        """Test d'analyse du modèle d'accès."""
        selector = BalancingStrategySelector()
        context = {'access_pattern': 'sequential'}
        
        pattern = selector._analyze_access_pattern(context)
        
        assert pattern == 'sequential'
    
    def test_analyze_access_pattern_default(self):
        """Test d'analyse du modèle d'accès par défaut."""
        selector = BalancingStrategySelector()
        context = {}
        
        pattern = selector._analyze_access_pattern(context)
        
        assert pattern == 'random'
    
    def test_analyze_memory_constraint(self):
        """Test d'analyse des contraintes mémoire."""
        selector = BalancingStrategySelector()
        context = {'memory_constraint': 'high'}
        
        constraint = selector._analyze_memory_constraint(context)
        
        assert constraint == 'high'
    
    def test_analyze_memory_constraint_default(self):
        """Test d'analyse des contraintes mémoire par défaut."""
        selector = BalancingStrategySelector()
        context = {}
        
        constraint = selector._analyze_memory_constraint(context)
        
        assert constraint == 'normal'
    
    def test_analyze_performance_requirement(self):
        """Test d'analyse des exigences de performance."""
        selector = BalancingStrategySelector()
        context = {'performance_requirement': 'high'}
        
        requirement = selector._analyze_performance_requirement(context)
        
        assert requirement == 'high'
    
    def test_analyze_performance_requirement_default(self):
        """Test d'analyse des exigences de performance par défaut."""
        selector = BalancingStrategySelector()
        context = {}
        
        requirement = selector._analyze_performance_requirement(context)
        
        assert requirement == 'balanced'
    
    def test_select_strategy_type_avl(self):
        """Test de sélection du type de stratégie AVL."""
        selector = BalancingStrategySelector()
        analysis = {'tree_type': 'avl'}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'avl'
    
    def test_select_strategy_type_red_black(self):
        """Test de sélection du type de stratégie rouge-noir."""
        selector = BalancingStrategySelector()
        analysis = {'tree_type': 'red_black'}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'red_black'
    
    def test_select_strategy_type_splay(self):
        """Test de sélection du type de stratégie Splay."""
        selector = BalancingStrategySelector()
        analysis = {'tree_type': 'splay'}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'splay'
    
    def test_select_strategy_type_treap(self):
        """Test de sélection du type de stratégie Treap."""
        selector = BalancingStrategySelector()
        analysis = {'tree_type': 'treap'}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'treap'
    
    def test_select_strategy_type_recent_access(self):
        """Test de sélection du type de stratégie avec accès récent."""
        selector = BalancingStrategySelector()
        analysis = {'access_pattern': 'recent'}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'splay'
    
    def test_select_strategy_type_low_memory(self):
        """Test de sélection du type de stratégie avec mémoire faible."""
        selector = BalancingStrategySelector()
        analysis = {'memory_constraint': 'low'}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'red_black'
    
    def test_select_strategy_type_guaranteed_performance(self):
        """Test de sélection du type de stratégie avec performance garantie."""
        selector = BalancingStrategySelector()
        analysis = {'performance_requirement': 'guaranteed'}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'avl'
    
    def test_select_strategy_type_small_tree(self):
        """Test de sélection du type de stratégie avec petit arbre."""
        selector = BalancingStrategySelector()
        analysis = {'node_count': 50}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'avl'
    
    def test_select_strategy_type_large_tree(self):
        """Test de sélection du type de stratégie avec grand arbre."""
        selector = BalancingStrategySelector()
        analysis = {'node_count': 10000}
        
        strategy_type = selector._select_strategy_type(analysis)
        
        assert strategy_type == 'red_black'
    
    def test_clear_cache(self):
        """Test de vidage du cache."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context = {'tree_type': 'avl'}
        
        # Ajouter au cache
        selector._select_strategy_internal(node, context)
        assert len(selector._selection_cache) > 0
        
        # Vider le cache
        selector.clear_cache()
        assert len(selector._selection_cache) == 0
    
    def test_get_cache_stats(self):
        """Test de récupération des statistiques du cache."""
        selector = BalancingStrategySelector()
        node = BinaryTreeNode(5)
        context = {'tree_type': 'avl'}
        
        # Ajouter au cache
        selector._select_strategy_internal(node, context)
        
        stats = selector.get_cache_stats()
        
        assert isinstance(stats, dict)
        assert 'cache_size' in stats
        assert 'cached_strategies' in stats
        assert stats['cache_size'] == 1
        assert isinstance(stats['cached_strategies'], list)