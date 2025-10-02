"""
Classe abstraite TreeOperations pour les opérations de base sur les arbres.

Ce module implémente la classe TreeOperations, classe abstraite de base pour
toutes les opérations sur les arbres dans la librairie. Cette classe fournit
les fonctionnalités communes et définit l'interface pour les opérations
spécialisées.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Tuple, TYPE_CHECKING

from .interfaces import T
from .tree_node import TreeNode

if TYPE_CHECKING:
    from .binary_tree_node import BinaryTreeNode


class TreeOperations(ABC, Generic[T]):
    """
    Classe abstraite pour les opérations de base sur les arbres.

    Cette classe définit l'interface commune pour toutes les opérations
    sur les arbres dans la librairie. Elle fournit les fonctionnalités
    de base et les méthodes abstraites que les classes spécialisées
    doivent implémenter.

    Les opérations incluent la recherche, l'insertion, la suppression
    et les opérations utilitaires pour manipuler les arbres.
    """

    @abstractmethod
    def search(self, root: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
        """
        Recherche une valeur dans l'arbre.

        :param root: Racine de l'arbre à rechercher
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvé
        :rtype: Optional[TreeNode[T]]
        """
        pass

    @abstractmethod
    def insert(self, root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]:
        """
        Insère une valeur dans l'arbre.

        :param root: Racine de l'arbre où insérer
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[TreeNode[T], bool]
        """
        pass

    @abstractmethod
    def delete(
        self, root: Optional[TreeNode[T]], value: T
    ) -> Tuple[Optional[TreeNode[T]], bool]:
        """
        Supprime une valeur de l'arbre.

        :param root: Racine de l'arbre où supprimer
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[TreeNode[T]], bool]
        """
        pass

    def contains(self, root: Optional[TreeNode[T]], value: T) -> bool:
        """
        Vérifie si une valeur existe dans l'arbre.

        :param root: Racine de l'arbre à vérifier
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à vérifier
        :type value: T
        :return: True si la valeur existe, False sinon
        :rtype: bool
        """
        return self.search(root, value) is not None

    def get_min(self, root: Optional[TreeNode[T]]) -> Optional[T]:
        """
        Trouve la valeur minimale dans l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Valeur minimale ou None si arbre vide
        :rtype: Optional[T]
        """
        if root is None:
            return None

        min_node = self.get_min_node(root)
        return min_node.value if min_node is not None else None

    def get_max(self, root: Optional[TreeNode[T]]) -> Optional[T]:
        """
        Trouve la valeur maximale dans l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Valeur maximale ou None si arbre vide
        :rtype: Optional[T]
        """
        if root is None:
            return None

        max_node = self.get_max_node(root)
        return max_node.value if max_node is not None else None

    def get_height(self, root: Optional[TreeNode[T]]) -> int:
        """
        Calcule la hauteur de l'arbre.

        La hauteur d'un arbre est la longueur du chemin le plus long
        de la racine vers une feuille.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Hauteur de l'arbre (-1 si vide)
        :rtype: int
        """
        if root is None:
            return -1
        return root.get_height()

    def get_size(self, root: Optional[TreeNode[T]]) -> int:
        """
        Calcule le nombre de nœuds dans l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Nombre de nœuds dans l'arbre
        :rtype: int
        """
        if root is None:
            return 0

        size = 1  # Compter le nœud racine
        for child in root.get_children():
            size += self.get_size(child)

        return size

    @abstractmethod
    def get_min_node(self, root: TreeNode[T]) -> TreeNode[T]:
        """
        Trouve le nœud avec la valeur minimale dans l'arbre.

        :param root: Racine de l'arbre
        :type root: TreeNode[T]
        :return: Nœud avec la valeur minimale
        :rtype: TreeNode[T]
        """
        pass

    @abstractmethod
    def get_max_node(self, root: TreeNode[T]) -> TreeNode[T]:
        """
        Trouve le nœud avec la valeur maximale dans l'arbre.

        :param root: Racine de l'arbre
        :type root: TreeNode[T]
        :return: Nœud avec la valeur maximale
        :rtype: TreeNode[T]
        """
        pass

    def get_leaf_nodes(self, root: Optional[TreeNode[T]]) -> List[TreeNode[T]]:
        """
        Récupère tous les nœuds feuilles de l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Liste des nœuds feuilles
        :rtype: List[TreeNode[T]]
        """
        if root is None:
            return []

        if root.is_leaf():
            return [root]

        leaves = []
        for child in root.get_children():
            leaves.extend(self.get_leaf_nodes(child))

        return leaves

    def get_internal_nodes(self, root: Optional[TreeNode[T]]) -> List[TreeNode[T]]:
        """
        Récupère tous les nœuds internes de l'arbre.

        Un nœud interne est un nœud qui n'est pas une feuille.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Liste des nœuds internes
        :rtype: List[TreeNode[T]]
        """
        if root is None or root.is_leaf():
            return []

        internal_nodes = [root]
        for child in root.get_children():
            internal_nodes.extend(self.get_internal_nodes(child))

        return internal_nodes

    def get_depth(self, node: TreeNode[T]) -> int:
        """
        Calcule la profondeur d'un nœud.

        La profondeur d'un nœud est la longueur du chemin de la racine
        vers ce nœud.

        :param node: Nœud dont calculer la profondeur
        :type node: TreeNode[T]
        :return: Profondeur du nœud
        :rtype: int
        """
        return node.get_depth()

    def is_balanced(self, root: Optional[TreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre est équilibré.

        Un arbre est équilibré si la différence de hauteur entre les
        sous-arbres de chaque nœud est au plus 1.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: True si l'arbre est équilibré, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        return self._is_balanced_recursive(root) != -1

    def _is_balanced_recursive(self, node: TreeNode[T]) -> int:
        """
        Vérifie récursivement l'équilibre du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: TreeNode[T]
        :return: Hauteur du sous-arbre si équilibré, -1 sinon
        :rtype: int
        """
        if node.is_leaf():
            return 0

        children = node.get_children()
        if len(children) == 0:
            return 0

        heights = []
        for child in children:
            height = self._is_balanced_recursive(child)
            if height == -1:
                return -1
            heights.append(height)

        if len(heights) == 1:
            return 1 + heights[0]

        # Pour les arbres avec plus d'un enfant, vérifier l'équilibre
        min_height = min(heights)
        max_height = max(heights)

        if max_height - min_height > 1:
            return -1

        return 1 + max_height

    def is_complete(self, root: Optional[TreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre est complet.

        Un arbre est complet si tous les niveaux sont remplis,
        sauf peut-être le dernier niveau qui est rempli de gauche à droite.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: True si l'arbre est complet, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        return self._is_complete_recursive(root, 0, self.get_size(root))

    def _is_complete_recursive(
        self, node: TreeNode[T], index: int, total_nodes: int
    ) -> bool:
        """
        Vérifie récursivement si l'arbre est complet.

        :param node: Nœud actuel
        :type node: TreeNode[T]
        :param index: Index du nœud dans l'arbre
        :type index: int
        :param total_nodes: Nombre total de nœuds
        :type total_nodes: int
        :return: True si le sous-arbre est complet, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        if index >= total_nodes:
            return False

        children = node.get_children()
        if len(children) == 0:
            return True

        # Pour un arbre binaire complet
        if len(children) <= 2:
            left_complete = True
            right_complete = True

            if len(children) >= 1:
                left_complete = self._is_complete_recursive(
                    children[0], 2 * index + 1, total_nodes
                )

            if len(children) >= 2:
                right_complete = self._is_complete_recursive(
                    children[1], 2 * index + 2, total_nodes
                )

            return left_complete and right_complete

        # Pour les arbres non-binaires, vérifier tous les enfants
        for i, child in enumerate(children):
            child_index = 2 * index + i + 1
            if not self._is_complete_recursive(child, child_index, total_nodes):
                return False

        return True

    def is_full(self, root: Optional[TreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre est plein.

        Un arbre est plein si chaque nœud a soit 0 soit le nombre maximum
        d'enfants possibles.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: True si l'arbre est plein, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        children = root.get_children()

        # Si c'est une feuille, c'est plein
        if len(children) == 0:
            return True

        # Vérifier récursivement tous les enfants
        for child in children:
            if not self.is_full(child):
                return False

        return True
