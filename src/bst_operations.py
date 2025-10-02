"""
Classe BSTOperations pour les opérations sur les arbres binaires de recherche.

Ce module implémente la classe BSTOperations, spécialisée pour les opérations
sur les arbres binaires de recherche (BST). Elle hérite de BinaryTreeOperations
et ajoute les fonctionnalités spécifiques aux BST avec respect des propriétés
de recherche binaire.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple, TYPE_CHECKING

from .binary_tree_node import BinaryTreeNode
from .binary_tree_operations import BinaryTreeOperations
from .interfaces import T
from .tree_node import TreeNode

if TYPE_CHECKING:
    from .binary_tree_node import BinaryTreeNode


class BSTOperations(BinaryTreeOperations[T]):
    """
    Opérations spécialisées pour les arbres binaires de recherche.

    Cette classe étend BinaryTreeOperations pour fournir des fonctionnalités
    spécifiques aux BST, respectant les propriétés de recherche binaire :
    - Tous les éléments du sous-arbre gauche sont inférieurs à la racine
    - Tous les éléments du sous-arbre droit sont supérieurs à la racine
    """

    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None):
        """
        Initialise les opérations BST.

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

    def search(self, root: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
        """
        Recherche une valeur dans le BST.

        Cette implémentation utilise la propriété BST pour une recherche
        efficace en O(h) où h est la hauteur de l'arbre.

        :param root: Racine de l'arbre à rechercher
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvé
        :rtype: Optional[TreeNode[T]]
        """
        if root is None:
            return None
        
        if not isinstance(root, BinaryTreeNode):
            raise TypeError("Root must be a BinaryTreeNode for BST operations")
        
        binary_root = root
        current = binary_root
        
        while current is not None:
            comparison = self._comparator(value, current.value)
            
            if comparison == 0:
                return current
            elif comparison < 0:
                current = current.left
            else:
                current = current.right
        
        return None

    def insert(self, root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]:
        """
        Insère une valeur dans le BST.

        Cette implémentation respecte les propriétés BST et insère la valeur
        à la position appropriée selon l'ordre.

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
            raise TypeError("Root must be a BinaryTreeNode for BST operations")
        
        binary_root = root
        return self._insert_recursive(binary_root, value)

    def _insert_recursive(self, node: BinaryTreeNode[T], value: T) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insère récursivement une valeur dans le BST.

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
                return node, True
            else:
                new_left, inserted = self._insert_recursive(node.left, value)
                node.set_left(new_left)
                return node, inserted
        elif comparison > 0:
            if node.right is None:
                new_node = BinaryTreeNode(value)
                node.set_right(new_node)
                return node, True
            else:
                new_right, inserted = self._insert_recursive(node.right, value)
                node.set_right(new_right)
                return node, inserted
        else:
            # Valeur déjà présente
            return node, False

    def delete(self, root: Optional[TreeNode[T]], value: T) -> Tuple[Optional[TreeNode[T]], bool]:
        """
        Supprime une valeur du BST.

        Cette implémentation gère les trois cas de suppression :
        1. Nœud feuille : suppression directe
        2. Nœud avec un enfant : remplacement par l'enfant
        3. Nœud avec deux enfants : remplacement par le successeur

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
            raise TypeError("Root must be a BinaryTreeNode for BST operations")
        
        binary_root = root
        return self._delete_recursive(binary_root, value)

    def _delete_recursive(self, node: BinaryTreeNode[T], value: T) -> Tuple[Optional[BinaryTreeNode[T]], bool]:
        """
        Supprime récursivement une valeur du BST.

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
            new_left, deleted = self._delete_recursive(node.left, value)
            node.set_left(new_left)
            return node, deleted
        elif comparison > 0:
            if node.right is None:
                return node, False
            new_right, deleted = self._delete_recursive(node.right, value)
            node.set_right(new_right)
            return node, deleted
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
                new_right, _ = self._delete_recursive(node.right, successor.value)
                node.set_right(new_right)
                return node, True

    def get_min_node(self, root: TreeNode[T]) -> TreeNode[T]:
        """
        Trouve le nœud avec la valeur minimale dans le BST.

        :param root: Racine de l'arbre
        :type root: TreeNode[T]
        :return: Nœud avec la valeur minimale
        :rtype: TreeNode[T]
        """
        if not isinstance(root, BinaryTreeNode):
            raise TypeError("Root must be a BinaryTreeNode for BST operations")
        
        binary_root = root
        current = binary_root
        
        # Parcourir vers la gauche pour trouver le minimum
        while current.left is not None:
            current = current.left
        
        return current

    def get_max_node(self, root: TreeNode[T]) -> TreeNode[T]:
        """
        Trouve le nœud avec la valeur maximale dans le BST.

        :param root: Racine de l'arbre
        :type root: TreeNode[T]
        :return: Nœud avec la valeur maximale
        :rtype: TreeNode[T]
        """
        if not isinstance(root, BinaryTreeNode):
            raise TypeError("Root must be a BinaryTreeNode for BST operations")
        
        binary_root = root
        current = binary_root
        
        # Parcourir vers la droite pour trouver le maximum
        while current.right is not None:
            current = current.right
        
        return current

    def search_recursive(self, root: Optional[BinaryTreeNode[T]], value: T) -> Optional[BinaryTreeNode[T]]:
        """
        Recherche récursive d'une valeur dans le BST.

        :param root: Racine de l'arbre à rechercher
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvé
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if root is None:
            return None
        
        comparison = self._comparator(value, root.value)
        
        if comparison == 0:
            return root
        elif comparison < 0:
            return self.search_recursive(root.left, value)
        else:
            return self.search_recursive(root.right, value)

    def search_iterative(self, root: Optional[BinaryTreeNode[T]], value: T) -> Optional[BinaryTreeNode[T]]:
        """
        Recherche itérative d'une valeur dans le BST.

        :param root: Racine de l'arbre à rechercher
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvé
        :rtype: Optional[BinaryTreeNode[T]]
        """
        current = root
        
        while current is not None:
            comparison = self._comparator(value, current.value)
            
            if comparison == 0:
                return current
            elif comparison < 0:
                current = current.left
            else:
                current = current.right
        
        return None

    def insert_recursive(self, root: Optional[BinaryTreeNode[T]], value: T) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insertion récursive d'une valeur dans le BST.

        :param root: Racine de l'arbre où insérer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[BinaryTreeNode[T], bool]
        """
        if root is None:
            new_node = BinaryTreeNode(value)
            return new_node, True
        
        return self._insert_recursive(root, value)

    def insert_iterative(self, root: Optional[BinaryTreeNode[T]], value: T) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insertion itérative d'une valeur dans le BST.

        :param root: Racine de l'arbre où insérer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[BinaryTreeNode[T], bool]
        """
        if root is None:
            new_node = BinaryTreeNode(value)
            return new_node, True
        
        current = root
        
        while True:
            comparison = self._comparator(value, current.value)
            
            if comparison < 0:
                if current.left is None:
                    new_node = BinaryTreeNode(value)
                    current.set_left(new_node)
                    return root, True
                current = current.left
            elif comparison > 0:
                if current.right is None:
                    new_node = BinaryTreeNode(value)
                    current.set_right(new_node)
                    return root, True
                current = current.right
            else:
                # Valeur déjà présente
                return root, False

    def delete_recursive(self, root: Optional[BinaryTreeNode[T]], value: T) -> Tuple[Optional[BinaryTreeNode[T]], bool]:
        """
        Suppression récursive d'une valeur du BST.

        :param root: Racine de l'arbre où supprimer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[BinaryTreeNode[T]], bool]
        """
        if root is None:
            return None, False
        
        return self._delete_recursive(root, value)

    def delete_iterative(self, root: Optional[BinaryTreeNode[T]], value: T) -> Tuple[Optional[BinaryTreeNode[T]], bool]:
        """
        Suppression itérative d'une valeur du BST.

        :param root: Racine de l'arbre où supprimer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[BinaryTreeNode[T]], bool]
        """
        if root is None:
            return None, False
        
        # Trouver le nœud à supprimer et son parent
        current = root
        parent = None
        is_left_child = False
        
        while current is not None:
            comparison = self._comparator(value, current.value)
            
            if comparison == 0:
                # Trouvé le nœud à supprimer
                break
            elif comparison < 0:
                parent = current
                current = current.left
                is_left_child = True
            else:
                parent = current
                current = current.right
                is_left_child = False
        
        if current is None:
            return root, False
        
        # Supprimer le nœud
        if current.left is None and current.right is None:
            # Cas 1: Nœud feuille
            replacement = None
        elif current.left is None:
            # Cas 2: Un seul enfant droit
            replacement = current.right
        elif current.right is None:
            # Cas 2: Un seul enfant gauche
            replacement = current.left
        else:
            # Cas 3: Deux enfants
            successor = self.get_min_node(current.right)
            current.value = successor.value
            
            # Supprimer le successeur
            current.right, _ = self._delete_recursive(current.right, successor.value)
            return root, True
        
        # Mettre à jour le parent
        if parent is None:
            # Suppression de la racine
            return replacement, True
        else:
            if is_left_child:
                parent.set_left(replacement)
            else:
                parent.set_right(replacement)
            return root, True

    def insert_with_validation(self, root: Optional[BinaryTreeNode[T]], value: T) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insertion avec validation des propriétés BST.

        :param root: Racine de l'arbre où insérer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[BinaryTreeNode[T], bool]
        """
        new_root, inserted = self.insert(root, value)
        
        if inserted and not self.is_valid_bst(new_root):
            # Annuler l'insertion si elle viole les propriétés BST
            new_root, _ = self.delete(new_root, value)
            return new_root, False
        
        return new_root, inserted

    def insert_with_duplicates(self, root: Optional[BinaryTreeNode[T]], value: T) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insertion permettant les doublons.

        Les doublons sont insérés dans le sous-arbre droit.

        :param root: Racine de l'arbre où insérer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à insérer
        :type value: T
        :return: Tuple (nouvelle racine, True si insertion réussie)
        :rtype: Tuple[BinaryTreeNode[T], bool]
        """
        if root is None:
            new_node = BinaryTreeNode(value)
            return new_node, True
        
        comparison = self._comparator(value, root.value)
        
        if comparison <= 0:
            # Insérer à gauche (y compris les doublons)
            new_left, inserted = self.insert_with_duplicates(root.left, value)
            root.set_left(new_left)
            return root, inserted
        else:
            # Insérer à droite
            new_right, inserted = self.insert_with_duplicates(root.right, value)
            root.set_right(new_right)
            return root, inserted

    def is_valid_bst(self, root: Optional[BinaryTreeNode[T]]) -> bool:
        """
        Valide les propriétés BST de l'arbre.

        :param root: Racine de l'arbre à valider
        :type root: Optional[BinaryTreeNode[T]]
        :return: True si l'arbre respecte les propriétés BST, False sinon
        :rtype: bool
        """
        return self._is_valid_bst_recursive(root, None, None)

    def _is_valid_bst_recursive(
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
            self._is_valid_bst_recursive(node.left, min_val, node.value) and
            self._is_valid_bst_recursive(node.right, node.value, max_val)
        )

    def get_balance_factor(self, node: BinaryTreeNode[T]) -> int:
        """
        Calcule le facteur d'équilibre d'un nœud.

        Le facteur d'équilibre est la différence entre la hauteur du
        sous-arbre droit et la hauteur du sous-arbre gauche.

        :param node: Nœud dont calculer le facteur d'équilibre
        :type node: BinaryTreeNode[T]
        :return: Facteur d'équilibre
        :rtype: int
        """
        left_height = node.left.get_height() if node.left is not None else -1
        right_height = node.right.get_height() if node.right is not None else -1
        
        return right_height - left_height