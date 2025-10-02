"""
Classe InorderTraversal pour le parcours infixe des arbres.

Ce module implémente la classe InorderTraversal, qui effectue un parcours
infixe (LNR: Gauche, Nœud, Droite) des arbres binaires.
"""

from __future__ import annotations

from typing import Iterator, List, Optional, TYPE_CHECKING

from .tree_traversal import TreeTraversal
from ..core.interfaces import T

if TYPE_CHECKING:
    from ..core.tree_node import TreeNode


class InorderTraversal(TreeTraversal[T]):
    """
    Parcours infixe (LNR: Gauche, Nœud, Droite) des arbres binaires.

    Cette classe implémente l'algorithme de parcours infixe, où chaque nœud
    est visité entre ses enfants gauche et droit. Pour un arbre binaire de
    recherche, ce parcours donne les valeurs dans l'ordre croissant.

    :param traversal_name: Nom du parcours (par défaut: "Inorder")
    :type traversal_name: Optional[str], optional
    """

    def __init__(self, traversal_name: Optional[str] = None):
        """
        Initialise un nouveau parcours infixe.

        :param traversal_name: Nom du parcours (par défaut: "Inorder")
        :type traversal_name: Optional[str], optional
        """
        super().__init__(traversal_name or "Inorder")

    def traverse(self, root: Optional["TreeNode"]) -> List[T]:
        """
        Effectue le parcours infixe récursif de l'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Liste des valeurs dans l'ordre infixe
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return []

        self.validate_tree(root)
        return self._traverse_recursive(root)

    def traverse_iter(self, root: Optional["TreeNode"]) -> Iterator[T]:
        """
        Effectue le parcours infixe itératif de l'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Itérateur sur les valeurs dans l'ordre infixe
        :rtype: Iterator[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return iter([])

        self.validate_tree(root)
        return self._traverse_iterative(root)

    def _traverse_recursive(self, node: "TreeNode") -> List[T]:
        """
        Parcourt récursivement l'arbre en ordre infixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :return: Liste des valeurs dans l'ordre infixe
        :rtype: List[T]
        """
        result = []
        children = node.get_children()

        # Pour les arbres binaires : gauche, nœud, droite
        if len(children) >= 1:
            result.extend(self._traverse_recursive(children[0]))

        result.append(node.value)

        if len(children) >= 2:
            result.extend(self._traverse_recursive(children[1]))

        return result

    def _traverse_iterative(self, root: "TreeNode") -> Iterator[T]:
        """
        Parcourt itérativement l'arbre en ordre infixe avec une pile.

        :param root: Nœud racine de l'arbre
        :type root: TreeNode
        :return: Itérateur sur les valeurs dans l'ordre infixe
        :rtype: Iterator[T]
        """
        stack = []
        current = root
        visited = set()

        while stack or current is not None:
            # Aller à gauche autant que possible
            while current is not None and current not in visited:
                stack.append(current)
                children = current.get_children()
                if children:
                    current = children[0]  # Enfant gauche
                else:
                    current = None

            if stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    yield current.value

                    # Passer au sous-arbre droit
                    children = current.get_children()
                    if len(children) >= 2:
                        current = children[1]  # Enfant droit
                    else:
                        current = None

    def _traverse_depth_limited_recursive(
        self, node: "TreeNode", max_depth: int, current_depth: int
    ) -> List[T]:
        """
        Parcourt récursivement l'arbre avec limitation de profondeur en ordre infixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :param max_depth: Profondeur maximale
        :type max_depth: int
        :param current_depth: Profondeur actuelle
        :type current_depth: int
        :return: Liste des valeurs dans l'ordre infixe limité
        :rtype: List[T]
        """
        if current_depth >= max_depth:
            return []

        result = []
        children = node.get_children()

        # Pour les arbres binaires : gauche, nœud, droite
        if len(children) >= 1:
            result.extend(
                self._traverse_depth_limited_recursive(
                    children[0], max_depth, current_depth + 1
                )
            )

        result.append(node.value)

        if len(children) >= 2:
            result.extend(
                self._traverse_depth_limited_recursive(
                    children[1], max_depth, current_depth + 1
                )
            )

        return result

    def _traverse_right_to_left_recursive(self, node: "TreeNode") -> List[T]:
        """
        Parcourt récursivement l'arbre de droite à gauche en ordre infixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :return: Liste des valeurs dans l'ordre infixe droite-gauche
        :rtype: List[T]
        """
        result = []
        children = node.get_children()

        # Pour les arbres binaires : droite, nœud, gauche (inverse de l'infixe normal)
        if len(children) >= 2:
            result.extend(self._traverse_right_to_left_recursive(children[1]))

        result.append(node.value)

        if len(children) >= 1:
            result.extend(self._traverse_right_to_left_recursive(children[0]))

        return result
