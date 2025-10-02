"""
Itérateurs pour les arbres binaires de recherche.

Ce module implémente les itérateurs pour les différents types de parcours
des arbres binaires de recherche (préfixe, infixe, postfixe, par niveaux).
"""

from __future__ import annotations

from typing import Iterator, List, Optional

from .binary_tree_node import BinaryTreeNode
from .interfaces import T


class BSTIterator:
    """
    Classe de base pour les itérateurs BST.

    Cette classe fournit les fonctionnalités communes à tous les
    itérateurs d'arbres binaires de recherche.
    """

    def __init__(self, root: Optional[BinaryTreeNode[T]]):
        """
        Initialise l'itérateur.

        :param root: Nœud racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        """
        self._root = root
        self._current_index = 0
        self._elements: List[T] = []

    def __iter__(self) -> Iterator[T]:
        """
        Retourne l'itérateur lui-même.

        :return: Itérateur
        :rtype: Iterator[T]
        """
        return self

    def __next__(self) -> T:
        """
        Retourne l'élément suivant.

        :return: Élément suivant
        :rtype: T
        :raises StopIteration: Si tous les éléments ont été parcourus
        """
        if self._current_index >= len(self._elements):
            raise StopIteration
        element = self._elements[self._current_index]
        self._current_index += 1
        return element

    def __len__(self) -> int:
        """
        Retourne le nombre d'éléments.

        :return: Nombre d'éléments
        :rtype: int
        """
        return len(self._elements)


class PreorderIterator(BSTIterator):
    """
    Itérateur pour le parcours préfixe (racine, gauche, droite).
    """

    def __init__(self, root: Optional[BinaryTreeNode[T]]):
        """
        Initialise l'itérateur préfixe.

        :param root: Nœud racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        """
        super().__init__(root)
        self._elements = self._preorder_traversal(root)

    def _preorder_traversal(self, node: Optional[BinaryTreeNode[T]]) -> List[T]:
        """
        Effectue le parcours préfixe récursif.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :return: Liste des valeurs dans l'ordre préfixe
        :rtype: List[T]
        """
        if node is None:
            return []

        result = [node.value]
        result.extend(self._preorder_traversal(node.left))
        result.extend(self._preorder_traversal(node.right))
        return result


class InorderIterator(BSTIterator):
    """
    Itérateur pour le parcours infixe (gauche, racine, droite).
    """

    def __init__(self, root: Optional[BinaryTreeNode[T]]):
        """
        Initialise l'itérateur infixe.

        :param root: Nœud racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        """
        super().__init__(root)
        self._elements = self._inorder_traversal(root)

    def _inorder_traversal(self, node: Optional[BinaryTreeNode[T]]) -> List[T]:
        """
        Effectue le parcours infixe récursif.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :return: Liste des valeurs dans l'ordre infixe
        :rtype: List[T]
        """
        if node is None:
            return []

        result = []
        result.extend(self._inorder_traversal(node.left))
        result.append(node.value)
        result.extend(self._inorder_traversal(node.right))
        return result


class PostorderIterator(BSTIterator):
    """
    Itérateur pour le parcours postfixe (gauche, droite, racine).
    """

    def __init__(self, root: Optional[BinaryTreeNode[T]]):
        """
        Initialise l'itérateur postfixe.

        :param root: Nœud racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        """
        super().__init__(root)
        self._elements = self._postorder_traversal(root)

    def _postorder_traversal(self, node: Optional[BinaryTreeNode[T]]) -> List[T]:
        """
        Effectue le parcours postfixe récursif.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :return: Liste des valeurs dans l'ordre postfixe
        :rtype: List[T]
        """
        if node is None:
            return []

        result = []
        result.extend(self._postorder_traversal(node.left))
        result.extend(self._postorder_traversal(node.right))
        result.append(node.value)
        return result


class LevelOrderIterator(BSTIterator):
    """
    Itérateur pour le parcours par niveaux (largeur d'abord).
    """

    def __init__(self, root: Optional[BinaryTreeNode[T]]):
        """
        Initialise l'itérateur par niveaux.

        :param root: Nœud racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        """
        super().__init__(root)
        self._elements = self._level_order_traversal(root)

    def _level_order_traversal(self, root: Optional[BinaryTreeNode[T]]) -> List[T]:
        """
        Effectue le parcours par niveaux.

        :param root: Nœud racine de l'arbre
        :type root: Optional[BinaryTreeNode[T]]
        :return: Liste des valeurs dans l'ordre par niveaux
        :rtype: List[T]
        """
        if root is None:
            return []

        result = []
        queue = [root]

        while queue:
            node = queue.pop(0)
            result.append(node.value)

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        return result