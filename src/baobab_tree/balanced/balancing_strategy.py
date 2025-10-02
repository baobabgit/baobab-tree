"""
Module contenant la classe abstraite BalancingStrategy et ses implémentations concrètes.

Ce module définit l'interface commune pour toutes les stratégies d'équilibrage des arbres,
incluant les méthodes abstraites et concrètes communes, ainsi que les métriques de performance.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar

from ..binary.binary_tree_node import BinaryTreeNode

T = TypeVar('T')


class BalancingStrategy(ABC, Generic[T]):
    """
    Classe abstraite pour les stratégies d'équilibrage des arbres.
    
    Cette classe définit l'interface commune pour toutes les stratégies d'équilibrage,
    incluant les méthodes abstraites obligatoires et les méthodes concrètes communes
    pour la validation, les métriques de performance et le diagnostic.
    
    Attributes:
        _performance_metrics (Dict[str, Any]): Métriques de performance de la stratégie
        _operation_count (int): Nombre d'opérations effectuées
        _success_count (int): Nombre d'opérations réussies
        _failure_count (int): Nombre d'opérations échouées
    """
    
    def __init__(self) -> None:
        """
        Initialise une nouvelle instance de BalancingStrategy.
        
        Initialise les métriques de performance et les compteurs d'opérations.
        """
        self._performance_metrics: Dict[str, Any] = {
            'total_operations': 0,
            'successful_operations': 0,
            'failed_operations': 0,
            'average_execution_time': 0.0,
            'last_operation_time': 0.0
        }
        self._operation_count: int = 0
        self._success_count: int = 0
        self._failure_count: int = 0
    
    @abstractmethod
    def balance(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Équilibre le nœud selon la stratégie.
        
        Args:
            node: Le nœud à équilibrer
            
        Returns:
            Le nouveau nœud racine après équilibrage, ou None si aucun équilibrage nécessaire
            
        Raises:
            BalancingStrategyError: Si l'équilibrage échoue
        """
        pass
    
    @abstractmethod
    def can_balance(self, node: BinaryTreeNode[T]) -> bool:
        """
        Vérifie si l'équilibrage peut être effectué.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            True si l'équilibrage peut être effectué, False sinon
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Retourne une description de la stratégie.
        
        Returns:
            Description textuelle de la stratégie
        """
        pass
    
    @abstractmethod
    def get_complexity(self) -> str:
        """
        Retourne la complexité temporelle de la stratégie.
        
        Returns:
            Complexité temporelle sous forme de chaîne (ex: "O(log n)")
        """
        pass
    
    def validate_before_balancing(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide qu'un équilibrage peut être effectué.
        
        Cette méthode effectue une validation complète avant l'équilibrage,
        incluant la vérification de l'existence du nœud, de l'applicabilité
        de la stratégie et de la validation spécifique.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la validation réussit, False sinon
            
        Raises:
            BalancingStrategyError: Si la validation échoue
        """
        # 1. Vérifier que le nœud existe
        if node is None:
            return False
        
        # 2. Vérifier que la stratégie est applicable
        if not self.can_balance(node):
            return False
        
        # 3. Validation spécifique à la stratégie
        try:
            return self._validate_strategy_specific(node)
        except Exception:
            return False
    
    def validate_after_balancing(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide qu'un équilibrage a été effectué correctement.
        
        Cette méthode effectue une validation complète après l'équilibrage,
        incluant la vérification de la cohérence des références, des propriétés
        de l'arbre et de la structure résultante.
        
        Args:
            node: Le nœud équilibré à valider
            
        Returns:
            True si la validation réussit, False sinon
        """
        if node is None:
            return False
        
        try:
            # 1. Vérifier la cohérence des références
            if not self._validate_references(node):
                return False
            
            # 2. Vérifier les propriétés de l'arbre
            if not self._validate_tree_properties(node):
                return False
            
            # 3. Vérifier la structure résultante
            if not self._validate_resulting_structure(node):
                return False
            
            return True
        except Exception:
            return False
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Retourne les métriques de performance de la stratégie.
        
        Returns:
            Dictionnaire contenant les métriques de performance
        """
        return {
            'strategy_type': self.__class__.__name__,
            'description': self.get_description(),
            'complexity': self.get_complexity(),
            'total_operations': self._operation_count,
            'successful_operations': self._success_count,
            'failed_operations': self._failure_count,
            'success_rate': (self._success_count / self._operation_count * 100) if self._operation_count > 0 else 0.0,
            'performance_metrics': self._performance_metrics.copy()
        }
    
    def analyze_strategy(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
        """
        Analyse l'effet d'une stratégie avant de l'effectuer.
        
        Cette méthode analyse l'état actuel du nœud et prédit l'effet
        de l'application de la stratégie, incluant les métriques de performance.
        
        Args:
            node: Le nœud à analyser
            
        Returns:
            Dictionnaire contenant l'analyse de la stratégie
        """
        if node is None:
            return {'error': 'Node is None'}
        
        try:
            analysis = {
                'node_value': node.value,
                'can_balance': self.can_balance(node),
                'strategy_type': self.__class__.__name__,
                'complexity': self.get_complexity(),
                'current_state': self._analyze_current_state(node),
                'predicted_effect': self._predict_effect(node),
                'performance_impact': self._analyze_performance_impact(node)
            }
            return analysis
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def get_strategy_stats(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
        """
        Retourne les statistiques de la stratégie sur le sous-arbre.
        
        Cette méthode analyse le sous-arbre à partir du nœud donné et retourne
        des statistiques détaillées sur les opérations effectuées et les
        métriques de performance.
        
        Args:
            node: Le nœud racine du sous-arbre à analyser
            
        Returns:
            Dictionnaire contenant les statistiques de la stratégie
        """
        if node is None:
            return {'error': 'Node is None'}
        
        try:
            stats = {
                'subtree_size': self._count_subtree_nodes(node),
                'operation_types': self._analyze_operation_types(node),
                'performance_metrics': self._calculate_subtree_metrics(node),
                'strategy_efficiency': self._calculate_strategy_efficiency(node)
            }
            return stats
        except Exception as e:
            return {'error': f'Statistics calculation failed: {str(e)}'}
    
    def validate_consistency(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide la cohérence de l'arbre après équilibrage.
        
        Cette méthode vérifie la cohérence des références, des propriétés
        de l'arbre et de la structure résultante après équilibrage.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si l'arbre est cohérent, False sinon
        """
        if node is None:
            return True
        
        try:
            return (self._validate_references(node) and
                    self._validate_tree_properties(node) and
                    self._validate_resulting_structure(node))
        except Exception:
            return False
    
    def validate_properties(self, node: BinaryTreeNode[T]) -> Dict[str, bool]:
        """
        Valide les propriétés spécifiques de l'arbre après équilibrage.
        
        Cette méthode vérifie les propriétés de base, d'équilibre et spécifiques
        de l'arbre après équilibrage.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            Dictionnaire contenant le résultat de validation pour chaque propriété
        """
        if node is None:
            return {'error': 'Node is None'}
        
        try:
            properties = {
                'basic_properties': self._validate_basic_properties(node),
                'balance_properties': self._validate_balance_properties(node),
                'specific_properties': self._validate_specific_properties(node)
            }
            return properties
        except Exception as e:
            return {'error': f'Property validation failed: {str(e)}'}
    
    def _validate_strategy_specific(self, node: BinaryTreeNode[T]) -> bool:
        """
        Validation spécifique à la stratégie.
        
        Cette méthode doit être implémentée par les classes dérivées pour
        effectuer des validations spécifiques à leur stratégie d'équilibrage.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la validation spécifique réussit, False sinon
        """
        return True
    
    def _validate_references(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide la cohérence des références dans l'arbre.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les références sont cohérentes, False sinon
        """
        if node is None:
            return True
        
        # Vérifier les références parent-enfant
        if node.left is not None and node.left.parent != node:
            return False
        if node.right is not None and node.right.parent != node:
            return False
        
        # Validation récursive des enfants
        return (self._validate_references(node.left) and
                self._validate_references(node.right))
    
    def _validate_tree_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés de base de l'arbre.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés sont valides, False sinon
        """
        if node is None:
            return True
        
        # Vérifier que les enfants respectent l'ordre (pour BST)
        if (node.left is not None and 
            hasattr(node.left, 'value') and 
            hasattr(node, 'value')):
            if node.left.value >= node.value:
                return False
        
        if (node.right is not None and 
            hasattr(node.right, 'value') and 
            hasattr(node, 'value')):
            if node.right.value <= node.value:
                return False
        
        # Validation récursive des enfants
        return (self._validate_tree_properties(node.left) and
                self._validate_tree_properties(node.right))
    
    def _validate_resulting_structure(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide la structure résultante après équilibrage.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la structure est valide, False sinon
        """
        # Cette méthode doit être implémentée par les classes dérivées
        # pour valider la structure spécifique à leur stratégie
        return True
    
    def _analyze_current_state(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
        """
        Analyse l'état actuel du nœud.
        
        Args:
            node: Le nœud à analyser
            
        Returns:
            Dictionnaire contenant l'analyse de l'état actuel
        """
        return {
            'has_left_child': node.left is not None,
            'has_right_child': node.right is not None,
            'has_parent': node.parent is not None,
            'node_type': type(node).__name__
        }
    
    def _predict_effect(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
        """
        Prédit l'effet de l'application de la stratégie.
        
        Args:
            node: Le nœud à analyser
            
        Returns:
            Dictionnaire contenant la prédiction de l'effet
        """
        return {
            'will_balance': self.can_balance(node),
            'estimated_operations': 1 if self.can_balance(node) else 0,
            'complexity': self.get_complexity()
        }
    
    def _analyze_performance_impact(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
        """
        Analyse l'impact sur les performances.
        
        Args:
            node: Le nœud à analyser
            
        Returns:
            Dictionnaire contenant l'analyse de l'impact sur les performances
        """
        return {
            'current_metrics': self._performance_metrics.copy(),
            'operation_count': self._operation_count,
            'success_rate': (self._success_count / self._operation_count * 100) if self._operation_count > 0 else 0.0
        }
    
    def _count_subtree_nodes(self, node: BinaryTreeNode[T]) -> int:
        """
        Compte le nombre de nœuds dans le sous-arbre.
        
        Args:
            node: Le nœud racine du sous-arbre
            
        Returns:
            Nombre de nœuds dans le sous-arbre
        """
        if node is None:
            return 0
        
        return (1 + 
                self._count_subtree_nodes(node.left) + 
                self._count_subtree_nodes(node.right))
    
    def _analyze_operation_types(self, node: BinaryTreeNode[T]) -> Dict[str, int]:
        """
        Analyse les types d'opérations effectuées.
        
        Args:
            node: Le nœud à analyser
            
        Returns:
            Dictionnaire contenant le nombre d'opérations par type
        """
        return {
            'balance_operations': self._success_count,
            'failed_operations': self._failure_count,
            'total_operations': self._operation_count
        }
    
    def _calculate_subtree_metrics(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
        """
        Calcule les métriques du sous-arbre.
        
        Args:
            node: Le nœud racine du sous-arbre
            
        Returns:
            Dictionnaire contenant les métriques du sous-arbre
        """
        subtree_size = self._count_subtree_nodes(node)
        return {
            'subtree_size': subtree_size,
            'operations_per_node': self._operation_count / subtree_size if subtree_size > 0 else 0,
            'efficiency_ratio': self._success_count / subtree_size if subtree_size > 0 else 0
        }
    
    def _calculate_strategy_efficiency(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
        """
        Calcule l'efficacité de la stratégie.
        
        Args:
            node: Le nœud à analyser
            
        Returns:
            Dictionnaire contenant les métriques d'efficacité
        """
        return {
            'success_rate': (self._success_count / self._operation_count * 100) if self._operation_count > 0 else 0.0,
            'average_operations': self._operation_count / max(1, self._success_count),
            'strategy_complexity': self.get_complexity()
        }
    
    def _validate_basic_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés de base de l'arbre.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés de base sont valides, False sinon
        """
        return self._validate_tree_properties(node)
    
    def _validate_balance_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés d'équilibre de l'arbre.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés d'équilibre sont valides, False sinon
        """
        # Cette méthode doit être implémentée par les classes dérivées
        # pour valider les propriétés d'équilibre spécifiques
        return True
    
    def _validate_specific_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés spécifiques de la stratégie.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés spécifiques sont valides, False sinon
        """
        # Cette méthode doit être implémentée par les classes dérivées
        # pour valider les propriétés spécifiques à leur stratégie
        return True