"""
Opérations utilitaires pour les arbres.

Ce module implémente les opérations utilitaires pour les arbres, incluant
la validation, le calcul de propriétés, et les opérations sur les nœuds.
"""

from __future__ import annotations

from typing import Generic, List, Optional, TYPE_CHECKING

from ..binary.binary_tree_node import BinaryTreeNode
from .interfaces import T
from .tree_node import TreeNode

if TYPE_CHECKING:
    from ..binary.binary_tree_node import BinaryTreeNode


class UtilityOperations(Generic[T]):
    """
    Opérations utilitaires pour les arbres.

    Cette classe fournit des opérations utilitaires pour analyser et
    manipuler les propriétés des arbres.
    """

    def get_height(self, root: Optional[TreeNode[T]]) -> int:
        """
        Calcule la hauteur de l'arbre.

        La hauteur d'un arbre est la longueur du chemin le plus long
        de la racine vers une feuille.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Hauteur de l'arbre (-1 si vide)
        :rtype: int
        """
        if root is None:
            return -1
        return root.get_height()

    def get_depth(self, node: TreeNode[T]) -> int:
        """
        Calcule la profondeur d'un nœud.

        La profondeur d'un nœud est la longueur du chemin de la racine
        vers ce nœud.

        :param node: Nœud dont calculer la profondeur
        :type node: TreeNode[T]
        :return: Profondeur du nœud
        :rtype: int
        """
        return node.get_depth()

    def get_size(self, root: Optional[TreeNode[T]]) -> int:
        """
        Calcule le nombre de nœuds dans l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Nombre de nœuds dans l'arbre
        :rtype: int
        """
        if root is None:
            return 0

        size = 1  # Compter le nœud racine
        for child in root.get_children():
            size += self.get_size(child)

        return size

    def get_balance_factor(self, node: BinaryTreeNode[T]) -> int:
        """
        Calcule le facteur d'équilibre d'un nœud binaire.

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

    def is_balanced(self, root: Optional[TreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre est équilibré.

        Un arbre est équilibré si la différence de hauteur entre les
        sous-arbres de chaque nœud est au plus 1.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: True si l'arbre est équilibré, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        # Pour les arbres binaires, utiliser la méthode spécialisée
        if isinstance(root, BinaryTreeNode):
            return self._is_binary_tree_balanced(root)

        return self._is_balanced_recursive(root) != -1

    def _is_binary_tree_balanced(self, node: BinaryTreeNode[T]) -> bool:
        """
        Vérifie si un arbre binaire est équilibré.

        :param node: Nœud racine de l'arbre binaire
        :type node: BinaryTreeNode[T]
        :return: True si l'arbre est équilibré, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        left_height = node.left.get_height() if node.left is not None else -1
        right_height = node.right.get_height() if node.right is not None else -1

        if abs(left_height - right_height) > 1:
            return False

        left_balanced = (
            self._is_binary_tree_balanced(node.left) if node.left is not None else True
        )
        right_balanced = (
            self._is_binary_tree_balanced(node.right)
            if node.right is not None
            else True
        )

        return left_balanced and right_balanced

    def _is_balanced_recursive(self, node: TreeNode[T]) -> int:
        """
        Vérifie récursivement l'équilibre du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: TreeNode[T]
        :return: Hauteur du sous-arbre si équilibré, -1 sinon
        :rtype: int
        """
        if node.is_leaf():
            return 0

        children = node.get_children()
        if len(children) == 0:
            return 0

        heights = []
        for child in children:
            height = self._is_balanced_recursive(child)
            if height == -1:
                return -1
            heights.append(height)

        if len(heights) == 1:
            return 1 + heights[0]

        # Pour les arbres avec plus d'un enfant, vérifier l'équilibre
        min_height = min(heights)
        max_height = max(heights)

        if max_height - min_height > 1:
            return -1

        return 1 + max_height

    def is_complete(self, root: Optional[TreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre est complet.

        Un arbre est complet si tous les niveaux sont remplis,
        sauf peut-être le dernier niveau qui est rempli de gauche à droite.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: True si l'arbre est complet, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        return self._is_complete_recursive(root, 0, self.get_size(root))

    def _is_complete_recursive(
        self, node: TreeNode[T], index: int, total_nodes: int
    ) -> bool:
        """
        Vérifie récursivement si l'arbre est complet.

        :param node: Nœud actuel
        :type node: TreeNode[T]
        :param index: Index du nœud dans l'arbre
        :type index: int
        :param total_nodes: Nombre total de nœuds
        :type total_nodes: int
        :return: True si le sous-arbre est complet, False sinon
        :rtype: bool
        """
        if node is None:
            return True

        if index >= total_nodes:
            return False

        children = node.get_children()
        if len(children) == 0:
            return True

        # Pour un arbre binaire complet
        if len(children) <= 2:
            left_complete = True
            right_complete = True

            if len(children) >= 1:
                left_complete = self._is_complete_recursive(
                    children[0], 2 * index + 1, total_nodes
                )

            if len(children) >= 2:
                right_complete = self._is_complete_recursive(
                    children[1], 2 * index + 2, total_nodes
                )

            return left_complete and right_complete

        # Pour les arbres non-binaires, vérifier tous les enfants
        for i, child in enumerate(children):
            child_index = 2 * index + i + 1
            if not self._is_complete_recursive(child, child_index, total_nodes):
                return False

        return True

    def is_full(self, root: Optional[TreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre est plein.

        Un arbre est plein si chaque nœud a soit 0 soit le nombre maximum
        d'enfants possibles.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: True si l'arbre est plein, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        children = root.get_children()

        # Si c'est une feuille, c'est plein
        if len(children) == 0:
            return True

        # Vérifier récursivement tous les enfants
        for child in children:
            if not self.is_full(child):
                return False

        return True

    def is_perfect(self, root: Optional[TreeNode[T]]) -> bool:
        """
        Vérifie si l'arbre est parfait.

        Un arbre est parfait si tous les niveaux sont complètement remplis.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: True si l'arbre est parfait, False sinon
        :rtype: bool
        """
        if root is None:
            return True

        height = self.get_height(root)
        expected_nodes = 2 ** (height + 1) - 1
        actual_nodes = self.get_size(root)

        return actual_nodes == expected_nodes

    def get_leaf_nodes(self, root: Optional[TreeNode[T]]) -> List[TreeNode[T]]:
        """
        Récupère tous les nœuds feuilles de l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Liste des nœuds feuilles
        :rtype: List[TreeNode[T]]
        """
        if root is None:
            return []

        if root.is_leaf():
            return [root]

        leaves = []
        for child in root.get_children():
            leaves.extend(self.get_leaf_nodes(child))

        return leaves

    def get_internal_nodes(self, root: Optional[TreeNode[T]]) -> List[TreeNode[T]]:
        """
        Récupère tous les nœuds internes de l'arbre.

        Un nœud interne est un nœud qui n'est pas une feuille.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Liste des nœuds internes
        :rtype: List[TreeNode[T]]
        """
        if root is None or root.is_leaf():
            return []

        internal_nodes = [root]
        for child in root.get_children():
            internal_nodes.extend(self.get_internal_nodes(child))

        return internal_nodes

    def get_nodes_at_level(
        self, root: Optional[TreeNode[T]], level: int
    ) -> List[TreeNode[T]]:
        """
        Récupère tous les nœuds à un niveau donné.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :param level: Niveau à récupérer (0 pour la racine)
        :type level: int
        :return: Liste des nœuds au niveau donné
        :rtype: List[TreeNode[T]]
        """
        if root is None or level < 0:
            return []

        if level == 0:
            return [root]

        nodes = []
        for child in root.get_children():
            nodes.extend(self.get_nodes_at_level(child, level - 1))

        return nodes

    def get_width(self, root: Optional[TreeNode[T]]) -> int:
        """
        Calcule la largeur maximale de l'arbre.

        La largeur est le nombre maximum de nœuds à n'importe quel niveau.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Largeur maximale de l'arbre
        :rtype: int
        """
        if root is None:
            return 0

        height = self.get_height(root)
        max_width = 0

        for level in range(height + 1):
            width = len(self.get_nodes_at_level(root, level))
            max_width = max(max_width, width)

        return max_width

    def get_diameter(self, root: Optional[TreeNode[T]]) -> int:
        """
        Calcule le diamètre de l'arbre.

        Le diamètre est la longueur du chemin le plus long entre deux
        nœuds quelconques de l'arbre.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :return: Diamètre de l'arbre
        :rtype: int
        """
        if root is None:
            return 0

        _, diameter = self._get_diameter_recursive(root)
        return diameter

    def _get_diameter_recursive(self, node: TreeNode[T]) -> tuple[int, int]:
        """
        Calcule récursivement le diamètre du sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: TreeNode[T]
        :return: Tuple (hauteur, diamètre)
        :rtype: tuple[int, int]
        """
        if node.is_leaf():
            return 0, 0

        children = node.get_children()
        if len(children) == 0:
            return 0, 0

        max_height = 0
        max_diameter = 0
        heights = []

        for child in children:
            child_height, child_diameter = self._get_diameter_recursive(child)
            heights.append(child_height)
            max_diameter = max(max_diameter, child_diameter)

        if len(heights) >= 2:
            heights.sort(reverse=True)
            max_diameter = max(max_diameter, heights[0] + heights[1] + 2)
        elif len(heights) == 1:
            max_diameter = max(max_diameter, heights[0] + 1)

        max_height = max(heights) + 1 if heights else 0

        return max_height, max_diameter

    def count_nodes_with_value(self, root: Optional[TreeNode[T]], value: T) -> int:
        """
        Compte le nombre de nœuds contenant une valeur donnée.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :param value: Valeur à compter
        :type value: T
        :return: Nombre de nœuds contenant la valeur
        :rtype: int
        """
        if root is None:
            return 0

        count = 1 if root.value == value else 0

        for child in root.get_children():
            count += self.count_nodes_with_value(child, value)

        return count

    def get_path_to_node(
        self, root: Optional[TreeNode[T]], target: TreeNode[T]
    ) -> List[TreeNode[T]]:
        """
        Récupère le chemin de la racine vers un nœud cible.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :param target: Nœud cible
        :type target: TreeNode[T]
        :return: Liste des nœuds du chemin (vide si nœud non trouvé)
        :rtype: List[TreeNode[T]]
        """
        if root is None:
            return []

        if root is target:
            return [root]

        for child in root.get_children():
            path = self.get_path_to_node(child, target)
            if path:
                return [root] + path

        return []

    def get_common_ancestor(
        self, root: Optional[TreeNode[T]], node1: TreeNode[T], node2: TreeNode[T]
    ) -> Optional[TreeNode[T]]:
        """
        Trouve l'ancêtre commun le plus proche de deux nœuds.

        :param root: Racine de l'arbre
        :type root: Optional[TreeNode[T]]
        :param node1: Premier nœud
        :type node1: TreeNode[T]
        :param node2: Deuxième nœud
        :type node2: TreeNode[T]
        :return: Ancêtre commun le plus proche ou None
        :rtype: Optional[TreeNode[T]]
        """
        if root is None:
            return None

        path1 = self.get_path_to_node(root, node1)
        path2 = self.get_path_to_node(root, node2)

        if not path1 or not path2:
            return None

        # Trouver le dernier nœud commun dans les chemins
        common_ancestor = None
        min_length = min(len(path1), len(path2))

        for i in range(min_length):
            if path1[i] is path2[i]:
                common_ancestor = path1[i]
            else:
                break

        return common_ancestor

    def is_subtree(
        self, root: Optional[TreeNode[T]], subtree_root: Optional[TreeNode[T]]
    ) -> bool:
        """
        Vérifie si un arbre est un sous-arbre d'un autre.

        :param root: Racine de l'arbre principal
        :type root: Optional[TreeNode[T]]
        :param subtree_root: Racine du sous-arbre à vérifier
        :type subtree_root: Optional[TreeNode[T]]
        :return: True si le sous-arbre est présent, False sinon
        :rtype: bool
        """
        if subtree_root is None:
            return True

        if root is None:
            return False

        if self._are_trees_identical(root, subtree_root):
            return True

        for child in root.get_children():
            if self.is_subtree(child, subtree_root):
                return True

        return False

    def _are_trees_identical(
        self, tree1: Optional[TreeNode[T]], tree2: Optional[TreeNode[T]]
    ) -> bool:
        """
        Vérifie si deux arbres sont identiques.

        :param tree1: Premier arbre
        :type tree1: Optional[TreeNode[T]]
        :param tree2: Deuxième arbre
        :type tree2: Optional[TreeNode[T]]
        :return: True si les arbres sont identiques, False sinon
        :rtype: bool
        """
        if tree1 is None and tree2 is None:
            return True

        if tree1 is None or tree2 is None:
            return False

        if tree1.value != tree2.value:
            return False

        children1 = tree1.get_children()
        children2 = tree2.get_children()

        if len(children1) != len(children2):
            return False

        for child1, child2 in zip(children1, children2):
            if not self._are_trees_identical(child1, child2):
                return False

        return True
