"""
Tests unitaires pour la classe AVLOptimizations.

Ce module contient tous les tests unitaires pour valider le bon fonctionnement
de la classe AVLOptimizations et de ses optimisations AVL.
"""

import pytest
import time
from typing import List

from src.baobab_tree.balanced.avl_optimizations import (
    AVLOptimizations,
    ObjectPool,
    CacheMetrics,
    LRUCache,
    PerformanceMonitor,
)
from src.baobab_tree.balanced.avl_tree import AVLTree
from src.baobab_tree.balanced.avl_node import AVLNode
from src.baobab_tree.core.exceptions import (
    AVLOptimizationError,
    CacheError,
    MemoryOptimizationError,
    PerformanceOptimizationError,
)


class TestObjectPool:
    """Tests pour la classe ObjectPool."""
    
    def test_pool_creation(self):
        """Test de création d'un pool d'objets."""
        pool = ObjectPool(size=100)
        assert pool._size == 100
        assert len(pool._pool) == 100
        assert len(pool._available) == 100
        assert len(pool._in_use) == 0
    
    def test_get_node(self):
        """Test de récupération d'un nœud du pool."""
        pool = ObjectPool(size=10)
        node = pool.get_node(42)
        
        assert node is not None
        assert node.value == 42
        assert node.balance_factor == 0
        assert node.height == 0
        assert len(pool._available) == 9
        assert len(pool._in_use) == 1
    
    def test_get_node_empty_pool(self):
        """Test de récupération d'un nœud quand le pool est vide."""
        pool = ObjectPool(size=1)
        pool.get_node(1)  # Utiliser le seul nœud disponible
        node = pool.get_node(2)  # Essayer de récupérer un autre nœud
        
        assert node is None
    
    def test_return_node(self):
        """Test de retour d'un nœud au pool."""
        pool = ObjectPool(size=10)
        node = pool.get_node(42)
        
        pool.return_node(node)
        
        assert len(pool._available) == 10
        assert len(pool._in_use) == 0
        assert node.value is None
        assert node.balance_factor == 0
    
    def test_pool_stats(self):
        """Test des statistiques du pool."""
        pool = ObjectPool(size=100)
        
        # Utiliser quelques nœuds
        for i in range(30):
            pool.get_node(i)
        
        stats = pool.get_stats()
        
        assert stats["total_size"] == 100
        assert stats["available"] == 70
        assert stats["in_use"] == 30
        assert stats["utilization_rate"] == 0.3


class TestCacheMetrics:
    """Tests pour la classe CacheMetrics."""
    
    def test_metrics_initialization(self):
        """Test d'initialisation des métriques."""
        metrics = CacheMetrics()
        
        assert metrics._hits == 0
        assert metrics._misses == 0
        assert metrics._evictions == 0
        assert metrics._insertions == 0
    
    def test_record_hit(self):
        """Test d'enregistrement d'un hit."""
        metrics = CacheMetrics()
        metrics.record_hit()
        
        assert metrics._hits == 1
        assert metrics.get_hit_rate() == 1.0
    
    def test_record_miss(self):
        """Test d'enregistrement d'un miss."""
        metrics = CacheMetrics()
        metrics.record_miss()
        
        assert metrics._misses == 1
        assert metrics.get_hit_rate() == 0.0
    
    def test_hit_rate_calculation(self):
        """Test du calcul du taux de hit."""
        metrics = CacheMetrics()
        
        # 3 hits, 2 misses
        for _ in range(3):
            metrics.record_hit()
        for _ in range(2):
            metrics.record_miss()
        
        assert metrics.get_hit_rate() == 0.6
    
    def test_get_stats(self):
        """Test des statistiques complètes."""
        metrics = CacheMetrics()
        
        metrics.record_hit()
        metrics.record_miss()
        metrics.record_eviction()
        metrics.record_insertion()
        
        stats = metrics.get_stats()
        
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["evictions"] == 1
        assert stats["insertions"] == 1
        assert stats["hit_rate"] == 0.5
        assert "uptime" in stats
        assert "hits_per_second" in stats
        assert "misses_per_second" in stats


class TestLRUCache:
    """Tests pour la classe LRUCache."""
    
    def test_cache_creation(self):
        """Test de création d'un cache LRU."""
        cache = LRUCache(max_size=10)
        
        assert cache._max_size == 10
        assert len(cache._cache) == 0
        assert len(cache._access_order) == 0
    
    def test_put_and_get(self):
        """Test d'ajout et de récupération dans le cache."""
        cache = LRUCache(max_size=10)
        
        cache.put("key1", "value1")
        value = cache.get("key1")
        
        assert value == "value1"
        assert len(cache._cache) == 1
        assert "key1" in cache._access_order
    
    def test_get_nonexistent_key(self):
        """Test de récupération d'une clé inexistante."""
        cache = LRUCache(max_size=10)
        
        value = cache.get("nonexistent")
        
        assert value is None
    
    def test_lru_eviction(self):
        """Test de l'éviction LRU."""
        cache = LRUCache(max_size=2)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")  # Devrait évincer key1
        
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
    
    def test_access_order_update(self):
        """Test de mise à jour de l'ordre d'accès."""
        cache = LRUCache(max_size=2)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        
        # Accéder à key1 pour le rendre récent
        cache.get("key1")
        
        cache.put("key3", "value3")  # Devrait évincer key2
        
        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None
        assert cache.get("key3") == "value3"
    
    def test_clear_cache(self):
        """Test de vidage du cache."""
        cache = LRUCache(max_size=10)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        
        cache.clear()
        
        assert len(cache._cache) == 0
        assert len(cache._access_order) == 0
        assert cache.get("key1") is None
        assert cache.get("key2") is None
    
    def test_cache_stats(self):
        """Test des statistiques du cache."""
        cache = LRUCache(max_size=10)
        
        cache.put("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        
        stats = cache.get_stats()
        
        assert stats["max_size"] == 10
        assert stats["current_size"] == 1
        assert stats["utilization_rate"] == 0.1
        assert stats["hits"] == 1
        assert stats["misses"] == 1


class TestPerformanceMonitor:
    """Tests pour la classe PerformanceMonitor."""
    
    def test_monitor_initialization(self):
        """Test d'initialisation du moniteur."""
        monitor = PerformanceMonitor()
        
        assert len(monitor._operation_times) == 0
        assert len(monitor._operation_counts) == 0
        assert len(monitor._memory_usage) == 0
    
    def test_record_operation(self):
        """Test d'enregistrement d'une opération."""
        monitor = PerformanceMonitor()
        
        monitor.record_operation("insert", 0.001)
        
        assert "insert" in monitor._operation_times
        assert monitor._operation_counts["insert"] == 1
        assert len(monitor._operation_times["insert"]) == 1
    
    def test_record_memory_usage(self):
        """Test d'enregistrement de l'utilisation mémoire."""
        monitor = PerformanceMonitor()
        
        monitor.record_memory_usage(1024)
        
        assert len(monitor._memory_usage) == 1
        assert monitor._memory_usage[0] == 1024
    
    def test_get_operation_stats(self):
        """Test des statistiques d'opération."""
        monitor = PerformanceMonitor()
        
        # Enregistrer plusieurs opérations
        monitor.record_operation("insert", 0.001)
        monitor.record_operation("insert", 0.002)
        monitor.record_operation("insert", 0.003)
        
        stats = monitor.get_operation_stats("insert")
        
        assert stats["count"] == 3
        assert stats["total_time"] == 0.006
        assert stats["average_time"] == 0.002
        assert stats["min_time"] == 0.001
        assert stats["max_time"] == 0.003
    
    def test_get_operation_stats_nonexistent(self):
        """Test des statistiques d'une opération inexistante."""
        monitor = PerformanceMonitor()
        
        stats = monitor.get_operation_stats("nonexistent")
        
        assert stats == {}
    
    def test_get_all_stats(self):
        """Test de toutes les statistiques."""
        monitor = PerformanceMonitor()
        
        monitor.record_operation("insert", 0.001)
        monitor.record_memory_usage(1024)
        
        stats = monitor.get_all_stats()
        
        assert "uptime" in stats
        assert "operations" in stats
        assert "memory" in stats
        assert "insert" in stats["operations"]
        assert stats["memory"]["current"] == 1024


class TestAVLOptimizations:
    """Tests pour la classe AVLOptimizations."""
    
    def test_create_node_pool(self):
        """Test de création d'un pool de nœuds."""
        pool = AVLOptimizations.create_node_pool(size=50)
        
        assert isinstance(pool, ObjectPool)
        assert pool._size == 50
        assert len(pool._pool) == 50
    
    def test_create_node_pool_invalid_size(self):
        """Test de création d'un pool avec une taille invalide."""
        with pytest.raises(MemoryOptimizationError):
            AVLOptimizations.create_node_pool(size=-1)
    
    def test_reuse_node(self):
        """Test de réutilisation d'un nœud."""
        node = AVLNode(10)
        node._balance_factor = 1
        node._cached_height = 2
        
        reused_node = AVLOptimizations.reuse_node(node, 20)
        
        assert reused_node.value == 20
        assert reused_node.balance_factor == 0
        assert reused_node.height == 0
        assert reused_node.parent is None
        assert reused_node.left is None
        assert reused_node.right is None
    
    def test_reuse_node_invalid_type(self):
        """Test de réutilisation d'un nœud de type invalide."""
        with pytest.raises(MemoryOptimizationError):
            AVLOptimizations.reuse_node("not_a_node", 20)
    
    def test_optimize_memory_usage(self):
        """Test d'optimisation de l'utilisation mémoire."""
        tree = AVLTree()
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        
        report = AVLOptimizations.optimize_memory_usage(tree)
        
        assert "current_size" in report
        assert "current_height" in report
        assert "theoretical_memory_usage" in report
        assert "height_efficiency" in report
        assert "optimizations_available" in report
        assert "recommendations" in report
        assert report["current_size"] == 3
    
    def test_optimize_memory_usage_invalid_tree(self):
        """Test d'optimisation avec un arbre invalide."""
        with pytest.raises(MemoryOptimizationError):
            AVLOptimizations.optimize_memory_usage("not_a_tree")
    
    def test_enable_height_cache(self):
        """Test d'activation du cache de hauteurs."""
        tree = AVLTree()
        tree.insert(10)
        
        AVLOptimizations.enable_height_cache(tree)
        
        assert hasattr(tree, '_height_cache')
        assert hasattr(tree, '_height_cache_enabled')
        assert tree._height_cache_enabled is True
    
    def test_enable_height_cache_invalid_tree(self):
        """Test d'activation du cache avec un arbre invalide."""
        with pytest.raises(PerformanceOptimizationError):
            AVLOptimizations.enable_height_cache("not_a_tree")
    
    def test_enable_balance_factor_cache(self):
        """Test d'activation du cache de facteurs d'équilibre."""
        tree = AVLTree()
        tree.insert(10)
        
        AVLOptimizations.enable_balance_factor_cache(tree)
        
        assert hasattr(tree, '_balance_factor_cache')
        assert hasattr(tree, '_balance_factor_cache_enabled')
        assert tree._balance_factor_cache_enabled is True
    
    def test_enable_balance_factor_cache_invalid_tree(self):
        """Test d'activation du cache avec un arbre invalide."""
        with pytest.raises(PerformanceOptimizationError):
            AVLOptimizations.enable_balance_factor_cache("not_a_tree")
    
    def test_optimize_rotations(self):
        """Test d'optimisation des rotations."""
        tree = AVLTree()
        tree.insert(10)
        
        AVLOptimizations.optimize_rotations(tree)
        
        assert hasattr(tree, '_rotation_optimization_enabled')
        assert hasattr(tree, '_rotation_cache')
        assert tree._rotation_optimization_enabled is True
    
    def test_optimize_rotations_invalid_tree(self):
        """Test d'optimisation des rotations avec un arbre invalide."""
        with pytest.raises(PerformanceOptimizationError):
            AVLOptimizations.optimize_rotations("not_a_tree")
    
    def test_monitor_performance(self):
        """Test de monitoring des performances."""
        tree = AVLTree()
        tree.insert(10)
        
        monitor = AVLOptimizations.monitor_performance(tree)
        
        assert isinstance(monitor, PerformanceMonitor)
        assert hasattr(tree, '_performance_monitor')
        assert hasattr(tree, '_performance_monitoring_enabled')
        assert tree._performance_monitoring_enabled is True
    
    def test_monitor_performance_invalid_tree(self):
        """Test de monitoring avec un arbre invalide."""
        with pytest.raises(PerformanceOptimizationError):
            AVLOptimizations.monitor_performance("not_a_tree")
    
    def test_analyze_metrics(self):
        """Test d'analyse des métriques."""
        tree = AVLTree()
        tree.insert(10)
        tree.insert(20)
        
        # Activer le monitoring
        AVLOptimizations.monitor_performance(tree)
        
        analysis = AVLOptimizations.analyze_metrics(tree)
        
        assert "tree_stats" in analysis
        assert "performance_stats" in analysis
        assert "recommendations" in analysis
        assert analysis["tree_stats"]["size"] == 2
    
    def test_analyze_metrics_no_monitoring(self):
        """Test d'analyse des métriques sans monitoring activé."""
        tree = AVLTree()
        tree.insert(10)
        
        analysis = AVLOptimizations.analyze_metrics(tree)
        
        assert "error" in analysis
        assert "Performance monitoring not enabled" in analysis["error"]
    
    def test_analyze_metrics_invalid_tree(self):
        """Test d'analyse des métriques avec un arbre invalide."""
        with pytest.raises(PerformanceOptimizationError):
            AVLOptimizations.analyze_metrics("not_a_tree")
    
    def test_get_optimization_recommendations(self):
        """Test des recommandations d'optimisation."""
        tree = AVLTree()
        
        # Créer un arbre avec beaucoup d'éléments
        for i in range(100):
            tree.insert(i)
        
        recommendations = AVLOptimizations.get_optimization_recommendations(tree)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert any("batch operations" in rec for rec in recommendations)
    
    def test_get_optimization_recommendations_invalid_tree(self):
        """Test des recommandations avec un arbre invalide."""
        with pytest.raises(PerformanceOptimizationError):
            AVLOptimizations.get_optimization_recommendations("not_a_tree")
    
    def test_integration_optimizations(self):
        """Test d'intégration de plusieurs optimisations."""
        tree = AVLTree()
        
        # Activer plusieurs optimisations
        AVLOptimizations.enable_height_cache(tree)
        AVLOptimizations.enable_balance_factor_cache(tree)
        AVLOptimizations.optimize_rotations(tree)
        monitor = AVLOptimizations.monitor_performance(tree)
        
        # Insérer des éléments
        for i in range(50):
            tree.insert(i)
        
        # Vérifier que les optimisations sont actives
        assert tree._height_cache_enabled is True
        assert tree._balance_factor_cache_enabled is True
        assert tree._rotation_optimization_enabled is True
        assert tree._performance_monitoring_enabled is True
        
        # Analyser les métriques
        analysis = AVLOptimizations.analyze_metrics(tree)
        assert "tree_stats" in analysis
        
        # Obtenir les recommandations
        recommendations = AVLOptimizations.get_optimization_recommendations(tree)
        assert len(recommendations) > 0


class TestAVLOptimizationsErrorHandling:
    """Tests de gestion d'erreurs pour AVLOptimizations."""
    
    def test_avl_optimization_error(self):
        """Test de l'exception AVLOptimizationError."""
        error = AVLOptimizationError("Test error", "test_operation")
        
        assert str(error) == "Test error (Operation: test_operation)"
        assert error.operation == "test_operation"
    
    def test_cache_error(self):
        """Test de l'exception CacheError."""
        error = CacheError("Cache error", "cache_operation", "test_key")
        
        assert "Cache error" in str(error)
        assert "test_key" in str(error)
        assert error.cache_key == "test_key"
    
    def test_memory_optimization_error(self):
        """Test de l'exception MemoryOptimizationError."""
        error = MemoryOptimizationError("Memory error", "memory_operation", 1024)
        
        assert "Memory error" in str(error)
        assert "1024 bytes" in str(error)
        assert error.memory_usage == 1024
    
    def test_performance_optimization_error(self):
        """Test de l'exception PerformanceOptimizationError."""
        error = PerformanceOptimizationError("Performance error", "perf_operation", "cpu_time")
        
        assert "Performance error" in str(error)
        assert "cpu_time" in str(error)
        assert error.performance_metric == "cpu_time"


if __name__ == "__main__":
    pytest.main([__file__])