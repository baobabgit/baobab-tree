"""
Arbre B (B-tree) pour les structures multi-chemins.

Ce module implémente la classe BTree qui représente un arbre B complet.
Les arbres B sont optimisés pour les accès disque en minimisant le nombre
de nœuds à lire et en maintenant une hauteur logarithmique.
"""

from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Tuple

try:
    from .interfaces import Comparable, TreeInterface
    from .btree_node import BTreeNode
    from .exceptions import (
        BTreeError,
        InvalidOrderError,
        NodeFullError,
        NodeUnderflowError,
    )
except ImportError:
    from interfaces import Comparable, TreeInterface
    from btree_node import BTreeNode
    from exceptions import (
        BTreeError,
        InvalidOrderError,
        NodeFullError,
        NodeUnderflowError,
    )


class BTree(TreeInterface[Comparable]):
    """
    Arbre B (B-tree) pour les structures multi-chemins.

    Un arbre B est un arbre de recherche équilibré qui maintient ses données
    triées et permet des insertions, suppressions et recherches en temps O(log n).
    Il est optimisé pour les systèmes de stockage avec des accès disque coûteux.

    :param order: Ordre minimum de l'arbre B (doit être >= 2)
    :type order: int
    """

    def __init__(self, order: int = 3):
        """
        Initialise un arbre B.

        :param order: Ordre minimum de l'arbre B (doit être >= 2)
        :type order: int
        :raises InvalidOrderError: Si l'ordre est invalide (< 2)
        """
        if order < 2:
            raise InvalidOrderError(
                f"Ordre invalide: {order}. L'ordre doit être >= 2", order
            )

        super().__init__()
        self.order = order
        self.root: Optional[BTreeNode[Comparable]] = None
        self.size = 0
        self.height = 0

    def insert(self, key: Comparable) -> None:
        """
        Insère une clé dans l'arbre B.

        :param key: Clé à insérer
        :type key: Comparable
        """
        if self.root is None:
            # Créer la racine si l'arbre est vide
            self.root = BTreeNode(self.order, is_leaf=True)
            self.root.insert_key(key)
            self.size = 1
            self.height = 1
        else:
            # Insérer dans l'arbre existant
            if self.root.is_full():
                # Diviser la racine si elle est pleine
                self._split_root()

            self._insert_non_full(self.root, key)
            self.size += 1

    def _insert_non_full(self, node: BTreeNode[Comparable], key: Comparable) -> None:
        """
        Insère une clé dans un nœud non plein.

        :param node: Nœud dans lequel insérer
        :type node: BTreeNode[Comparable]
        :param key: Clé à insérer
        :type key: Comparable
        """
        if node.is_leaf:
            # Insérer directement dans la feuille
            node.insert_key(key)
        else:
            # Trouver l'enfant approprié
            child_index = node.get_child_index(key)
            child = node.children[child_index]

            if child is None:
                raise BTreeError(
                    f"Enfant manquant à l'index {child_index}",
                    "insert_non_full",
                    node,
                )

            if child.is_full():
                # Diviser l'enfant s'il est plein
                self._split_child(node, child_index)
                # Réévaluer l'enfant approprié après la division
                if key > node.keys[child_index]:
                    child_index += 1
                    child = node.children[child_index]

            self._insert_non_full(child, key)

    def _split_root(self) -> None:
        """
        Divise la racine de l'arbre.
        """
        if self.root is None:
            raise BTreeError("Impossible de diviser une racine nulle", "split_root")

        # Créer une nouvelle racine
        new_root = BTreeNode(self.order, is_leaf=False)
        new_root.children = [self.root]

        # Diviser l'ancienne racine
        left_node, median_key, right_node = self.root.split()

        # Mettre à jour la nouvelle racine
        new_root.keys = [median_key]
        new_root.children = [left_node, right_node]

        # Mettre à jour les références parent
        left_node.parent = new_root
        right_node.parent = new_root

        # Mettre à jour la racine et la hauteur
        self.root = new_root
        self.height += 1

    def _split_child(
        self, parent: BTreeNode[Comparable], child_index: int
    ) -> None:
        """
        Divise un enfant d'un nœud parent.

        :param parent: Nœud parent
        :type parent: BTreeNode[Comparable]
        :param child_index: Index de l'enfant à diviser
        :type child_index: int
        """
        child = parent.children[child_index]
        if child is None:
            raise BTreeError(
                f"Enfant manquant à l'index {child_index}",
                "split_child",
                parent,
            )

        # Diviser l'enfant
        left_node, median_key, right_node = child.split()

        # Insérer la clé médiane dans le parent
        parent.keys.insert(child_index, median_key)
        parent.children[child_index] = left_node
        parent.children.insert(child_index + 1, right_node)

        # Mettre à jour les références parent
        left_node.parent = parent
        right_node.parent = parent

    def delete(self, key: Comparable) -> bool:
        """
        Supprime une clé de l'arbre B.

        :param key: Clé à supprimer
        :type key: Comparable
        :return: True si la clé a été supprimée, False sinon
        :rtype: bool
        """
        if self.root is None:
            return False

        result = self._delete_key(self.root, key)
        if result:
            self.size -= 1

            # Si la racine est vide et n'est pas une feuille, la remplacer
            if not self.root.is_leaf and len(self.root.keys) == 0:
                if len(self.root.children) > 0:
                    self.root = self.root.children[0]
                    self.root.parent = None
                    self.height -= 1
                else:
                    self.root = None
                    self.height = 0

        return result

    def _delete_key(
        self, node: BTreeNode[Comparable], key: Comparable
    ) -> bool:
        """
        Supprime une clé d'un nœud.

        :param node: Nœud dans lequel supprimer
        :type node: BTreeNode[Comparable]
        :param key: Clé à supprimer
        :type key: Comparable
        :return: True si la clé a été supprimée, False sinon
        :rtype: bool
        """
        if node.is_leaf:
            # Supprimer directement de la feuille
            return node.delete_key(key)
        else:
            # Trouver l'enfant approprié
            child_index = node.get_child_index(key)
            child = node.children[child_index]

            if child is None:
                raise BTreeError(
                    f"Enfant manquant à l'index {child_index}",
                    "delete_key",
                    node,
                )

            # Vérifier si la clé est dans ce nœud
            if child_index < len(node.keys) and node.keys[child_index] == key:
                # La clé est dans ce nœud interne
                return self._delete_internal_key(node, child_index)
            else:
                # La clé est dans le sous-arbre
                if child.is_minimum():
                    # Garantir que l'enfant a au moins le minimum de clés
                    self._ensure_minimum_keys(node, child_index)

                # Réévaluer l'enfant après la garantie
                child = node.children[child_index]
                if child is None:
                    raise BTreeError(
                        f"Enfant manquant après garantie à l'index {child_index}",
                        "delete_key",
                        node,
                    )

                return self._delete_key(child, key)

    def _delete_internal_key(
        self, node: BTreeNode[Comparable], key_index: int
    ) -> bool:
        """
        Supprime une clé d'un nœud interne.

        :param node: Nœud interne
        :type node: BTreeNode[Comparable]
        :param key_index: Index de la clé à supprimer
        :type key_index: int
        :return: True si la clé a été supprimée, False sinon
        :rtype: bool
        """
        left_child = node.children[key_index]
        right_child = node.children[key_index + 1]

        if left_child is None or right_child is None:
            raise BTreeError(
                f"Enfant manquant pour la suppression interne à l'index {key_index}",
                "delete_internal_key",
                node,
            )

        # Cas 1: L'enfant gauche a plus que le minimum de clés
        if len(left_child.keys) > self.order - 1:
            predecessor = self._get_predecessor(left_child)
            node.keys[key_index] = predecessor
            return self._delete_key(left_child, predecessor)

        # Cas 2: L'enfant droit a plus que le minimum de clés
        elif len(right_child.keys) > self.order - 1:
            successor = self._get_successor(right_child)
            node.keys[key_index] = successor
            return self._delete_key(right_child, successor)

        # Cas 3: Les deux enfants ont le minimum de clés
        else:
            # Fusionner les deux enfants
            self._merge_children(node, key_index)
            return self._delete_key(left_child, node.keys[key_index])

    def _get_predecessor(self, node: BTreeNode[Comparable]) -> Comparable:
        """
        Retourne le prédécesseur d'un nœud.

        :param node: Nœud pour lequel trouver le prédécesseur
        :type node: BTreeNode[Comparable]
        :return: Prédécesseur du nœud
        :rtype: Comparable
        """
        while not node.is_leaf:
            node = node.children[-1]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du prédécesseur", "get_predecessor")
        return node.keys[-1]

    def _get_successor(self, node: BTreeNode[Comparable]) -> Comparable:
        """
        Retourne le successeur d'un nœud.

        :param node: Nœud pour lequel trouver le successeur
        :type node: BTreeNode[Comparable]
        :return: Successeur du nœud
        :rtype: Comparable
        """
        while not node.is_leaf:
            node = node.children[0]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du successeur", "get_successor")
        return node.keys[0]

    def _ensure_minimum_keys(
        self, parent: BTreeNode[Comparable], child_index: int
    ) -> None:
        """
        Garantit qu'un enfant a au moins le minimum de clés.

        :param parent: Nœud parent
        :type parent: BTreeNode[Comparable]
        :param child_index: Index de l'enfant
        :type child_index: int
        """
        child = parent.children[child_index]
        if child is None:
            raise BTreeError(
                f"Enfant manquant à l'index {child_index}",
                "ensure_minimum_keys",
                parent,
            )

        # Essayer d'emprunter au frère gauche
        if child_index > 0:
            left_sibling = parent.children[child_index - 1]
            if left_sibling is not None and len(left_sibling.keys) > self.order - 1:
                child.borrow_from_left()
                return

        # Essayer d'emprunter au frère droit
        if child_index < len(parent.children) - 1:
            right_sibling = parent.children[child_index + 1]
            if right_sibling is not None and len(right_sibling.keys) > self.order - 1:
                child.borrow_from_right()
                return

        # Fusionner avec un frère
        if child_index > 0:
            # Fusionner avec le frère gauche
            left_sibling = parent.children[child_index - 1]
            if left_sibling is not None:
                separator_key = parent.keys[child_index - 1]
                left_sibling.merge_with(child, separator_key)
                parent.keys.pop(child_index - 1)
                parent.children.pop(child_index)
        else:
            # Fusionner avec le frère droit
            right_sibling = parent.children[child_index + 1]
            if right_sibling is not None:
                separator_key = parent.keys[child_index]
                child.merge_with(right_sibling, separator_key)
                parent.keys.pop(child_index)
                parent.children.pop(child_index + 1)

    def _merge_children(
        self, parent: BTreeNode[Comparable], key_index: int
    ) -> None:
        """
        Fusionne deux enfants d'un nœud parent.

        :param parent: Nœud parent
        :type parent: BTreeNode[Comparable]
        :param key_index: Index de la clé séparatrice
        :type key_index: int
        """
        left_child = parent.children[key_index]
        right_child = parent.children[key_index + 1]

        if left_child is None or right_child is None:
            raise BTreeError(
                f"Enfant manquant pour la fusion à l'index {key_index}",
                "merge_children",
                parent,
            )

        separator_key = parent.keys[key_index]
        left_child.merge_with(right_child, separator_key)

        # Supprimer la clé séparatrice et l'enfant droit du parent
        parent.keys.pop(key_index)
        parent.children.pop(key_index + 1)

    def search(self, key: Comparable) -> Optional[BTreeNode[Comparable]]:
        """
        Recherche une clé dans l'arbre B.

        :param key: Clé à rechercher
        :type key: Comparable
        :return: Nœud contenant la clé, None si non trouvé
        :rtype: Optional[BTreeNode[Comparable]]
        """
        if self.root is None:
            return None

        return self._search_node(self.root, key)

    def _search_node(
        self, node: BTreeNode[Comparable], key: Comparable
    ) -> Optional[BTreeNode[Comparable]]:
        """
        Recherche une clé dans un nœud.

        :param node: Nœud dans lequel rechercher
        :type node: BTreeNode[Comparable]
        :param key: Clé à rechercher
        :type key: Comparable
        :return: Nœud contenant la clé, None si non trouvé
        :rtype: Optional[BTreeNode[Comparable]]
        """
        # Rechercher la clé dans le nœud
        index = node.search_key(key)
        if index < len(node.keys) and node.keys[index] == key:
            return node

        # Si c'est une feuille, la clé n'existe pas
        if node.is_leaf:
            return None

        # Rechercher dans le sous-arbre approprié
        child_index = node.get_child_index(key)
        child = node.children[child_index]
        if child is None:
            return None

        return self._search_node(child, key)

    def contains(self, key: Comparable) -> bool:
        """
        Vérifie si une clé existe dans l'arbre B.

        :param key: Clé à vérifier
        :type key: Comparable
        :return: True si la clé existe, False sinon
        :rtype: bool
        """
        return self.search(key) is not None

    def clear(self) -> None:
        """
        Vide l'arbre B.
        """
        self.root = None
        self.size = 0
        self.height = 0

    def is_empty(self) -> bool:
        """
        Vérifie si l'arbre B est vide.

        :return: True si l'arbre est vide, False sinon
        :rtype: bool
        """
        return self.root is None

    def get_size(self) -> int:
        """
        Retourne le nombre de clés dans l'arbre B.

        :return: Nombre de clés
        :rtype: int
        """
        return self.size

    def get_height(self) -> int:
        """
        Retourne la hauteur de l'arbre B.

        :return: Hauteur de l'arbre
        :rtype: int
        """
        return self.height

    def get_min(self) -> Optional[Comparable]:
        """
        Retourne la clé minimale de l'arbre B.

        :return: Clé minimale, None si l'arbre est vide
        :rtype: Optional[Comparable]
        """
        if self.root is None:
            return None

        node = self.root
        while not node.is_leaf:
            node = node.children[0]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du minimum", "get_min")

        return node.keys[0] if node.keys else None

    def get_max(self) -> Optional[Comparable]:
        """
        Retourne la clé maximale de l'arbre B.

        :return: Clé maximale, None si l'arbre est vide
        :rtype: Optional[Comparable]
        """
        if self.root is None:
            return None

        node = self.root
        while not node.is_leaf:
            node = node.children[-1]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du maximum", "get_max")

        return node.keys[-1] if node.keys else None

    def is_valid(self) -> bool:
        """
        Vérifie si l'arbre B respecte toutes ses propriétés.

        :return: True si l'arbre est valide, False sinon
        :rtype: bool
        """
        if self.root is None:
            return self.size == 0 and self.height == 0

        try:
            return self._validate_tree(self.root, None, 0)
        except BTreeError:
            return False

    def _validate_tree(
        self,
        node: BTreeNode[Comparable],
        parent: Optional[BTreeNode[Comparable]],
        depth: int,
    ) -> bool:
        """
        Valide récursivement un sous-arbre.

        :param node: Nœud à valider
        :type node: BTreeNode[Comparable]
        :param parent: Nœud parent
        :type parent: Optional[BTreeNode[Comparable]]
        :param depth: Profondeur actuelle
        :type depth: int
        :return: True si le sous-arbre est valide, False sinon
        :rtype: bool
        """
        # Vérifier les propriétés de base
        if not node.validate_node():
            return False

        # Vérifier la référence parent
        if node.parent != parent:
            return False

        # Vérifier le nombre de clés
        if len(node.keys) > 2 * self.order - 1:
            return False

        if not node.is_leaf and len(node.children) != len(node.keys) + 1:
            return False

        # Vérifier les enfants
        if not node.is_leaf:
            for child in node.children:
                if child is not None:
                    if not self._validate_tree(child, node, depth + 1):
                        return False

        return True

    def range_query(self, min_key: Comparable, max_key: Comparable) -> List[Comparable]:
        """
        Retourne toutes les clés dans une plage donnée.

        :param min_key: Clé minimale (incluse)
        :type min_key: Comparable
        :param max_key: Clé maximale (incluse)
        :type max_key: Comparable
        :return: Liste des clés dans la plage
        :rtype: List[Comparable]
        """
        result = []
        if self.root is not None:
            self._range_query_recursive(self.root, min_key, max_key, result)
        return result

    def _range_query_recursive(
        self,
        node: BTreeNode[Comparable],
        min_key: Comparable,
        max_key: Comparable,
        result: List[Comparable],
    ) -> None:
        """
        Effectue une requête de plage récursivement.

        :param node: Nœud actuel
        :type node: BTreeNode[Comparable]
        :param min_key: Clé minimale
        :type min_key: Comparable
        :param max_key: Clé maximale
        :type max_key: Comparable
        :param result: Liste pour stocker les résultats
        :type result: List[Comparable]
        """
        i = 0
        while i < len(node.keys) and node.keys[i] < min_key:
            i += 1

        if not node.is_leaf:
            if i < len(node.children):
                child = node.children[i]
                if child is not None:
                    self._range_query_recursive(child, min_key, max_key, result)

        while i < len(node.keys) and node.keys[i] <= max_key:
            result.append(node.keys[i])
            if not node.is_leaf and i + 1 < len(node.children):
                child = node.children[i + 1]
                if child is not None:
                    self._range_query_recursive(child, min_key, max_key, result)
            i += 1

    def count_range(self, min_key: Comparable, max_key: Comparable) -> int:
        """
        Compte le nombre de clés dans une plage donnée.

        :param min_key: Clé minimale (incluse)
        :type min_key: Comparable
        :param max_key: Clé maximale (incluse)
        :type max_key: Comparable
        :return: Nombre de clés dans la plage
        :rtype: int
        """
        return len(self.range_query(min_key, max_key))

    def bulk_load(self, keys: List[Comparable]) -> None:
        """
        Charge un ensemble de clés de manière optimisée.

        :param keys: Liste des clés à charger
        :type keys: List[Comparable]
        """
        if not keys:
            return

        # Trier les clés
        sorted_keys = sorted(keys)

        # Construire l'arbre de manière optimisée
        self.clear()
        self._build_tree_optimized(sorted_keys)

    def _build_tree_optimized(self, sorted_keys: List[Comparable]) -> None:
        """
        Construit l'arbre de manière optimisée à partir de clés triées.

        :param sorted_keys: Clés triées
        :type sorted_keys: List[Comparable]
        """
        if not sorted_keys:
            return

        # Calculer le nombre de feuilles nécessaires
        keys_per_leaf = 2 * self.order - 1
        num_leaves = (len(sorted_keys) + keys_per_leaf - 1) // keys_per_leaf

        # Créer les feuilles
        leaves = []
        for i in range(num_leaves):
            start = i * keys_per_leaf
            end = min(start + keys_per_leaf, len(sorted_keys))
            leaf_keys = sorted_keys[start:end]

            leaf = BTreeNode(self.order, is_leaf=True)
            leaf.keys = leaf_keys
            leaves.append(leaf)

        # Construire les niveaux supérieurs
        current_level = leaves
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2 * self.order - 1):
                # Grouper les nœuds du niveau actuel
                group = current_level[i : i + 2 * self.order - 1]
                if len(group) == 1:
                    next_level.append(group[0])
                else:
                    # Créer un nœud parent pour ce groupe
                    parent = BTreeNode(self.order, is_leaf=False)
                    parent.children = group
                    for child in group:
                        child.parent = parent

                    # Extraire les clés séparatrices
                    separator_keys = []
                    for child in group[1:]:
                        if child.keys:
                            separator_keys.append(child.keys[0])

                    parent.keys = separator_keys
                    next_level.append(parent)

            current_level = next_level

        # Définir la racine
        if current_level:
            self.root = current_level[0]
            self.root.parent = None
            self.size = len(sorted_keys)
            self.height = self._calculate_height(self.root)

    def _calculate_height(self, node: BTreeNode[Comparable]) -> int:
        """
        Calcule la hauteur d'un nœud.

        :param node: Nœud pour lequel calculer la hauteur
        :type node: BTreeNode[Comparable]
        :return: Hauteur du nœud
        :rtype: int
        """
        if node.is_leaf:
            return 1

        max_child_height = 0
        for child in node.children:
            if child is not None:
                child_height = self._calculate_height(child)
                max_child_height = max(max_child_height, child_height)

        return max_child_height + 1

    def get_leaf_nodes(self) -> List[BTreeNode[Comparable]]:
        """
        Retourne tous les nœuds feuilles de l'arbre.

        :return: Liste des nœuds feuilles
        :rtype: List[BTreeNode[Comparable]]
        """
        leaves = []
        if self.root is not None:
            self._collect_leaves(self.root, leaves)
        return leaves

    def _collect_leaves(
        self, node: BTreeNode[Comparable], leaves: List[BTreeNode[Comparable]]
    ) -> None:
        """
        Collecte récursivement tous les nœuds feuilles.

        :param node: Nœud actuel
        :type node: BTreeNode[Comparable]
        :param leaves: Liste pour stocker les feuilles
        :type leaves: List[BTreeNode[Comparable]]
        """
        if node.is_leaf:
            leaves.append(node)
        else:
            for child in node.children:
                if child is not None:
                    self._collect_leaves(child, leaves)

    def get_internal_nodes(self) -> List[BTreeNode[Comparable]]:
        """
        Retourne tous les nœuds internes de l'arbre.

        :return: Liste des nœuds internes
        :rtype: List[BTreeNode[Comparable]]
        """
        internals = []
        if self.root is not None:
            self._collect_internals(self.root, internals)
        return internals

    def _collect_internals(
        self, node: BTreeNode[Comparable], internals: List[BTreeNode[Comparable]]
    ) -> None:
        """
        Collecte récursivement tous les nœuds internes.

        :param node: Nœud actuel
        :type node: BTreeNode[Comparable]
        :param internals: Liste pour stocker les nœuds internes
        :type internals: List[BTreeNode[Comparable]]
        """
        if not node.is_leaf:
            internals.append(node)
            for child in node.children:
                if child is not None:
                    self._collect_internals(child, internals)

    def get_node_count(self) -> Dict[str, int]:
        """
        Retourne des statistiques sur les nœuds de l'arbre.

        :return: Dictionnaire contenant les statistiques
        :rtype: Dict[str, int]
        """
        stats = {
            "total_nodes": 0,
            "leaf_nodes": 0,
            "internal_nodes": 0,
            "total_keys": self.size,
            "height": self.height,
        }

        if self.root is not None:
            self._count_nodes(self.root, stats)

        return stats

    def _count_nodes(
        self, node: BTreeNode[Comparable], stats: Dict[str, int]
    ) -> None:
        """
        Compte récursivement les nœuds.

        :param node: Nœud actuel
        :type node: BTreeNode[Comparable]
        :param stats: Dictionnaire pour stocker les statistiques
        :type stats: Dict[str, int]
        """
        stats["total_nodes"] += 1

        if node.is_leaf:
            stats["leaf_nodes"] += 1
        else:
            stats["internal_nodes"] += 1
            for child in node.children:
                if child is not None:
                    self._count_nodes(child, stats)

    def validate_properties(self) -> Dict[str, bool]:
        """
        Valide toutes les propriétés de l'arbre B.

        :return: Dictionnaire contenant les résultats de validation
        :rtype: Dict[str, bool]
        """
        return {
            "is_valid": self.is_valid(),
            "height_consistent": self._validate_height(),
            "size_consistent": self._validate_size(),
            "keys_sorted": self._validate_keys_sorted(),
            "node_capacity": self._validate_node_capacity(),
        }

    def _validate_height(self) -> bool:
        """
        Valide la cohérence de la hauteur.

        :return: True si la hauteur est cohérente, False sinon
        :rtype: bool
        """
        if self.root is None:
            return self.height == 0

        calculated_height = self._calculate_height(self.root)
        return calculated_height == self.height

    def _validate_size(self) -> bool:
        """
        Valide la cohérence de la taille.

        :return: True si la taille est cohérente, False sinon
        :rtype: bool
        """
        if self.root is None:
            return self.size == 0

        calculated_size = self._count_total_keys(self.root)
        return calculated_size == self.size

    def _count_total_keys(self, node: BTreeNode[Comparable]) -> int:
        """
        Compte le nombre total de clés dans un sous-arbre.

        :param node: Nœud racine du sous-arbre
        :type node: BTreeNode[Comparable]
        :return: Nombre total de clés
        :rtype: int
        """
        count = len(node.keys)
        if not node.is_leaf:
            for child in node.children:
                if child is not None:
                    count += self._count_total_keys(child)
        return count

    def _validate_keys_sorted(self) -> bool:
        """
        Valide que toutes les clés sont triées.

        :return: True si les clés sont triées, False sinon
        :rtype: bool
        """
        if self.root is None:
            return True

        try:
            self._validate_keys_sorted_recursive(self.root)
            return True
        except BTreeError:
            return False

    def _validate_keys_sorted_recursive(self, node: BTreeNode[Comparable]) -> None:
        """
        Valide récursivement que les clés sont triées.

        :param node: Nœud à valider
        :type node: BTreeNode[Comparable]
        :raises BTreeError: Si les clés ne sont pas triées
        """
        # Vérifier que les clés du nœud sont triées
        for i in range(len(node.keys) - 1):
            if node.keys[i] >= node.keys[i + 1]:
                raise BTreeError(
                    f"Clés non triées dans le nœud: {node.keys[i]} >= {node.keys[i + 1]}",
                    "validate_keys_sorted",
                    node,
                )

        # Valider récursivement les enfants
        if not node.is_leaf:
            for child in node.children:
                if child is not None:
                    self._validate_keys_sorted_recursive(child)

    def _validate_node_capacity(self) -> bool:
        """
        Valide la capacité des nœuds.

        :return: True si la capacité est respectée, False sinon
        :rtype: bool
        """
        if self.root is None:
            return True

        try:
            self._validate_node_capacity_recursive(self.root)
            return True
        except BTreeError:
            return False

    def _validate_node_capacity_recursive(self, node: BTreeNode[Comparable]) -> None:
        """
        Valide récursivement la capacité des nœuds.

        :param node: Nœud à valider
        :type node: BTreeNode[Comparable]
        :raises BTreeError: Si la capacité n'est pas respectée
        """
        # Vérifier la capacité du nœud
        if len(node.keys) > 2 * self.order - 1:
            raise BTreeError(
                f"Nœud dépasse la capacité maximale: {len(node.keys)} > {2 * self.order - 1}",
                "validate_node_capacity",
                node,
            )

        if not node.is_leaf and len(node.children) > 2 * self.order:
            raise BTreeError(
                f"Nœud a trop d'enfants: {len(node.children)} > {2 * self.order}",
                "validate_node_capacity",
                node,
            )

        # Valider récursivement les enfants
        if not node.is_leaf:
            for child in node.children:
                if child is not None:
                    self._validate_node_capacity_recursive(child)

    def __str__(self) -> str:
        """
        Retourne une représentation string de l'arbre B.

        :return: Représentation string de l'arbre
        :rtype: str
        """
        if self.root is None:
            return "BTree(order={}, empty)".format(self.order)

        return "BTree(order={}, size={}, height={})".format(
            self.order, self.size, self.height
        )

    def __repr__(self) -> str:
        """
        Retourne une représentation détaillée de l'arbre B.

        :return: Représentation détaillée de l'arbre
        :rtype: str
        """
        return (
            f"BTree(order={self.order}, size={self.size}, "
            f"height={self.height}, root={'present' if self.root else 'None'})"
        )