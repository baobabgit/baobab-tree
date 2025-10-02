"""
Classe RedBlackTree pour les arbres rouge-noir auto-équilibrés.

Ce module implémente la classe RedBlackTree, arbre auto-équilibré alternatif à l'AVL
utilisant la recoloration et les rotations pour maintenir l'équilibre.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from ..binary.binary_search_tree import BinarySearchTree
from ..core.exceptions import (
    BSTError,
    ColorViolationError,
    PathViolationError,
    RedBlackBalancingError,
    RedBlackTreeError,
)
from ..core.interfaces import T
from .red_black_node import Color, RedBlackNode


class RedBlackTree(BinarySearchTree):
    """
    Arbre rouge-noir auto-équilibré.

    Cette classe hérite de BinarySearchTree et ajoute l'équilibrage rouge-noir.
    Elle maintient automatiquement les propriétés rouge-noir après chaque
    insertion et suppression.

    :param comparator: Fonction de comparaison personnalisée (optionnel)
    :type comparator: Optional[Callable[[T, T], int]], optional
    """

    def __init__(self, comparator: Optional[Callable[[T, T], int]] = None) -> None:
        """
        Initialise un nouvel arbre rouge-noir.

        :param comparator: Fonction de comparaison personnalisée (optionnel)
        :type comparator: Optional[Callable[[T, T], int]], optional
        """
        super().__init__(comparator)
        
        # Nœud sentinelle (toujours noir)
        self._nil: RedBlackNode[T] = RedBlackNode(None, Color.BLACK)
        
        # Compteurs pour debugging
        self._recolor_count: int = 0
        self._rotation_count: int = 0

    def _create_node(self, value: T) -> RedBlackNode[T]:
        """
        Crée un nouveau nœud rouge-noir.

        :param value: Valeur à stocker dans le nœud
        :type value: T
        :return: Nouveau nœud rouge-noir
        :rtype: RedBlackNode[T]
        """
        return RedBlackNode(value, Color.RED)

    def insert(self, value: T) -> bool:
        """
        Insère une valeur avec équilibrage automatique rouge-noir.

        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False si la valeur existe déjà
        :rtype: bool
        :raises RedBlackTreeError: Si une erreur survient lors de l'insertion
        """
        try:
            # Insertion rouge-noir personnalisée
            if self._root is None:
                self._root = self._create_node(value)
                self._root.set_black()  # La racine est toujours noire
                self._size = 1
                return True

            return self._insert_recursive(self._root, value)
        except Exception as e:
            if isinstance(e, RedBlackTreeError):
                raise
            raise RedBlackTreeError(f"Error during insertion: {str(e)}", "insert")

    def _insert_recursive(self, node: RedBlackNode[T], value: T) -> bool:
        """
        Insère récursivement une valeur dans le sous-arbre rouge-noir.

        :param node: Nœud racine du sous-arbre
        :type node: RedBlackNode[T]
        :param value: Valeur à insérer
        :type value: T
        :return: True si l'insertion a réussi, False si la valeur existe déjà
        :rtype: bool
        """
        comparison = self._comparator(value, node.value)

        if comparison < 0:
            if node.left is None:
                new_node = self._create_node(value)
                node.set_left(new_node)
                self._size += 1
                # Corriger les violations après insertion
                self._fix_insertion_violations(new_node)
                return True
            else:
                return self._insert_recursive(node.left, value)
        elif comparison > 0:
            if node.right is None:
                new_node = self._create_node(value)
                node.set_right(new_node)
                self._size += 1
                # Corriger les violations après insertion
                self._fix_insertion_violations(new_node)
                return True
            else:
                return self._insert_recursive(node.right, value)
        else:
            # Valeur déjà présente
            return False

    def delete(self, value: T) -> bool:
        """
        Supprime une valeur avec équilibrage automatique rouge-noir.

        :param value: Valeur à supprimer
        :type value: T
        :return: True si la suppression a réussi, False si la valeur n'existe pas
        :rtype: bool
        :raises RedBlackTreeError: Si une erreur survient lors de la suppression
        """
        try:
            # Trouver le nœud à supprimer
            node_to_delete = self._find_node(value)
            if node_to_delete is None:
                return False
            
            # Gérer les cas de suppression
            if node_to_delete.left is None:
                self._delete_node_with_at_most_one_child(node_to_delete)
            elif node_to_delete.right is None:
                self._delete_node_with_at_most_one_child(node_to_delete)
            else:
                # Nœud avec deux enfants
                successor = self._find_successor(node_to_delete)
                node_to_delete.value = successor.value
                self._delete_node_with_at_most_one_child(successor)
            
            return True
        except Exception as e:
            if isinstance(e, RedBlackTreeError):
                raise
            raise RedBlackTreeError(f"Error during deletion: {str(e)}", "delete")

    def _find_node(self, value: T) -> Optional[RedBlackNode[T]]:
        """
        Trouve un nœud avec la valeur donnée.

        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud trouvé ou None
        :rtype: Optional[RedBlackNode[T]]
        """
        return self._search_recursive(self._root, value)

    def _search_recursive(
        self, node: Optional[RedBlackNode[T]], value: T
    ) -> Optional[RedBlackNode[T]]:
        """
        Recherche récursivement une valeur dans le sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: Optional[RedBlackNode[T]]
        :param value: Valeur à rechercher
        :type value: T
        :return: Nœud contenant la valeur ou None si non trouvée
        :rtype: Optional[RedBlackNode[T]]
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

    def _find_successor(self, node: RedBlackNode[T]) -> RedBlackNode[T]:
        """
        Trouve le successeur d'un nœud.

        :param node: Nœud dont on cherche le successeur
        :type node: RedBlackNode[T]
        :return: Successeur du nœud
        :rtype: RedBlackNode[T]
        """
        if node.right is not None:
            return self._find_min_node(node.right)
        
        # Remonter jusqu'à trouver un ancêtre dont le fils gauche est aussi un ancêtre
        current = node
        parent = node.parent
        while parent is not None and current == parent.right:
            current = parent
            parent = parent.parent
        
        return parent

    def _find_min_node(self, node: RedBlackNode[T]) -> RedBlackNode[T]:
        """
        Trouve le nœud avec la valeur minimale dans le sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: RedBlackNode[T]
        :return: Nœud avec la valeur minimale
        :rtype: RedBlackNode[T]
        """
        while node.left is not None:
            node = node.left
        return node

    def _delete_node_with_at_most_one_child(self, node: RedBlackNode[T]) -> None:
        """
        Supprime un nœud qui a au plus un enfant.

        :param node: Nœud à supprimer
        :type node: RedBlackNode[T]
        """
        child = node.left if node.left is not None else node.right
        
        if child is not None:
            # Le nœud a un enfant
            child.parent = node.parent
            
            if node.parent is None:
                # Le nœud est la racine
                self._root = child
            elif node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
            
            # Si le nœud supprimé était noir, corriger les violations
            if node.is_black():
                self._fix_deletion_violations(child)
        else:
            # Le nœud est une feuille
            if node.parent is None:
                # Le nœud est la racine
                self._root = None
            else:
                # Si le nœud supprimé était noir, corriger les violations
                if node.is_black():
                    self._fix_deletion_violations(node)
                
                # Supprimer la référence du parent
                if node == node.parent.left:
                    node.parent.left = None
                else:
                    node.parent.right = None
        
        self._size -= 1

    def _fix_insertion_violations(self, node: RedBlackNode[T]) -> None:
        """
        Corrige les violations de propriétés après insertion.

        :param node: Nœud inséré
        :type node: RedBlackNode[T]
        :raises RedBlackBalancingError: Si la correction échoue
        """
        try:
            while node.parent is not None and node.parent.is_red():
                if node.parent == node.parent.parent.left:
                    # Cas 1: Parent gauche
                    uncle = node.parent.parent.right
                    if uncle is not None and uncle.is_red():
                        # Cas 1a: Oncle rouge
                        node.parent.set_black()
                        uncle.set_black()
                        node.parent.parent.set_red()
                        node = node.parent.parent
                        self._recolor_count += 3
                    else:
                        # Cas 1b: Oncle noir
                        if node == node.parent.right:
                            node = node.parent
                            self._rotate_left(node)
                        node.parent.set_black()
                        node.parent.parent.set_red()
                        self._rotate_right(node.parent.parent)
                        self._recolor_count += 2
                        self._rotation_count += 2
                else:
                    # Cas 2: Parent droit (symétrique)
                    uncle = node.parent.parent.left
                    if uncle is not None and uncle.is_red():
                        # Cas 2a: Oncle rouge
                        node.parent.set_black()
                        uncle.set_black()
                        node.parent.parent.set_red()
                        node = node.parent.parent
                        self._recolor_count += 3
                    else:
                        # Cas 2b: Oncle noir
                        if node == node.parent.left:
                            node = node.parent
                            self._rotate_right(node)
                        node.parent.set_black()
                        node.parent.parent.set_red()
                        self._rotate_left(node.parent.parent)
                        self._recolor_count += 2
                        self._rotation_count += 2
            
            # S'assurer que la racine est toujours noire
            if self._root is not None:
                self._root.set_black()
        except Exception as e:
            raise RedBlackBalancingError(
                f"Failed to fix insertion violations: {str(e)}",
                "fix_insertion_violations",
                node,
            ) from e

    def _fix_deletion_violations(self, node: RedBlackNode[T]) -> None:
        """
        Corrige les violations de propriétés après suppression.

        :param node: Nœud concerné par la suppression
        :type node: RedBlackNode[T]
        :raises RedBlackBalancingError: Si la correction échoue
        """
        try:
            while node != self._root and node.is_black():
                if node == node.parent.left:
                    # Cas 1: Nœud gauche
                    sibling = node.parent.right
                    if sibling is not None and sibling.is_red():
                        # Cas 1a: Frère rouge
                        sibling.set_black()
                        node.parent.set_red()
                        self._rotate_left(node.parent)
                        sibling = node.parent.right
                        self._recolor_count += 2
                        self._rotation_count += 1
                    
                    if (sibling is None or 
                        (sibling.left is None or sibling.left.is_black()) and
                        (sibling.right is None or sibling.right.is_black())):
                        # Cas 1b: Frère noir avec enfants noirs
                        if sibling is not None:
                            sibling.set_red()
                            self._recolor_count += 1
                        node = node.parent
                    else:
                        # Cas 1c: Frère noir avec au moins un enfant rouge
                        if sibling is None or sibling.right is None or sibling.right.is_black():
                            if sibling is not None and sibling.left is not None:
                                sibling.left.set_black()
                                sibling.set_red()
                                self._rotate_right(sibling)
                                sibling = node.parent.right
                                self._recolor_count += 2
                                self._rotation_count += 1
                        
                        if sibling is not None:
                            sibling.color = node.parent.color
                            node.parent.set_black()
                            if sibling.right is not None:
                                sibling.right.set_black()
                            self._rotate_left(node.parent)
                            self._recolor_count += 3
                            self._rotation_count += 1
                        node = self._root
                else:
                    # Cas 2: Nœud droit (symétrique)
                    sibling = node.parent.left
                    if sibling is not None and sibling.is_red():
                        # Cas 2a: Frère rouge
                        sibling.set_black()
                        node.parent.set_red()
                        self._rotate_right(node.parent)
                        sibling = node.parent.left
                        self._recolor_count += 2
                        self._rotation_count += 1
                    
                    if (sibling is None or 
                        (sibling.left is None or sibling.left.is_black()) and
                        (sibling.right is None or sibling.right.is_black())):
                        # Cas 2b: Frère noir avec enfants noirs
                        if sibling is not None:
                            sibling.set_red()
                            self._recolor_count += 1
                        node = node.parent
                    else:
                        # Cas 2c: Frère noir avec au moins un enfant rouge
                        if sibling is None or sibling.left is None or sibling.left.is_black():
                            if sibling is not None and sibling.right is not None:
                                sibling.right.set_black()
                                sibling.set_red()
                                self._rotate_left(sibling)
                                sibling = node.parent.left
                                self._recolor_count += 2
                                self._rotation_count += 1
                        
                        if sibling is not None:
                            sibling.color = node.parent.color
                            node.parent.set_black()
                            if sibling.left is not None:
                                sibling.left.set_black()
                            self._rotate_right(node.parent)
                            self._recolor_count += 3
                            self._rotation_count += 1
                        node = self._root
            
            node.set_black()
            self._recolor_count += 1
        except Exception as e:
            raise RedBlackBalancingError(
                f"Failed to fix deletion violations: {str(e)}",
                "fix_deletion_violations",
                node,
            ) from e

    def _rotate_left(self, node: RedBlackNode[T]) -> None:
        """
        Effectue une rotation gauche sur le nœud.

        :param node: Nœud sur lequel effectuer la rotation
        :type node: RedBlackNode[T]
        :raises RedBlackBalancingError: Si la rotation échoue
        """
        try:
            right_child = node.right
            if right_child is None:
                raise RedBlackBalancingError(
                    "Cannot perform left rotation: no right child",
                    "rotate_left",
                    node,
                )
            
            # Effectuer la rotation en utilisant directement les attributs privés
            node._right = right_child.left
            if right_child.left is not None:
                right_child.left._parent = node
            
            right_child._parent = node.parent
            
            if node.parent is None:
                self._root = right_child
            elif node == node.parent.left:
                node.parent._left = right_child
            else:
                node.parent._right = right_child
            
            right_child._left = node
            node._parent = right_child
        except Exception as e:
            raise RedBlackBalancingError(
                f"Failed to perform left rotation: {str(e)}",
                "rotate_left",
                node,
            ) from e

    def _rotate_right(self, node: RedBlackNode[T]) -> None:
        """
        Effectue une rotation droite sur le nœud.

        :param node: Nœud sur lequel effectuer la rotation
        :type node: RedBlackNode[T]
        :raises RedBlackBalancingError: Si la rotation échoue
        """
        try:
            left_child = node.left
            if left_child is None:
                raise RedBlackBalancingError(
                    "Cannot perform right rotation: no left child",
                    "rotate_right",
                    node,
                )
            
            # Effectuer la rotation en utilisant directement les attributs privés
            node._left = left_child.right
            if left_child.right is not None:
                left_child.right._parent = node
            
            left_child._parent = node.parent
            
            if node.parent is None:
                self._root = left_child
            elif node == node.parent.right:
                node.parent._right = left_child
            else:
                node.parent._left = left_child
            
            left_child._right = node
            node._parent = left_child
        except Exception as e:
            raise RedBlackBalancingError(
                f"Failed to perform right rotation: {str(e)}",
                "rotate_right",
                node,
            ) from e

    def is_red_black_valid(self) -> bool:
        """
        Valide que l'arbre respecte toutes les propriétés rouge-noir.

        :return: True si l'arbre respecte toutes les propriétés rouge-noir, False sinon
        :rtype: bool
        """
        try:
            if self._root is None:
                return True
            
            # Vérifier la propriété de couleur
            if not self.validate_colors():
                return False
            
            # Vérifier la propriété de racine
            if not self._root.is_black():
                return False
            
            # Vérifier la propriété de chemin
            if not self.validate_paths():
                return False
            
            return True
        except Exception:
            return False

    def validate_colors(self) -> bool:
        """
        Valide que les couleurs sont correctement assignées.

        :return: True si les couleurs sont valides, False sinon
        :rtype: bool
        """
        try:
            if self._root is None:
                return True
            
            return self._root.validate_colors()
        except Exception:
            return False

    def validate_paths(self) -> bool:
        """
        Valide que tous les chemins ont le même nombre de nœuds noirs.

        :return: True si tous les chemins ont le même nombre de nœuds noirs, False sinon
        :rtype: bool
        """
        try:
            if self._root is None:
                return True
            
            return self._root.validate_paths()
        except Exception:
            return False

    def get_color_analysis(self) -> Dict[str, Any]:
        """
        Analyse la distribution des couleurs dans l'arbre.

        :return: Dictionnaire contenant l'analyse des couleurs
        :rtype: Dict[str, Any]
        """
        analysis = {
            "red_count": 0,
            "black_count": 0,
            "total_nodes": 0,
            "red_percentage": 0.0,
            "black_percentage": 0.0,
            "color_distribution_by_level": {},
        }
        
        if self._root is None:
            return analysis
        
        # Compter les nœuds par couleur
        self._analyze_colors_recursive(self._root, analysis, 0)
        
        # Calculer les pourcentages
        if analysis["total_nodes"] > 0:
            analysis["red_percentage"] = (analysis["red_count"] / analysis["total_nodes"]) * 100
            analysis["black_percentage"] = (analysis["black_count"] / analysis["total_nodes"]) * 100
        
        return analysis

    def _analyze_colors_recursive(
        self, node: RedBlackNode[T], analysis: Dict[str, Any], level: int
    ) -> None:
        """
        Analyse récursivement les couleurs des nœuds.

        :param node: Nœud à analyser
        :type node: RedBlackNode[T]
        :param analysis: Dictionnaire d'analyse à mettre à jour
        :type analysis: Dict[str, Any]
        :param level: Niveau actuel dans l'arbre
        :type level: int
        """
        if node is None:
            return
        
        # Compter le nœud
        analysis["total_nodes"] += 1
        
        if node.is_red():
            analysis["red_count"] += 1
        else:
            analysis["black_count"] += 1
        
        # Analyser par niveau
        if level not in analysis["color_distribution_by_level"]:
            analysis["color_distribution_by_level"][level] = {"red": 0, "black": 0}
        
        if node.is_red():
            analysis["color_distribution_by_level"][level]["red"] += 1
        else:
            analysis["color_distribution_by_level"][level]["black"] += 1
        
        # Analyser récursivement les enfants
        self._analyze_colors_recursive(node.left, analysis, level + 1)
        self._analyze_colors_recursive(node.right, analysis, level + 1)

    def get_balancing_stats(self) -> Dict[str, int]:
        """
        Retourne les statistiques d'équilibrage de l'arbre.

        :return: Dictionnaire contenant les statistiques d'équilibrage
        :rtype: Dict[str, int]
        """
        return {
            "recolor_count": self._recolor_count,
            "rotation_count": self._rotation_count,
            "total_operations": self._recolor_count + self._rotation_count,
        }

    def get_performance_analysis(self) -> Dict[str, Any]:
        """
        Analyse la performance de l'arbre rouge-noir.

        :return: Dictionnaire contenant l'analyse de performance
        :rtype: Dict[str, Any]
        """
        analysis = {
            "size": self._size,
            "height": self.get_height(),
            "is_balanced": self.is_balanced(),
            "is_red_black_valid": self.is_red_black_valid(),
            "balancing_stats": self.get_balancing_stats(),
            "color_analysis": self.get_color_analysis(),
        }
        
        # Calculer les métriques de performance
        if self._size > 0:
            analysis["height_ratio"] = self.get_height() / self._size
            analysis["balancing_efficiency"] = (
                self._recolor_count + self._rotation_count
            ) / self._size if self._size > 0 else 0
        
        return analysis

    def find_red_nodes(self) -> List[RedBlackNode[T]]:
        """
        Retourne tous les nœuds rouges de l'arbre.

        :return: Liste des nœuds rouges
        :rtype: List[RedBlackNode[T]]
        """
        red_nodes = []
        if self._root is not None:
            self._find_red_nodes_recursive(self._root, red_nodes)
        return red_nodes

    def _find_red_nodes_recursive(
        self, node: RedBlackNode[T], red_nodes: List[RedBlackNode[T]]
    ) -> None:
        """
        Trouve récursivement tous les nœuds rouges.

        :param node: Nœud à analyser
        :type node: RedBlackNode[T]
        :param red_nodes: Liste des nœuds rouges trouvés
        :type red_nodes: List[RedBlackNode[T]]
        """
        if node is None:
            return
        
        if node.is_red():
            red_nodes.append(node)
        
        self._find_red_nodes_recursive(node.left, red_nodes)
        self._find_red_nodes_recursive(node.right, red_nodes)

    def find_black_nodes(self) -> List[RedBlackNode[T]]:
        """
        Retourne tous les nœuds noirs de l'arbre.

        :return: Liste des nœuds noirs
        :rtype: List[RedBlackNode[T]]
        """
        black_nodes = []
        if self._root is not None:
            self._find_black_nodes_recursive(self._root, black_nodes)
        return black_nodes

    def _find_black_nodes_recursive(
        self, node: RedBlackNode[T], black_nodes: List[RedBlackNode[T]]
    ) -> None:
        """
        Trouve récursivement tous les nœuds noirs.

        :param node: Nœud à analyser
        :type node: RedBlackNode[T]
        :param black_nodes: Liste des nœuds noirs trouvés
        :type black_nodes: List[RedBlackNode[T]]
        """
        if node is None:
            return
        
        if node.is_black():
            black_nodes.append(node)
        
        self._find_black_nodes_recursive(node.left, black_nodes)
        self._find_black_nodes_recursive(node.right, black_nodes)

    def get_structure_analysis(self) -> Dict[str, Any]:
        """
        Analyse la structure de l'arbre rouge-noir.

        :return: Dictionnaire contenant l'analyse de structure
        :rtype: Dict[str, Any]
        """
        analysis = {
            "size": self._size,
            "height": self.get_height(),
            "is_balanced": self.is_balanced(),
            "is_red_black_valid": self.is_red_black_valid(),
            "color_analysis": self.get_color_analysis(),
            "balancing_stats": self.get_balancing_stats(),
        }
        
        # Analyser la structure des nœuds
        if self._root is not None:
            analysis["root_color"] = "red" if self._root.is_red() else "black"
            analysis["red_nodes_count"] = len(self.find_red_nodes())
            analysis["black_nodes_count"] = len(self.find_black_nodes())
        
        return analysis

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'arbre rouge-noir.

        :return: Représentation string de l'arbre rouge-noir
        :rtype: str
        """
        if self._root is None:
            return "RedBlackTree(empty)"
        return f"RedBlackTree(size={self._size}, height={self.get_height()})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de l'arbre rouge-noir.

        :return: Représentation détaillée de l'arbre rouge-noir
        :rtype: str
        """
        return f"RedBlackTree(root={self._root}, size={self._size})"