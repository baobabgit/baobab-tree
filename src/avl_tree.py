"""
Classe AVLTree pour les arbres AVL auto-équilibrés.

Ce module implémente la classe AVLTree, structure auto-équilibrée qui hérite
de BinarySearchTree et ajoute les fonctionnalités d'équilibrage automatique
des arbres AVL.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, Optional

from .avl_node import AVLNode
from .avl_rotations import AVLRotations
from .binary_search_tree import BinarySearchTree
from .exceptions import AVLError, RotationError
from .interfaces import T


class AVLTree(BinarySearchTree[T]):
    """
    Arbre AVL auto-équilibré.

    Cette classe implémente un arbre AVL (Adelson-Velskii et Landis) qui
    maintient automatiquement l'équilibre après chaque insertion et suppression.
    Elle garantit une hauteur logarithmique et des performances optimales.

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

        # Seuil de déséquilibre (constante = 1 pour AVL)
        self._balance_threshold: int = 1

        # Compteur de rotations (pour debugging et statistiques)
        self._rotation_count: int = 0

    @property
    def balance_threshold(self) -> int:
        """
        Retourne le seuil de déséquilibre.

        :return: Seuil de déséquilibre (1 pour AVL)
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
                # Rééquilibrer le chemin vers la racine
                self._rebalance_path(node)
                return True
            else:
                return self._insert_avl(node.left, value)
        elif comparison > 0:
            if node.right is None:
                new_node = AVLNode(value)
                node.set_right(new_node)
                self._size += 1
                # Rééquilibrer le chemin vers la racine
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
                self._root = self._delete_node_avl(self._root)
                self._size -= 1
                if self._root is not None:
                    self._rebalance_path(self._root)
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
                node.set_left(self._delete_node_avl(node.left))
                self._size -= 1
                self._rebalance_path(node)
                return True
            else:
                return self._delete_avl(node.left, value)
        elif comparison > 0:
            if node.right is None:
                return False
            if self._comparator(value, node.right.value) == 0:
                node.set_right(self._delete_node_avl(node.right))
                self._size -= 1
                self._rebalance_path(node)
                return True
            else:
                return self._delete_avl(node.right, value)
        else:
            # Ce cas ne devrait pas arriver car on gère la racine séparément
            return False

    def _delete_node_avl(self, node: AVLNode[T]) -> Optional[AVLNode[T]]:
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
        successor = self._find_min_node_avl(node.right)
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

    def _find_min_node_avl(self, node: AVLNode[T]) -> AVLNode[T]:
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

    def _balance_node(self, node: AVLNode[T]) -> Optional[AVLNode[T]]:
        """
        Équilibre un nœud en effectuant les rotations nécessaires.

        :param node: Nœud à équilibrer
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après équilibrage
        :rtype: Optional[AVLNode[T]]
        :raises AVLError: Si une erreur survient lors de l'équilibrage
        """
        try:
            if node is None:
                return None

            # Mettre à jour les métadonnées AVL
            node._update_avl_metadata()

            # Vérifier si le nœud est déséquilibré
            if not node.is_balanced():
                # Effectuer la rotation appropriée
                new_root = AVLRotations.perform_rotation(node)
                self._rotation_count += 1

                # Valider le résultat de la rotation
                if not AVLRotations.validate_rotation_result(new_root):
                    raise RotationError(
                        "Rotation produced invalid result",
                        "balance_node",
                        new_root,
                    )

                return new_root

            return node
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(
                f"Error during node balancing: {str(e)}", "balance_node", node
            )

    def _rebalance_path(self, node: AVLNode[T]) -> None:
        """
        Rééquilibre le chemin de la racine vers le nœud donné.

        :param node: Nœud à partir duquel remonter vers la racine
        :type node: AVLNode[T]
        :raises AVLError: Si une erreur survient lors du rééquilibrage
        """
        try:
            current = node
            while current is not None:
                # Équilibrer le nœud actuel
                new_root = self._balance_node(current)

                # Si une rotation a été effectuée, mettre à jour la racine si nécessaire
                if new_root is not None and new_root.parent is None:
                    self._root = new_root

                # Remonter vers le parent
                current = current.parent
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(
                f"Error during path rebalancing: {str(e)}", "rebalance_path", node
            )

    def is_avl_valid(self) -> bool:
        """
        Valide les propriétés AVL de l'arbre.

        Cette méthode vérifie que l'arbre respecte toutes les propriétés AVL :
        - Propriétés BST
        - Facteurs d'équilibre dans [-1, 0, 1]
        - Hauteurs cohérentes

        :return: True si l'arbre respecte les propriétés AVL, False sinon
        :rtype: bool
        :raises AVLError: Si une erreur survient lors de la validation
        """
        try:
            # Vérifier les propriétés BST de base
            if not self.is_valid():
                return False

            # Vérifier les propriétés AVL spécifiques
            return self._validate_avl_recursive(self._root)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(f"Error during AVL validation: {str(e)}", "is_avl_valid")

    def _validate_avl_recursive(self, node: Optional[AVLNode[T]]) -> bool:
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

        # Vérifier les propriétés AVL
        if not node.is_balanced():
            return False

        # Vérifier la cohérence des hauteurs
        if not self._validate_height_consistency(node):
            return False

        # Valider récursivement les sous-arbres
        return self._validate_avl_recursive(node.left) and self._validate_avl_recursive(
            node.right
        )

    def _validate_height_consistency(self, node: AVLNode[T]) -> bool:
        """
        Valide la cohérence des hauteurs d'un nœud AVL.

        :param node: Nœud à valider
        :type node: AVLNode[T]
        :return: True si les hauteurs sont cohérentes, False sinon
        :rtype: bool
        """
        try:
            # Calculer la hauteur réelle
            real_height = (
                super().get_height() if node == self._root else node.get_height()
            )

            # Vérifier la cohérence avec la hauteur mise en cache
            if node._cached_height != real_height:
                return False

            return True
        except Exception:
            return False

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
            raise AVLError(
                f"Error during balance factor check: {str(e)}", "check_balance_factors"
            )

    def _check_balance_factors_recursive(self, node: Optional[AVLNode[T]]) -> bool:
        """
        Vérifie récursivement les facteurs d'équilibre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[AVLNode[T]]
        :return: True si tous les facteurs d'équilibre sont valides, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        # Vérifier que le nœud est un AVLNode
        if not isinstance(node, AVLNode):
            return False

        # Vérifier le facteur d'équilibre
        if not node.is_balanced():
            return False

        # Vérifier récursivement les sous-arbres
        return self._check_balance_factors_recursive(
            node.left
        ) and self._check_balance_factors_recursive(node.right)

    def validate_heights(self) -> bool:
        """
        Valide le calcul des hauteurs dans l'arbre AVL.

        :return: True si toutes les hauteurs sont valides, False sinon
        :rtype: bool
        :raises AVLError: Si une erreur survient lors de la validation
        """
        try:
            return self._validate_heights_recursive(self._root)
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(
                f"Error during height validation: {str(e)}", "validate_heights"
            )

    def _validate_heights_recursive(self, node: Optional[AVLNode[T]]) -> bool:
        """
        Valide récursivement les hauteurs.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[AVLNode[T]]
        :return: True si toutes les hauteurs sont valides, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        # Vérifier que le nœud est un AVLNode
        if not isinstance(node, AVLNode):
            return False

        # Vérifier la cohérence des hauteurs
        if not self._validate_height_consistency(node):
            return False

        # Vérifier récursivement les sous-arbres
        return self._validate_heights_recursive(
            node.left
        ) and self._validate_heights_recursive(node.right)

    def get_balance_statistics(self) -> Dict[str, int]:
        """
        Retourne les statistiques d'équilibre de l'arbre.

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
                "perfectly_balanced_nodes": 0,
            }

            self._collect_balance_statistics(self._root, stats)
            return stats
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(
                f"Error during balance statistics calculation: {str(e)}",
                "get_balance_statistics",
            )

    def _collect_balance_statistics(
        self, node: Optional[AVLNode[T]], stats: Dict[str, int]
    ) -> None:
        """
        Collecte récursivement les statistiques d'équilibre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[AVLNode[T]]
        :param stats: Dictionnaire pour stocker les statistiques
        :type stats: Dict[str, int]
        """
        if node is None:
            return

        # Vérifier que le nœud est un AVLNode
        if isinstance(node, AVLNode):
            stats["total_nodes"] += 1

            if node.is_balanced():
                stats["balanced_nodes"] += 1
                if node.balance_factor == 0:
                    stats["perfectly_balanced_nodes"] += 1
            else:
                if node.is_left_heavy():
                    stats["left_heavy_nodes"] += 1
                elif node.is_right_heavy():
                    stats["right_heavy_nodes"] += 1

        # Collecter récursivement les statistiques des sous-arbres
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
        Retourne l'analyse des hauteurs de l'arbre.

        :return: Dictionnaire contenant l'analyse des hauteurs
        :rtype: Dict[str, int]
        :raises AVLError: Si une erreur survient lors de l'analyse
        """
        try:
            analysis = {
                "actual_height": self.get_height(),
                "optimal_height": (
                    int(math.log2(self._size + 1)) if self._size > 0 else 0
                ),
                "height_difference": 0,
                "is_optimal": False,
            }

            if self._size > 0:
                analysis["height_difference"] = (
                    analysis["actual_height"] - analysis["optimal_height"]
                )
                analysis["is_optimal"] = analysis["height_difference"] <= 1

            return analysis
        except Exception as e:
            if isinstance(e, AVLError):
                raise
            raise AVLError(
                f"Error during height analysis: {str(e)}", "get_height_analysis"
            )

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
