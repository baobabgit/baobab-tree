"""
Classe AVLTree pour les arbres AVL auto-équilibrés.

Ce module implémente la classe AVLTree, arbre binaire de recherche auto-équilibré
utilisant l'algorithme AVL. Cette classe garantit une hauteur logarithmique
et des performances optimales pour toutes les opérations.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Dict, Iterator, List, Optional

from .avl_node import AVLNode
from .binary_search_tree import BinarySearchTree
from .bst_iterators import (
    InorderIterator,
    LevelOrderIterator,
    PostorderIterator,
    PreorderIterator,
)
from .exceptions import (
    AVLError,
    BSTError,
    DuplicateValueError,
    HeightMismatchError,
    InvalidOperationError,
    RotationError,
    ValueNotFoundError,
)
from .interfaces import T


class AVLTree(BinarySearchTree):
    """
    Arbre AVL auto-équilibré.

    Cette classe implémente un arbre binaire de recherche auto-équilibré
    utilisant l'algorithme AVL. Elle garantit une hauteur logarithmique
    et des performances O(log n) pour toutes les opérations.

    :param comparator: Fonction de comparaison personnalisée (optionnel)
    :type comparator: Optional[Callable[[T, T], int]], optional
    """

    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None) -> None:
        """
        Initialise un nouvel arbre AVL.

        :param comparator: Fonction de comparaison personnalisée (optionnel)
        :type comparator: Optional[Callable[[T, T], int]], optional
        """
        super().__init__(comparator)
        self._balance_threshold: int = 1
        self._rotation_count: int = 0

    @property
    def balance_threshold(self) -> int:
        """
        Retourne le seuil de déséquilibre.

        :return: Seuil de déséquilibre (constante = 1)
        :rtype: int
        """
        return self._balance_threshold

    @property
    def rotation_count(self) -> int:
        """
        Retourne le nombre de rotations effectuées.

        :return: Nombre de rotations effectuées
        :rtype: int
        """
        return self._rotation_count

    def insert(self, value: T) -> bool:
        """
        Insère une valeur dans l'arbre AVL avec équilibrage automatique.

        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False si la valeur existe déjà
        :rtype: bool
        :raises AVLError: Si une erreur survient lors de l'insertion
        """
        try:
            if self._root is None:
                self._root = AVLNode(value)
                self._size = 1
                return True

            return self._insert_avl(self._root, value)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Error during AVL insertion: {str(e)}", "insert")

    def _insert_avl(self, node: AVLNode[T], value: T) -> bool:
        """
        Insère récursivement une valeur dans l'arbre AVL avec équilibrage.

        :param node: Nœud racine du sous-arbre
        :type node: AVLNode[T]
        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False si la valeur existe déjà
        :rtype: bool
        """
        comparison = self._comparator(value, node.value)

        if comparison < 0:
            if node.left is None:
                new_node = AVLNode(value)
                node.set_left(new_node)
                self._size += 1
                self._rebalance_path(node)
                return True
            else:
                return self._insert_avl(node.left, value)
        elif comparison > 0:
            if node.right is None:
                new_node = AVLNode(value)
                node.set_right(new_node)
                self._size += 1
                self._rebalance_path(node)
                return True
            else:
                return self._insert_avl(node.right, value)
        else:
            # Valeur déjà présente
            return False

    def delete(self, value: T) -> bool:
        """
        Supprime une valeur de l'arbre AVL avec équilibrage automatique.

        :param value: Valeur à supprimer
        :type value: T
        :return: True si la suppression a réussi, False si la valeur n'existe pas
        :rtype: bool
        :raises AVLError: Si une erreur survient lors de la suppression
        """
        try:
            if self._root is None:
                return False

            # Cas spécial : suppression de la racine
            if self._comparator(value, self._root.value) == 0:
                self._root = self._delete_avl_node(self._root)
                self._size -= 1
                return True

            return self._delete_avl(self._root, value)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Error during AVL deletion: {str(e)}", "delete")

    def _delete_avl(self, node: AVLNode[T], value: T) -> bool:
        """
        Supprime récursivement une valeur de l'arbre AVL avec équilibrage.

        :param node: Nœud racine du sous-arbre
        :type node: AVLNode[T]
        :param value: Valeur à supprimer
        :type value: T
        :return: True si la suppression a réussi, False si la valeur n'existe pas
        :rtype: bool
        """
        comparison = self._comparator(value, node.value)

        if comparison < 0:
            if node.left is None:
                return False
            if self._comparator(value, node.left.value) == 0:
                node.set_left(self._delete_avl_node(node.left))
                self._size -= 1
                self._rebalance_path(node)
                return True
            else:
                return self._delete_avl(node.left, value)
        elif comparison > 0:
            if node.right is None:
                return False
            if self._comparator(value, node.right.value) == 0:
                node.set_right(self._delete_avl_node(node.right))
                self._size -= 1
                self._rebalance_path(node)
                return True
            else:
                return self._delete_avl(node.right, value)
        else:
            # Ce cas ne devrait pas arriver car on gère la racine séparément
            return False

    def _delete_avl_node(self, node: AVLNode[T]) -> Optional[AVLNode[T]]:
        """
        Supprime un nœud AVL et retourne son remplaçant avec équilibrage.

        :param node: Nœud à supprimer
        :type node: AVLNode[T]
        :return: Nœud remplaçant ou None
        :rtype: Optional[AVLNode[T]]
        """
        # Cas 1: Nœud feuille
        if node.is_leaf():
            return None

        # Cas 2: Un seul enfant
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left

        # Cas 3: Deux enfants - remplacer par le successeur
        successor = self._find_min_avl_node(node.right)
        node.value = successor.value
        # Supprimer le successeur (qui a au plus un enfant droit)
        if successor.right is not None:
            if successor.parent.left == successor:
                successor.parent.set_left(successor.right)
            else:
                successor.parent.set_right(successor.right)
        else:
            if successor.parent.left == successor:
                successor.parent.set_left(None)
            else:
                successor.parent.set_right(None)
        return node

    def _find_min_avl_node(self, node: AVLNode[T]) -> AVLNode[T]:
        """
        Trouve le nœud avec la valeur minimale dans le sous-arbre AVL.

        :param node: Nœud racine du sous-arbre
        :type node: AVLNode[T]
        :return: Nœud avec la valeur minimale
        :rtype: AVLNode[T]
        """
        while node.left is not None:
            node = node.left
        return node

    def _rotate_left(self, node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation gauche pour équilibrer l'arbre AVL.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation échoue
        """
        try:
            if node.right is None:
                raise RotationError(
                    "Cannot perform left rotation: right child is None",
                    "left_rotation",
                    "rotation"
                )

            # Sauvegarder le nœud droit
            right_child = node.right
            
            # Remplacer le nœud droit par son enfant gauche
            node.set_right(right_child.left)
            
            # Définir le nœud comme enfant gauche du nœud droit
            right_child.set_left(node)
            
            # Mettre à jour les références parent
            if node.parent is not None:
                if node.parent.left == node:
                    node.parent.set_left(right_child)
                else:
                    node.parent.set_right(right_child)
            else:
                # Le nœud était la racine
                self._root = right_child
                right_child._parent = None

            # Incrémenter le compteur de rotations
            self._rotation_count += 1
            
            return right_child
        except Exception as e:
            if isinstance(e, RotationError):
                raise
            raise RotationError(f"Left rotation failed: {str(e)}", "left_rotation", "rotation")

    def _rotate_right(self, node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation droite pour équilibrer l'arbre AVL.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation échoue
        """
        try:
            if node.left is None:
                raise RotationError(
                    "Cannot perform right rotation: left child is None",
                    "right_rotation",
                    "rotation"
                )

            # Sauvegarder le nœud gauche
            left_child = node.left
            
            # Remplacer le nœud gauche par son enfant droit
            node.set_left(left_child.right)
            
            # Définir le nœud comme enfant droit du nœud gauche
            left_child.set_right(node)
            
            # Mettre à jour les références parent
            if node.parent is not None:
                if node.parent.left == node:
                    node.parent.set_left(left_child)
                else:
                    node.parent.set_right(left_child)
            else:
                # Le nœud était la racine
                self._root = left_child
                left_child._parent = None

            # Incrémenter le compteur de rotations
            self._rotation_count += 1
            
            return left_child
        except Exception as e:
            if isinstance(e, RotationError):
                raise
            raise RotationError(f"Right rotation failed: {str(e)}", "right_rotation", "rotation")

    def _rotate_left_right(self, node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation gauche-droite pour équilibrer l'arbre AVL.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation échoue
        """
        try:
            if node.left is None:
                raise RotationError(
                    "Cannot perform left-right rotation: left child is None",
                    "left_right_rotation",
                    "rotation"
                )

            # Rotation gauche sur le fils gauche
            node.set_left(self._rotate_left(node.left))
            
            # Rotation droite sur le nœud
            return self._rotate_right(node)
        except Exception as e:
            if isinstance(e, RotationError):
                raise
            raise RotationError(f"Left-right rotation failed: {str(e)}", "left_right_rotation", "rotation")

    def _rotate_right_left(self, node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation droite-gauche pour équilibrer l'arbre AVL.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation échoue
        """
        try:
            if node.right is None:
                raise RotationError(
                    "Cannot perform right-left rotation: right child is None",
                    "right_left_rotation",
                    "rotation"
                )

            # Rotation droite sur le fils droit
            node.set_right(self._rotate_right(node.right))
            
            # Rotation gauche sur le nœud
            return self._rotate_left(node)
        except Exception as e:
            if isinstance(e, RotationError):
                raise
            raise RotationError(f"Right-left rotation failed: {str(e)}", "right_left_rotation", "rotation")

    def _balance_node(self, node: AVLNode[T]) -> None:
        """
        Équilibre un nœud AVL en effectuant les rotations nécessaires.

        :param node: Nœud à équilibrer
        :type node: AVLNode[T]
        :raises AVLError: Si l'équilibrage échoue
        """
        try:
            if abs(node.balance_factor) <= self._balance_threshold:
                return

            if node.is_left_heavy():
                # Le nœud penche à gauche
                if node.left is not None and node.left.is_right_heavy():
                    # Cas gauche-droite
                    self._rotate_left_right(node)
                else:
                    # Cas gauche-gauche
                    self._rotate_right(node)
            else:
                # Le nœud penche à droite
                if node.right is not None and node.right.is_left_heavy():
                    # Cas droite-gauche
                    self._rotate_right_left(node)
                else:
                    # Cas droite-droite
                    self._rotate_left(node)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Node balancing failed: {str(e)}", "balance_node")

    def _rebalance_path(self, node: AVLNode[T]) -> None:
        """
        Rééquilibre le chemin de la racine vers le nœud donné.

        :param node: Nœud à partir duquel remonter vers la racine
        :type node: AVLNode[T]
        :raises AVLError: Si le rééquilibrage échoue
        """
        try:
            current = node
            while current is not None:
                current.update_height()
                current.update_balance_factor()
                
                if abs(current.balance_factor) > self._balance_threshold:
                    self._balance_node(current)
                
                current = current.parent
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Path rebalancing failed: {str(e)}", "rebalance_path")

    def is_avl_valid(self) -> bool:
        """
        Valide les propriétés AVL de l'arbre.

        :return: True si l'arbre respecte les propriétés AVL, False sinon
        :rtype: bool
        :raises AVLError: Si une erreur survient lors de la validation
        """
        try:
            return self._is_avl_valid_recursive(self._root)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"AVL validation failed: {str(e)}", "is_avl_valid")

    def _is_avl_valid_recursive(self, node: Optional[AVLNode[T]]) -> bool:
        """
        Valide récursivement les propriétés AVL du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[AVLNode[T]]
        :return: True si le sous-arbre respecte les propriétés AVL, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        # Vérifier que le nœud est un AVLNode
        if not isinstance(node, AVLNode):
            return False

        # Vérifier les propriétés BST
        if not self._is_valid_recursive(node, None, None):
            return False

        # Vérifier le facteur d'équilibre
        if not node.is_balanced():
            return False

        # Valider récursivement les sous-arbres
        return (
            self._is_avl_valid_recursive(node.left) and
            self._is_avl_valid_recursive(node.right)
        )

    def check_balance_factors(self) -> bool:
        """
        Vérifie que tous les facteurs d'équilibre sont valides.

        :return: True si tous les facteurs d'équilibre sont valides, False sinon
        :rtype: bool
        :raises AVLError: Si une erreur survient lors de la vérification
        """
        try:
            return self._check_balance_factors_recursive(self._root)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Balance factors check failed: {str(e)}", "check_balance_factors")

    def _check_balance_factors_recursive(self, node: Optional[AVLNode[T]]) -> bool:
        """
        Vérifie récursivement les facteurs d'équilibre du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[AVLNode[T]]
        :return: True si tous les facteurs d'équilibre sont valides, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        # Vérifier le facteur d'équilibre du nœud
        if not node.is_balanced():
            return False

        # Vérifier récursivement les sous-arbres
        return (
            self._check_balance_factors_recursive(node.left) and
            self._check_balance_factors_recursive(node.right)
        )

    def validate_heights(self) -> bool:
        """
        Valide le calcul des hauteurs dans l'arbre AVL.

        :return: True si toutes les hauteurs sont correctes, False sinon
        :rtype: bool
        :raises AVLError: Si une erreur survient lors de la validation
        """
        try:
            return self._validate_heights_recursive(self._root)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Height validation failed: {str(e)}", "validate_heights")

    def _validate_heights_recursive(self, node: Optional[AVLNode[T]]) -> bool:
        """
        Valide récursivement les hauteurs du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[AVLNode[T]]
        :return: True si toutes les hauteurs sont correctes, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        # Calculer la hauteur attendue
        left_height = node.left.height if node.left is not None else -1
        right_height = node.right.height if node.right is not None else -1
        expected_height = 1 + max(left_height, right_height)

        # Vérifier que la hauteur stockée correspond à la hauteur calculée
        if node.height != expected_height:
            return False

        # Valider récursivement les sous-arbres
        return (
            self._validate_heights_recursive(node.left) and
            self._validate_heights_recursive(node.right)
        )

    def get_balance_statistics(self) -> Dict[str, int]:
        """
        Retourne les statistiques d'équilibre de l'arbre AVL.

        :return: Dictionnaire contenant les statistiques d'équilibre
        :rtype: Dict[str, int]
        :raises AVLError: Si une erreur survient lors du calcul des statistiques
        """
        try:
            stats = {
                "total_nodes": 0,
                "balanced_nodes": 0,
                "left_heavy_nodes": 0,
                "right_heavy_nodes": 0,
                "perfectly_balanced_nodes": 0
            }
            
            self._collect_balance_statistics(self._root, stats)
            return stats
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Balance statistics calculation failed: {str(e)}", "get_balance_statistics")

    def _collect_balance_statistics(self, node: Optional[AVLNode[T]], stats: Dict[str, int]) -> None:
        """
        Collecte récursivement les statistiques d'équilibre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[AVLNode[T]]
        :param stats: Dictionnaire pour stocker les statistiques
        :type stats: Dict[str, int]
        """
        if node is None:
            return

        stats["total_nodes"] += 1
        
        if node.balance_factor == 0:
            stats["perfectly_balanced_nodes"] += 1
        elif node.is_left_heavy():
            stats["left_heavy_nodes"] += 1
        elif node.is_right_heavy():
            stats["right_heavy_nodes"] += 1
        else:
            stats["balanced_nodes"] += 1

        self._collect_balance_statistics(node.left, stats)
        self._collect_balance_statistics(node.right, stats)

    def get_rotation_count(self) -> int:
        """
        Retourne le nombre de rotations effectuées.

        :return: Nombre de rotations effectuées
        :rtype: int
        """
        return self._rotation_count

    def get_height_analysis(self) -> Dict[str, int]:
        """
        Retourne l'analyse des hauteurs de l'arbre AVL.

        :return: Dictionnaire contenant l'analyse des hauteurs
        :rtype: Dict[str, int]
        :raises AVLError: Si une erreur survient lors de l'analyse
        """
        try:
            if self._root is None:
                return {
                    "actual_height": -1,
                    "theoretical_max_height": 0,
                    "height_efficiency": 100
                }

            actual_height = self._root.height
            theoretical_max_height = int(2 * math.log2(self._size + 1))
            height_efficiency = int((theoretical_max_height / max(actual_height, 1)) * 100)

            return {
                "actual_height": actual_height,
                "theoretical_max_height": theoretical_max_height,
                "height_efficiency": min(height_efficiency, 100)
            }
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Height analysis failed: {str(e)}", "get_height_analysis")

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'arbre AVL.

        :return: Représentation string de l'arbre AVL
        :rtype: str
        """
        if self._root is None:
            return "AVLTree(empty)"
        return f"AVLTree(size={self._size}, height={self.get_height()}, rotations={self._rotation_count})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de l'arbre AVL.

        :return: Représentation détaillée de l'arbre AVL
        :rtype: str
        """
        return f"AVLTree(root={self._root}, size={self._size}, rotations={self._rotation_count})"