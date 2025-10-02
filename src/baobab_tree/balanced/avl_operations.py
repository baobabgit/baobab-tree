"""
Classe AVLOperations pour les opérations sur les arbres AVL.

Ce module implémente la classe AVLOperations, spécialisée pour les opérations
sur les arbres AVL. Elle hérite de BSTOperations et ajoute les fonctionnalités
spécifiques aux arbres AVL avec équilibrage automatique.
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple, TYPE_CHECKING

from ..binary.binary_tree_node import BinaryTreeNode
from ..binary.bst_operations import BSTOperations
from ..core.interfaces import T
from ..core.tree_node import TreeNode

if TYPE_CHECKING:
    from .binary_tree_node import BinaryTreeNode


class AVLOperations(BSTOperations[T]):
    """
    Opérations spécialisées pour les arbres AVL.

    Cette classe étend BSTOperations pour fournir des fonctionnalités
    spécifiques aux arbres AVL, incluant l'équilibrage automatique et
    les rotations nécessaires pour maintenir les propriétés AVL.
    """

    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None):
        """
        Initialise les opérations AVL.

        :param comparator: Fonction de comparaison personnalisée (optionnel)
        :type comparator: Optional[Callable[[T, T], int]], optional
        """
        super().__init__(comparator)

    def insert(self, root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]:
        """
        Insère une valeur dans l'arbre AVL avec équilibrage automatique.

        Cette implémentation maintient les propriétés AVL en effectuant
        les rotations nécessaires après insertion.

        :param root: Racine de l'arbre où insérer
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[TreeNode[T], bool]
        """
        if root is None:
            new_node = BinaryTreeNode(value)
            return new_node, True

        if not isinstance(root, BinaryTreeNode):
            raise TypeError("Root must be a BinaryTreeNode for AVL operations")

        binary_root = root
        new_root, inserted = self._insert_avl(binary_root, value)

        return new_root, inserted

    def _insert_avl(
        self, node: BinaryTreeNode[T], value: T
    ) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insère une valeur dans l'arbre AVL avec équilibrage.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[BinaryTreeNode[T], bool]
        """
        comparison = self._comparator(value, node.value)

        if comparison < 0:
            if node.left is None:
                new_node = BinaryTreeNode(value)
                node.set_left(new_node)
                return self._balance_node(node), True
            else:
                new_left, inserted = self._insert_avl(node.left, value)
                node.set_left(new_left)
                return self._balance_node(node), inserted
        elif comparison > 0:
            if node.right is None:
                new_node = BinaryTreeNode(value)
                node.set_right(new_node)
                return self._balance_node(node), True
            else:
                new_right, inserted = self._insert_avl(node.right, value)
                node.set_right(new_right)
                return self._balance_node(node), inserted
        else:
            # Valeur déjà présente
            return node, False

    def delete(
        self, root: Optional[TreeNode[T]], value: T
    ) -> Tuple[Optional[TreeNode[T]], bool]:
        """
        Supprime une valeur de l'arbre AVL avec équilibrage automatique.

        Cette implémentation maintient les propriétés AVL en effectuant
        les rotations nécessaires après suppression.

        :param root: Racine de l'arbre où supprimer
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[TreeNode[T]], bool]
        """
        if root is None:
            return None, False

        if not isinstance(root, BinaryTreeNode):
            raise TypeError("Root must be a BinaryTreeNode for AVL operations")

        binary_root = root
        new_root, deleted = self._delete_avl(binary_root, value)

        return new_root, deleted

    def _delete_avl(
        self, node: BinaryTreeNode[T], value: T
    ) -> Tuple[Optional[BinaryTreeNode[T]], bool]:
        """
        Supprime une valeur de l'arbre AVL avec équilibrage.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[BinaryTreeNode[T]], bool]
        """
        comparison = self._comparator(value, node.value)

        if comparison < 0:
            if node.left is None:
                return node, False
            new_left, deleted = self._delete_avl(node.left, value)
            node.set_left(new_left)
            return self._balance_node(node), deleted
        elif comparison > 0:
            if node.right is None:
                return node, False
            new_right, deleted = self._delete_avl(node.right, value)
            node.set_right(new_right)
            return self._balance_node(node), deleted
        else:
            # Nœud à supprimer trouvé
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                # Nœud avec deux enfants
                successor = self.get_min_node(node.right)
                node.value = successor.value
                new_right, _ = self._delete_avl(node.right, successor.value)
                node.set_right(new_right)
                return self._balance_node(node), True

    def _balance_node(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Équilibre un nœud AVL en effectuant les rotations nécessaires.

        :param node: Nœud à équilibrer
        :type node: BinaryTreeNode[T]
        :return: Nouvelle racine du sous-arbre équilibré
        :rtype: BinaryTreeNode[T]
        """
        balance_factor = self.get_balance_factor(node)

        # Cas déséquilibré à gauche
        if balance_factor < -1:
            if self.get_balance_factor(node.left) <= 0:
                # Rotation simple à droite
                return self._rotate_right(node)
            else:
                # Rotation double gauche-droite
                node.set_left(self._rotate_left(node.left))
                return self._rotate_right(node)

        # Cas déséquilibré à droite
        elif balance_factor > 1:
            if self.get_balance_factor(node.right) >= 0:
                # Rotation simple à gauche
                return self._rotate_left(node)
            else:
                # Rotation double droite-gauche
                node.set_right(self._rotate_right(node.right))
                return self._rotate_left(node)

        # Le nœud est déjà équilibré
        return node

    def _rotate_left(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation à gauche sur un nœud.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: BinaryTreeNode[T]
        :return: Nouvelle racine du sous-arbre
        :rtype: BinaryTreeNode[T]
        """
        if node.right is None:
            return node

        right_child = node.right
        left_subtree = right_child.left

        # Effectuer la rotation
        node.set_right(left_subtree)
        right_child.set_left(node)

        return right_child

    def _rotate_right(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """
        Effectue une rotation à droite sur un nœud.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: BinaryTreeNode[T]
        :return: Nouvelle racine du sous-arbre
        :rtype: BinaryTreeNode[T]
        """
        if node.left is None:
            return node

        left_child = node.left
        right_subtree = left_child.right

        # Effectuer la rotation
        node.set_left(right_subtree)
        left_child.set_right(node)

        return left_child

    def get_balance_factor(self, node: BinaryTreeNode[T]) -> int:
        """
        Calcule le facteur d'équilibre d'un nœud AVL.

        :param node: Nœud dont calculer le facteur d'équilibre
        :type node: BinaryTreeNode[T]
        :return: Facteur d'équilibre
        :rtype: int
        """
        left_height = node.left.get_height() if node.left is not None else -1
        right_height = node.right.get_height() if node.right is not None else -1

        return right_height - left_height

    def is_avl_tree(self, root: Optional[BinaryTreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre respecte les propriétés AVL.

        :param root: Racine de l'arbre à vérifier
        :type root: Optional[BinaryTreeNode[T]]
        :return: True si l'arbre est un AVL valide, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        # Vérifier les propriétés BST
        if not self.is_valid_bst(root):
            return False

        # Vérifier l'équilibre AVL
        return self._is_avl_balanced(root)

    def _is_avl_balanced(self, node: Optional[BinaryTreeNode[T]]) -> bool:
        """
        Vérifie récursivement l'équilibre AVL.

        :param node: Nœud à vérifier
        :type node: Optional[BinaryTreeNode[T]]
        :return: True si le sous-arbre est équilibré AVL, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        balance_factor = self.get_balance_factor(node)

        # Le facteur d'équilibre doit être entre -1 et 1
        if abs(balance_factor) > 1:
            return False

        # Vérifier récursivement les enfants
        return self._is_avl_balanced(node.left) and self._is_avl_balanced(node.right)

    def insert_with_avl_validation(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insertion avec validation des propriétés AVL.

        :param root: Racine de l'arbre où insérer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[BinaryTreeNode[T], bool]
        """
        new_root, inserted = self.insert(root, value)

        if inserted and not self.is_avl_tree(new_root):
            # Annuler l'insertion si elle viole les propriétés AVL
            new_root, _ = self.delete(new_root, value)
            return new_root, False

        return new_root, inserted

    def get_avl_height(self, root: Optional[BinaryTreeNode[T]]) -> int:
        """
        Calcule la hauteur d'un arbre AVL.

        Pour un arbre AVL, la hauteur est garantie d'être O(log n).

        :param root: Racine de l'arbre AVL
        :type root: Optional[BinaryTreeNode[T]]
        :return: Hauteur de l'arbre AVL
        :rtype: int
        """
        if root is None:
            return -1

        return root.get_height()

    def get_min_avl_height(self, n: int) -> int:
        """
        Calcule la hauteur minimale d'un arbre AVL avec n nœuds.

        :param n: Nombre de nœuds
        :type n: int
        :return: Hauteur minimale
        :rtype: int
        """
        if n <= 0:
            return -1

        # Formule pour la hauteur minimale d'un AVL
        # h = floor(log2(n + 1)) - 1
        import math

        return int(math.floor(math.log2(n + 1))) - 1

    def get_max_avl_height(self, n: int) -> int:
        """
        Calcule la hauteur maximale d'un arbre AVL avec n nœuds.

        :param n: Nombre de nœuds
        :type n: int
        :return: Hauteur maximale
        :rtype: int
        """
        if n <= 0:
            return -1

        # Formule pour la hauteur maximale d'un AVL
        # h = floor(1.44 * log2(n + 2)) - 0.328
        import math

        return int(math.floor(1.44 * math.log2(n + 2))) - 1

    def balance_tree(
        self, root: Optional[BinaryTreeNode[T]]
    ) -> Optional[BinaryTreeNode[T]]:
        """
        Équilibre complètement un arbre BST pour en faire un AVL.

        :param root: Racine de l'arbre BST à équilibrer
        :type root: Optional[BinaryTreeNode[T]]
        :return: Nouvelle racine de l'arbre AVL équilibré
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if root is None:
            return None

        # Collecter tous les nœuds dans l'ordre infixe
        nodes = []
        self._collect_nodes_inorder(root, nodes)

        # Reconstruire l'arbre AVL équilibré
        return self._build_balanced_avl(nodes, 0, len(nodes) - 1)

    def _collect_nodes_inorder(self, node: BinaryTreeNode[T], nodes: list) -> None:
        """
        Collecte les nœuds dans l'ordre infixe.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :param nodes: Liste pour stocker les nœuds
        :type nodes: list
        """
        if node is None:
            return

        self._collect_nodes_inorder(node.left, nodes)
        nodes.append(node.value)
        self._collect_nodes_inorder(node.right, nodes)

    def _build_balanced_avl(
        self, values: list, start: int, end: int
    ) -> Optional[BinaryTreeNode[T]]:
        """
        Construit un arbre AVL équilibré à partir d'une liste triée.

        :param values: Liste des valeurs triées
        :type values: list
        :param start: Index de début
        :type start: int
        :param end: Index de fin
        :type end: int
        :return: Racine de l'arbre AVL équilibré
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if start > end:
            return None

        mid = (start + end) // 2
        node = BinaryTreeNode(values[mid])

        node.set_left(self._build_balanced_avl(values, start, mid - 1))
        node.set_right(self._build_balanced_avl(values, mid + 1, end))

        return node
