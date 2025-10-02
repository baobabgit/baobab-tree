"""
Itérateurs spécialisés pour les parcours d'arbres.

Ce module implémente les itérateurs concrets pour chaque type de parcours
d'arbres : PreorderIterator, InorderIterator, PostorderIterator et
LevelOrderIterator.
"""

from __future__ import annotations

from collections import deque
from typing import Optional, TYPE_CHECKING

from .tree_iterator import TreeIterator
from ..core.interfaces import T

if TYPE_CHECKING:
    from ..core.tree_node import TreeNode


class PreorderIterator(TreeIterator[T]):
    """
    Itérateur préfixe avec pile.

    Cet itérateur implémente le parcours préfixe (NLR) en utilisant une pile
    pour maintenir l'ordre de visite des nœuds.

    :param root: Nœud racine de l'arbre à parcourir
    :type root: Optional[TreeNode]
    """

    def __init__(self, root: Optional["TreeNode"]):
        """
        Initialise un nouvel itérateur préfixe.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        """
        super().__init__(root)
        self._stack = []
        if root is not None:
            self._stack.append(root)

    def __iter__(self) -> "PreorderIterator[T]":
        """
        Retourne l'itérateur lui-même.

        :return: L'itérateur lui-même
        :rtype: PreorderIterator[T]
        """
        return self

    def __next__(self) -> T:
        """
        Retourne la valeur suivante dans l'ordre préfixe.

        :return: Valeur suivante
        :rtype: T
        :raises StopIteration: Quand il n'y a plus d'éléments à parcourir
        """
        if not self._stack:
            raise StopIteration

        node = self._stack.pop()

        # Ajouter les enfants en ordre inverse pour maintenir l'ordre préfixe
        children = node.get_children()
        children.reverse()
        self._stack.extend(children)

        return node.value


class InorderIterator(TreeIterator[T]):
    """
    Itérateur infixe avec pile.

    Cet itérateur implémente le parcours infixe (LNR) en utilisant une pile
    et un ensemble de nœuds visités pour maintenir l'ordre de visite.

    :param root: Nœud racine de l'arbre à parcourir
    :type root: Optional[TreeNode]
    """

    def __init__(self, root: Optional["TreeNode"]):
        """
        Initialise un nouvel itérateur infixe.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        """
        super().__init__(root)
        self._stack = []
        self._visited = set()
        self._current = root

    def __iter__(self) -> "InorderIterator[T]":
        """
        Retourne l'itérateur lui-même.

        :return: L'itérateur lui-même
        :rtype: InorderIterator[T]
        """
        return self

    def __next__(self) -> T:
        """
        Retourne la valeur suivante dans l'ordre infixe.

        :return: Valeur suivante
        :rtype: T
        :raises StopIteration: Quand il n'y a plus d'éléments à parcourir
        """
        # Aller à gauche autant que possible
        while self._current is not None and self._current not in self._visited:
            self._stack.append(self._current)
            children = self._current.get_children()
            if children:
                self._current = children[0]  # Enfant gauche
            else:
                self._current = None

        if self._stack:
            self._current = self._stack.pop()
            if self._current not in self._visited:
                self._visited.add(self._current)
                value = self._current.value

                # Passer au sous-arbre droit
                children = self._current.get_children()
                if len(children) >= 2:
                    self._current = children[1]  # Enfant droit
                else:
                    self._current = None

                return value

        raise StopIteration


class PostorderIterator(TreeIterator[T]):
    """
    Itérateur postfixe avec pile.

    Cet itérateur implémente le parcours postfixe (LRN) en utilisant une pile
    et un pointeur vers le dernier nœud visité pour maintenir l'ordre de visite.

    :param root: Nœud racine de l'arbre à parcourir
    :type root: Optional[TreeNode]
    """

    def __init__(self, root: Optional["TreeNode"]):
        """
        Initialise un nouvel itérateur postfixe.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        """
        super().__init__(root)
        self._stack = []
        self._current = root
        self._last_visited = None

    def __iter__(self) -> "PostorderIterator[T]":
        """
        Retourne l'itérateur lui-même.

        :return: L'itérateur lui-même
        :rtype: PostorderIterator[T]
        """
        return self

    def __next__(self) -> T:
        """
        Retourne la valeur suivante dans l'ordre postfixe.

        :return: Valeur suivante
        :rtype: T
        :raises StopIteration: Quand il n'y a plus d'éléments à parcourir
        """
        while True:
            # Aller à gauche autant que possible
            while self._current is not None:
                self._stack.append(self._current)
                children = self._current.get_children()
                if children:
                    self._current = children[0]  # Enfant gauche
                else:
                    self._current = None

            if not self._stack:
                raise StopIteration

            self._current = self._stack[-1]
            children = self._current.get_children()

            # Si le nœud n'a pas d'enfant droit ou si l'enfant droit a déjà été visité
            if len(children) < 2 or children[1] == self._last_visited:
                value = self._current.value
                self._last_visited = self._current
                self._stack.pop()
                self._current = None
                return value

            # Aller au sous-arbre droit
            self._current = children[1]


class LevelOrderIterator(TreeIterator[T]):
    """
    Itérateur par niveaux avec file.

    Cet itérateur implémente le parcours par niveaux (BFS) en utilisant une file
    pour maintenir l'ordre de visite des nœuds niveau par niveau.

    :param root: Nœud racine de l'arbre à parcourir
    :type root: Optional[TreeNode]
    """

    def __init__(self, root: Optional["TreeNode"]):
        """
        Initialise un nouvel itérateur par niveaux.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        """
        super().__init__(root)
        self._queue = deque()
        if root is not None:
            self._queue.append(root)

    def __iter__(self) -> "LevelOrderIterator[T]":
        """
        Retourne l'itérateur lui-même.

        :return: L'itérateur lui-même
        :rtype: LevelOrderIterator[T]
        """
        return self

    def __next__(self) -> T:
        """
        Retourne la valeur suivante dans l'ordre par niveaux.

        :return: Valeur suivante
        :rtype: T
        :raises StopIteration: Quand il n'y a plus d'éléments à parcourir
        """
        if not self._queue:
            raise StopIteration

        node = self._queue.popleft()

        # Ajouter tous les enfants à la file
        for child in node.get_children():
            self._queue.append(child)

        return node.value


class LevelOrderWithLevelIterator(TreeIterator[tuple[T, int]]):
    """
    Itérateur par niveaux avec information du niveau.

    Cet itérateur implémente le parcours par niveaux en retournant des tuples
    (valeur, niveau) pour chaque nœud visité.

    :param root: Nœud racine de l'arbre à parcourir
    :type root: Optional[TreeNode]
    """

    def __init__(self, root: Optional["TreeNode"]):
        """
        Initialise un nouvel itérateur par niveaux avec information du niveau.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        """
        super().__init__(root)
        self._queue = deque()
        if root is not None:
            self._queue.append((root, 0))  # (node, level)

    def __iter__(self) -> "LevelOrderWithLevelIterator[T]":
        """
        Retourne l'itérateur lui-même.

        :return: L'itérateur lui-même
        :rtype: LevelOrderWithLevelIterator[T]
        """
        return self

    def __next__(self) -> tuple[T, int]:
        """
        Retourne le tuple (valeur, niveau) suivant dans l'ordre par niveaux.

        :return: Tuple (valeur, niveau) suivant
        :rtype: tuple[T, int]
        :raises StopIteration: Quand il n'y a plus d'éléments à parcourir
        """
        if not self._queue:
            raise StopIteration

        node, level = self._queue.popleft()

        # Ajouter tous les enfants avec leur niveau
        for child in node.get_children():
            self._queue.append((child, level + 1))

        return (node.value, level)
