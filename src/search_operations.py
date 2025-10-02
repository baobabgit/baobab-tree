"""
Opérations de recherche avancées pour les arbres binaires de recherche.

Ce module implémente les opérations de recherche avancées pour les BST,
incluant la recherche de successeur, prédécesseur, plancher, plafond,
et les requêtes de plage.
"""

from __future__ import annotations

from typing import Callable, Generic, List, Optional, TYPE_CHECKING

from .binary_tree_node import BinaryTreeNode
from .interfaces import T

if TYPE_CHECKING:
    from .binary_tree_node import BinaryTreeNode


class SearchOperations(Generic[T]):
    """
    Opérations de recherche avancées pour les BST.

    Cette classe fournit des algorithmes de recherche avancés pour les
    arbres binaires de recherche, incluant les opérations de navigation
    et de requêtes de plage.
    """

    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None):
        """
        Initialise les opérations de recherche.

        :param comparator: Fonction de comparaison personnalisée (optionnel)
        :type comparator: Optional[Callable[[T, T], int]], optional
        """
        self._comparator: Callable[[T, T], int] = comparator or self._default_comparator

    def _default_comparator(self, a: T, b: T) -> int:
        """
        Comparateur par défaut utilisant les opérateurs de comparaison Python.

        :param a: Première valeur à comparer
        :type a: T
        :param b: Deuxième valeur à comparer
        :type b: T
        :return: -1 si a < b, 0 si a == b, 1 si a > b
        :rtype: int
        """
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

    def find_successor(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Trouve le successeur d'un nœud.

        Le successeur est le nœud avec la plus petite valeur supérieure
        à la valeur du nœud donné.

        :param node: Nœud dont trouver le successeur
        :type node: BinaryTreeNode[T]
        :return: Successeur ou None si aucun successeur
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if node.right is not None:
            # Le successeur est le minimum du sous-arbre droit
            return self._get_min_node(node.right)

        # Remonter jusqu'à trouver un ancêtre dont le fils gauche est aussi un ancêtre
        current = node
        parent = node.parent

        while parent is not None and current == parent.right:
            current = parent
            parent = parent.parent

        return parent

    def find_predecessor(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Trouve le prédécesseur d'un nœud.

        Le prédécesseur est le nœud avec la plus grande valeur inférieure
        à la valeur du nœud donné.

        :param node: Nœud dont trouver le prédécesseur
        :type node: BinaryTreeNode[T]
        :return: Prédécesseur ou None si aucun prédécesseur
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if node.left is not None:
            # Le prédécesseur est le maximum du sous-arbre gauche
            return self._get_max_node(node.left)

        # Remonter jusqu'à trouver un ancêtre dont le fils droit est aussi un ancêtre
        current = node
        parent = node.parent

        while parent is not None and current == parent.left:
            current = parent
            parent = parent.parent

        return parent

    def find_floor(self, root: Optional[BinaryTreeNode[T]], value: T) -> Optional[T]:
        """
        Trouve la plus grande valeur inférieure ou égale à la valeur donnée.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur de référence
        :type value: T
        :return: Plus grande valeur <= value ou None
        :rtype: Optional[T]
        """
        return self._find_floor_recursive(root, value)

    def _find_floor_recursive(
        self, node: Optional[BinaryTreeNode[T]], value: T
    ) -> Optional[T]:
        """
        Trouve récursivement la plus grande valeur inférieure ou égale.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param value: Valeur de référence
        :type value: T
        :return: Plus grande valeur <= value ou None
        :rtype: Optional[T]
        """
        if node is None:
            return None

        comparison = self._comparator(value, node.value)

        if comparison == 0:
            return node.value
        elif comparison < 0:
            return self._find_floor_recursive(node.left, value)
        else:
            # La valeur du nœud est inférieure, chercher dans le sous-arbre droit
            right_result = self._find_floor_recursive(node.right, value)
            return right_result if right_result is not None else node.value

    def find_ceiling(self, root: Optional[BinaryTreeNode[T]], value: T) -> Optional[T]:
        """
        Trouve la plus petite valeur supérieure ou égale à la valeur donnée.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur de référence
        :type value: T
        :return: Plus petite valeur >= value ou None
        :rtype: Optional[T]
        """
        return self._find_ceiling_recursive(root, value)

    def _find_ceiling_recursive(
        self, node: Optional[BinaryTreeNode[T]], value: T
    ) -> Optional[T]:
        """
        Trouve récursivement la plus petite valeur supérieure ou égale.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param value: Valeur de référence
        :type value: T
        :return: Plus petite valeur >= value ou None
        :rtype: Optional[T]
        """
        if node is None:
            return None

        comparison = self._comparator(value, node.value)

        if comparison == 0:
            return node.value
        elif comparison > 0:
            return self._find_ceiling_recursive(node.right, value)
        else:
            # La valeur du nœud est supérieure, chercher dans le sous-arbre gauche
            left_result = self._find_ceiling_recursive(node.left, value)
            return left_result if left_result is not None else node.value

    def range_search(
        self, root: Optional[BinaryTreeNode[T]], min_val: T, max_val: T
    ) -> List[T]:
        """
        Effectue une recherche de plage sur l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param min_val: Valeur minimale (incluse)
        :type min_val: T
        :param max_val: Valeur maximale (incluse)
        :type max_val: T
        :return: Liste des valeurs dans la plage
        :rtype: List[T]
        """
        if self._comparator(min_val, max_val) > 0:
            return []

        result = []
        self._range_search_recursive(root, min_val, max_val, result)
        return result

    def _range_search_recursive(
        self, node: Optional[BinaryTreeNode[T]], min_val: T, max_val: T, result: List[T]
    ) -> None:
        """
        Effectue récursivement la recherche de plage.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param min_val: Valeur minimale (incluse)
        :type min_val: T
        :param max_val: Valeur maximale (incluse)
        :type max_val: T
        :param result: Liste pour stocker les résultats
        :type result: List[T]
        """
        if node is None:
            return

        # Si la valeur du nœud est dans la plage, l'ajouter
        if (
            self._comparator(node.value, min_val) >= 0
            and self._comparator(node.value, max_val) <= 0
        ):
            result.append(node.value)

        # Explorer le sous-arbre gauche si nécessaire
        if self._comparator(node.value, min_val) > 0:
            self._range_search_recursive(node.left, min_val, max_val, result)

        # Explorer le sous-arbre droit si nécessaire
        if self._comparator(node.value, max_val) < 0:
            self._range_search_recursive(node.right, min_val, max_val, result)

    def count_range(
        self, root: Optional[BinaryTreeNode[T]], min_val: T, max_val: T
    ) -> int:
        """
        Compte le nombre de valeurs dans une plage.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param min_val: Valeur minimale (incluse)
        :type min_val: T
        :param max_val: Valeur maximale (incluse)
        :type max_val: T
        :return: Nombre de valeurs dans la plage
        :rtype: int
        """
        if self._comparator(min_val, max_val) > 0:
            return 0

        return self._count_range_recursive(root, min_val, max_val)

    def _count_range_recursive(
        self, node: Optional[BinaryTreeNode[T]], min_val: T, max_val: T
    ) -> int:
        """
        Compte récursivement le nombre de valeurs dans la plage.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param min_val: Valeur minimale (incluse)
        :type min_val: T
        :param max_val: Valeur maximale (incluse)
        :type max_val: T
        :return: Nombre de valeurs dans la plage
        :rtype: int
        """
        if node is None:
            return 0

        count = 0

        # Si la valeur du nœud est dans la plage, l'ajouter au compte
        if (
            self._comparator(node.value, min_val) >= 0
            and self._comparator(node.value, max_val) <= 0
        ):
            count += 1

        # Explorer le sous-arbre gauche si nécessaire
        if self._comparator(node.value, min_val) > 0:
            count += self._count_range_recursive(node.left, min_val, max_val)

        # Explorer le sous-arbre droit si nécessaire
        if self._comparator(node.value, max_val) < 0:
            count += self._count_range_recursive(node.right, min_val, max_val)

        return count

    def find_kth_smallest(
        self, root: Optional[BinaryTreeNode[T]], k: int
    ) -> Optional[T]:
        """
        Trouve la k-ième plus petite valeur dans l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param k: Rang de la valeur à trouver (1-indexé)
        :type k: int
        :return: K-ième plus petite valeur ou None si k est invalide
        :rtype: Optional[T]
        """
        if k <= 0:
            return None

        result = []
        self._inorder_traversal(root, result)

        if k > len(result):
            return None

        return result[k - 1]

    def find_kth_largest(
        self, root: Optional[BinaryTreeNode[T]], k: int
    ) -> Optional[T]:
        """
        Trouve la k-ième plus grande valeur dans l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param k: Rang de la valeur à trouver (1-indexé)
        :type k: int
        :return: K-ième plus grande valeur ou None si k est invalide
        :rtype: Optional[T]
        """
        if k <= 0:
            return None

        result = []
        self._inorder_traversal(root, result)

        if k > len(result):
            return None

        return result[len(result) - k]

    def _inorder_traversal(
        self, node: Optional[BinaryTreeNode[T]], result: List[T]
    ) -> None:
        """
        Effectue un parcours infixe pour obtenir les valeurs triées.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param result: Liste pour stocker les résultats
        :type result: List[T]
        """
        if node is None:
            return

        self._inorder_traversal(node.left, result)
        result.append(node.value)
        self._inorder_traversal(node.right, result)

    def _get_min_node(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Trouve le nœud avec la valeur minimale dans le sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Nœud avec la valeur minimale
        :rtype: BinaryTreeNode[T]
        """
        while node.left is not None:
            node = node.left
        return node

    def _get_max_node(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Trouve le nœud avec la valeur maximale dans le sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Nœud avec la valeur maximale
        :rtype: BinaryTreeNode[T]
        """
        while node.right is not None:
            node = node.right
        return node

    def find_closest_value(
        self, root: Optional[BinaryTreeNode[T]], target: T
    ) -> Optional[T]:
        """
        Trouve la valeur la plus proche de la valeur cible.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param target: Valeur cible
        :type target: T
        :return: Valeur la plus proche ou None si arbre vide
        :rtype: Optional[T]
        """
        if root is None:
            return None

        closest = root.value
        current = root

        while current is not None:
            if self._comparator(current.value, target) == 0:
                return current.value

            # Mettre à jour la valeur la plus proche
            if abs(self._comparator(current.value, target)) < abs(
                self._comparator(closest, target)
            ):
                closest = current.value

            # Naviguer vers la valeur cible
            if self._comparator(current.value, target) > 0:
                current = current.left
            else:
                current = current.right

        return closest

    def find_all_values(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> List[BinaryTreeNode[T]]:
        """
        Trouve tous les nœuds contenant une valeur donnée.

        Cette méthode est utile pour les BST qui permettent les doublons.

        :param root: Racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Liste de tous les nœuds contenant la valeur
        :rtype: List[BinaryTreeNode[T]]
        """
        result = []
        self._find_all_values_recursive(root, value, result)
        return result

    def _find_all_values_recursive(
        self,
        node: Optional[BinaryTreeNode[T]],
        value: T,
        result: List[BinaryTreeNode[T]],
    ) -> None:
        """
        Trouve récursivement tous les nœuds contenant une valeur.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :param result: Liste pour stocker les résultats
        :type result: List[BinaryTreeNode[T]]
        """
        if node is None:
            return

        comparison = self._comparator(value, node.value)

        if comparison == 0:
            result.append(node)
            # Chercher dans les deux sous-arbres pour les doublons
            self._find_all_values_recursive(node.left, value, result)
            self._find_all_values_recursive(node.right, value, result)
        elif comparison < 0:
            self._find_all_values_recursive(node.left, value, result)
        else:
            self._find_all_values_recursive(node.right, value, result)
