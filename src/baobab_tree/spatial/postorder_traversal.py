"""
Classe PostorderTraversal pour le parcours postfixe des arbres.

Ce module implémente la classe PostorderTraversal, qui effectue un parcours
postfixe (LRN: Gauche, Droite, Nœud) des arbres binaires.
"""

from __future__ import annotations

from typing import Iterator, List, Optional, TYPE_CHECKING

from .tree_traversal import TreeTraversal
from ..core.interfaces import T

if TYPE_CHECKING:
    from ..core.tree_node import TreeNode


class PostorderTraversal(TreeTraversal[T]):
    """
    Parcours postfixe (LRN: Gauche, Droite, Nœud) des arbres.

    Cette classe implémente l'algorithme de parcours postfixe, où chaque nœud
    est visité après ses enfants. Pour un arbre binaire, l'ordre est :
    Sous-arbre gauche -> Sous-arbre droit -> Nœud.

    :param traversal_name: Nom du parcours (par défaut: "Postorder")
    :type traversal_name: Optional[str], optional
    """

    def __init__(self, traversal_name: Optional[str] = None):
        """
        Initialise un nouveau parcours postfixe.

        :param traversal_name: Nom du parcours (par défaut: "Postorder")
        :type traversal_name: Optional[str], optional
        """
        super().__init__(traversal_name or "Postorder")

    def traverse(self, root: Optional["TreeNode"]) -> List[T]:
        """
        Effectue le parcours postfixe récursif de l'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Liste des valeurs dans l'ordre postfixe
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return []

        self.validate_tree(root)
        return self._traverse_recursive(root)

    def traverse_iter(self, root: Optional["TreeNode"]) -> Iterator[T]:
        """
        Effectue le parcours postfixe itératif de l'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Itérateur sur les valeurs dans l'ordre postfixe
        :rtype: Iterator[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return iter([])

        self.validate_tree(root)
        return self._traverse_iterative(root)

    def _traverse_recursive(self, node: "TreeNode") -> List[T]:
        """
        Parcourt récursivement l'arbre en ordre postfixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :return: Liste des valeurs dans l'ordre postfixe
        :rtype: List[T]
        """
        result = []

        # Parcourir tous les enfants d'abord
        for child in node.get_children():
            result.extend(self._traverse_recursive(child))

        # Visiter le nœud après ses enfants
        result.append(node.value)

        return result

    def _traverse_iterative(self, root: "TreeNode") -> Iterator[T]:
        """
        Parcourt itérativement l'arbre en ordre postfixe avec une pile.

        :param root: Nœud racine de l'arbre
        :type root: TreeNode
        :return: Itérateur sur les valeurs dans l'ordre postfixe
        :rtype: Iterator[T]
        """
        stack = []
        current = root
        last_visited = None

        while stack or current is not None:
            # Aller à gauche autant que possible
            while current is not None:
                stack.append(current)
                children = current.get_children()
                if children:
                    current = children[0]  # Enfant gauche
                else:
                    current = None

            if stack:
                current = stack[-1]
                children = current.get_children()

                # Si le nœud n'a pas d'enfant droit ou si l'enfant droit
                # a déjà été visité
                if len(children) < 2 or children[1] == last_visited:
                    yield current.value
                    last_visited = current
                    stack.pop()
                    current = None
                else:
                    # Aller au sous-arbre droit
                    current = children[1]

    def _traverse_depth_limited_recursive(
        self, node: "TreeNode", max_depth: int, current_depth: int
    ) -> List[T]:
        """
        Parcourt récursivement l'arbre avec limitation de profondeur en ordre postfixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :param max_depth: Profondeur maximale
        :type max_depth: int
        :param current_depth: Profondeur actuelle
        :type current_depth: int
        :return: Liste des valeurs dans l'ordre postfixe limité
        :rtype: List[T]
        """
        if current_depth >= max_depth:
            return []

        result = []

        # Parcourir tous les enfants d'abord
        for child in node.get_children():
            result.extend(
                self._traverse_depth_limited_recursive(
                    child, max_depth, current_depth + 1
                )
            )

        # Visiter le nœud après ses enfants
        result.append(node.value)

        return result

    def _traverse_right_to_left_recursive(self, node: "TreeNode") -> List[T]:
        """
        Parcourt récursivement l'arbre de droite à gauche en ordre postfixe.

        :param node: Nœud actuel
        :type node: TreeNode
        :return: Liste des valeurs dans l'ordre postfixe droite-gauche
        :rtype: List[T]
        """
        result = []

        # Parcourir les enfants en ordre inverse (droite à gauche)
        children = node.get_children()
        children.reverse()
        for child in children:
            result.extend(self._traverse_right_to_left_recursive(child))

        # Visiter le nœud après ses enfants
        result.append(node.value)

        return result
