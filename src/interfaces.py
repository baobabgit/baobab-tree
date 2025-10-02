"""
Interfaces et types pour la librairie d'arbres.

Ce module définit les interfaces et types génériques utilisés dans toute
la librairie d'arbres pour assurer la cohérence et la type safety.
"""

from typing import Any, Generic, Protocol, TypeVar, runtime_checkable


# Type générique pour les valeurs stockées dans les nœuds
T = TypeVar("T", bound="Comparable")


@runtime_checkable
class Comparable(Protocol):
    """
    Interface pour les types comparables.

    Cette interface définit les méthodes de comparaison requises pour
    les valeurs stockées dans les nœuds d'arbres. Elle permet d'assurer
    que les valeurs peuvent être comparées de manière cohérente.

    Tous les types implémentant cette interface doivent fournir les
    méthodes de comparaison standard de Python.
    """

    def __lt__(self, other: Any) -> bool:
        """
        Teste si self est strictement inférieur à other.

        :param other: Valeur à comparer
        :type other: Any
        :return: True si self < other, False sinon
        :rtype: bool
        """
        ...

    def __le__(self, other: Any) -> bool:
        """
        Teste si self est inférieur ou égal à other.

        :param other: Valeur à comparer
        :type other: Any
        :return: True si self <= other, False sinon
        :rtype: bool
        """
        ...

    def __gt__(self, other: Any) -> bool:
        """
        Teste si self est strictement supérieur à other.

        :param other: Valeur à comparer
        :type other: Any
        :return: True si self > other, False sinon
        :rtype: bool
        """
        ...

    def __ge__(self, other: Any) -> bool:
        """
        Teste si self est supérieur ou égal à other.

        :param other: Valeur à comparer
        :type other: Any
        :return: True si self >= other, False sinon
        :rtype: bool
        """
        ...

    def __eq__(self, other: Any) -> bool:
        """
        Teste si self est égal à other.

        :param other: Valeur à comparer
        :type other: Any
        :return: True si self == other, False sinon
        :rtype: bool
        """
        ...

    def __ne__(self, other: Any) -> bool:
        """
        Teste si self est différent de other.

        :param other: Valeur à comparer
        :type other: Any
        :return: True si self != other, False sinon
        :rtype: bool
        """
        ...


class TreeInterface(Protocol, Generic[T]):
    """
    Interface de base pour tous les types d'arbres.

    Cette interface définit les méthodes communes que tous les arbres
    doivent implémenter, assurant une API cohérente à travers la librairie.
    """

    def is_empty(self) -> bool:
        """
        Vérifie si l'arbre est vide.

        :return: True si l'arbre est vide, False sinon
        :rtype: bool
        """
        ...

    def size(self) -> int:
        """
        Retourne le nombre de nœuds dans l'arbre.

        :return: Nombre de nœuds dans l'arbre
        :rtype: int
        """
        ...

    def height(self) -> int:
        """
        Retourne la hauteur de l'arbre.

        :return: Hauteur de l'arbre (-1 si vide)
        :rtype: int
        """
        ...

    def clear(self) -> None:
        """
        Vide l'arbre de tous ses nœuds.

        :return: None
        :rtype: None
        """
        ...


class TreeTraversalInterface(Protocol):
    """
    Interface pour les algorithmes de parcours d'arbres.

    Cette interface définit les méthodes communes pour tous les
    algorithmes de parcours d'arbres.
    """

    def traverse(self, root) -> list:
        """
        Effectue le parcours de l'arbre à partir de la racine.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: TreeNode
        :return: Liste des nœuds dans l'ordre de parcours
        :rtype: list
        """
        ...

    def __iter__(self):
        """
        Permet l'itération sur les nœuds de l'arbre.

        :return: Itérateur sur les nœuds
        :rtype: Iterator
        """
        ...


class TreeOperationInterface(Protocol):
    """
    Interface pour les opérations sur les arbres.

    Cette interface définit les méthodes communes pour toutes les
    opérations sur les arbres (insertion, suppression, recherche).
    """

    def insert(self, value: T) -> bool:
        """
        Insère une valeur dans l'arbre.

        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False sinon
        :rtype: bool
        """
        ...

    def delete(self, value: T) -> bool:
        """
        Supprime une valeur de l'arbre.

        :param value: Valeur à supprimer
        :type value: T
        :return: True si la suppression a réussi, False sinon
        :rtype: bool
        """
        ...

    def search(self, value: T) -> bool:
        """
        Recherche une valeur dans l'arbre.

        :param value: Valeur à rechercher
        :type value: T
        :return: True si la valeur est trouvée, False sinon
        :rtype: bool
        """
        ...
