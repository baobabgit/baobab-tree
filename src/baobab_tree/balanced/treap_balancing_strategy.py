"""
Module contenant l'implémentation de la stratégie d'équilibrage Treap.

Ce module implémente la classe TreapBalancingStrategy qui utilise les priorités
pour maintenir l'équilibre basé sur les propriétés de heap.
"""

from __future__ import annotations

from typing import Optional, TypeVar

from ..core.exceptions import BalancingStrategyError, StrategyApplicationError
from ..binary.binary_tree_node import BinaryTreeNode
from .balancing_strategy import BalancingStrategy

T = TypeVar('T')


class TreapBalancingStrategy(BalancingStrategy[T]):
    """
    Stratégie d'équilibrage Treap basée sur les priorités.
    
    Cette stratégie utilise les priorités des nœuds pour maintenir les propriétés
    de heap, combinant ainsi les avantages des arbres binaires de recherche
    et des heaps.
    
    Attributes:
        _rotation_count (int): Nombre de rotations effectuées
        _priority_updates (int): Nombre de mises à jour de priorités
        _heap_violations (int): Nombre de violations de heap détectées
    """
    
    def __init__(self) -> None:
        """
        Initialise une nouvelle instance de TreapBalancingStrategy.
        
        Initialise les compteurs spécifiques à la stratégie Treap.
        """
        super().__init__()
        self._rotation_count: int = 0
        self._priority_updates: int = 0
        self._heap_violations: int = 0
    
    def balance(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Équilibre selon la stratégie Treap.
        
        Cette méthode implémente l'algorithme d'équilibrage Treap complet :
        1. Vérification des propriétés de heap
        2. Application des rotations pour maintenir le heap
        3. Mise à jour des propriétés
        4. Retour de la nouvelle racine
        
        Args:
            node: Le nœud à équilibrer
            
        Returns:
            Le nouveau nœud racine après équilibrage, ou None si aucun équilibrage nécessaire
            
        Raises:
            BalancingStrategyError: Si l'équilibrage échoue
            StrategyApplicationError: Si l'application de la stratégie échoue
        """
        try:
            # Validation pré-équilibrage
            if not self.validate_before_balancing(node):
                raise BalancingStrategyError(
                    "Équilibrage Treap invalide",
                    "TreapBalancingStrategy",
                    "balance",
                    node
                )
            
            # Vérifier les propriétés de heap
            violations = self._check_heap_violations(node)
            
            # Appliquer les rotations pour maintenir le heap
            result = node
            for violation in violations:
                result = self._fix_heap_violation(violation)
            
            # Mettre à jour les propriétés
            self._update_treap_properties(result)
            
            return result
                    
        except Exception as e:
            self._failure_count += 1
            self._operation_count += 1
            raise StrategyApplicationError(
                f"Échec de l'équilibrage Treap: {str(e)}",
                "TreapBalancingStrategy",
                "balance",
                node
            ) from e
        finally:
            self._operation_count += 1
            if self._operation_count > self._failure_count:
                self._success_count += 1
    
    def can_balance(self, node: BinaryTreeNode[T]) -> bool:
        """
        Vérifie si un équilibrage Treap peut être effectué.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            True si l'équilibrage peut être effectué, False sinon
        """
        return node is not None and hasattr(node, 'priority')
    
    def get_description(self) -> str:
        """
        Retourne la description de la stratégie Treap.
        
        Returns:
            Description textuelle de la stratégie Treap
        """
        return "Stratégie d'équilibrage Treap basée sur les priorités"
    
    def get_complexity(self) -> str:
        """
        Retourne la complexité temporelle de la stratégie Treap.
        
        Returns:
            Complexité temporelle sous forme de chaîne
        """
        return "O(log n)"
    
    def _validate_strategy_specific(self, node: BinaryTreeNode[T]) -> bool:
        """
        Validation spécifique à la stratégie Treap.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la validation spécifique réussit, False sinon
        """
        # Vérifier que le nœud a une priorité
        if not hasattr(node, 'priority'):
            return False
        
        # Vérifier que la priorité est valide
        priority = getattr(node, 'priority', None)
        return isinstance(priority, (int, float))
    
    def _validate_resulting_structure(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide la structure résultante après équilibrage Treap.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la structure est valide, False sinon
        """
        if node is None:
            return True
        
        # Vérifier les propriétés de heap
        return self._validate_heap_properties(node)
    
    def _validate_balance_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés d'équilibre Treap.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés d'équilibre sont valides, False sinon
        """
        return self._validate_heap_properties(node)
    
    def _validate_specific_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés spécifiques à la stratégie Treap.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés spécifiques sont valides, False sinon
        """
        return self._validate_heap_properties(node)
    
    def _validate_heap_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés de heap d'un nœud et de ses descendants.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés de heap sont respectées, False sinon
        """
        if node is None:
            return True
        
        # Vérifier que le nœud a une priorité
        if not hasattr(node, 'priority'):
            return False
        
        node_priority = getattr(node, 'priority', None)
        
        # Vérifier la propriété de heap : parent a priorité plus élevée que les enfants
        if node.left_child is not None:
            if hasattr(node.left_child, 'priority'):
                left_priority = getattr(node.left_child, 'priority', None)
                if left_priority is not None and left_priority > node_priority:
                    return False
        
        if node.right_child is not None:
            if hasattr(node.right_child, 'priority'):
                right_priority = getattr(node.right_child, 'priority', None)
                if right_priority is not None and right_priority > node_priority:
                    return False
        
        # Validation récursive des enfants
        return (self._validate_heap_properties(node.left_child) and
                self._validate_heap_properties(node.right_child))
    
    def _check_heap_violations(self, node: BinaryTreeNode[T]) -> list[dict[str, any]]:
        """
        Vérifie les violations de propriétés de heap.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            Liste des violations détectées
        """
        violations = []
        
        if node is None:
            return violations
        
        # Vérifier les violations avec l'enfant gauche
        if node.left_child is not None:
            if self._has_heap_violation(node, node.left_child):
                violations.append({
                    'type': 'heap_violation',
                    'parent': node,
                    'child': node.left_child,
                    'side': 'left'
                })
        
        # Vérifier les violations avec l'enfant droit
        if node.right_child is not None:
            if self._has_heap_violation(node, node.right_child):
                violations.append({
                    'type': 'heap_violation',
                    'parent': node,
                    'child': node.right_child,
                    'side': 'right'
                })
        
        return violations
    
    def _has_heap_violation(self, parent: BinaryTreeNode[T], child: BinaryTreeNode[T]) -> bool:
        """
        Vérifie s'il y a une violation de heap entre parent et enfant.
        
        Args:
            parent: Le nœud parent
            child: Le nœud enfant
            
        Returns:
            True s'il y a une violation de heap, False sinon
        """
        if not (hasattr(parent, 'priority') and hasattr(child, 'priority')):
            return False
        
        parent_priority = getattr(parent, 'priority', None)
        child_priority = getattr(child, 'priority', None)
        
        if parent_priority is None or child_priority is None:
            return False
        
        # Violation si l'enfant a une priorité plus élevée que le parent
        return child_priority > parent_priority
    
    def _fix_heap_violation(self, violation: dict[str, any]) -> BinaryTreeNode[T]:
        """
        Corrige une violation de heap.
        
        Args:
            violation: La violation à corriger
            
        Returns:
            Le nouveau nœud racine après correction
        """
        parent = violation['parent']
        child = violation['child']
        side = violation['side']
        
        if side == 'left':
            # Rotation droite pour corriger la violation
            return self._rotate_right(parent)
        else:
            # Rotation gauche pour corriger la violation
            return self._rotate_left(parent)
    
    def _rotate_right(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation droite pour maintenir les propriétés de heap.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
            
        Returns:
            Le nouveau nœud racine après rotation
        """
        if node.left_child is None:
            return node
        
        left_child = node.left_child
        
        # Effectuer la rotation
        node.left_child = left_child.right_child
        if left_child.right_child is not None:
            left_child.right_child.parent = node
        
        left_child.parent = node.parent
        if node.parent is None:
            # node était la racine
            pass
        elif node == node.parent.left_child:
            node.parent.left_child = left_child
        else:
            node.parent.right_child = left_child
        
        left_child.right_child = node
        node.parent = left_child
        
        self._rotation_count += 1
        return left_child
    
    def _rotate_left(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation gauche pour maintenir les propriétés de heap.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
            
        Returns:
            Le nouveau nœud racine après rotation
        """
        if node.right_child is None:
            return node
        
        right_child = node.right_child
        
        # Effectuer la rotation
        node.right_child = right_child.left_child
        if right_child.left_child is not None:
            right_child.left_child.parent = node
        
        right_child.parent = node.parent
        if node.parent is None:
            # node était la racine
            pass
        elif node == node.parent.left_child:
            node.parent.left_child = right_child
        else:
            node.parent.right_child = right_child
        
        right_child.left_child = node
        node.parent = right_child
        
        self._rotation_count += 1
        return right_child
    
    def _update_treap_properties(self, node: BinaryTreeNode[T]) -> None:
        """
        Met à jour les propriétés après équilibrage Treap.
        
        Args:
            node: Le nœud dont mettre à jour les propriétés
        """
        if node is None:
            return
        
        # Mettre à jour les métadonnées Treap si disponibles
        if hasattr(node, 'last_balanced'):
            import time
            setattr(node, 'last_balanced', time.time())
        
        self._priority_updates += 1