"""
Classe abstraite TreeIterator pour les itérateurs d'arbres.

Ce module implémente la classe TreeIterator, classe abstraite de base pour tous
les itérateurs d'arbres dans la librairie. Cette classe fournit l'interface
commune pour tous les types d'itérateurs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TYPE_CHECKING

from .interfaces import T

if TYPE_CHECKING:
    from .tree_node import TreeNode


class TreeIterator(ABC, Generic[T]):
    """
    Classe abstraite pour tous les itérateurs d'arbres.

    Cette classe définit l'interface commune pour tous les itérateurs d'arbres
    dans la librairie. Elle fournit les méthodes abstraites que chaque type
    d'itérateur doit implémenter.

    :param root: Nœud racine de l'arbre à parcourir
    :type root: Optional[TreeNode]
    """

    def __init__(self, root: Optional["TreeNode"]):
        """
        Initialise un nouvel itérateur d'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        """
        self._root = root
        self._initialized = False

    @abstractmethod
    def __iter__(self) -> "TreeIterator[T]":
        """
        Retourne l'itérateur lui-même.

        :return: L'itérateur lui-même
        :rtype: TreeIterator[T]
        """

    @abstractmethod
    def __next__(self) -> T:
        """
        Retourne la valeur suivante dans l'ordre de parcours.

        :return: Valeur suivante
        :rtype: T
        :raises StopIteration: Quand il n'y a plus d'éléments à parcourir
        """

    def has_next(self) -> bool:
        """
        Vérifie s'il y a encore des éléments à parcourir.

        Cette méthode peut être surchargée par les classes spécialisées
        pour une implémentation plus efficace.

        :return: True s'il y a encore des éléments, False sinon
        :rtype: bool
        """
        try:
            # Essayer de voir le prochain élément sans le consommer
            next_value = next(self)
            # Si on arrive ici, il y a un élément, mais on l'a consommé
            # On doit le remettre en place pour la prochaine fois
            self._put_back(next_value)
            return True
        except StopIteration:
            return False

    def _put_back(self, value: T) -> None:
        """
        Remet une valeur en place pour la prochaine itération.

        Cette méthode doit être implémentée par les classes spécialisées
        si elles veulent supporter has_next() efficacement.

        :param value: Valeur à remettre en place
        :type value: T
        """
        # Implémentation par défaut : ne fait rien
        # Les classes spécialisées peuvent surcharger cette méthode

    def peek(self) -> Optional[T]:
        """
        Regarde la prochaine valeur sans la consommer.

        :return: Prochaine valeur ou None s'il n'y en a pas
        :rtype: Optional[T]
        """
        try:
            next_value = next(self)
            self._put_back(next_value)
            return next_value
        except StopIteration:
            return None

    def to_list(self) -> list[T]:
        """
        Convertit l'itérateur en liste.

        :return: Liste de toutes les valeurs dans l'ordre de parcours
        :rtype: list[T]
        """
        return list(self)

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'itérateur.

        :return: Représentation string de l'itérateur
        :rtype: str
        """
        return f"{self.__class__.__name__}(root={self._root})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de l'itérateur.

        :return: Représentation détaillée de l'itérateur
        :rtype: str
        """
        return f"{self.__class__.__name__}(root={self._root!r})"
