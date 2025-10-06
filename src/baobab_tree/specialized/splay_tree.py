"""
Classe SplayTree pour les arbres auto-ajustables.

Ce module implémente la classe SplayTree, un arbre binaire de recherche
auto-ajustable qui déplace automatiquement les éléments accédés vers la racine.
"""

from __future__ import annotations

from typing import Any, List, Optional, Callable, TYPE_CHECKING

from ..core.exceptions import SplayTreeError, SplayOperationError, SplayValidationError
from ..core.interfaces import T, Comparable
from ..binary.binary_search_tree import BinarySearchTree
from .splay_node import SplayNode

if TYPE_CHECKING:
    from .splay_tree import SplayTree


class SplayTree(BinarySearchTree):
    """
    Arbre binaire de recherche auto-ajustable (Splay Tree).

    Cette classe implémente un arbre binaire de recherche qui déplace automatiquement
    les éléments accédés vers la racine. Cette propriété améliore les performances
    pour les accès répétés aux mêmes éléments.

    :param comparator: Fonction de comparaison personnalisée (optionnel)
    :type comparator: Optional[Callable[[T, T], int]], optional
    """

    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None):
        """
        Initialise un nouvel arbre Splay.

        :param comparator: Fonction de comparaison personnalisée (optionnel)
        :type comparator: Optional[Callable[[T, T], int]], optional
        :raises SplayTreeError: Si l'initialisation échoue
        """
        try:
            super().__init__(comparator)
            self._splay_count = 0
            self._total_accesses = 0
        except Exception as e:
            raise SplayTreeError(f"Failed to initialize SplayTree: {e}")

    def _create_node(self, value: T, parent: Optional[SplayNode] = None) -> SplayNode:
        """
        Crée un nouveau nœud Splay.

        :param value: Valeur du nœud
        :type value: T
        :param parent: Nœud parent (optionnel)
        :type parent: Optional[SplayNode], optional
        :return: Nouveau nœud Splay
        :rtype: SplayNode
        :raises SplayTreeError: Si la création du nœud échoue
        """
        try:
            return SplayNode(value, parent)
        except Exception as e:
            raise SplayTreeError(f"Failed to create SplayNode: {e}")

    def _splay(self, node: SplayNode) -> SplayNode:
        """
        Effectue l'opération de splay sur un nœud.

        :param node: Nœud à splay
        :type node: SplayNode
        :return: Nouvelle racine après splay
        :rtype: SplayNode
        :raises SplayOperationError: Si l'opération de splay échoue
        """
        try:
            if node is None:
                return None

            node.increment_splay()
            self._splay_count += 1

            while node._parent is not None:
                parent = node._parent
                grandparent = parent._parent

                if grandparent is None:
                    # Cas zig : parent est la racine
                    self._zig(node)
                elif self._is_zig_zig(node):
                    # Cas zig-zig
                    self._zig_zig(node)
                else:
                    # Cas zig-zag
                    self._zig_zag(node)

            return node
        except Exception as e:
            raise SplayOperationError(f"Failed to splay node: {e}", node)

    def _zig(self, node: SplayNode) -> None:
        """
        Effectue une rotation simple (zig).

        :param node: Nœud à faire tourner
        :type node: SplayNode
        :raises SplayOperationError: Si la rotation échoue
        """
        try:
            parent = node._parent
            if parent is None:
                return

            if node == parent.left:
                # Rotation droite
                parent.set_left(node.right)
                if node.right is not None:
                    node.right._parent = parent
                node.set_right(parent)
            else:
                # Rotation gauche
                parent.set_right(node.left)
                if node.left is not None:
                    node.left._parent = parent
                node.set_left(parent)

            # Mettre à jour les références parent
            grandparent = parent._parent
            parent._parent = node
            node._parent = grandparent

            if grandparent is not None:
                if grandparent.left == parent:
                    grandparent.set_left(node)
                else:
                    grandparent.set_right(node)
        except Exception as e:
            raise SplayOperationError(f"Failed to perform zig rotation: {e}", node)

    def _zig_zig(self, node: SplayNode) -> None:
        """
        Effectue une rotation double zig-zig.

        :param node: Nœud à faire tourner
        :type node: SplayNode
        :raises SplayOperationError: Si la rotation échoue
        """
        try:
            parent = node._parent
            grandparent = parent._parent

            if node == parent.left and parent == grandparent.left:
                # Double rotation droite
                self._zig(parent)
                self._zig(node)
            elif node == parent.right and parent == grandparent.right:
                # Double rotation gauche
                self._zig(parent)
                self._zig(node)
        except Exception as e:
            raise SplayOperationError(f"Failed to perform zig-zig rotation: {e}", node)

    def _zig_zag(self, node: SplayNode) -> None:
        """
        Effectue une rotation double zig-zag.

        :param node: Nœud à faire tourner
        :type node: SplayNode
        :raises SplayOperationError: Si la rotation échoue
        """
        try:
            parent = node._parent
            grandparent = parent._parent

            if node == parent.left and parent == grandparent.right:
                # Rotation gauche puis droite
                self._zig(node)
                self._zig(node)
            elif node == parent.right and parent == grandparent.left:
                # Rotation droite puis gauche
                self._zig(node)
                self._zig(node)
        except Exception as e:
            raise SplayOperationError(f"Failed to perform zig-zag rotation: {e}", node)

    def _is_zig_zig(self, node: SplayNode) -> bool:
        """
        Vérifie si c'est un cas zig-zig.

        :param node: Nœud à vérifier
        :type node: SplayNode
        :return: True si c'est un cas zig-zig, False sinon
        :rtype: bool
        :raises SplayOperationError: Si la vérification échoue
        """
        try:
            parent = node._parent
            grandparent = parent._parent if parent else None

            if grandparent is None:
                return False

            return (node == parent.left and parent == grandparent.left) or \
                   (node == parent.right and parent == grandparent.right)
        except Exception as e:
            raise SplayOperationError(f"Failed to check zig-zig case: {e}", node)

    def insert(self, value: T) -> bool:
        """
        Insère une valeur dans l'arbre Splay.

        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False si la valeur existe déjà
        :rtype: bool
        :raises SplayTreeError: Si l'insertion échoue
        """
        try:
            if self._root is None:
                self._root = self._create_node(value)
                self._size = 1
                return True

            # Rechercher la position d'insertion
            current = self._root
            parent = None

            while current is not None:
                parent = current
                if self.comparator(value, current.value) < 0:
                    current = current.left
                elif self.comparator(value, current.value) > 0:
                    current = current.right
                else:
                    # Valeur déjà présente, splay et retourner False
                    self._root = self._splay(current)
                    return False

            # Créer le nouveau nœud
            new_node = self._create_node(value)
            
            if self.comparator(value, parent.value) < 0:
                parent.set_left(new_node)
            else:
                parent.set_right(new_node)

            # Splay le nouveau nœud vers la racine
            self._root = self._splay(new_node)
            self._size += 1
            return True
        except Exception as e:
            raise SplayTreeError(f"Failed to insert value {value}: {e}")

    def search(self, value: T) -> bool:
        """
        Recherche une valeur dans l'arbre Splay.

        :param value: Valeur à rechercher
        :type value: T
        :return: True si la valeur est trouvée, False sinon
        :rtype: bool
        :raises SplayTreeError: Si la recherche échoue
        """
        try:
            if self._root is None:
                return False

            current = self._root
            while current is not None:
                if self.comparator(value, current.value) < 0:
                    current = current.left
                elif self.comparator(value, current.value) > 0:
                    current = current.right
                else:
                    # Valeur trouvée, splay vers la racine
                    current.increment_access()
                    self._total_accesses += 1
                    self._root = self._splay(current)
                    return True

            return False
        except Exception as e:
            raise SplayTreeError(f"Failed to search value {value}: {e}")

    def delete(self, value: T) -> bool:
        """
        Supprime une valeur de l'arbre Splay.

        :param value: Valeur à supprimer
        :type value: T
        :return: True si la suppression a réussi, False si la valeur n'existe pas
        :rtype: bool
        :raises SplayTreeError: Si la suppression échoue
        """
        try:
            if self._root is None:
                return False

            # Rechercher le nœud à supprimer
            current = self._root
            while current is not None:
                if self.comparator(value, current.value) < 0:
                    current = current.left
                elif self.comparator(value, current.value) > 0:
                    current = current.right
                else:
                    # Valeur trouvée, splay vers la racine
                    self._root = self._splay(current)
                    break

            if current is None:
                return False

            # Supprimer le nœud
            if current.left is None:
                self._root = current.right
                if self._root is not None:
                    self._root.parent = None
            elif current.right is None:
                self._root = current.left
                if self._root is not None:
                    self._root.parent = None
            else:
                # Nœud avec deux enfants
                # Trouver le successeur (minimum du sous-arbre droit)
                successor = current.right
                while successor.left is not None:
                    successor = successor.left

                # Remplacer la valeur du nœud par celle du successeur
                current.value = successor.value

                # Supprimer le successeur
                if successor.parent.left == successor:
                    successor.parent.set_left(successor.right)
                else:
                    successor.parent.set_right(successor.right)

                if successor.right is not None:
                    successor.right.parent = successor.parent

            self._size -= 1
            return True
        except Exception as e:
            raise SplayTreeError(f"Failed to delete value {value}: {e}")

    def find(self, value: T) -> Optional[T]:
        """
        Trouve une valeur dans l'arbre Splay et la retourne.

        :param value: Valeur à trouver
        :type value: T
        :return: Valeur trouvée ou None
        :rtype: Optional[T]
        :raises SplayTreeError: Si la recherche échoue
        """
        try:
            if self.search(value):
                return self._root.value
            return None
        except Exception as e:
            raise SplayTreeError(f"Failed to find value {value}: {e}")

    def get_min(self) -> Optional[T]:
        """
        Retourne la valeur minimale de l'arbre Splay.

        :return: Valeur minimale ou None si l'arbre est vide
        :rtype: Optional[T]
        :raises SplayTreeError: Si la recherche échoue
        """
        try:
            if self._root is None:
                return None

            current = self._root
            while current.left is not None:
                current = current.left

            # Splay le nœud minimum vers la racine
            self._root = self._splay(current)
            return current.value
        except Exception as e:
            raise SplayTreeError(f"Failed to get minimum value: {e}")

    def get_max(self) -> Optional[T]:
        """
        Retourne la valeur maximale de l'arbre Splay.

        :return: Valeur maximale ou None si l'arbre est vide
        :rtype: Optional[T]
        :raises SplayTreeError: Si la recherche échoue
        """
        try:
            if self._root is None:
                return None

            current = self._root
            while current.right is not None:
                current = current.right

            # Splay le nœud maximum vers la racine
            self._root = self._splay(current)
            return current.value
        except Exception as e:
            raise SplayTreeError(f"Failed to get maximum value: {e}")

    def remove_min(self) -> Optional[T]:
        """
        Supprime et retourne la valeur minimale de l'arbre Splay.

        :return: Valeur minimale supprimée ou None si l'arbre est vide
        :rtype: Optional[T]
        :raises SplayTreeError: Si la suppression échoue
        """
        try:
            min_value = self.get_min()
            if min_value is not None:
                self.delete(min_value)
            return min_value
        except Exception as e:
            raise SplayTreeError(f"Failed to remove minimum value: {e}")

    def remove_max(self) -> Optional[T]:
        """
        Supprime et retourne la valeur maximale de l'arbre Splay.

        :return: Valeur maximale supprimée ou None si l'arbre est vide
        :rtype: Optional[T]
        :raises SplayTreeError: Si la suppression échoue
        """
        try:
            max_value = self.get_max()
            if max_value is not None:
                self.delete(max_value)
            return max_value
        except Exception as e:
            raise SplayTreeError(f"Failed to remove maximum value: {e}")

    def merge(self, other: "SplayTree") -> None:
        """
        Fusionne cet arbre Splay avec un autre.

        :param other: Autre arbre Splay à fusionner
        :type other: SplayTree
        :raises SplayTreeError: Si la fusion échoue
        """
        try:
            if other is None or other._root is None:
                return

            if self._root is None:
                self._root = other._root
                self._size = other._size
                other._root = None
                other._size = 0
                return

            # Trouver le maximum de cet arbre
            max_node = self._root
            while max_node.right is not None:
                max_node = max_node.right

            # Splay le maximum vers la racine
            self._root = self._splay(max_node)

            # Attacher l'autre arbre comme sous-arbre droit
            self._root.set_right(other._root)
            if other._root is not None:
                other._root._parent = self._root

            self._size += other._size
            other._root = None
            other._size = 0
        except Exception as e:
            raise SplayTreeError(f"Failed to merge trees: {e}")

    def split(self, value: T) -> "SplayTree":
        """
        Divise l'arbre Splay en deux arbres basés sur une valeur.

        :param value: Valeur de division
        :type value: T
        :return: Nouvel arbre Splay contenant les valeurs >= value
        :rtype: SplayTree
        :raises SplayTreeError: Si la division échoue
        """
        try:
            if self._root is None:
                return SplayTree(self._comparator)

            # Rechercher la valeur de division
            current = self._root
            while current is not None:
                if self.comparator(value, current.value) < 0:
                    current = current.left
                elif self.comparator(value, current.value) > 0:
                    current = current.right
                else:
                    break

            if current is None:
                # Valeur non trouvée, trouver la position d'insertion
                current = self._root
                while current is not None:
                    if self.comparator(value, current.value) < 0:
                        if current.left is None:
                            break
                        current = current.left
                    else:
                        if current.right is None:
                            break
                        current = current.right

            # Splay le nœud vers la racine
            self._root = self._splay(current)

            # Créer le nouvel arbre avec le sous-arbre droit
            new_tree = SplayTree(self._comparator)
            if self._root.right is not None:
                new_tree._root = self._root.right
                new_tree._root._parent = None
                new_tree._size = self._count_nodes(new_tree._root)

            # Supprimer le sous-arbre droit de cet arbre
            self._root.set_right(None)
            self._size = self._count_nodes(self._root)

            return new_tree
        except Exception as e:
            raise SplayTreeError(f"Failed to split tree at value {value}: {e}")

    def _count_nodes(self, node: Optional[SplayNode]) -> int:
        """
        Compte récursivement le nombre de nœuds dans un sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[SplayNode]
        :return: Nombre de nœuds
        :rtype: int
        """
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def get_splay_count(self) -> int:
        """
        Retourne le nombre total d'opérations de splay effectuées.

        :return: Nombre total de splay
        :rtype: int
        """
        return self._splay_count

    def get_total_accesses(self) -> int:
        """
        Retourne le nombre total d'accès à l'arbre.

        :return: Nombre total d'accès
        :rtype: int
        """
        return self._total_accesses

    def get_performance_metrics(self) -> dict:
        """
        Retourne les métriques de performance de l'arbre.

        :return: Dictionnaire contenant les métriques
        :rtype: dict
        :raises SplayTreeError: Si la récupération des métriques échoue
        """
        try:
            return {
                "size": self._size,
                "height": self.get_height(),
                "splay_count": self._splay_count,
                "total_accesses": self._total_accesses,
                "average_splay_per_access": self._splay_count / max(1, self._total_accesses),
            }
        except Exception as e:
            raise SplayTreeError(f"Failed to get performance metrics: {e}")

    def is_valid(self) -> bool:
        """
        Vérifie si l'arbre Splay est valide.

        :return: True si l'arbre est valide, False sinon
        :rtype: bool
        :raises SplayValidationError: Si la validation échoue
        """
        try:
            if not super().is_valid():
                return False

            # Vérifier que tous les nœuds sont des SplayNode
            if self._root is not None:
                return self._validate_splay_nodes(self._root)

            return True
        except Exception as e:
            raise SplayValidationError(f"Failed to validate SplayTree: {e}", self)

    def _validate_splay_nodes(self, node: SplayNode) -> bool:
        """
        Valide récursivement que tous les nœuds sont des SplayNode.

        :param node: Nœud à valider
        :type node: SplayNode
        :return: True si tous les nœuds sont valides, False sinon
        :rtype: bool
        """
        if not isinstance(node, SplayNode):
            return False

        if node.left is not None and not self._validate_splay_nodes(node.left):
            return False

        if node.right is not None and not self._validate_splay_nodes(node.right):
            return False

        return True

    def print(self) -> None:
        """
        Affiche l'arbre Splay.

        :raises SplayTreeError: Si l'affichage échoue
        """
        try:
            if self._root is None:
                print("Empty SplayTree")
            else:
                print("SplayTree:")
                print(self._root.to_string())
        except Exception as e:
            raise SplayTreeError(f"Failed to print tree: {e}")

    def __str__(self) -> str:
        """
        Retourne une représentation string de l'arbre Splay.

        :return: Représentation string de l'arbre
        :rtype: str
        """
        try:
            if self._root is None:
                return "SplayTree(empty)"
            return f"SplayTree(size={self._size}, height={self.get_height()}, splay_count={self._splay_count})"
        except Exception:
            return "SplayTree(empty)"

    def __repr__(self) -> str:
        """
        Retourne une représentation détaillée de l'arbre Splay.

        :return: Représentation détaillée de l'arbre
        :rtype: str
        """
        try:
            return f"SplayTree(size={self._size}, root={self._root!r})"
        except Exception:
            return "SplayTree(empty)"