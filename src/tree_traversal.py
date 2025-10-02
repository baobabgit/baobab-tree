"""
Classe abstraite TreeTraversal pour les algorithmes de parcours d'arbres.

Ce module implémente la classe TreeTraversal, classe abstraite de base pour tous
les algorithmes de parcours d'arbres dans la librairie. Cette classe fournit
l'interface commune et les fonctionnalités de base pour tous les types de parcours.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, Iterator, List, Optional, TYPE_CHECKING

from .exceptions import NodeValidationError
from .interfaces import T

if TYPE_CHECKING:
    from .tree_node import TreeNode


class TreeTraversal(ABC, Generic[T]):
    """
    Classe abstraite pour tous les parcours d'arbres.

    Cette classe définit l'interface commune pour tous les algorithmes de
    parcours d'arbres dans la librairie. Elle fournit les méthodes abstraites
    que chaque type de parcours doit implémenter, ainsi que des méthodes
    utilitaires communes.

    :param traversal_name: Nom du type de parcours (optionnel)
    :type traversal_name: Optional[str], optional
    """

    def __init__(self, traversal_name: Optional[str] = None):
        """
        Initialise un nouveau parcours d'arbre.

        :param traversal_name: Nom du type de parcours (optionnel)
        :type traversal_name: Optional[str], optional
        """
        self._traversal_name = traversal_name or self.__class__.__name__

    @abstractmethod
    def traverse(self, root: Optional["TreeNode"]) -> List[T]:
        """
        Effectue le parcours complet de l'arbre à partir de la racine.

        Cette méthode abstraite doit être implémentée par chaque classe
        de parcours pour définir l'algorithme spécifique de parcours.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Liste des valeurs dans l'ordre de parcours
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """

    @abstractmethod
    def traverse_iter(self, root: Optional["TreeNode"]) -> Iterator[T]:
        """
        Effectue le parcours itératif de l'arbre à partir de la racine.

        Cette méthode abstraite doit être implémentée par chaque classe
        de parcours pour fournir un itérateur sur les valeurs.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Itérateur sur les valeurs dans l'ordre de parcours
        :rtype: Iterator[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """

    def get_traversal_name(self) -> str:
        """
        Retourne le nom du type de parcours.

        :return: Nom du parcours
        :rtype: str
        """
        return self._traversal_name

    def is_empty(self, root: Optional["TreeNode"]) -> bool:
        """
        Vérifie si l'arbre est vide.

        :param root: Nœud racine de l'arbre à vérifier
        :type root: Optional[TreeNode]
        :return: True si l'arbre est vide, False sinon
        :rtype: bool
        """
        return root is None

    def validate_tree(self, root: Optional["TreeNode"]) -> bool:
        """
        Valide la structure de l'arbre.

        Cette méthode vérifie que l'arbre est valide en termes de structure
        et de cohérence des relations parent-enfant.

        :param root: Nœud racine de l'arbre à valider
        :type root: Optional[TreeNode]
        :return: True si l'arbre est valide, False sinon
        :rtype: bool
        :raises NodeValidationError: Si la validation échoue
        """
        if root is None:
            return True

        try:
            return self._validate_node_recursive(root, set())
        except NodeValidationError:
            raise
        except Exception as e:
            raise NodeValidationError(
                f"Unexpected error during tree validation: {str(e)}",
                "tree_validation_error",
                root,
            ) from e

    def traverse_with_callback(
        self, root: Optional["TreeNode"], callback: Callable[[T], None]
    ) -> None:
        """
        Effectue le parcours avec une fonction de callback pour chaque nœud.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :param callback: Fonction à appeler pour chaque valeur
        :type callback: Callable[[T], None]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        :raises ValueError: Si la fonction callback est None
        """
        if callback is None:
            raise ValueError("Callback function cannot be None")

        if root is None:
            return

        self.validate_tree(root)

        for value in self.traverse_iter(root):
            callback(value)

    def traverse_with_condition(
        self, root: Optional["TreeNode"], condition: Callable[[T], bool]
    ) -> List[T]:
        """
        Effectue le parcours en filtrant les nœuds selon une condition.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :param condition: Fonction de condition pour filtrer les valeurs
        :type condition: Callable[[T], bool]
        :return: Liste des valeurs filtrées dans l'ordre de parcours
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        :raises ValueError: Si la fonction condition est None
        """
        if condition is None:
            raise ValueError("Condition function cannot be None")

        if root is None:
            return []

        self.validate_tree(root)

        result = []
        for value in self.traverse_iter(root):
            if condition(value):
                result.append(value)

        return result

    def traverse_depth_limited(
        self, root: Optional["TreeNode"], max_depth: int
    ) -> List[T]:
        """
        Effectue le parcours limité par la profondeur maximale.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :param max_depth: Profondeur maximale à parcourir
        :type max_depth: int
        :return: Liste des valeurs dans l'ordre de parcours limité
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        :raises ValueError: Si max_depth est négatif
        """
        if max_depth < 0:
            raise ValueError("Max depth must be non-negative")

        if root is None:
            return []

        self.validate_tree(root)

        return self._traverse_depth_limited_recursive(root, max_depth, 0)

    def traverse_count_limited(
        self, root: Optional["TreeNode"], max_count: int
    ) -> List[T]:
        """
        Effectue le parcours limité par le nombre maximum de nœuds.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :param max_count: Nombre maximum de nœuds à parcourir
        :type max_count: int
        :return: Liste des valeurs dans l'ordre de parcours limité
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        :raises ValueError: Si max_count est négatif
        """
        if max_count < 0:
            raise ValueError("Max count must be non-negative")

        if root is None:
            return []

        self.validate_tree(root)

        result = []
        count = 0
        for value in self.traverse_iter(root):
            if count >= max_count:
                break
            result.append(value)
            count += 1

        return result

    def traverse_reverse(self, root: Optional["TreeNode"]) -> List[T]:
        """
        Effectue le parcours inversé de l'arbre.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Liste des valeurs dans l'ordre de parcours inversé
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return []

        self.validate_tree(root)

        result = list(self.traverse_iter(root))
        result.reverse()
        return result

    def traverse_right_to_left(self, root: Optional["TreeNode"]) -> List[T]:
        """
        Effectue le parcours de droite à gauche de l'arbre.

        Cette méthode est spécifique aux arbres binaires et inverse l'ordre
        des enfants gauche et droit.

        :param root: Nœud racine de l'arbre à parcourir
        :type root: Optional[TreeNode]
        :return: Liste des valeurs dans l'ordre de parcours droite-gauche
        :rtype: List[T]
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return []

        self.validate_tree(root)

        return self._traverse_right_to_left_recursive(root)

    def get_tree_statistics(self, root: Optional["TreeNode"]) -> dict:
        """
        Calcule les statistiques de l'arbre.

        :param root: Nœud racine de l'arbre à analyser
        :type root: Optional[TreeNode]
        :return: Dictionnaire contenant les statistiques de l'arbre
        :rtype: dict
        :raises NodeValidationError: Si la validation de l'arbre échoue
        """
        if root is None:
            return {
                "node_count": 0,
                "height": -1,
                "leaf_count": 0,
                "internal_node_count": 0,
                "is_valid": True,
            }

        self.validate_tree(root)

        stats = {
            "node_count": 0,
            "height": root.get_height(),
            "leaf_count": 0,
            "internal_node_count": 0,
            "is_valid": True,
        }

        for value in self.traverse_iter(root):
            stats["node_count"] += 1

        # Compter les feuilles et nœuds internes
        self._count_nodes_recursive(root, stats)

        return stats

    def _validate_node_recursive(self, node: "TreeNode", visited: set) -> bool:
        """
        Valide récursivement un nœud et ses descendants.

        :param node: Nœud à valider
        :type node: TreeNode
        :param visited: Ensemble des nœuds déjà visités (pour détecter les cycles)
        :type visited: set
        :return: True si le nœud est valide, False sinon
        :rtype: bool
        :raises NodeValidationError: Si la validation échoue
        """
        if node in visited:
            raise NodeValidationError(
                "Circular reference detected in tree structure",
                "circular_reference",
                node,
            )

        visited.add(node)

        try:
            # Valider le nœud lui-même
            if not node.validate():
                return False

            # Valider les enfants
            for child in node.get_children():
                if not self._validate_node_recursive(child, visited):
                    return False

        finally:
            visited.remove(node)

        return True

    def _traverse_depth_limited_recursive(
        self, node: "TreeNode", max_depth: int, current_depth: int
    ) -> List[T]:
        """
        Parcourt récursivement l'arbre avec limitation de profondeur.

        Cette méthode doit être surchargée par les classes spécialisées
        pour implémenter le parcours spécifique.

        :param node: Nœud actuel
        :type node: TreeNode
        :param max_depth: Profondeur maximale
        :type max_depth: int
        :param current_depth: Profondeur actuelle
        :type current_depth: int
        :return: Liste des valeurs dans l'ordre de parcours limité
        :rtype: List[T]
        """
        if current_depth >= max_depth:
            return []

        # Implémentation par défaut : parcours préfixe
        result = [node.value]
        for child in node.get_children():
            result.extend(
                self._traverse_depth_limited_recursive(
                    child, max_depth, current_depth + 1
                )
            )

        return result

    def _traverse_right_to_left_recursive(self, node: "TreeNode") -> List[T]:
        """
        Parcourt récursivement l'arbre de droite à gauche.

        Cette méthode doit être surchargée par les classes spécialisées
        pour implémenter le parcours spécifique.

        :param node: Nœud actuel
        :type node: TreeNode
        :return: Liste des valeurs dans l'ordre de parcours droite-gauche
        :rtype: List[T]
        """
        # Implémentation par défaut : parcours préfixe inversé
        result = [node.value]
        children = node.get_children()
        children.reverse()  # Inverser l'ordre des enfants
        for child in children:
            result.extend(self._traverse_right_to_left_recursive(child))

        return result

    def _count_nodes_recursive(self, node: "TreeNode", stats: dict) -> None:
        """
        Compte récursivement les nœuds de l'arbre.

        :param node: Nœud actuel
        :type node: TreeNode
        :param stats: Dictionnaire des statistiques à mettre à jour
        :type stats: dict
        """
        if node.is_leaf():
            stats["leaf_count"] += 1
        else:
            stats["internal_node_count"] += 1

        for child in node.get_children():
            self._count_nodes_recursive(child, stats)

    def __str__(self) -> str:
        """
        Retourne la représentation string du parcours.

        :return: Représentation string du parcours
        :rtype: str
        """
        return f"{self.__class__.__name__}(name={self._traversal_name})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du parcours.

        :return: Représentation détaillée du parcours
        :rtype: str
        """
        return f"{self.__class__.__name__}(traversal_name={self._traversal_name!r})"
