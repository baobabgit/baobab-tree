"""
Nœud B-tree pour les arbres multi-chemins.

Ce module implémente la classe BTreeNode qui représente un nœud dans un B-tree.
Un nœud B-tree peut contenir plusieurs clés et plusieurs enfants, permettant
une structure multi-chemins optimisée pour les accès disque.
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple, Dict

from ..core.tree_node import TreeNode
from ..core.interfaces import Comparable
from ..core.exceptions import (
    BTreeError,
    NodeFullError,
    NodeUnderflowError,
    SplitError,
    MergeError,
    RedistributionError,
)


class BTreeNode(TreeNode[Comparable]):
    """
    Nœud B-tree pour les arbres multi-chemins.

    Un nœud B-tree peut contenir entre (order-1) et (2*order-1) clés,
    et entre order et (2*order) enfants. Cette structure permet d'optimiser
    les accès disque en minimisant le nombre de nœuds à lire.

    :param order: Ordre minimum du B-tree (doit être >= 2)
    :type order: int
    :param is_leaf: Indique si ce nœud est une feuille
    :type is_leaf: bool
    :param keys: Liste initiale des clés (optionnel)
    :type keys: List[Comparable], optional
    :param children: Liste initiale des enfants (optionnel)
    :type children: List[Optional[BTreeNode[Comparable]]], optional
    :param parent: Référence vers le nœud parent (optionnel)
    :type parent: Optional[BTreeNode[Comparable]], optional
    """

    def __init__(
        self,
        order: int,
        is_leaf: bool = True,
        keys: Optional[List[Comparable]] = None,
        children: Optional[List[Optional[BTreeNode[Comparable]]]] = None,
        parent: Optional[BTreeNode[Comparable]] = None,
    ):
        """
        Initialise un nœud B-tree.

        :param order: Ordre minimum du B-tree (doit être >= 2)
        :type order: int
        :param is_leaf: Indique si ce nœud est une feuille
        :type is_leaf: bool
        :param keys: Liste initiale des clés (optionnel)
        :type keys: List[Comparable], optional
        :param children: Liste initiale des enfants (optionnel)
        :type children: List[Optional[BTreeNode[Comparable]]], optional
        :param parent: Référence vers le nœud parent (optionnel)
        :type parent: Optional[BTreeNode[Comparable]], optional
        :raises InvalidOrderError: Si l'ordre est invalide (< 2)
        """
        if order < 2:
            raise BTreeError(f"Ordre invalide: {order}. L'ordre doit être >= 2")

        super().__init__()
        self.order = order
        self.is_leaf = is_leaf
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.parent = parent

        # Validation initiale
        self._validate_node()

    def _validate_node(self) -> None:
        """
        Valide les propriétés du nœud B-tree.

        :raises BTreeError: Si les propriétés du nœud sont invalides
        """
        max_keys = 2 * self.order - 1
        max_children = 2 * self.order

        if len(self.keys) > max_keys:
            raise BTreeError(
                f"Trop de clés: {len(self.keys)} > {max_keys}",
                "validation",
                self,
            )

        if not self.is_leaf and len(self.children) > max_children:
            raise BTreeError(
                f"Trop d'enfants: {len(self.children)} > {max_children}",
                "validation",
                self,
            )

        # Vérifier que les clés sont triées
        for i in range(len(self.keys) - 1):
            if self.keys[i] >= self.keys[i + 1]:
                raise BTreeError(
                    f"Clés non triées: {self.keys[i]} >= {self.keys[i + 1]}",
                    "validation",
                    self,
                )

    def get_key_count(self) -> int:
        """
        Retourne le nombre de clés dans le nœud.

        :return: Nombre de clés
        :rtype: int
        """
        return len(self.keys)

    def get_child_count(self) -> int:
        """
        Retourne le nombre d'enfants dans le nœud.

        :return: Nombre d'enfants
        :rtype: int
        """
        return len(self.children)

    def is_full(self) -> bool:
        """
        Vérifie si le nœud est plein (contient le maximum de clés).

        :return: True si le nœud est plein, False sinon
        :rtype: bool
        """
        return len(self.keys) >= 2 * self.order - 1

    def is_minimum(self) -> bool:
        """
        Vérifie si le nœud contient le minimum de clés.

        :return: True si le nœud contient le minimum de clés, False sinon
        :rtype: bool
        """
        return len(self.keys) <= self.order - 1

    def search_key(self, key: Comparable) -> int:
        """
        Recherche l'index d'une clé dans le nœud.

        :param key: Clé à rechercher
        :type key: Comparable
        :return: Index de la clé si trouvée, sinon index où l'insérer
        :rtype: int
        """
        left, right = 0, len(self.keys)
        while left < right:
            mid = (left + right) // 2
            if self.keys[mid] < key:
                left = mid + 1
            else:
                right = mid
        return left

    def insert_key(self, key: Comparable) -> int:
        """
        Insère une clé dans le nœud à la bonne position.

        :param key: Clé à insérer
        :type key: Comparable
        :return: Index où la clé a été insérée
        :rtype: int
        :raises NodeFullError: Si le nœud est plein
        """
        if self.is_full():
            raise NodeFullError(
                f"Nœud plein, impossible d'insérer la clé {key}",
                self,
                key,
            )

        index = self.search_key(key)
        self.keys.insert(index, key)
        return index

    def delete_key(self, key: Comparable) -> bool:
        """
        Supprime une clé du nœud.

        :param key: Clé à supprimer
        :type key: Comparable
        :return: True si la clé a été supprimée, False sinon
        :rtype: bool
        """
        try:
            index = self.keys.index(key)
            self.keys.pop(index)
            return True
        except ValueError:
            return False

    def get_child_index(self, key: Comparable) -> int:
        """
        Retourne l'index de l'enfant approprié pour une clé donnée.

        :param key: Clé pour laquelle trouver l'enfant
        :type key: Comparable
        :return: Index de l'enfant approprié
        :rtype: int
        """
        if self.is_leaf:
            raise BTreeError(
                "Impossible de récupérer l'enfant d'une feuille",
                "get_child_index",
                self,
            )

        index = self.search_key(key)
        return index

    def split(self) -> Tuple[BTreeNode[Comparable], Comparable, BTreeNode[Comparable]]:
        """
        Divise le nœud en deux nœuds et retourne la clé médiane.

        :return: Tuple contenant (nœud gauche, clé médiane, nœud droit)
        :rtype: Tuple[BTreeNode[Comparable], Comparable, BTreeNode[Comparable]]
        :raises SplitError: Si la division ne peut pas être effectuée
        """
        if not self.is_full():
            raise SplitError(
                "Impossible de diviser un nœud qui n'est pas plein",
                self,
                "node_not_full",
            )

        # Clé médiane
        mid_index = self.order - 1
        median_key = self.keys[mid_index]

        # Créer le nœud droit
        right_keys = self.keys[mid_index + 1 :]
        right_children = (
            self.children[mid_index + 1 :] if not self.is_leaf else []
        )
        right_node = BTreeNode(
            self.order,
            self.is_leaf,
            right_keys,
            right_children,
            self.parent,
        )

        # Mettre à jour le nœud gauche (nœud actuel)
        self.keys = self.keys[:mid_index]
        if not self.is_leaf:
            self.children = self.children[: mid_index + 1]

        # Mettre à jour les références parent des enfants du nœud droit
        if not self.is_leaf:
            for child in right_node.children:
                if child is not None:
                    child.parent = right_node

        return self, median_key, right_node

    def merge_with(self, other: BTreeNode[Comparable], separator_key: Comparable) -> None:
        """
        Fusionne ce nœud avec un autre nœud.

        :param other: Nœud à fusionner avec ce nœud
        :type other: BTreeNode[Comparable]
        :param separator_key: Clé séparatrice entre les deux nœuds
        :type separator_key: Comparable
        :raises MergeError: Si la fusion ne peut pas être effectuée
        """
        if self.parent != other.parent:
            raise MergeError(
                "Impossible de fusionner des nœuds avec des parents différents",
                self,
                other,
                "different_parents",
            )

        if len(self.keys) + len(other.keys) + 1 > 2 * self.order - 1:
            raise MergeError(
                "Impossible de fusionner: résultat dépasserait la capacité maximale",
                self,
                other,
                "capacity_exceeded",
            )

        # Ajouter la clé séparatrice et les clés de l'autre nœud
        self.keys.append(separator_key)
        self.keys.extend(other.keys)

        # Fusionner les enfants si nécessaire
        if not self.is_leaf:
            self.children.extend(other.children)
            # Mettre à jour les références parent
            for child in other.children:
                if child is not None:
                    child.parent = self

    def borrow_from_left(self) -> bool:
        """
        Emprunte une clé au nœud frère gauche.

        :return: True si l'emprunt a réussi, False sinon
        :rtype: bool
        """
        if self.parent is None:
            return False

        # Trouver l'index de ce nœud dans les enfants du parent
        parent_index = self.parent.children.index(self)
        if parent_index == 0:  # Pas de frère gauche
            return False

        left_sibling = self.parent.children[parent_index - 1]
        if left_sibling is None or left_sibling.is_minimum():
            return False

        # Emprunter la dernière clé du frère gauche
        borrowed_key = left_sibling.keys.pop()
        separator_key = self.parent.keys[parent_index - 1]

        # Insérer la clé séparatrice dans ce nœud
        self.keys.insert(0, separator_key)

        # Mettre à jour la clé séparatrice dans le parent
        self.parent.keys[parent_index - 1] = borrowed_key

        # Gérer les enfants si nécessaire
        if not self.is_leaf:
            borrowed_child = left_sibling.children.pop()
            if borrowed_child is not None:
                borrowed_child.parent = self
            self.children.insert(0, borrowed_child)

        return True

    def borrow_from_right(self) -> bool:
        """
        Emprunte une clé au nœud frère droit.

        :return: True si l'emprunt a réussi, False sinon
        :rtype: bool
        """
        if self.parent is None:
            return False

        # Trouver l'index de ce nœud dans les enfants du parent
        parent_index = self.parent.children.index(self)
        if parent_index >= len(self.parent.children) - 1:  # Pas de frère droit
            return False

        right_sibling = self.parent.children[parent_index + 1]
        if right_sibling is None or right_sibling.is_minimum():
            return False

        # Emprunter la première clé du frère droit
        borrowed_key = right_sibling.keys.pop(0)
        separator_key = self.parent.keys[parent_index]

        # Ajouter la clé séparatrice à ce nœud
        self.keys.append(separator_key)

        # Mettre à jour la clé séparatrice dans le parent
        self.parent.keys[parent_index] = borrowed_key

        # Gérer les enfants si nécessaire
        if not self.is_leaf:
            borrowed_child = right_sibling.children.pop(0)
            if borrowed_child is not None:
                borrowed_child.parent = self
            self.children.append(borrowed_child)

        return True

    def redistribute_keys(self) -> None:
        """
        Redistribue les clés entre ce nœud et ses frères.

        :raises RedistributionError: Si la redistribution ne peut pas être effectuée
        """
        if self.parent is None:
            raise RedistributionError(
                "Impossible de redistribuer: pas de parent",
                self,
                None,
                "no_parent",
            )

        # Essayer d'emprunter à gauche puis à droite
        if not self.borrow_from_left() and not self.borrow_from_right():
            raise RedistributionError(
                "Impossible de redistribuer: aucun frère disponible",
                self,
                None,
                "no_siblings_available",
            )

    def get_predecessor(self, key: Comparable) -> Optional[Comparable]:
        """
        Retourne le prédécesseur d'une clé dans le nœud.

        :param key: Clé pour laquelle trouver le prédécesseur
        :type key: Comparable
        :return: Prédécesseur de la clé, None si non trouvé
        :rtype: Optional[Comparable]
        """
        index = self.search_key(key)
        if index > 0:
            return self.keys[index - 1]
        return None

    def get_successor(self, key: Comparable) -> Optional[Comparable]:
        """
        Retourne le successeur d'une clé dans le nœud.

        :param key: Clé pour laquelle trouver le successeur
        :type key: Comparable
        :return: Successeur de la clé, None si non trouvé
        :rtype: Optional[Comparable]
        """
        index = self.search_key(key)
        if index < len(self.keys):
            return self.keys[index]
        return None

    def validate_node(self) -> bool:
        """
        Valide les propriétés du nœud B-tree.

        :return: True si le nœud est valide, False sinon
        :rtype: bool
        """
        try:
            self._validate_node()
            return True
        except BTreeError:
            return False

    def to_string(self, indent: int = 0) -> str:
        """
        Retourne une représentation textuelle du nœud.

        :param indent: Niveau d'indentation
        :type indent: int
        :return: Représentation textuelle du nœud
        :rtype: str
        """
        indent_str = "  " * indent
        result = f"{indent_str}BTreeNode(order={self.order}, is_leaf={self.is_leaf})\n"
        result += f"{indent_str}  Keys: {self.keys}\n"
        result += f"{indent_str}  Children: {len(self.children)}\n"

        if not self.is_leaf:
            for i, child in enumerate(self.children):
                if child is not None:
                    result += f"{indent_str}  Child {i}:\n"
                    result += child.to_string(indent + 2)

        return result

    def get_node_info(self) -> Dict[str, Any]:
        """
        Retourne des informations détaillées sur le nœud.

        :return: Dictionnaire contenant les informations du nœud
        :rtype: Dict[str, Any]
        """
        return {
            "order": self.order,
            "is_leaf": self.is_leaf,
            "key_count": len(self.keys),
            "child_count": len(self.children),
            "is_full": self.is_full(),
            "is_minimum": self.is_minimum(),
            "keys": self.keys.copy(),
            "parent": self.parent is not None,
        }

    def __str__(self) -> str:
        """
        Retourne une représentation string du nœud.

        :return: Représentation string du nœud
        :rtype: str
        """
        return f"BTreeNode(keys={self.keys}, is_leaf={self.is_leaf})"

    def __repr__(self) -> str:
        """
        Retourne une représentation détaillée du nœud.

        :return: Représentation détaillée du nœud
        :rtype: str
        """
        return (
            f"BTreeNode(order={self.order}, keys={self.keys}, "
            f"is_leaf={self.is_leaf}, children={len(self.children)})"
        )