"""
Optimisations spécifiques pour les arbres AVL.

Ce module implémente la classe AVLOptimizations contenant toutes les optimisations
spécifiques pour améliorer les performances des arbres AVL.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .avl_tree import AVLTree
from .avl_node import AVLNode
from ..core.exceptions import (
    AVLError,
    AVLOptimizationError,
    CacheError,
    MemoryOptimizationError,
    PerformanceOptimizationError,
)
from ..core.interfaces import T

if TYPE_CHECKING:
    pass


class ObjectPool:
    """
    Pool d'objets pour réutiliser les nœuds AVL.
    
    Cette classe implémente un pool d'objets simple pour éviter
    les allocations/désallocations fréquentes de nœuds AVL.
    """
    
    def __init__(self, size: int = 1000):
        """
        Initialise un pool d'objets.
        
        :param size: Taille du pool
        :type size: int
        """
        self._size = size
        self._pool: List[AVLNode] = []
        self._available: List[AVLNode] = []
        self._in_use: List[AVLNode] = []
        
        # Initialiser le pool avec des nœuds vides
        for _ in range(size):
            node = AVLNode(None)  # Nœud avec valeur None
            self._pool.append(node)
            self._available.append(node)
    
    def get_node(self, value: T) -> Optional[AVLNode[T]]:
        """
        Récupère un nœud du pool.
        
        :param value: Valeur pour le nœud
        :type value: T
        :return: Nœud du pool ou None si pool vide
        :rtype: Optional[AVLNode[T]]
        """
        if not self._available:
            return None
        
        node = self._available.pop()
        node._value = value
        node._balance_factor = 0
        node._cached_height = 0
        node._parent = None
        node._left = None
        node._right = None
        node._children = []
        node._metadata = {}
        
        self._in_use.append(node)
        return node
    
    def return_node(self, node: AVLNode[T]) -> None:
        """
        Retourne un nœud au pool.
        
        :param node: Nœud à retourner
        :type node: AVLNode[T]
        """
        if node in self._in_use:
            self._in_use.remove(node)
            # Réinitialiser le nœud
            node._value = None
            node._balance_factor = 0
            node._cached_height = 0
            node._parent = None
            node._left = None
            node._right = None
            node._children = []
            node._metadata = {}
            self._available.append(node)
    
    def get_stats(self) -> Dict[str, int]:
        """
        Retourne les statistiques du pool.
        
        :return: Statistiques du pool
        :rtype: Dict[str, int]
        """
        return {
            "total_size": self._size,
            "available": len(self._available),
            "in_use": len(self._in_use),
            "utilization_rate": len(self._in_use) / self._size if self._size > 0 else 0
        }


class CacheMetrics:
    """
    Métriques de cache pour les optimisations AVL.
    
    Cette classe collecte et analyse les métriques de performance
    des différents caches utilisés dans les optimisations AVL.
    """
    
    def __init__(self):
        """Initialise les métriques de cache."""
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._insertions = 0
        self._start_time = time.time()
    
    def record_hit(self) -> None:
        """Enregistre un hit de cache."""
        self._hits += 1
    
    def record_miss(self) -> None:
        """Enregistre un miss de cache."""
        self._misses += 1
    
    def record_eviction(self) -> None:
        """Enregistre une éviction de cache."""
        self._evictions += 1
    
    def record_insertion(self) -> None:
        """Enregistre une insertion dans le cache."""
        self._insertions += 1
    
    def get_hit_rate(self) -> float:
        """
        Calcule le taux de hit du cache.
        
        :return: Taux de hit (0.0 à 1.0)
        :rtype: float
        """
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques complètes du cache.
        
        :return: Statistiques du cache
        :rtype: Dict[str, Any]
        """
        uptime = time.time() - self._start_time
        return {
            "hits": self._hits,
            "misses": self._misses,
            "evictions": self._evictions,
            "insertions": self._insertions,
            "hit_rate": self.get_hit_rate(),
            "uptime": uptime,
            "hits_per_second": self._hits / uptime if uptime > 0 else 0,
            "misses_per_second": self._misses / uptime if uptime > 0 else 0
        }


class LRUCache:
    """
    Cache LRU (Least Recently Used) pour les optimisations AVL.
    
    Cette classe implémente un cache LRU simple pour mettre en cache
    les résultats de calculs coûteux dans les arbres AVL.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialise un cache LRU.
        
        :param max_size: Taille maximale du cache
        :type max_size: int
        """
        self._max_size = max_size
        self._cache: Dict[str, Any] = {}
        self._access_order: List[str] = []
        self._metrics = CacheMetrics()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Récupère une valeur du cache.
        
        :param key: Clé de la valeur
        :type key: str
        :return: Valeur mise en cache ou None
        :rtype: Optional[Any]
        """
        if key in self._cache:
            # Mettre à jour l'ordre d'accès
            self._access_order.remove(key)
            self._access_order.append(key)
            self._metrics.record_hit()
            return self._cache[key]
        
        self._metrics.record_miss()
        return None
    
    def put(self, key: str, value: Any) -> None:
        """
        Met une valeur dans le cache.
        
        :param key: Clé de la valeur
        :type key: str
        :param value: Valeur à mettre en cache
        :type value: Any
        """
        if key in self._cache:
            # Mettre à jour l'ordre d'accès
            self._access_order.remove(key)
            self._access_order.append(key)
        else:
            # Nouvelle entrée
            if len(self._cache) >= self._max_size:
                # Éviction LRU
                oldest_key = self._access_order.pop(0)
                del self._cache[oldest_key]
                self._metrics.record_eviction()
            
            self._cache[key] = value
            self._access_order.append(key)
            self._metrics.record_insertion()
    
    def clear(self) -> None:
        """Vide le cache."""
        self._cache.clear()
        self._access_order.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques du cache.
        
        :return: Statistiques du cache
        :rtype: Dict[str, Any]
        """
        stats = self._metrics.get_stats()
        stats.update({
            "max_size": self._max_size,
            "current_size": len(self._cache),
            "utilization_rate": len(self._cache) / self._max_size if self._max_size > 0 else 0
        })
        return stats


class PerformanceMonitor:
    """
    Moniteur de performance pour les arbres AVL.
    
    Cette classe collecte et analyse les métriques de performance
    des opérations sur les arbres AVL.
    """
    
    def __init__(self):
        """Initialise le moniteur de performance."""
        self._operation_times: Dict[str, List[float]] = {}
        self._operation_counts: Dict[str, int] = {}
        self._memory_usage: List[int] = []
        self._start_time = time.time()
    
    def record_operation(self, operation: str, duration: float) -> None:
        """
        Enregistre une opération et sa durée.
        
        :param operation: Nom de l'opération
        :type operation: str
        :param duration: Durée de l'opération en secondes
        :type duration: float
        """
        if operation not in self._operation_times:
            self._operation_times[operation] = []
            self._operation_counts[operation] = 0
        
        self._operation_times[operation].append(duration)
        self._operation_counts[operation] += 1
    
    def record_memory_usage(self, usage: int) -> None:
        """
        Enregistre l'utilisation mémoire.
        
        :param usage: Utilisation mémoire en bytes
        :type usage: int
        """
        self._memory_usage.append(usage)
    
    def get_operation_stats(self, operation: str) -> Dict[str, Any]:
        """
        Retourne les statistiques d'une opération.
        
        :param operation: Nom de l'opération
        :type operation: str
        :return: Statistiques de l'opération
        :rtype: Dict[str, Any]
        """
        if operation not in self._operation_times:
            return {}
        
        times = self._operation_times[operation]
        return {
            "count": self._operation_counts[operation],
            "total_time": sum(times),
            "average_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "times_per_second": len(times) / (time.time() - self._start_time) if time.time() - self._start_time > 0 else 0
        }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """
        Retourne toutes les statistiques.
        
        :return: Toutes les statistiques
        :rtype: Dict[str, Any]
        """
        stats = {
            "uptime": time.time() - self._start_time,
            "operations": {},
            "memory": {
                "current": self._memory_usage[-1] if self._memory_usage else 0,
                "peak": max(self._memory_usage) if self._memory_usage else 0,
                "average": sum(self._memory_usage) / len(self._memory_usage) if self._memory_usage else 0
            }
        }
        
        for operation in self._operation_times:
            stats["operations"][operation] = self.get_operation_stats(operation)
        
        return stats


class AVLOptimizations:
    """
    Classe utilitaire contenant toutes les optimisations AVL.
    
    Cette classe fournit des méthodes statiques pour optimiser
    les performances des arbres AVL dans différents domaines :
    mémoire, performance, accès, insertion, suppression et recherche.
    """
    
    # Pools d'objets globaux
    _node_pools: Dict[str, ObjectPool] = {}
    
    # Caches globaux
    _height_caches: Dict[str, LRUCache] = {}
    _balance_factor_caches: Dict[str, LRUCache] = {}
    _search_caches: Dict[str, LRUCache] = {}
    
    # Moniteurs de performance
    _performance_monitors: Dict[str, PerformanceMonitor] = {}
    
    @staticmethod
    def create_node_pool(size: int = 1000) -> ObjectPool:
        """
        Crée un pool d'objets pour réutiliser les nœuds AVL.
        
        :param size: Taille du pool
        :type size: int
        :return: Pool d'objets créé
        :rtype: ObjectPool
        :raises MemoryOptimizationError: Si la création du pool échoue
        """
        try:
            pool_id = f"pool_{len(AVLOptimizations._node_pools)}"
            pool = ObjectPool(size)
            AVLOptimizations._node_pools[pool_id] = pool
            return pool
        except Exception as e:
            raise MemoryOptimizationError(
                f"Failed to create node pool: {str(e)}",
                "create_node_pool",
            ) from e
    
    @staticmethod
    def reuse_node(node: AVLNode[T], new_value: T) -> AVLNode[T]:
        """
        Réutilise un nœud existant avec une nouvelle valeur.
        
        :param node: Nœud à réutiliser
        :type node: AVLNode[T]
        :param new_value: Nouvelle valeur pour le nœud
        :type new_value: T
        :return: Nœud réutilisé
        :rtype: AVLNode[T]
        :raises MemoryOptimizationError: Si la réutilisation échoue
        """
        try:
            if not isinstance(node, AVLNode):
                raise MemoryOptimizationError(
                    "Node must be an AVLNode instance",
                    "reuse_node",
                )
            
            # Réinitialiser les propriétés du nœud
            node._value = new_value
            node._balance_factor = 0
            node._cached_height = 0
            node._parent = None
            node._left = None
            node._right = None
            node._children = []
            node._metadata = {}
            
            return node
        except Exception as e:
            if isinstance(e, MemoryOptimizationError):
                raise
            raise MemoryOptimizationError(
                f"Failed to reuse node: {str(e)}",
                "reuse_node",
            ) from e
    
    @staticmethod
    def optimize_memory_usage(tree: AVLTree[T]) -> Dict[str, Any]:
        """
        Optimise l'utilisation mémoire de l'arbre AVL.
        
        :param tree: Arbre AVL à optimiser
        :type tree: AVLTree[T]
        :return: Rapport d'optimisation mémoire
        :rtype: Dict[str, Any]
        :raises MemoryOptimizationError: Si l'optimisation échoue
        """
        try:
            if not isinstance(tree, AVLTree):
                raise MemoryOptimizationError(
                    "Tree must be an AVLTree instance",
                    "optimize_memory_usage",
                )
            
            # Analyser l'utilisation mémoire actuelle
            current_size = tree.get_size()
            current_height = tree.get_height()
            
            # Calculer l'utilisation mémoire théorique
            theoretical_size = current_size * 64  # Estimation en bytes par nœud
            
            # Identifier les optimisations possibles
            optimizations = []
            
            if current_height > 2 * (current_size.bit_length() - 1):
                optimizations.append("Tree height could be optimized")
            
            if current_size > 1000:
                optimizations.append("Consider using object pooling for large trees")
            
            # Générer le rapport
            report = {
                "current_size": current_size,
                "current_height": current_height,
                "theoretical_memory_usage": theoretical_size,
                "height_efficiency": current_height / (current_size.bit_length() - 1) if current_size > 1 else 1,
                "optimizations_available": optimizations,
                "recommendations": [
                    "Enable height caching for frequently accessed trees",
                    "Use batch operations for multiple insertions/deletions",
                    "Consider object pooling for high-frequency operations"
                ]
            }
            
            return report
        except Exception as e:
            if isinstance(e, MemoryOptimizationError):
                raise
            raise MemoryOptimizationError(
                f"Failed to optimize memory usage: {str(e)}",
                "optimize_memory_usage",
            ) from e
    
    @staticmethod
    def enable_height_cache(tree: AVLTree[T]) -> None:
        """
        Active la mise en cache des hauteurs.
        
        :param tree: Arbre AVL pour lequel activer le cache
        :type tree: AVLTree[T]
        :raises PerformanceOptimizationError: Si l'activation échoue
        """
        try:
            if not isinstance(tree, AVLTree):
                raise PerformanceOptimizationError(
                    "Tree must be an AVLTree instance",
                    "enable_height_cache",
                )
            
            tree_id = id(tree)
            cache_id = f"height_cache_{tree_id}"
            
            # Créer le cache de hauteurs
            cache = LRUCache(max_size=1000)
            AVLOptimizations._height_caches[cache_id] = cache
            
            # Configurer le cache sur l'arbre
            tree._height_cache = cache
            tree._height_cache_enabled = True
            
        except Exception as e:
            if isinstance(e, PerformanceOptimizationError):
                raise
            raise PerformanceOptimizationError(
                f"Failed to enable height cache: {str(e)}",
                "enable_height_cache",
            ) from e
    
    @staticmethod
    def enable_balance_factor_cache(tree: AVLTree[T]) -> None:
        """
        Active la mise en cache des facteurs d'équilibre.
        
        :param tree: Arbre AVL pour lequel activer le cache
        :type tree: AVLTree[T]
        :raises PerformanceOptimizationError: Si l'activation échoue
        """
        try:
            if not isinstance(tree, AVLTree):
                raise PerformanceOptimizationError(
                    "Tree must be an AVLTree instance",
                    "enable_balance_factor_cache",
                )
            
            tree_id = id(tree)
            cache_id = f"balance_factor_cache_{tree_id}"
            
            # Créer le cache de facteurs d'équilibre
            cache = LRUCache(max_size=1000)
            AVLOptimizations._balance_factor_caches[cache_id] = cache
            
            # Configurer le cache sur l'arbre
            tree._balance_factor_cache = cache
            tree._balance_factor_cache_enabled = True
            
        except Exception as e:
            if isinstance(e, PerformanceOptimizationError):
                raise
            raise PerformanceOptimizationError(
                f"Failed to enable balance factor cache: {str(e)}",
                "enable_balance_factor_cache",
            ) from e
    
    @staticmethod
    def optimize_rotations(tree: AVLTree[T]) -> None:
        """
        Optimise les algorithmes de rotation.
        
        :param tree: Arbre AVL à optimiser
        :type tree: AVLTree[T]
        :raises PerformanceOptimizationError: Si l'optimisation échoue
        """
        try:
            if not isinstance(tree, AVLTree):
                raise PerformanceOptimizationError(
                    "Tree must be an AVLTree instance",
                    "optimize_rotations",
                )
            
            # Activer l'optimisation des rotations
            tree._rotation_optimization_enabled = True
            tree._rotation_cache = LRUCache(max_size=500)
            
        except Exception as e:
            if isinstance(e, PerformanceOptimizationError):
                raise
            raise PerformanceOptimizationError(
                f"Failed to optimize rotations: {str(e)}",
                "optimize_rotations",
            ) from e
    
    @staticmethod
    def monitor_performance(tree: AVLTree[T]) -> PerformanceMonitor:
        """
        Active le monitoring des performances.
        
        :param tree: Arbre AVL à monitorer
        :type tree: AVLTree[T]
        :return: Moniteur de performance
        :rtype: PerformanceMonitor
        :raises PerformanceOptimizationError: Si l'activation échoue
        """
        try:
            if not isinstance(tree, AVLTree):
                raise PerformanceOptimizationError(
                    "Tree must be an AVLTree instance",
                    "monitor_performance",
                )
            
            tree_id = id(tree)
            monitor_id = f"monitor_{tree_id}"
            
            # Créer le moniteur de performance
            monitor = PerformanceMonitor()
            AVLOptimizations._performance_monitors[monitor_id] = monitor
            
            # Configurer le monitoring sur l'arbre
            tree._performance_monitor = monitor
            tree._performance_monitoring_enabled = True
            
            return monitor
        except Exception as e:
            if isinstance(e, PerformanceOptimizationError):
                raise
            raise PerformanceOptimizationError(
                f"Failed to monitor performance: {str(e)}",
                "monitor_performance",
            ) from e
    
    @staticmethod
    def analyze_metrics(tree: AVLTree[T]) -> Dict[str, Any]:
        """
        Analyse les métriques de performance de l'arbre.
        
        :param tree: Arbre AVL à analyser
        :type tree: AVLTree[T]
        :return: Analyse des métriques
        :rtype: Dict[str, Any]
        :raises PerformanceOptimizationError: Si l'analyse échoue
        """
        try:
            if not isinstance(tree, AVLTree):
                raise PerformanceOptimizationError(
                    "Tree must be an AVLTree instance",
                    "analyze_metrics",
                )
            
            tree_id = id(tree)
            monitor_id = f"monitor_{tree_id}"
            
            if monitor_id not in AVLOptimizations._performance_monitors:
                return {"error": "Performance monitoring not enabled for this tree"}
            
            monitor = AVLOptimizations._performance_monitors[monitor_id]
            stats = monitor.get_all_stats()
            
            # Ajouter l'analyse des tendances
            analysis = {
                "tree_stats": {
                    "size": tree.get_size(),
                    "height": tree.get_height(),
                    "rotation_count": tree.get_rotation_count()
                },
                "performance_stats": stats,
                "recommendations": []
            }
            
            # Générer des recommandations basées sur les métriques
            if stats["operations"]:
                for operation, op_stats in stats["operations"].items():
                    if op_stats["average_time"] > 0.001:  # Plus de 1ms
                        analysis["recommendations"].append(
                            f"Consider optimizing {operation} operations (avg: {op_stats['average_time']:.4f}s)"
                        )
            
            return analysis
        except Exception as e:
            if isinstance(e, PerformanceOptimizationError):
                raise
            raise PerformanceOptimizationError(
                f"Failed to analyze metrics: {str(e)}",
                "analyze_metrics",
            ) from e
    
    @staticmethod
    def get_optimization_recommendations(tree: AVLTree[T]) -> List[str]:
        """
        Retourne les recommandations d'optimisation.
        
        :param tree: Arbre AVL à analyser
        :type tree: AVLTree[T]
        :return: Liste des recommandations d'optimisation
        :rtype: List[str]
        :raises PerformanceOptimizationError: Si l'analyse échoue
        """
        try:
            if not isinstance(tree, AVLTree):
                raise PerformanceOptimizationError(
                    "Tree must be an AVLTree instance",
                    "get_optimization_recommendations",
                )
            
            recommendations = []
            
            # Analyser la taille de l'arbre
            size = tree.get_size()
            height = tree.get_height()
            
            if size > 1000:
                recommendations.append("Consider using batch operations for large trees")
            
            if height > 2 * (size.bit_length() - 1):
                recommendations.append("Tree height could be optimized with better insertion order")
            
            if tree.get_rotation_count() > size * 0.1:
                recommendations.append("High rotation count - consider optimizing insertion patterns")
            
            # Recommandations générales
            recommendations.extend([
                "Enable height caching for frequently accessed trees",
                "Use object pooling for high-frequency operations",
                "Consider enabling performance monitoring for detailed analysis"
            ])
            
            return recommendations
        except Exception as e:
            if isinstance(e, PerformanceOptimizationError):
                raise
            raise PerformanceOptimizationError(
                f"Failed to get optimization recommendations: {str(e)}",
                "get_optimization_recommendations",
            ) from e