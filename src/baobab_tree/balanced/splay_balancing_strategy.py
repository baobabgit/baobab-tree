"""
Module contenant l'implémentation de la stratégie d'équilibrage Splay.

Ce module implémente la classe SplayBalancingStrategy qui utilise les rotations
de splay pour maintenir l'équilibre basé sur l'accès récent.
"""

from __future__ import annotations

from typing import Optional, TypeVar

from ..core.exceptions import BalancingStrategyError, StrategyApplicationError
from ..binary.binary_tree_node import BinaryTreeNode
from .balancing_strategy import BalancingStrategy

T = TypeVar('T')


class SplayBalancingStrategy(BalancingStrategy[T]):
    """
    Stratégie d'équilibrage Splay basée sur l'accès récent.
    
    Cette stratégie utilise les rotations de splay pour déplacer le nœud accédé
    vers la racine, optimisant ainsi les accès futurs aux éléments récemment utilisés.
    
    Attributes:
        _splay_count (int): Nombre de splay effectués
        _access_count (int): Nombre d'accès effectués
        _target_node (Optional[BinaryTreeNode[T]]): Nœud cible pour le splay
    """
    
    def __init__(self) -> None:
        """
        Initialise une nouvelle instance de SplayBalancingStrategy.
        
        Initialise les compteurs spécifiques à la stratégie Splay.
        """
        super().__init__()
        self._splay_count: int = 0
        self._access_count: int = 0
        self._target_node: Optional[BinaryTreeNode[T]] = None
    
    def balance(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Équilibre selon la stratégie Splay.
        
        Cette méthode implémente l'algorithme de splay complet :
        1. Identification du nœud à splay
        2. Application des rotations de splay
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
                    "Équilibrage Splay invalide",
                    "SplayBalancingStrategy",
                    "balance",
                    node
                )
            
            # Identifier le nœud à splay
            target = self._target_node or node
            
            # Appliquer les rotations de splay
            result = self._splay(target)
            
            # Mettre à jour les propriétés
            self._update_splay_properties(result)
            
            return result
                    
        except Exception as e:
            self._failure_count += 1
            self._operation_count += 1
            raise StrategyApplicationError(
                f"Échec de l'équilibrage Splay: {str(e)}",
                "SplayBalancingStrategy",
                "balance",
                node
            ) from e
        finally:
            self._operation_count += 1
            if self._operation_count > self._failure_count:
                self._success_count += 1
    
    def can_balance(self, node: BinaryTreeNode[T]) -> bool:
        """
        Vérifie si un équilibrage Splay peut être effectué.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            True si l'équilibrage peut être effectué, False sinon
        """
        return node is not None
    
    def get_description(self) -> str:
        """
        Retourne la description de la stratégie Splay.
        
        Returns:
            Description textuelle de la stratégie Splay
        """
        return "Stratégie d'équilibrage Splay basée sur l'accès récent"
    
    def get_complexity(self) -> str:
        """
        Retourne la complexité temporelle de la stratégie Splay.
        
        Returns:
            Complexité temporelle sous forme de chaîne
        """
        return "O(log n) amorti"
    
    def set_target_node(self, target: BinaryTreeNode[T]) -> None:
        """
        Définit le nœud cible pour le splay.
        
        Args:
            target: Le nœud cible à splay
        """
        self._target_node = target
        self._access_count += 1
    
    def _validate_strategy_specific(self, node: BinaryTreeNode[T]) -> bool:
        """
        Validation spécifique à la stratégie Splay.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la validation spécifique réussit, False sinon
        """
        # Pour Splay, tout nœud peut être équilibré
        return True
    
    def _validate_resulting_structure(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide la structure résultante après équilibrage Splay.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la structure est valide, False sinon
        """
        if node is None:
            return True
        
        # Vérifier que le nœud splayé est à la racine
        if self._target_node is not None:
            return node == self._target_node
        
        return True
    
    def _validate_balance_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés d'équilibre Splay.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés d'équilibre sont valides, False sinon
        """
        # Pour Splay, les propriétés d'équilibre sont maintenues par l'algorithme
        return True
    
    def _validate_specific_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés spécifiques à la stratégie Splay.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés spécifiques sont valides, False sinon
        """
        return self._validate_resulting_structure(node)
    
    def _splay(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue l'opération de splay sur un nœud.
        
        Args:
            node: Le nœud à splay
            
        Returns:
            Le nœud après splay (maintenant à la racine)
        """
        if node is None:
            return node
        
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent
            
            if grandparent is None:
                # Cas simple : parent est la racine
                if node == parent.left_child:
                    self._zig_right(node)
                else:
                    self._zig_left(node)
            else:
                # Cas complexe : grandparent existe
                if (node == parent.left_child and 
                    parent == grandparent.left_child):
                    # Zig-zig droite
                    self._zig_zig_right(node)
                elif (node == parent.right_child and 
                      parent == grandparent.right_child):
                    # Zig-zig gauche
                    self._zig_zig_left(node)
                elif (node == parent.left_child and 
                      parent == grandparent.right_child):
                    # Zig-zag droite-gauche
                    self._zig_zag_right_left(node)
                else:
                    # Zig-zag gauche-droite
                    self._zig_zag_left_right(node)
        
        self._splay_count += 1
        return node
    
    def _zig_right(self, node: BinaryTreeNode[T]) -> None:
        """
        Effectue une rotation zig droite.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
        """
        parent = node.parent
        if parent is None:
            return
        
        # Effectuer la rotation droite
        parent.left_child = node.right_child
        if node.right_child is not None:
            node.right_child.parent = parent
        
        node.parent = parent.parent
        if parent.parent is not None:
            if parent == parent.parent.left_child:
                parent.parent.left_child = node
            else:
                parent.parent.right_child = node
        
        node.right_child = parent
        parent.parent = node
    
    def _zig_left(self, node: BinaryTreeNode[T]) -> None:
        """
        Effectue une rotation zig gauche.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
        """
        parent = node.parent
        if parent is None:
            return
        
        # Effectuer la rotation gauche
        parent.right_child = node.left_child
        if node.left_child is not None:
            node.left_child.parent = parent
        
        node.parent = parent.parent
        if parent.parent is not None:
            if parent == parent.parent.left_child:
                parent.parent.left_child = node
            else:
                parent.parent.right_child = node
        
        node.left_child = parent
        parent.parent = node
    
    def _zig_zig_right(self, node: BinaryTreeNode[T]) -> None:
        """
        Effectue une rotation zig-zig droite.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
        """
        self._zig_right(node.parent)
        self._zig_right(node)
    
    def _zig_zig_left(self, node: BinaryTreeNode[T]) -> None:
        """
        Effectue une rotation zig-zig gauche.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
        """
        self._zig_left(node.parent)
        self._zig_left(node)
    
    def _zig_zag_right_left(self, node: BinaryTreeNode[T]) -> None:
        """
        Effectue une rotation zig-zag droite-gauche.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
        """
        self._zig_right(node)
        self._zig_left(node)
    
    def _zig_zag_left_right(self, node: BinaryTreeNode[T]) -> None:
        """
        Effectue une rotation zig-zag gauche-droite.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
        """
        self._zig_left(node)
        self._zig_right(node)
    
    def _update_splay_properties(self, node: BinaryTreeNode[T]) -> None:
        """
        Met à jour les propriétés après splay.
        
        Args:
            node: Le nœud dont mettre à jour les propriétés
        """
        if node is None:
            return
        
        # Mettre à jour les métadonnées de splay si disponibles
        if hasattr(node, 'last_accessed'):
            import time
            setattr(node, 'last_accessed', time.time())
        
        if hasattr(node, 'access_count'):
            access_count = getattr(node, 'access_count', 0)
            setattr(node, 'access_count', access_count + 1)