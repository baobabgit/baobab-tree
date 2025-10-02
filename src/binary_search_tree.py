"""
Classe BinarySearchTree pour les arbres binaires de recherche.

Ce module implémente la classe BinarySearchTree, structure fondamentale
pour les arbres binaires de recherche. Cette classe fournit toutes les
opérations de base nécessaires pour manipuler un BST.
"""

from __future__ import annotations

from typing import Any, Callable, Iterator, List, Optional

from .binary_tree_node import BinaryTreeNode
from .bst_iterators import (
    InorderIterator,
    LevelOrderIterator,
    PostorderIterator,
    PreorderIterator,
)
from .exceptions import (
    BSTError,
    DuplicateValueError,
    InvalidOperationError,
    ValueNotFoundError,
)
from .interfaces import T



class BinarySearchTree:
    """
    Arbre binaire de recherche générique.

    Cette classe implémente un arbre binaire de recherche (BST) avec toutes
    les opérations de base : insertion, suppression, recherche, parcours.
    Elle respecte la propriété BST : pour chaque nœud, tous les éléments
    du sous-arbre gauche sont inférieurs et tous les éléments du sous-arbre
    droit sont supérieurs.

    :param comparator: Fonction de comparaison personnalisée (optionnel)
    :type comparator: Optional[Callable[[T, T], int]], optional
    """

    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None) -> None:
        """
        Initialise un nouvel arbre binaire de recherche.

        :param comparator: Fonction de comparaison personnalisée (optionnel)
        :type comparator: Optional[Callable[[T, T], int]], optional
        """
        self._root: Optional[BinaryTreeNode[T]] = None
        self._size: int = 0
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

    @property
    def root(self) -> Optional[BinaryTreeNode[T]]:
        """
        Retourne la racine de l'arbre.

        :return: Nœud racine ou None si l'arbre est vide
        :rtype: Optional[BinaryTreeNode[T]]
        """
        return self._root

    @property
    def size(self) -> int:
        """
        Retourne le nombre d'éléments dans l'arbre.

        :return: Nombre d'éléments dans l'arbre
        :rtype: int
        """
        return self._size

    @property
    def comparator(self) -> Callable[[T, T], int]:
        """
        Retourne la fonction de comparaison utilisée.

        :return: Fonction de comparaison
        :rtype: Callable[[T, T], int]
        """
        return self._comparator

    def is_empty(self) -> bool:
        """
        Vérifie si l'arbre est vide.

        :return: True si l'arbre est vide, False sinon
        :rtype: bool
        """
        return self._root is None

    def clear(self) -> None:
        """
        Vide l'arbre de tous ses éléments.

        :return: None
        :rtype: None
        """
        self._root = None
        self._size = 0

    def get_root(self) -> Optional[BinaryTreeNode[T]]:
        """
        Retourne la racine de l'arbre.

        :return: Nœud racine ou None si l'arbre est vide
        :rtype: Optional[BinaryTreeNode[T]]
        """
        return self._root

    def get_size(self) -> int:
        """
        Retourne le nombre d'éléments dans l'arbre.

        :return: Nombre d'éléments dans l'arbre
        :rtype: int
        """
        return self._size

    def get_height(self) -> int:
        """
        Calcule la hauteur de l'arbre.

        La hauteur d'un arbre est la longueur du chemin le plus long
        de la racine vers une feuille.

        :return: Hauteur de l'arbre (-1 si vide)
        :rtype: int
        """
        if self._root is None:
            return -1
        return self._root.get_height()

    def get_min(self) -> Optional[T]:
        """
        Trouve la valeur minimale dans l'arbre.

        :return: Valeur minimale ou None si l'arbre est vide
        :rtype: Optional[T]
        """
        if self._root is None:
            return None

        current = self._root
        while current.left is not None:
            current = current.left
        return current.value

    def get_max(self) -> Optional[T]:
        """
        Trouve la valeur maximale dans l'arbre.

        :return: Valeur maximale ou None si l'arbre est vide
        :rtype: Optional[T]
        """
        if self._root is None:
            return None

        current = self._root
        while current.right is not None:
            current = current.right
        return current.value

    def insert(self, value: T) -> bool:
        """
        Insère une valeur dans l'arbre BST.

        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False si la valeur existe déjà
        :rtype: bool
        :raises BSTError: Si une erreur survient lors de l'insertion
        """
        try:
            if self._root is None:
                self._root = BinaryTreeNode(value)
                self._size = 1
                return True

            return self._insert_recursive(self._root, value)
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during insertion: {str(e)}", "insert")

    def _insert_recursive(self, node: BinaryTreeNode[T], value: T) -> bool:
        """
        Insère récursivement une valeur dans le sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False si la valeur existe déjà
        :rtype: bool
        """
        comparison = self._comparator(value, node.value)

        if comparison < 0:
            if node.left is None:
                new_node = BinaryTreeNode(value)
                node.set_left(new_node)
                self._size += 1
                return True
            else:
                return self._insert_recursive(node.left, value)
        elif comparison > 0:
            if node.right is None:
                new_node = BinaryTreeNode(value)
                node.set_right(new_node)
                self._size += 1
                return True
            else:
                return self._insert_recursive(node.right, value)
        else:
            # Valeur déjà présente
            return False

    def delete(self, value: T) -> bool:
        """
        Supprime une valeur de l'arbre BST.

        :param value: Valeur à supprimer
        :type value: T
        :return: True si la suppression a réussi, False si la valeur n'existe pas
        :rtype: bool
        :raises BSTError: Si une erreur survient lors de la suppression
        """
        try:
            if self._root is None:
                return False

            # Cas spécial : suppression de la racine
            if self._comparator(value, self._root.value) == 0:
                self._root = self._delete_node(self._root)
                self._size -= 1
                return True

            return self._delete_recursive(self._root, value)
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during deletion: {str(e)}", "delete")

    def _delete_recursive(self, node: BinaryTreeNode[T], value: T) -> bool:
        """
        Supprime récursivement une valeur du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
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
                node.set_left(self._delete_node(node.left))
                self._size -= 1
                return True
            else:
                return self._delete_recursive(node.left, value)
        elif comparison > 0:
            if node.right is None:
                return False
            if self._comparator(value, node.right.value) == 0:
                node.set_right(self._delete_node(node.right))
                self._size -= 1
                return True
            else:
                return self._delete_recursive(node.right, value)
        else:
            # Ce cas ne devrait pas arriver car on gère la racine séparément
            return False

    def _delete_node(self, node: BinaryTreeNode[T]) -> Optional[BinaryTreeNode[T]]:
        """
        Supprime un nœud et retourne son remplaçant.

        :param node: Nœud à supprimer
        :type node: BinaryTreeNode[T]
        :return: Nœud remplaçant ou None
        :rtype: Optional[BinaryTreeNode[T]]
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
        successor = self._find_min_node(node.right)
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

    def _find_min_node(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
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

    def search(self, value: T) -> Optional[BinaryTreeNode[T]]:
        """
        Recherche une valeur dans l'arbre BST.

        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvée
        :rtype: Optional[BinaryTreeNode[T]]
        :raises BSTError: Si une erreur survient lors de la recherche
        """
        try:
            return self._search_recursive(self._root, value)
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during search: {str(e)}", "search")

    def _search_recursive(self, node: Optional[BinaryTreeNode[T]], value: T) -> Optional[BinaryTreeNode[T]]:
        """
        Recherche récursivement une valeur dans le sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvée
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if node is None:
            return None

        comparison = self._comparator(value, node.value)

        if comparison < 0:
            return self._search_recursive(node.left, value)
        elif comparison > 0:
            return self._search_recursive(node.right, value)
        else:
            return node

    def contains(self, value: T) -> bool:
        """
        Vérifie si une valeur existe dans l'arbre.

        :param value: Valeur à vérifier
        :type value: T
        :return: True si la valeur existe, False sinon
        :rtype: bool
        """
        return self.search(value) is not None

    def is_valid(self) -> bool:
        """
        Valide les propriétés BST de l'arbre.

        :return: True si l'arbre respecte les propriétés BST, False sinon
        :rtype: bool
        :raises BSTError: Si une erreur survient lors de la validation
        """
        try:
            return self._is_valid_recursive(self._root, None, None)
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during validation: {str(e)}", "is_valid")

    def _is_valid_recursive(
        self, 
        node: Optional[BinaryTreeNode[T]], 
        min_val: Optional[T], 
        max_val: Optional[T]
    ) -> bool:
        """
        Valide récursivement les propriétés BST du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :param min_val: Valeur minimale autorisée
        :type min_val: Optional[T]
        :param max_val: Valeur maximale autorisée
        :type max_val: Optional[T]
        :return: True si le sous-arbre respecte les propriétés BST, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        # Vérifier les contraintes min/max
        if min_val is not None and self._comparator(node.value, min_val) <= 0:
            return False
        if max_val is not None and self._comparator(node.value, max_val) >= 0:
            return False

        # Valider récursivement les sous-arbres
        return (
            self._is_valid_recursive(node.left, min_val, node.value) and
            self._is_valid_recursive(node.right, node.value, max_val)
        )

    def is_balanced(self) -> bool:
        """
        Vérifie si l'arbre est équilibré.

        Un arbre est équilibré si la différence de hauteur entre les
        sous-arbres gauche et droit de chaque nœud est au plus 1.

        :return: True si l'arbre est équilibré, False sinon
        :rtype: bool
        :raises BSTError: Si une erreur survient lors de la vérification
        """
        try:
            return self._is_balanced_recursive(self._root) != -1
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during balance check: {str(e)}", "is_balanced")

    def _is_balanced_recursive(self, node: Optional[BinaryTreeNode[T]]) -> int:
        """
        Vérifie récursivement l'équilibre du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[BinaryTreeNode[T]]
        :return: Hauteur du sous-arbre si équilibré, -1 sinon
        :rtype: int
        """
        if node is None:
            return 0

        left_height = self._is_balanced_recursive(node.left)
        if left_height == -1:
            return -1

        right_height = self._is_balanced_recursive(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return 1 + max(left_height, right_height)

    def get_balance_factor(self) -> int:
        """
        Calcule le facteur d'équilibre de l'arbre.

        Le facteur d'équilibre est la différence entre la hauteur du
        sous-arbre droit et la hauteur du sous-arbre gauche.

        :return: Facteur d'équilibre (0 si équilibré)
        :rtype: int
        """
        if self._root is None:
            return 0

        left_height = self._root.left.get_height() if self._root.left is not None else -1
        right_height = self._root.right.get_height() if self._root.right is not None else -1

        return right_height - left_height

    def preorder_traversal(self) -> List[T]:
        """
        Effectue le parcours préfixe de l'arbre.

        :return: Liste des valeurs dans l'ordre préfixe
        :rtype: List[T]
        """
        if self._root is None:
            return []
        return self._preorder_traversal_recursive(self._root)

    def _preorder_traversal_recursive(self, node: BinaryTreeNode[T]) -> List[T]:
        """
        Effectue le parcours préfixe récursif.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Liste des valeurs dans l'ordre préfixe
        :rtype: List[T]
        """
        result = [node.value]
        if node.left is not None:
            result.extend(self._preorder_traversal_recursive(node.left))
        if node.right is not None:
            result.extend(self._preorder_traversal_recursive(node.right))
        return result

    def inorder_traversal(self) -> List[T]:
        """
        Effectue le parcours infixe de l'arbre.

        :return: Liste des valeurs dans l'ordre infixe (triée pour un BST)
        :rtype: List[T]
        """
        if self._root is None:
            return []
        return self._inorder_traversal_recursive(self._root)

    def _inorder_traversal_recursive(self, node: BinaryTreeNode[T]) -> List[T]:
        """
        Effectue le parcours infixe récursif.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Liste des valeurs dans l'ordre infixe
        :rtype: List[T]
        """
        result = []
        if node.left is not None:
            result.extend(self._inorder_traversal_recursive(node.left))
        result.append(node.value)
        if node.right is not None:
            result.extend(self._inorder_traversal_recursive(node.right))
        return result

    def postorder_traversal(self) -> List[T]:
        """
        Effectue le parcours postfixe de l'arbre.

        :return: Liste des valeurs dans l'ordre postfixe
        :rtype: List[T]
        """
        if self._root is None:
            return []
        return self._postorder_traversal_recursive(self._root)

    def _postorder_traversal_recursive(self, node: BinaryTreeNode[T]) -> List[T]:
        """
        Effectue le parcours postfixe récursif.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Liste des valeurs dans l'ordre postfixe
        :rtype: List[T]
        """
        result = []
        if node.left is not None:
            result.extend(self._postorder_traversal_recursive(node.left))
        if node.right is not None:
            result.extend(self._postorder_traversal_recursive(node.right))
        result.append(node.value)
        return result

    def level_order_traversal(self) -> List[T]:
        """
        Effectue le parcours par niveaux de l'arbre.

        :return: Liste des valeurs dans l'ordre par niveaux
        :rtype: List[T]
        """
        if self._root is None:
            return []

        result = []
        queue = [self._root]

        while queue:
            node = queue.pop(0)
            result.append(node.value)

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        return result

    def preorder_iter(self) -> Iterator[T]:
        """
        Retourne un itérateur pour le parcours préfixe.

        :return: Itérateur préfixe
        :rtype: Iterator[T]
        """
        return PreorderIterator(self._root)

    def inorder_iter(self) -> Iterator[T]:
        """
        Retourne un itérateur pour le parcours infixe.

        :return: Itérateur infixe
        :rtype: Iterator[T]
        """
        return InorderIterator(self._root)

    def postorder_iter(self) -> Iterator[T]:
        """
        Retourne un itérateur pour le parcours postfixe.

        :return: Itérateur postfixe
        :rtype: Iterator[T]
        """
        return PostorderIterator(self._root)

    def level_order_iter(self) -> Iterator[T]:
        """
        Retourne un itérateur pour le parcours par niveaux.

        :return: Itérateur par niveaux
        :rtype: Iterator[T]
        """
        return LevelOrderIterator(self._root)

    def find_successor(self, value: T) -> Optional[T]:
        """
        Trouve le successeur d'une valeur dans l'arbre.

        Le successeur est la plus petite valeur supérieure à la valeur donnée.

        :param value: Valeur dont on cherche le successeur
        :type value: T
        :return: Successeur ou None si aucun successeur
        :rtype: Optional[T]
        :raises BSTError: Si une erreur survient lors de la recherche
        """
        try:
            node = self.search(value)
            if node is None:
                raise ValueNotFoundError(f"Value {value} not found", value, "find_successor")

            # Si le nœud a un sous-arbre droit, le successeur est le minimum de ce sous-arbre
            if node.right is not None:
                min_node = self._find_min_node(node.right)
                return min_node.value

            # Sinon, remonter jusqu'à trouver un ancêtre dont le fils gauche est aussi un ancêtre
            current = node
            parent = node.parent
            while parent is not None and current == parent.right:
                current = parent
                parent = parent.parent

            return parent.value if parent is not None else None
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during successor search: {str(e)}", "find_successor")

    def find_predecessor(self, value: T) -> Optional[T]:
        """
        Trouve le prédécesseur d'une valeur dans l'arbre.

        Le prédécesseur est la plus grande valeur inférieure à la valeur donnée.

        :param value: Valeur dont on cherche le prédécesseur
        :type value: T
        :return: Prédécesseur ou None si aucun prédécesseur
        :rtype: Optional[T]
        :raises BSTError: Si une erreur survient lors de la recherche
        """
        try:
            node = self.search(value)
            if node is None:
                raise ValueNotFoundError(f"Value {value} not found", value, "find_predecessor")

            # Si le nœud a un sous-arbre gauche, le prédécesseur est le maximum de ce sous-arbre
            if node.left is not None:
                max_node = self._find_max_node(node.left)
                return max_node.value

            # Sinon, remonter jusqu'à trouver un ancêtre dont le fils droit est aussi un ancêtre
            current = node
            parent = node.parent
            while parent is not None and current == parent.left:
                current = parent
                parent = parent.parent

            return parent.value if parent is not None else None
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during predecessor search: {str(e)}", "find_predecessor")

    def _find_max_node(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
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

    def find_floor(self, value: T) -> Optional[T]:
        """
        Trouve la plus grande valeur inférieure ou égale à la valeur donnée.

        :param value: Valeur de référence
        :type value: T
        :return: Plus grande valeur <= value ou None
        :rtype: Optional[T]
        :raises BSTError: Si une erreur survient lors de la recherche
        """
        try:
            return self._find_floor_recursive(self._root, value)
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during floor search: {str(e)}", "find_floor")

    def _find_floor_recursive(self, node: Optional[BinaryTreeNode[T]], value: T) -> Optional[T]:
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

    def find_ceiling(self, value: T) -> Optional[T]:
        """
        Trouve la plus petite valeur supérieure ou égale à la valeur donnée.

        :param value: Valeur de référence
        :type value: T
        :return: Plus petite valeur >= value ou None
        :rtype: Optional[T]
        :raises BSTError: Si une erreur survient lors de la recherche
        """
        try:
            return self._find_ceiling_recursive(self._root, value)
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during ceiling search: {str(e)}", "find_ceiling")

    def _find_ceiling_recursive(self, node: Optional[BinaryTreeNode[T]], value: T) -> Optional[T]:
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

    def range_query(self, min_val: T, max_val: T) -> List[T]:
        """
        Effectue une requête de plage sur l'arbre.

        :param min_val: Valeur minimale (incluse)
        :type min_val: T
        :param max_val: Valeur maximale (incluse)
        :type max_val: T
        :return: Liste des valeurs dans la plage
        :rtype: List[T]
        :raises BSTError: Si une erreur survient lors de la requête
        """
        try:
            if self._comparator(min_val, max_val) > 0:
                return []

            result = []
            self._range_query_recursive(self._root, min_val, max_val, result)
            return result
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during range query: {str(e)}", "range_query")

    def _range_query_recursive(
        self, 
        node: Optional[BinaryTreeNode[T]], 
        min_val: T, 
        max_val: T, 
        result: List[T]
    ) -> None:
        """
        Effectue récursivement la requête de plage.

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
        if (self._comparator(node.value, min_val) >= 0 and 
            self._comparator(node.value, max_val) <= 0):
            result.append(node.value)

        # Explorer le sous-arbre gauche si nécessaire
        if self._comparator(node.value, min_val) > 0:
            self._range_query_recursive(node.left, min_val, max_val, result)

        # Explorer le sous-arbre droit si nécessaire
        if self._comparator(node.value, max_val) < 0:
            self._range_query_recursive(node.right, min_val, max_val, result)

    def count_range(self, min_val: T, max_val: T) -> int:
        """
        Compte le nombre de valeurs dans une plage.

        :param min_val: Valeur minimale (incluse)
        :type min_val: T
        :param max_val: Valeur maximale (incluse)
        :type max_val: T
        :return: Nombre de valeurs dans la plage
        :rtype: int
        :raises BSTError: Si une erreur survient lors du comptage
        """
        try:
            if self._comparator(min_val, max_val) > 0:
                return 0

            return self._count_range_recursive(self._root, min_val, max_val)
        except Exception as e:
            if isinstance(e, BSTError):
                raise
            raise BSTError(f"Error during range count: {str(e)}", "count_range")

    def _count_range_recursive(
        self, 
        node: Optional[BinaryTreeNode[T]], 
        min_val: T, 
        max_val: T
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
        if (self._comparator(node.value, min_val) >= 0 and 
            self._comparator(node.value, max_val) <= 0):
            count += 1

        # Explorer le sous-arbre gauche si nécessaire
        if self._comparator(node.value, min_val) > 0:
            count += self._count_range_recursive(node.left, min_val, max_val)

        # Explorer le sous-arbre droit si nécessaire
        if self._comparator(node.value, max_val) < 0:
            count += self._count_range_recursive(node.right, min_val, max_val)

        return count

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'arbre.

        :return: Représentation string de l'arbre
        :rtype: str
        """
        if self._root is None:
            return "BinarySearchTree(empty)"
        return f"BinarySearchTree(size={self._size}, height={self.get_height()})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de l'arbre.

        :return: Représentation détaillée de l'arbre
        :rtype: str
        """
        return f"BinarySearchTree(root={self._root}, size={self._size})"

    def __len__(self) -> int:
        """
        Retourne le nombre d'éléments dans l'arbre.

        :return: Nombre d'éléments dans l'arbre
        :rtype: int
        """
        return self._size

    def __bool__(self) -> bool:
        """
        Retourne True si l'arbre n'est pas vide.

        :return: True si l'arbre n'est pas vide, False sinon
        :rtype: bool
        """
        return not self.is_empty()