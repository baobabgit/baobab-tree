"""
Module contenant le sélecteur automatique de stratégies d'équilibrage.

Ce module implémente la classe BalancingStrategySelector qui permet de sélectionner
automatiquement la stratégie d'équilibrage appropriée selon le contexte.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TypeVar

from ..core.exceptions import InvalidStrategyError
from ..binary.binary_tree_node import BinaryTreeNode
from .balancing_strategy import BalancingStrategy
from .balancing_strategy_factory import BalancingStrategyFactory

T = TypeVar('T')


class BalancingStrategySelector:
    """
    Sélecteur automatique de stratégie selon le contexte.
    
    Cette classe analyse le contexte d'un nœud et sélectionne automatiquement
    la stratégie d'équilibrage la plus appropriée selon les caractéristiques
    de l'arbre et les exigences de performance.
    
    Attributes:
        _selection_cache (Dict[str, BalancingStrategy]): Cache des sélections précédentes
        _context_weights (Dict[str, float]): Poids des différents facteurs contextuels
    """
    
    def __init__(self) -> None:
        """
        Initialise une nouvelle instance de BalancingStrategySelector.
        
        Initialise le cache de sélection et les poids contextuels.
        """
        self._selection_cache: Dict[str, BalancingStrategy[T]] = {}
        self._context_weights: Dict[str, float] = {
            'tree_type': 0.3,
            'node_count': 0.2,
            'access_pattern': 0.2,
            'memory_constraint': 0.15,
            'performance_requirement': 0.15
        }
    
    @staticmethod
    def select_strategy(node: BinaryTreeNode[T], context: Dict[str, Any]) -> BalancingStrategy[T]:
        """
        Sélectionne la stratégie appropriée selon le contexte.
        
        Cette méthode analyse le contexte fourni et sélectionne automatiquement
        la stratégie d'équilibrage la plus appropriée selon les caractéristiques
        de l'arbre et les exigences de performance.
        
        Args:
            node: Le nœud pour lequel sélectionner la stratégie
            context: Dictionnaire contenant le contexte de sélection
            
        Returns:
            Instance de la stratégie d'équilibrage sélectionnée
            
        Raises:
            InvalidStrategyError: Si aucune stratégie appropriée ne peut être sélectionnée
            
        Examples:
            >>> context = {
            ...     'tree_type': 'avl',
            ...     'node_count': 1000,
            ...     'access_pattern': 'random'
            ... }
            >>> strategy = BalancingStrategySelector.select_strategy(node, context)
        """
        selector = BalancingStrategySelector()
        return selector._select_strategy_internal(node, context)
    
    def _select_strategy_internal(self, node: BinaryTreeNode[T], context: Dict[str, Any]) -> BalancingStrategy[T]:
        """
        Sélectionne la stratégie selon le contexte interne.
        
        Args:
            node: Le nœud pour lequel sélectionner la stratégie
            context: Dictionnaire contenant le contexte de sélection
            
        Returns:
            Instance de la stratégie d'équilibrage sélectionnée
        """
        # Générer une clé de cache
        cache_key = self._generate_cache_key(node, context)
        
        # Vérifier le cache
        if cache_key in self._selection_cache:
            return self._selection_cache[cache_key]
        
        # Analyser le contexte
        analysis = self._analyze_context(node, context)
        
        # Sélectionner la stratégie
        strategy_type = self._select_strategy_type(analysis)
        
        # Créer la stratégie
        try:
            strategy = BalancingStrategyFactory.create_strategy(strategy_type)
            self._selection_cache[cache_key] = strategy
            return strategy
        except Exception as e:
            raise InvalidStrategyError(
                f"Impossible de sélectionner une stratégie: {str(e)}",
                "auto_selection",
                f"Erreur lors de la sélection: {str(e)}"
            )
    
    def _generate_cache_key(self, node: BinaryTreeNode[T], context: Dict[str, Any]) -> str:
        """
        Génère une clé de cache pour la sélection.
        
        Args:
            node: Le nœud pour lequel générer la clé
            context: Le contexte de sélection
            
        Returns:
            Clé de cache générée
        """
        # Créer une représentation simplifiée du contexte
        context_str = str(sorted(context.items()))
        node_type = type(node).__name__ if node else "None"
        
        return f"{node_type}:{hash(context_str)}"
    
    def _analyze_context(self, node: BinaryTreeNode[T], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse le contexte pour la sélection de stratégie.
        
        Args:
            node: Le nœud à analyser
            context: Le contexte à analyser
            
        Returns:
            Dictionnaire contenant l'analyse du contexte
        """
        analysis = {
            'tree_type': self._analyze_tree_type(node, context),
            'node_count': self._analyze_node_count(node, context),
            'access_pattern': self._analyze_access_pattern(context),
            'memory_constraint': self._analyze_memory_constraint(context),
            'performance_requirement': self._analyze_performance_requirement(context)
        }
        
        return analysis
    
    def _analyze_tree_type(self, node: BinaryTreeNode[T], context: Dict[str, Any]) -> str:
        """
        Analyse le type d'arbre.
        
        Args:
            node: Le nœud à analyser
            context: Le contexte à analyser
            
        Returns:
            Type d'arbre identifié
        """
        # Vérifier le contexte explicite
        if 'tree_type' in context:
            return context['tree_type']
        
        # Analyser le type de nœud
        if node is None:
            return 'unknown'
        
        node_type = type(node).__name__.lower()
        
        if 'avl' in node_type:
            return 'avl'
        elif 'redblack' in node_type or 'red_black' in node_type:
            return 'red_black'
        elif 'splay' in node_type:
            return 'splay'
        elif 'treap' in node_type:
            return 'treap'
        else:
            return 'binary_search_tree'
    
    def _analyze_node_count(self, node: BinaryTreeNode[T], context: Dict[str, Any]) -> int:
        """
        Analyse le nombre de nœuds dans l'arbre.
        
        Args:
            node: Le nœud à analyser
            context: Le contexte à analyser
            
        Returns:
            Nombre estimé de nœuds
        """
        # Vérifier le contexte explicite
        if 'node_count' in context:
            return context['node_count']
        
        # Estimer le nombre de nœuds
        if node is None:
            return 0
        
        # Compter récursivement (simplifié)
        return self._count_nodes_recursive(node)
    
    def _count_nodes_recursive(self, node: BinaryTreeNode[T]) -> int:
        """
        Compte récursivement le nombre de nœuds.
        
        Args:
            node: Le nœud à compter
            
        Returns:
            Nombre de nœuds dans le sous-arbre
        """
        if node is None:
            return 0
        
        return (1 + 
                self._count_nodes_recursive(node.left) + 
                self._count_nodes_recursive(node.right))
    
    def _analyze_access_pattern(self, context: Dict[str, Any]) -> str:
        """
        Analyse le modèle d'accès.
        
        Args:
            context: Le contexte à analyser
            
        Returns:
            Modèle d'accès identifié
        """
        if 'access_pattern' in context:
            return context['access_pattern']
        
        return 'random'  # Par défaut
    
    def _analyze_memory_constraint(self, context: Dict[str, Any]) -> str:
        """
        Analyse les contraintes mémoire.
        
        Args:
            context: Le contexte à analyser
            
        Returns:
            Contrainte mémoire identifiée
        """
        if 'memory_constraint' in context:
            return context['memory_constraint']
        
        return 'normal'  # Par défaut
    
    def _analyze_performance_requirement(self, context: Dict[str, Any]) -> str:
        """
        Analyse les exigences de performance.
        
        Args:
            context: Le contexte à analyser
            
        Returns:
            Exigence de performance identifiée
        """
        if 'performance_requirement' in context:
            return context['performance_requirement']
        
        return 'balanced'  # Par défaut
    
    def _select_strategy_type(self, analysis: Dict[str, Any]) -> str:
        """
        Sélectionne le type de stratégie selon l'analyse.
        
        Args:
            analysis: L'analyse du contexte
            
        Returns:
            Type de stratégie sélectionné
        """
        tree_type = analysis['tree_type']
        node_count = analysis['node_count']
        access_pattern = analysis['access_pattern']
        memory_constraint = analysis['memory_constraint']
        performance_requirement = analysis['performance_requirement']
        
        # Sélection basée sur le type d'arbre
        if tree_type == 'avl':
            return 'avl'
        elif tree_type == 'red_black':
            return 'red_black'
        elif tree_type == 'splay':
            return 'splay'
        elif tree_type == 'treap':
            return 'treap'
        
        # Sélection basée sur les caractéristiques
        if access_pattern == 'recent':
            return 'splay'
        elif memory_constraint == 'low':
            return 'red_black'
        elif performance_requirement == 'guaranteed':
            return 'avl'
        elif node_count < 100:
            return 'avl'  # AVL pour les petits arbres
        else:
            return 'red_black'  # Red-black pour les grands arbres
    
    def clear_cache(self) -> None:
        """
        Vide le cache de sélection.
        """
        self._selection_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques du cache.
        
        Returns:
            Dictionnaire contenant les statistiques du cache
        """
        return {
            'cache_size': len(self._selection_cache),
            'cached_strategies': list(self._selection_cache.keys())
        }