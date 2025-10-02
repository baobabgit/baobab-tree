"""
Classe PreorderTraversal pour le parcours préfixe des arbres.

Ce module implémente la classe PreorderTraversal, qui effectue un parcours
préfixe (NLR: Nœud, Gauche, Droite) des arbres binaires.
"""

from __future__ import annotations

from typing import Iterator, List, Optional, TYPE_CHECKING

from .tree_traversal import TreeTraversal
from .interfaces import T

if TYPE_CHECKING:
    from .tree_node import TreeNode


class PreorderTraversal(TreeTraversal[T]):
    """
    Parcours préfixe (NLR: Nœud, Gauche, Droite) des arbres.

    Cette classe implémente l'algorithme de parcours préfixe, où chaque nœud
    est visité avant ses enfants. Pour un arbre binaire, l'ordre est :
    Nœud -> Sous-arbre gauche -> Sous-arbre droit.

    :param traversal_name: Nom du parcours (par défaut: "Preorder")
    :type traversal_name: Optional[str], optional
    """

    def __init__(self, traversal_name: Optional[str] = None):
        """
        Initialise un nouveau parcours préfixe.

        :param traversal_name: Nom du parcours (par défaut: "Preorder")
        :type traversal_name: Optional[str], optional
        """
        super().__init__(traversal_name or "Preorder")

    def traverse(self, root: Optional["TreeNode"]) -> List[T]:
        """
        Effectue le parcours préfixe récursif de l'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Liste des valeurs dans l'ordre préfixe
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return []

        self.validate_tree(root)
        return self._traverse_recursive(root)

    def traverse_iter(self, root: Optional["TreeNode"]) -> Iterator[T]:
        """
        Effectue le parcours préfixe itératif de l'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Itérateur sur les valeurs dans l'ordre préfixe
        :rtype: Iterator[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return iter([])

        self.validate_tree(root)
        return self._traverse_iterative(root)

    def _traverse_recursive(self, node: "TreeNode") -> List[T]:
        """
        Parcourt récursivement l'arbre en ordre préfixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :return: Liste des valeurs dans l'ordre préfixe
        :rtype: List[T]
        """
        result = [node.value]

        # Parcourir les enfants dans l'ordre
        for child in node.get_children():
            result.extend(self._traverse_recursive(child))

        return result

    def _traverse_iterative(self, root: "TreeNode") -> Iterator[T]:
        """
        Parcourt itérativement l'arbre en ordre préfixe avec une pile.

        :param root: Nœud racine de l'arbre
        :type root: TreeNode
        :return: Itérateur sur les valeurs dans l'ordre préfixe
        :rtype: Iterator[T]
        """
        stack = [root]

        while stack:
            node = stack.pop()
            yield node.value

            # Ajouter les enfants en ordre inverse pour maintenir l'ordre préfixe
            children = node.get_children()
            children.reverse()
            stack.extend(children)

    def _traverse_depth_limited_recursive(
        self, node: "TreeNode", max_depth: int, current_depth: int
    ) -> List[T]:
        """
        Parcourt récursivement l'arbre avec limitation de profondeur en ordre préfixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :param max_depth: Profondeur maximale
        :type max_depth: int
        :param current_depth: Profondeur actuelle
        :type current_depth: int
        :return: Liste des valeurs dans l'ordre préfixe limité
        :rtype: List[T]
        """
        if current_depth >= max_depth:
            return []

        result = [node.value]

        # Parcourir les enfants dans l'ordre
        for child in node.get_children():
            result.extend(
                self._traverse_depth_limited_recursive(
                    child, max_depth, current_depth + 1
                )
            )

        return result

    def _traverse_right_to_left_recursive(self, node: "TreeNode") -> List[T]:
        """
        Parcourt récursivement l'arbre de droite à gauche en ordre préfixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :return: Liste des valeurs dans l'ordre préfixe droite-gauche
        :rtype: List[T]
        """
        result = [node.value]

        # Parcourir les enfants en ordre inverse (droite à gauche)
        children = node.get_children()
        children.reverse()
        for child in children:
            result.extend(self._traverse_right_to_left_recursive(child))

        return result
