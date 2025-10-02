"""
Module contenant l'implémentation de la stratégie d'équilibrage AVL.

Ce module implémente la classe AVLBalancingStrategy qui utilise les facteurs
d'équilibre pour maintenir l'équilibre des arbres AVL.
"""

from __future__ import annotations

from typing import Optional, TypeVar

from ..core.exceptions import BalancingStrategyError, StrategyApplicationError
from ..binary.binary_tree_node import BinaryTreeNode
from .balancing_strategy import BalancingStrategy

T = TypeVar('T')


class AVLBalancingStrategy(BalancingStrategy[T]):
    """
    Stratégie d'équilibrage AVL basée sur les facteurs d'équilibre.
    
    Cette stratégie utilise les facteurs d'équilibre des nœuds AVL pour détecter
    les déséquilibres et appliquer les rotations appropriées pour maintenir
    l'équilibre de l'arbre.
    
    Attributes:
        _rotation_count (int): Nombre de rotations effectuées
        _balance_factor_cache (Dict[BinaryTreeNode[T], int]): Cache des facteurs d'équilibre
    """
    
    def __init__(self) -> None:
        """
        Initialise une nouvelle instance de AVLBalancingStrategy.
        
        Initialise les compteurs et caches spécifiques à la stratégie AVL.
        """
        super().__init__()
        self._rotation_count: int = 0
        self._balance_factor_cache: dict[BinaryTreeNode[T], int] = {}
    
    def balance(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Équilibre selon la stratégie AVL.
        
        Cette méthode implémente l'algorithme d'équilibrage AVL complet :
        1. Calcul du facteur d'équilibre
        2. Identification du type de déséquilibre
        3. Application de la rotation appropriée
        4. Mise à jour des propriétés AVL
        5. Retour de la nouvelle racine
        
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
                    "Équilibrage AVL invalide",
                    "AVLBalancingStrategy",
                    "balance",
                    node
                )
            
            # Calculer le facteur d'équilibre
            balance_factor = self._calculate_balance_factor(node)
            
            # Identifier le type de déséquilibre
            if abs(balance_factor) <= 1:
                return node  # Déjà équilibré
            
            # Appliquer la rotation appropriée
            if balance_factor > 1:
                # Déséquilibre à gauche
                if self._calculate_balance_factor(node.left_child) < 0:
                    # Rotation gauche-droite
                    return self._rotate_left_right(node)
                else:
                    # Rotation droite
                    return self._rotate_right(node)
            else:
                # Déséquilibre à droite
                if self._calculate_balance_factor(node.right_child) > 0:
                    # Rotation droite-gauche
                    return self._rotate_right_left(node)
                else:
                    # Rotation gauche
                    return self._rotate_left(node)
                    
        except Exception as e:
            self._failure_count += 1
            self._operation_count += 1
            raise StrategyApplicationError(
                f"Échec de l'équilibrage AVL: {str(e)}",
                "AVLBalancingStrategy",
                "balance",
                node
            ) from e
        finally:
            self._operation_count += 1
            if self._operation_count > self._failure_count:
                self._success_count += 1
    
    def can_balance(self, node: BinaryTreeNode[T]) -> bool:
        """
        Vérifie si un équilibrage AVL peut être effectué.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            True si l'équilibrage peut être effectué, False sinon
        """
        return node is not None and hasattr(node, 'balance_factor')
    
    def get_description(self) -> str:
        """
        Retourne la description de la stratégie AVL.
        
        Returns:
            Description textuelle de la stratégie AVL
        """
        return "Stratégie d'équilibrage AVL basée sur les facteurs d'équilibre"
    
    def get_complexity(self) -> str:
        """
        Retourne la complexité temporelle de la stratégie AVL.
        
        Returns:
            Complexité temporelle sous forme de chaîne
        """
        return "O(log n)"
    
    def _validate_strategy_specific(self, node: BinaryTreeNode[T]) -> bool:
        """
        Validation spécifique à la stratégie AVL.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la validation spécifique réussit, False sinon
        """
        # Vérifier que le nœud a un facteur d'équilibre
        if not hasattr(node, 'balance_factor'):
            return False
        
        # Vérifier que le facteur d'équilibre est dans la plage valide
        balance_factor = getattr(node, 'balance_factor', 0)
        return -2 <= balance_factor <= 2  # Plage étendue pour détecter les déséquilibres
    
    def _validate_resulting_structure(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide la structure résultante après équilibrage AVL.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la structure est valide, False sinon
        """
        if node is None:
            return True
        
        # Vérifier que le facteur d'équilibre est dans la plage AVL valide
        if hasattr(node, 'balance_factor'):
            balance_factor = getattr(node, 'balance_factor', 0)
            if abs(balance_factor) > 1:
                return False
        
        # Validation récursive des enfants
        return (self._validate_resulting_structure(node.left) and
                self._validate_resulting_structure(node.right))
    
    def _validate_balance_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés d'équilibre AVL.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés d'équilibre sont valides, False sinon
        """
        if node is None:
            return True
        
        # Vérifier que le facteur d'équilibre est dans la plage AVL valide
        if hasattr(node, 'balance_factor'):
            balance_factor = getattr(node, 'balance_factor', 0)
            if abs(balance_factor) > 1:
                return False
        
        # Validation récursive des enfants
        return (self._validate_balance_properties(node.left) and
                self._validate_balance_properties(node.right))
    
    def _validate_specific_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés spécifiques à la stratégie AVL.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés spécifiques sont valides, False sinon
        """
        return self._validate_balance_properties(node)
    
    def _calculate_balance_factor(self, node: BinaryTreeNode[T]) -> int:
        """
        Calcule le facteur d'équilibre d'un nœud.
        
        Args:
            node: Le nœud dont calculer le facteur d'équilibre
            
        Returns:
            Le facteur d'équilibre du nœud
        """
        if node is None:
            return 0
        
        # Utiliser le cache si disponible
        if node in self._balance_factor_cache:
            return self._balance_factor_cache[node]
        
        # Calculer le facteur d'équilibre
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        balance_factor = left_height - right_height
        
        # Mettre en cache le résultat
        self._balance_factor_cache[node] = balance_factor
        
        return balance_factor
    
    def _get_height(self, node: BinaryTreeNode[T]) -> int:
        """
        Obtient la hauteur d'un nœud.
        
        Args:
            node: Le nœud dont obtenir la hauteur
            
        Returns:
            La hauteur du nœud
        """
        if node is None:
            return 0
        
        # Utiliser la hauteur mise en cache si disponible
        if hasattr(node, 'height'):
            return getattr(node, 'height', 0)
        
        # Calculer la hauteur récursivement
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        return 1 + max(left_height, right_height)
    
    def _rotate_left(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation gauche.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
            
        Returns:
            Le nouveau nœud racine après rotation
        """
        if node.right is None:
            raise StrategyApplicationError(
                "Rotation gauche impossible: enfant droit manquant",
                "AVLBalancingStrategy",
                "rotate_left",
                node
            )
        
        # Effectuer la rotation
        right_child = node.right
        node.set_right(right_child.left)
        
        if right_child.left is not None:
            right_child.left.parent = node
        
        right_child.parent = node.parent
        
        if node.parent is None:
            # node était la racine
            pass
        elif node == node.parent.left:
            node.parent.set_left(right_child)
        else:
            node.parent.set_right(right_child)
        
        right_child.set_left(node)
        node.parent = right_child
        
        # Mettre à jour les hauteurs et facteurs d'équilibre
        self._update_avl_properties(node)
        self._update_avl_properties(right_child)
        
        # Invalider le cache
        self._invalidate_cache(node)
        self._invalidate_cache(right_child)
        
        self._rotation_count += 1
        
        return right_child
    
    def _rotate_right(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation droite.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
            
        Returns:
            Le nouveau nœud racine après rotation
        """
        if node.left is None:
            raise StrategyApplicationError(
                "Rotation droite impossible: enfant gauche manquant",
                "AVLBalancingStrategy",
                "rotate_right",
                node
            )
        
        # Effectuer la rotation
        left_child = node.left
        node.set_left(left_child.right)
        
        if left_child.right is not None:
            left_child.right.parent = node
        
        left_child.parent = node.parent
        
        if node.parent is None:
            # node était la racine
            pass
        elif node == node.parent.left:
            node.parent.set_left(left_child)
        else:
            node.parent.set_right(left_child)
        
        left_child.set_right(node)
        node.parent = left_child
        
        # Mettre à jour les hauteurs et facteurs d'équilibre
        self._update_avl_properties(node)
        self._update_avl_properties(left_child)
        
        # Invalider le cache
        self._invalidate_cache(node)
        self._invalidate_cache(left_child)
        
        self._rotation_count += 1
        
        return left_child
    
    def _rotate_left_right(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation gauche-droite (double rotation).
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
            
        Returns:
            Le nouveau nœud racine après rotation
        """
        if node.left is None:
            raise StrategyApplicationError(
                "Rotation gauche-droite impossible: enfant gauche manquant",
                "AVLBalancingStrategy",
                "rotate_left_right",
                node
            )
        
        # Première rotation : rotation gauche sur l'enfant gauche
        node.set_left(self._rotate_left(node.left))
        
        # Deuxième rotation : rotation droite sur le nœud
        return self._rotate_right(node)
    
    def _rotate_right_left(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation droite-gauche (double rotation).
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
            
        Returns:
            Le nouveau nœud racine après rotation
        """
        if node.right is None:
            raise StrategyApplicationError(
                "Rotation droite-gauche impossible: enfant droit manquant",
                "AVLBalancingStrategy",
                "rotate_right_left",
                node
            )
        
        # Première rotation : rotation droite sur l'enfant droit
        node.set_right(self._rotate_right(node.right))
        
        # Deuxième rotation : rotation gauche sur le nœud
        return self._rotate_left(node)
    
    def _update_avl_properties(self, node: BinaryTreeNode[T]) -> None:
        """
        Met à jour les propriétés AVL d'un nœud.
        
        Args:
            node: Le nœud dont mettre à jour les propriétés
        """
        if node is None:
            return
        
        # Calculer et mettre à jour la hauteur
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        height = 1 + max(left_height, right_height)
        
        if hasattr(node, 'height'):
            setattr(node, 'height', height)
        
        # Calculer et mettre à jour le facteur d'équilibre
        balance_factor = left_height - right_height
        if hasattr(node, 'balance_factor'):
            setattr(node, 'balance_factor', balance_factor)
        
        # Mettre à jour le cache
        self._balance_factor_cache[node] = balance_factor
    
    def _invalidate_cache(self, node: BinaryTreeNode[T]) -> None:
        """
        Invalide le cache pour un nœud et ses ancêtres.
        
        Args:
            node: Le nœud dont invalider le cache
        """
        current = node
        while current is not None:
            if current in self._balance_factor_cache:
                del self._balance_factor_cache[current]
            current = current.parent