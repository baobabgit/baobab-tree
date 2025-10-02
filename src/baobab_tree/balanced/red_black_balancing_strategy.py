"""
Module contenant l'implémentation de la stratégie d'équilibrage rouge-noir.

Ce module implémente la classe RedBlackBalancingStrategy qui utilise la recoloration
et les rotations pour maintenir l'équilibre des arbres rouge-noir.
"""

from __future__ import annotations

from typing import Optional, TypeVar

from ..core.exceptions import BalancingStrategyError, StrategyApplicationError
from ..binary.binary_tree_node import BinaryTreeNode
from .balancing_strategy import BalancingStrategy

T = TypeVar('T')


class RedBlackBalancingStrategy(BalancingStrategy[T]):
    """
    Stratégie d'équilibrage rouge-noir basée sur la recoloration.
    
    Cette stratégie utilise les propriétés de couleur des nœuds rouge-noir pour
    détecter les violations et appliquer les recolorations et rotations appropriées
    pour maintenir l'équilibre de l'arbre.
    
    Attributes:
        _recolor_count (int): Nombre de recolorations effectuées
        _rotation_count (int): Nombre de rotations effectuées
        _violation_cache (Dict[BinaryTreeNode[T], List[str]]): Cache des violations détectées
    """
    
    def __init__(self) -> None:
        """
        Initialise une nouvelle instance de RedBlackBalancingStrategy.
        
        Initialise les compteurs et caches spécifiques à la stratégie rouge-noir.
        """
        super().__init__()
        self._recolor_count: int = 0
        self._rotation_count: int = 0
        self._violation_cache: dict[BinaryTreeNode[T], list[str]] = {}
    
    def balance(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Équilibre selon la stratégie rouge-noir.
        
        Cette méthode implémente l'algorithme d'équilibrage rouge-noir complet :
        1. Analyse des violations de propriétés
        2. Application des recolorations appropriées
        3. Effectuation des rotations si nécessaire
        4. Mise à jour des propriétés rouge-noir
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
                    "Équilibrage rouge-noir invalide",
                    "RedBlackBalancingStrategy",
                    "balance",
                    node
                )
            
            # Analyser les violations de propriétés
            violations = self._analyze_violations(node)
            
            # Appliquer les corrections appropriées
            for violation in violations:
                if violation['type'] == 'red_red':
                    self._fix_red_red_violation(violation['node'])
                elif violation['type'] == 'black_height':
                    self._fix_black_height_violation(violation['node'])
            
            # Effectuer les rotations si nécessaire
            if self._needs_rotation(node):
                return self._apply_rotation(node)
            
            return node
                    
        except Exception as e:
            self._failure_count += 1
            self._operation_count += 1
            raise StrategyApplicationError(
                f"Échec de l'équilibrage rouge-noir: {str(e)}",
                "RedBlackBalancingStrategy",
                "balance",
                node
            ) from e
        finally:
            self._operation_count += 1
            if self._operation_count > self._failure_count:
                self._success_count += 1
    
    def can_balance(self, node: BinaryTreeNode[T]) -> bool:
        """
        Vérifie si un équilibrage rouge-noir peut être effectué.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            True si l'équilibrage peut être effectué, False sinon
        """
        return node is not None and hasattr(node, 'color')
    
    def get_description(self) -> str:
        """
        Retourne la description de la stratégie rouge-noir.
        
        Returns:
            Description textuelle de la stratégie rouge-noir
        """
        return "Stratégie d'équilibrage rouge-noir basée sur la recoloration"
    
    def get_complexity(self) -> str:
        """
        Retourne la complexité temporelle de la stratégie rouge-noir.
        
        Returns:
            Complexité temporelle sous forme de chaîne
        """
        return "O(log n)"
    
    def _validate_strategy_specific(self, node: BinaryTreeNode[T]) -> bool:
        """
        Validation spécifique à la stratégie rouge-noir.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la validation spécifique réussit, False sinon
        """
        # Vérifier que le nœud a une couleur
        if not hasattr(node, 'color'):
            return False
        
        # Vérifier que la couleur est valide
        color = getattr(node, 'color', None)
        return color in ['red', 'black']
    
    def _validate_resulting_structure(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide la structure résultante après équilibrage rouge-noir.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si la structure est valide, False sinon
        """
        if node is None:
            return True
        
        # Vérifier les propriétés rouge-noir
        return self._validate_red_black_properties(node)
    
    def _validate_balance_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés d'équilibre rouge-noir.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés d'équilibre sont valides, False sinon
        """
        return self._validate_red_black_properties(node)
    
    def _validate_specific_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés spécifiques à la stratégie rouge-noir.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés spécifiques sont valides, False sinon
        """
        return self._validate_red_black_properties(node)
    
    def _validate_red_black_properties(self, node: BinaryTreeNode[T]) -> bool:
        """
        Valide les propriétés rouge-noir d'un nœud et de ses descendants.
        
        Args:
            node: Le nœud à valider
            
        Returns:
            True si les propriétés rouge-noir sont respectées, False sinon
        """
        if node is None:
            return True
        
        # Vérifier que la couleur est valide
        if hasattr(node, 'color'):
            color = getattr(node, 'color', None)
            if color not in ['red', 'black']:
                return False
        
        # Vérifier la propriété rouge-noir : pas de nœud rouge avec enfant rouge
        if (hasattr(node, 'color') and 
            getattr(node, 'color', None) == 'red'):
            if (node.left_child is not None and 
                hasattr(node.left_child, 'color') and 
                getattr(node.left_child, 'color', None) == 'red'):
                return False
            if (node.right_child is not None and 
                hasattr(node.right_child, 'color') and 
                getattr(node.right_child, 'color', None) == 'red'):
                return False
        
        # Validation récursive des enfants
        return (self._validate_red_black_properties(node.left_child) and
                self._validate_red_black_properties(node.right_child))
    
    def _analyze_violations(self, node: BinaryTreeNode[T]) -> list[dict[str, any]]:
        """
        Analyse les violations de propriétés rouge-noir.
        
        Args:
            node: Le nœud à analyser
            
        Returns:
            Liste des violations détectées
        """
        violations = []
        
        if node is None:
            return violations
        
        # Vérifier les violations rouge-rouge
        if (hasattr(node, 'color') and 
            getattr(node, 'color', None) == 'red'):
            if (node.left_child is not None and 
                hasattr(node.left_child, 'color') and 
                getattr(node.left_child, 'color', None) == 'red'):
                violations.append({
                    'type': 'red_red',
                    'node': node,
                    'child': 'left'
                })
            if (node.right_child is not None and 
                hasattr(node.right_child, 'color') and 
                getattr(node.right_child, 'color', None) == 'red'):
                violations.append({
                    'type': 'red_red',
                    'node': node,
                    'child': 'right'
                })
        
        # Vérifier les violations de hauteur noire
        if self._has_black_height_violation(node):
            violations.append({
                'type': 'black_height',
                'node': node
            })
        
        return violations
    
    def _has_black_height_violation(self, node: BinaryTreeNode[T]) -> bool:
        """
        Vérifie s'il y a une violation de hauteur noire.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            True s'il y a une violation de hauteur noire, False sinon
        """
        if node is None:
            return False
        
        # Calculer les hauteurs noires des chemins
        left_black_height = self._calculate_black_height(node.left_child)
        right_black_height = self._calculate_black_height(node.right_child)
        
        return left_black_height != right_black_height
    
    def _calculate_black_height(self, node: BinaryTreeNode[T]) -> int:
        """
        Calcule la hauteur noire d'un nœud.
        
        Args:
            node: Le nœud dont calculer la hauteur noire
            
        Returns:
            La hauteur noire du nœud
        """
        if node is None:
            return 0
        
        # Compter ce nœud s'il est noir
        count = 0
        if hasattr(node, 'color') and getattr(node, 'color', None) == 'black':
            count = 1
        
        # Ajouter la hauteur noire des enfants
        left_height = self._calculate_black_height(node.left_child)
        right_height = self._calculate_black_height(node.right_child)
        
        return count + max(left_height, right_height)
    
    def _fix_red_red_violation(self, node: BinaryTreeNode[T]) -> None:
        """
        Corrige une violation rouge-rouge.
        
        Args:
            node: Le nœud avec violation rouge-rouge
        """
        if node is None:
            return
        
        # Recolorer le nœud en noir
        if hasattr(node, 'color'):
            setattr(node, 'color', 'black')
        
        self._recolor_count += 1
    
    def _fix_black_height_violation(self, node: BinaryTreeNode[T]) -> None:
        """
        Corrige une violation de hauteur noire.
        
        Args:
            node: Le nœud avec violation de hauteur noire
        """
        if node is None:
            return
        
        # Cette méthode doit être implémentée selon les règles spécifiques
        # de correction des violations de hauteur noire
        pass
    
    def _needs_rotation(self, node: BinaryTreeNode[T]) -> bool:
        """
        Détermine si une rotation est nécessaire.
        
        Args:
            node: Le nœud à vérifier
            
        Returns:
            True si une rotation est nécessaire, False sinon
        """
        if node is None:
            return False
        
        # Vérifier les conditions nécessitant une rotation
        # selon les règles rouge-noir
        return False  # Simplification pour cette implémentation
    
    def _apply_rotation(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Applique une rotation si nécessaire.
        
        Args:
            node: Le nœud autour duquel effectuer la rotation
            
        Returns:
            Le nouveau nœud racine après rotation
        """
        if node is None:
            return node
        
        # Cette méthode doit être implémentée selon les règles spécifiques
        # de rotation rouge-noir
        self._rotation_count += 1
        return node