"""
Classe BinaryTreeOperations pour les opérations sur les arbres binaires.

Ce module implémente la classe BinaryTreeOperations, spécialisée pour les
opérations sur les arbres binaires. Elle hérite de TreeOperations et ajoute
les fonctionnalités spécifiques aux nœuds binaires.
"""

from __future__ import annotations

from typing import List, Optional, Tuple, TYPE_CHECKING

from .binary_tree_node import BinaryTreeNode
from ..core.interfaces import T
from ..core.tree_node import TreeNode
from ..core.tree_operations import TreeOperations

if TYPE_CHECKING:
    from .binary_tree_node import BinaryTreeNode


class BinaryTreeOperations(TreeOperations[T]):
    """
    Opérations spécialisées pour les arbres binaires.

    Cette classe étend TreeOperations pour fournir des fonctionnalités
    spécifiques aux arbres binaires, avec des enfants gauche et droit
    explicites.
    """

    def search(self, root: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
        """
        Recherche une valeur dans l'arbre binaire.

        Cette implémentation utilise un parcours en profondeur pour
        rechercher la valeur dans l'arbre binaire.

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
            raise TypeError("Root must be a BinaryTreeNode for binary tree operations")

        binary_root = root
        if binary_root.value == value:
            return binary_root

        # Rechercher dans le sous-arbre gauche
        if binary_root.left is not None:
            result = self.search(binary_root.left, value)
            if result is not None:
                return result

        # Rechercher dans le sous-arbre droit
        if binary_root.right is not None:
            result = self.search(binary_root.right, value)
            if result is not None:
                return result

        return None

    def insert(self, root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]:
        """
        Insère une valeur dans l'arbre binaire.

        Cette implémentation insère la valeur comme enfant gauche du premier
        nœud disponible qui n'a pas d'enfant gauche.

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
            raise TypeError("Root must be a BinaryTreeNode for binary tree operations")

        binary_root = root

        # Trouver le premier nœud qui n'a pas d'enfant gauche
        node_to_insert = self._find_insertion_point(binary_root)
        if node_to_insert is None:
            return binary_root, False

        new_node = BinaryTreeNode(value)
        node_to_insert.set_left(new_node)

        return binary_root, True

    def _find_insertion_point(
        self, root: BinaryTreeNode[T]
    ) -> Optional[BinaryTreeNode[T]]:
        """
        Trouve le point d'insertion pour un nouvel élément.

        :param root: Racine de l'arbre
        :type root: BinaryTreeNode[T]
        :return: Nœud où insérer ou None si impossible
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if root.left is None:
            return root

        if root.right is None:
            return root

        # Chercher récursivement dans le sous-arbre gauche
        left_result = self._find_insertion_point(root.left)
        if left_result is not None:
            return left_result

        # Chercher récursivement dans le sous-arbre droit
        return self._find_insertion_point(root.right)

    def delete(
        self, root: Optional[TreeNode[T]], value: T
    ) -> Tuple[Optional[TreeNode[T]], bool]:
        """
        Supprime une valeur de l'arbre binaire.

        Cette implémentation supprime le nœud contenant la valeur et
        réorganise l'arbre en remplaçant le nœud supprimé par son
        sous-arbre droit si disponible, sinon par son sous-arbre gauche.

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
            raise TypeError("Root must be a BinaryTreeNode for binary tree operations")

        binary_root = root

        # Cas spécial : suppression de la racine
        if binary_root.value == value:
            if binary_root.right is not None:
                return binary_root.right, True
            elif binary_root.left is not None:
                return binary_root.left, True
            else:
                return None, True

        # Supprimer récursivement
        return self._delete_recursive(binary_root, value)

    def _delete_recursive(
        self, node: BinaryTreeNode[T], value: T
    ) -> Tuple[Optional[TreeNode[T]], bool]:
        """
        Supprime récursivement une valeur du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[TreeNode[T]], bool]
        """
        # Vérifier le sous-arbre gauche
        if node.left is not None and node.left.value == value:
            # Supprimer le nœud gauche
            if node.left.right is not None:
                node.set_left(node.left.right)
            elif node.left.left is not None:
                node.set_left(node.left.left)
            else:
                node.set_left(None)
            return node, True

        # Vérifier le sous-arbre droit
        if node.right is not None and node.right.value == value:
            # Supprimer le nœud droit
            if node.right.right is not None:
                node.set_right(node.right.right)
            elif node.right.left is not None:
                node.set_right(node.right.left)
            else:
                node.set_right(None)
            return node, True

        # Rechercher récursivement
        if node.left is not None:
            new_left, deleted = self._delete_recursive(node.left, value)
            if deleted:
                node.set_left(new_left)
                return node, True

        if node.right is not None:
            new_right, deleted = self._delete_recursive(node.right, value)
            if deleted:
                node.set_right(new_right)
                return node, True

        return node, False

    def get_min_node(self, root: TreeNode[T]) -> TreeNode[T]:
        """
        Trouve le nœud avec la valeur minimale dans l'arbre binaire.

        :param root: Racine de l'arbre
        :type root: TreeNode[T]
        :return: Nœud avec la valeur minimale
        :rtype: TreeNode[T]
        """
        if not isinstance(root, BinaryTreeNode):
            raise TypeError("Root must be a BinaryTreeNode for binary tree operations")

        binary_root = root
        current = binary_root

        # Parcourir vers la gauche pour trouver le minimum
        while current.left is not None:
            current = current.left

        return current

    def get_max_node(self, root: TreeNode[T]) -> TreeNode[T]:
        """
        Trouve le nœud avec la valeur maximale dans l'arbre binaire.

        :param root: Racine de l'arbre
        :type root: TreeNode[T]
        :return: Nœud avec la valeur maximale
        :rtype: TreeNode[T]
        """
        if not isinstance(root, BinaryTreeNode):
            raise TypeError("Root must be a BinaryTreeNode for binary tree operations")

        binary_root = root
        current = binary_root

        # Parcourir vers la droite pour trouver le maximum
        while current.right is not None:
            current = current.right

        return current

    def search_recursive(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> Optional[BinaryTreeNode[T]]:
        """
        Recherche récursive d'une valeur dans l'arbre binaire.

        :param root: Racine de l'arbre à rechercher
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvé
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if root is None:
            return None

        if root.value == value:
            return root

        # Rechercher dans le sous-arbre gauche
        left_result = self.search_recursive(root.left, value)
        if left_result is not None:
            return left_result

        # Rechercher dans le sous-arbre droit
        return self.search_recursive(root.right, value)

    def search_iterative(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> Optional[BinaryTreeNode[T]]:
        """
        Recherche itérative d'une valeur dans l'arbre binaire.

        :param root: Racine de l'arbre à rechercher
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvé
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if root is None:
            return None

        stack = [root]

        while stack:
            current = stack.pop()

            if current.value == value:
                return current

            # Ajouter les enfants à la pile
            if current.right is not None:
                stack.append(current.right)
            if current.left is not None:
                stack.append(current.left)

        return None

    def insert_recursive(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insertion récursive d'une valeur dans l'arbre binaire.

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

        # Trouver le point d'insertion
        insertion_point = self._find_insertion_point_recursive(root)
        if insertion_point is None:
            return root, False

        new_node = BinaryTreeNode(value)
        insertion_point.set_left(new_node)

        return root, True

    def _find_insertion_point_recursive(
        self, node: BinaryTreeNode[T]
    ) -> Optional[BinaryTreeNode[T]]:
        """
        Trouve récursivement le point d'insertion.

        :param node: Nœud actuel
        :type node: BinaryTreeNode[T]
        :return: Nœud où insérer ou None si impossible
        :rtype: Optional[BinaryTreeNode[T]]
        """
        if node.left is None:
            return node

        if node.right is None:
            return node

        # Chercher dans le sous-arbre gauche
        left_result = self._find_insertion_point_recursive(node.left)
        if left_result is not None:
            return left_result

        # Chercher dans le sous-arbre droit
        return self._find_insertion_point_recursive(node.right)

    def insert_iterative(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> Tuple[BinaryTreeNode[T], bool]:
        """
        Insertion itérative d'une valeur dans l'arbre binaire.

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

        # Utiliser une file pour trouver le premier nœud disponible
        queue = [root]

        while queue:
            current = queue.pop(0)

            if current.left is None:
                new_node = BinaryTreeNode(value)
                current.set_left(new_node)
                return root, True

            if current.right is None:
                new_node = BinaryTreeNode(value)
                current.set_right(new_node)
                return root, True

            # Ajouter les enfants à la file
            if current.left is not None:
                queue.append(current.left)
            if current.right is not None:
                queue.append(current.right)

        return root, False

    def delete_recursive(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> Tuple[Optional[BinaryTreeNode[T]], bool]:
        """
        Suppression récursive d'une valeur de l'arbre binaire.

        :param root: Racine de l'arbre où supprimer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[BinaryTreeNode[T]], bool]
        """
        if root is None:
            return None, False

        # Cas spécial : suppression de la racine
        if root.value == value:
            if root.right is not None:
                return root.right, True
            elif root.left is not None:
                return root.left, True
            else:
                return None, True

        # Supprimer récursivement
        return self._delete_recursive(root, value)

    def delete_iterative(
        self, root: Optional[BinaryTreeNode[T]], value: T
    ) -> Tuple[Optional[BinaryTreeNode[T]], bool]:
        """
        Suppression itérative d'une valeur de l'arbre binaire.

        :param root: Racine de l'arbre où supprimer
        :type root: Optional[BinaryTreeNode[T]]
        :param value: Valeur à supprimer
        :type value: T
        :return: Tuple (nouvelle racine, True si suppression réussie)
        :rtype: Tuple[Optional[BinaryTreeNode[T]], bool]
        """
        if root is None:
            return None, False

        # Cas spécial : suppression de la racine
        if root.value == value:
            if root.right is not None:
                return root.right, True
            elif root.left is not None:
                return root.left, True
            else:
                return None, True

        # Utiliser une pile pour parcourir l'arbre
        stack = [(root, None, None)]  # (node, parent, is_left_child)

        while stack:
            current, parent, is_left = stack.pop()

            if current.value == value:
                # Trouvé le nœud à supprimer
                replacement = None
                if current.right is not None:
                    replacement = current.right
                elif current.left is not None:
                    replacement = current.left

                # Mettre à jour le parent
                if parent is not None:
                    if is_left:
                        parent.set_left(replacement)
                    else:
                        parent.set_right(replacement)

                return root, True

            # Ajouter les enfants à la pile
            if current.right is not None:
                stack.append((current.right, current, False))
            if current.left is not None:
                stack.append((current.left, current, True))

        return root, False
