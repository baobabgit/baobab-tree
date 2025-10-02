#!/usr/bin/env python3
"""
Exemple d'utilisation des optimisations AVL.

Ce script démontre l'utilisation de la classe AVLOptimizations
pour optimiser les performances des arbres AVL.
"""

import time
import random
from typing import List

# Import des classes nécessaires
from src.baobab_tree.balanced.avl_tree import AVLTree
from src.baobab_tree.balanced.avl_optimizations import AVLOptimizations


def demonstrate_memory_optimizations():
    """Démontre les optimisations mémoire."""
    print("=== Optimisations Mémoire ===")
    
    # Créer un arbre AVL
    tree = AVLTree()
    
    # Insérer des éléments
    for i in range(100):
        tree.insert(i)
    
    # Analyser l'utilisation mémoire
    memory_report = AVLOptimizations.optimize_memory_usage(tree)
    print(f"Taille actuelle: {memory_report['current_size']}")
    print(f"Hauteur actuelle: {memory_report['current_height']}")
    print(f"Efficacité de hauteur: {memory_report['height_efficiency']:.2f}")
    print(f"Utilisation mémoire théorique: {memory_report['theoretical_memory_usage']} bytes")
    
    # Créer un pool d'objets
    pool = AVLOptimizations.create_node_pool(size=50)
    print(f"Pool créé avec {pool._size} nœuds")
    
    # Obtenir des nœuds du pool
    node1 = pool.get_node(42)
    node2 = pool.get_node(84)
    
    print(f"Nœud 1: {node1.value}")
    print(f"Nœud 2: {node2.value}")
    
    # Statistiques du pool
    stats = pool.get_stats()
    print(f"Statistiques du pool: {stats}")
    
    # Retourner les nœuds au pool
    pool.return_node(node1)
    pool.return_node(node2)
    
    print(f"Statistiques après retour: {pool.get_stats()}")
    print()


def demonstrate_performance_optimizations():
    """Démontre les optimisations de performance."""
    print("=== Optimisations de Performance ===")
    
    # Créer un arbre AVL
    tree = AVLTree()
    
    # Activer les optimisations de performance
    AVLOptimizations.enable_height_cache(tree)
    AVLOptimizations.enable_balance_factor_cache(tree)
    AVLOptimizations.optimize_rotations(tree)
    
    print("Optimisations de performance activées:")
    print(f"- Cache de hauteurs: {hasattr(tree, '_height_cache_enabled')}")
    print(f"- Cache de facteurs d'équilibre: {hasattr(tree, '_balance_factor_cache_enabled')}")
    print(f"- Optimisation des rotations: {hasattr(tree, '_rotation_optimization_enabled')}")
    
    # Insérer des éléments et mesurer les performances
    start_time = time.time()
    
    for i in range(1000):
        tree.insert(i)
    
    end_time = time.time()
    
    print(f"Insertion de 1000 éléments: {end_time - start_time:.4f} secondes")
    print(f"Nombre de rotations: {tree.get_rotation_count()}")
    print()


def demonstrate_monitoring():
    """Démontre le monitoring des performances."""
    print("=== Monitoring des Performances ===")
    
    # Créer un arbre AVL
    tree = AVLTree()
    
    # Activer le monitoring
    monitor = AVLOptimizations.monitor_performance(tree)
    
    print("Monitoring activé")
    
    # Effectuer des opérations
    for i in range(100):
        tree.insert(i)
    
    # Analyser les métriques
    analysis = AVLOptimizations.analyze_metrics(tree)
    
    print("Analyse des métriques:")
    print(f"- Taille de l'arbre: {analysis['tree_stats']['size']}")
    print(f"- Hauteur de l'arbre: {analysis['tree_stats']['height']}")
    print(f"- Nombre de rotations: {analysis['tree_stats']['rotation_count']}")
    
    # Obtenir les recommandations
    recommendations = AVLOptimizations.get_optimization_recommendations(tree)
    
    print("Recommandations d'optimisation:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    print()


def demonstrate_cache_functionality():
    """Démontre le fonctionnement des caches."""
    print("=== Fonctionnement des Caches ===")
    
    from src.baobab_tree.balanced.avl_optimizations import LRUCache, CacheMetrics
    
    # Créer un cache LRU
    cache = LRUCache(max_size=5)
    
    # Ajouter des éléments
    for i in range(7):  # Plus que la taille du cache
        cache.put(f"key{i}", f"value{i}")
    
    print("Cache LRU créé avec taille 5, 7 éléments ajoutés")
    
    # Récupérer des éléments
    value1 = cache.get("key6")  # Hit
    value2 = cache.get("key0")  # Miss (évincé)
    
    print(f"Récupération key6: {value1}")
    print(f"Récupération key0: {value2}")
    
    # Statistiques du cache
    stats = cache.get_stats()
    print(f"Statistiques du cache: {stats}")
    
    # Créer des métriques de cache
    metrics = CacheMetrics()
    
    # Simuler des hits et misses
    for _ in range(10):
        metrics.record_hit()
    for _ in range(5):
        metrics.record_miss()
    
    print(f"Taux de hit: {metrics.get_hit_rate():.2f}")
    print()


def demonstrate_performance_comparison():
    """Démontre une comparaison de performance."""
    print("=== Comparaison de Performance ===")
    
    # Test avec optimisations
    tree_optimized = AVLTree()
    AVLOptimizations.enable_height_cache(tree_optimized)
    AVLOptimizations.optimize_rotations(tree_optimized)
    
    start_time = time.time()
    for i in range(500):
        tree_optimized.insert(random.randint(1, 1000))
    end_time = time.time()
    
    optimized_time = end_time - start_time
    
    # Test sans optimisations
    tree_normal = AVLTree()
    
    start_time = time.time()
    for i in range(500):
        tree_normal.insert(random.randint(1, 1000))
    end_time = time.time()
    
    normal_time = end_time - start_time
    
    print(f"Temps avec optimisations: {optimized_time:.4f} secondes")
    print(f"Temps sans optimisations: {normal_time:.4f} secondes")
    print(f"Amélioration: {((normal_time - optimized_time) / normal_time * 100):.1f}%")
    print()


def main():
    """Fonction principale."""
    print("Exemple d'utilisation des optimisations AVL")
    print("=" * 50)
    print()
    
    try:
        demonstrate_memory_optimizations()
        demonstrate_performance_optimizations()
        demonstrate_monitoring()
        demonstrate_cache_functionality()
        demonstrate_performance_comparison()
        
        print("Tous les exemples ont été exécutés avec succès!")
        
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()