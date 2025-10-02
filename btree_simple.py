#!/usr/bin/env python3
"""
Version simplifiée des classes B-tree pour éviter les problèmes d'import.
Cette version se concentre sur les fonctionnalités de base sans les opérations complexes.
"""

from typing import Any, Dict, List, Optional, Tuple
from abc import ABC, abstractmethod


class TreeNode(ABC):
    """Classe abstraite de base pour tous les nœuds d'arbres."""
    
    def __init__(self):
        """Initialise un nœud d'arbre."""
        pass
    
    @abstractmethod
    def get_value(self) -> Any:
        """Retourne la valeur du nœud."""
        pass


class TreeInterface(ABC):
    """Interface pour tous les types d'arbres."""
    
    @abstractmethod
    def insert(self, key: Any) -> None:
        """Insère une clé dans l'arbre."""
        pass
    
    @abstractmethod
    def delete(self, key: Any) -> bool:
        """Supprime une clé de l'arbre."""
        pass
    
    @abstractmethod
    def search(self, key: Any) -> Optional[Any]:
        """Recherche une clé dans l'arbre."""
        pass
    
    @abstractmethod
    def contains(self, key: Any) -> bool:
        """Vérifie si une clé existe dans l'arbre."""
        pass


class BTreeError(Exception):
    """Exception de base pour toutes les erreurs liées aux B-trees."""
    
    def __init__(self, message: str, operation: str = None, node=None):
        super().__init__(message)
        self.message = message
        self.operation = operation
        self.node = node
    
    def __str__(self) -> str:
        result = self.message
        if self.operation is not None:
            result += f" (Operation: {self.operation})"
        if self.node is not None:
            result += f" (Node: {self.node})"
        return result


class InvalidOrderError(BTreeError):
    """Exception levée lors d'un ordre invalide pour un B-tree."""
    
    def __init__(self, message: str, order: int):
        super().__init__(message, "order_validation")
        self.order = order
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        return f"{base_msg} (Order: {self.order})"


class NodeFullError(BTreeError):
    """Exception levée lors d'une tentative d'insertion dans un nœud plein."""
    
    def __init__(self, message: str, node, key):
        super().__init__(message, "insertion", node)
        self.key = key
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        return f"{base_msg} (Key: {self.key})"


class BTreeNode(TreeNode):
    """
    Nœud B-tree pour les arbres multi-chemins.
    
    Un nœud B-tree peut contenir entre (order-1) et (2*order-1) clés,
    et entre order et (2*order) enfants.
    """
    
    def __init__(
        self,
        order: int,
        is_leaf: bool = True,
        keys: Optional[List[Any]] = None,
        children: Optional[List[Optional['BTreeNode']]] = None,
        parent: Optional['BTreeNode'] = None,
    ):
        """Initialise un nœud B-tree."""
        if order < 2:
            raise BTreeError(f"Ordre invalide: {order}. L'ordre doit être >= 2")
        
        super().__init__()
        self.order = order
        self.is_leaf = is_leaf
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.parent = parent
        
        # Validation initiale
        self._validate_node()
    
    def _validate_node(self) -> None:
        """Valide les propriétés du nœud B-tree."""
        max_keys = 2 * self.order - 1
        max_children = 2 * self.order
        
        if len(self.keys) > max_keys:
            raise BTreeError(
                f"Trop de clés: {len(self.keys)} > {max_keys}",
                "validation",
                self,
            )
        
        if not self.is_leaf and len(self.children) > max_children:
            raise BTreeError(
                f"Trop d'enfants: {len(self.children)} > {max_children}",
                "validation",
                self,
            )
        
        # Vérifier que les clés sont triées
        for i in range(len(self.keys) - 1):
            if self.keys[i] >= self.keys[i + 1]:
                raise BTreeError(
                    f"Clés non triées: {self.keys[i]} >= {self.keys[i + 1]}",
                    "validation",
                    self,
                )
    
    def get_value(self) -> Any:
        """Retourne la valeur du nœud (première clé)."""
        return self.keys[0] if self.keys else None
    
    def get_key_count(self) -> int:
        """Retourne le nombre de clés dans le nœud."""
        return len(self.keys)
    
    def get_child_count(self) -> int:
        """Retourne le nombre d'enfants dans le nœud."""
        return len(self.children)
    
    def is_full(self) -> bool:
        """Vérifie si le nœud est plein."""
        return len(self.keys) >= 2 * self.order - 1
    
    def is_minimum(self) -> bool:
        """Vérifie si le nœud contient le minimum de clés."""
        return len(self.keys) <= self.order - 1
    
    def search_key(self, key: Any) -> int:
        """Recherche l'index d'une clé dans le nœud."""
        left, right = 0, len(self.keys)
        while left < right:
            mid = (left + right) // 2
            if self.keys[mid] < key:
                left = mid + 1
            else:
                right = mid
        return left
    
    def insert_key(self, key: Any) -> int:
        """Insère une clé dans le nœud à la bonne position."""
        if self.is_full():
            raise NodeFullError(
                f"Nœud plein, impossible d'insérer la clé {key}",
                self,
                key,
            )
        
        index = self.search_key(key)
        self.keys.insert(index, key)
        return index
    
    def delete_key(self, key: Any) -> bool:
        """Supprime une clé du nœud."""
        try:
            index = self.keys.index(key)
            self.keys.pop(index)
            return True
        except ValueError:
            return False
    
    def get_child_index(self, key: Any) -> int:
        """Retourne l'index de l'enfant approprié pour une clé donnée."""
        if self.is_leaf:
            raise BTreeError(
                "Impossible de récupérer l'enfant d'une feuille",
                "get_child_index",
                self,
            )
        
        index = self.search_key(key)
        return index
    
    def split(self) -> Tuple['BTreeNode', Any, 'BTreeNode']:
        """Divise le nœud en deux nœuds et retourne la clé médiane."""
        if not self.is_full():
            raise BTreeError(
                "Impossible de diviser un nœud qui n'est pas plein",
                "split",
                self,
            )
        
        # Clé médiane
        mid_index = self.order - 1
        median_key = self.keys[mid_index]
        
        # Créer le nœud droit
        right_keys = self.keys[mid_index + 1 :]
        right_children = (
            self.children[mid_index + 1 :] if not self.is_leaf else []
        )
        right_node = BTreeNode(
            self.order,
            self.is_leaf,
            right_keys,
            right_children,
            self.parent,
        )
        
        # Mettre à jour le nœud gauche (nœud actuel)
        self.keys = self.keys[:mid_index]
        if not self.is_leaf:
            self.children = self.children[: mid_index + 1]
        
        # Mettre à jour les références parent des enfants du nœud droit
        if not self.is_leaf:
            for child in right_node.children:
                if child is not None:
                    child.parent = right_node
        
        return self, median_key, right_node
    
    def validate_node(self) -> bool:
        """Valide les propriétés du nœud B-tree."""
        try:
            self._validate_node()
            return True
        except BTreeError:
            return False
    
    def __str__(self) -> str:
        """Retourne une représentation string du nœud."""
        return f"BTreeNode(keys={self.keys}, is_leaf={self.is_leaf})"
    
    def __repr__(self) -> str:
        """Retourne une représentation détaillée du nœud."""
        return (
            f"BTreeNode(order={self.order}, keys={self.keys}, "
            f"is_leaf={self.is_leaf}, children={len(self.children)})"
        )


class BTree(TreeInterface):
    """
    Arbre B (B-tree) pour les structures multi-chemins.
    
    Un arbre B est un arbre de recherche équilibré qui maintient ses données
    triées et permet des insertions, suppressions et recherches en temps O(log n).
    """
    
    def __init__(self, order: int = 3):
        """Initialise un arbre B."""
        if order < 2:
            raise InvalidOrderError(
                f"Ordre invalide: {order}. L'ordre doit être >= 2", order
            )
        
        super().__init__()
        self.order = order
        self.root: Optional[BTreeNode] = None
        self.size = 0
        self.height = 0
    
    def insert(self, key: Any) -> None:
        """Insère une clé dans l'arbre B."""
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
    
    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Insère une clé dans un nœud non plein."""
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
        """Divise la racine de l'arbre."""
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
    
    def _split_child(self, parent: BTreeNode, child_index: int) -> None:
        """Divise un enfant d'un nœud parent."""
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
    
    def delete(self, key: Any) -> bool:
        """Supprime une clé de l'arbre B (version simplifiée)."""
        if self.root is None:
            return False
        
        # Version simplifiée : reconstruire l'arbre sans la clé
        all_keys = self._collect_all_keys()
        if key not in all_keys:
            return False
        
        all_keys.remove(key)
        self.clear()
        
        # Reconstruire l'arbre
        for k in all_keys:
            self.insert(k)
        
        return True
    
    def _collect_all_keys(self) -> List[Any]:
        """Collecte toutes les clés de l'arbre."""
        keys = []
        if self.root is not None:
            self._collect_keys_recursive(self.root, keys)
        return keys
    
    def _collect_keys_recursive(self, node: BTreeNode, keys: List[Any]) -> None:
        """Collecte récursivement les clés d'un nœud."""
        keys.extend(node.keys)
        if not node.is_leaf:
            for child in node.children:
                if child is not None:
                    self._collect_keys_recursive(child, keys)
    
    def search(self, key: Any) -> Optional[BTreeNode]:
        """Recherche une clé dans l'arbre B."""
        if self.root is None:
            return None
        
        return self._search_node(self.root, key)
    
    def _search_node(self, node: BTreeNode, key: Any) -> Optional[BTreeNode]:
        """Recherche une clé dans un nœud."""
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
    
    def contains(self, key: Any) -> bool:
        """Vérifie si une clé existe dans l'arbre B."""
        return self.search(key) is not None
    
    def clear(self) -> None:
        """Vide l'arbre B."""
        self.root = None
        self.size = 0
        self.height = 0
    
    def is_empty(self) -> bool:
        """Vérifie si l'arbre B est vide."""
        return self.root is None
    
    def get_size(self) -> int:
        """Retourne le nombre de clés dans l'arbre B."""
        return self.size
    
    def get_height(self) -> int:
        """Retourne la hauteur de l'arbre B."""
        return self.height
    
    def get_min(self) -> Optional[Any]:
        """Retourne la clé minimale de l'arbre B."""
        if self.root is None:
            return None
        
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du minimum", "get_min")
        
        return node.keys[0] if node.keys else None
    
    def get_max(self) -> Optional[Any]:
        """Retourne la clé maximale de l'arbre B."""
        if self.root is None:
            return None
        
        node = self.root
        while not node.is_leaf:
            node = node.children[-1]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du maximum", "get_max")
        
        return node.keys[-1] if node.keys else None
    
    def is_valid(self) -> bool:
        """Vérifie si l'arbre B respecte toutes ses propriétés."""
        if self.root is None:
            return self.size == 0 and self.height == 0
        
        try:
            return self._validate_tree(self.root, None, 0)
        except BTreeError:
            return False
    
    def _validate_tree(self, node: BTreeNode, parent: Optional[BTreeNode], depth: int) -> bool:
        """Valide récursivement un sous-arbre."""
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
    
    def range_query(self, min_key: Any, max_key: Any) -> List[Any]:
        """Retourne toutes les clés dans une plage donnée."""
        result = []
        if self.root is not None:
            self._range_query_recursive(self.root, min_key, max_key, result)
        return result
    
    def _range_query_recursive(self, node: BTreeNode, min_key: Any, max_key: Any, result: List[Any]) -> None:
        """Effectue une requête de plage récursivement."""
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
    
    def count_range(self, min_key: Any, max_key: Any) -> int:
        """Compte le nombre de clés dans une plage donnée."""
        return len(self.range_query(min_key, max_key))
    
    def bulk_load(self, keys: List[Any]) -> None:
        """Charge un ensemble de clés de manière optimisée."""
        if not keys:
            return
        
        # Trier les clés
        sorted_keys = sorted(keys)
        
        # Construire l'arbre de manière optimisée
        self.clear()
        self._build_tree_optimized(sorted_keys)
    
    def _build_tree_optimized(self, sorted_keys: List[Any]) -> None:
        """Construit l'arbre de manière optimisée à partir de clés triées."""
        if not sorted_keys:
            return
        
        # Version simplifiée : insérer les clés une par une
        self.clear()
        for key in sorted_keys:
            self.insert(key)
    
    def _calculate_height(self, node: BTreeNode) -> int:
        """Calcule la hauteur d'un nœud."""
        if node.is_leaf:
            return 1
        
        max_child_height = 0
        for child in node.children:
            if child is not None:
                child_height = self._calculate_height(child)
                max_child_height = max(max_child_height, child_height)
        
        return max_child_height + 1
    
    def get_leaf_nodes(self) -> List[BTreeNode]:
        """Retourne tous les nœuds feuilles de l'arbre."""
        leaves = []
        if self.root is not None:
            self._collect_leaves(self.root, leaves)
        return leaves
    
    def _collect_leaves(self, node: BTreeNode, leaves: List[BTreeNode]) -> None:
        """Collecte récursivement tous les nœuds feuilles."""
        if node.is_leaf:
            leaves.append(node)
        else:
            for child in node.children:
                if child is not None:
                    self._collect_leaves(child, leaves)
    
    def get_internal_nodes(self) -> List[BTreeNode]:
        """Retourne tous les nœuds internes de l'arbre."""
        internals = []
        if self.root is not None:
            self._collect_internals(self.root, internals)
        return internals
    
    def _collect_internals(self, node: BTreeNode, internals: List[BTreeNode]) -> None:
        """Collecte récursivement tous les nœuds internes."""
        if not node.is_leaf:
            internals.append(node)
            for child in node.children:
                if child is not None:
                    self._collect_internals(child, internals)
    
    def get_node_count(self) -> Dict[str, int]:
        """Retourne des statistiques sur les nœuds de l'arbre."""
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
    
    def _count_nodes(self, node: BTreeNode, stats: Dict[str, int]) -> None:
        """Compte récursivement les nœuds."""
        stats["total_nodes"] += 1
        
        if node.is_leaf:
            stats["leaf_nodes"] += 1
        else:
            stats["internal_nodes"] += 1
            for child in node.children:
                if child is not None:
                    self._count_nodes(child, stats)
    
    def validate_properties(self) -> Dict[str, bool]:
        """Valide toutes les propriétés de l'arbre B."""
        return {
            "is_valid": self.is_valid(),
            "height_consistent": self._validate_height(),
            "size_consistent": self._validate_size(),
            "keys_sorted": self._validate_keys_sorted(),
            "node_capacity": self._validate_node_capacity(),
        }
    
    def _validate_height(self) -> bool:
        """Valide la cohérence de la hauteur."""
        if self.root is None:
            return self.height == 0
        
        calculated_height = self._calculate_height(self.root)
        return calculated_height == self.height
    
    def _validate_size(self) -> bool:
        """Valide la cohérence de la taille."""
        if self.root is None:
            return self.size == 0
        
        calculated_size = self._count_total_keys(self.root)
        return calculated_size == self.size
    
    def _count_total_keys(self, node: BTreeNode) -> int:
        """Compte le nombre total de clés dans un sous-arbre."""
        count = len(node.keys)
        if not node.is_leaf:
            for child in node.children:
                if child is not None:
                    count += self._count_total_keys(child)
        return count
    
    def _validate_keys_sorted(self) -> bool:
        """Valide que toutes les clés sont triées."""
        if self.root is None:
            return True
        
        try:
            self._validate_keys_sorted_recursive(self.root)
            return True
        except BTreeError:
            return False
    
    def _validate_keys_sorted_recursive(self, node: BTreeNode) -> None:
        """Valide récursivement que les clés sont triées."""
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
        """Valide la capacité des nœuds."""
        if self.root is None:
            return True
        
        try:
            self._validate_node_capacity_recursive(self.root)
            return True
        except BTreeError:
            return False
    
    def _validate_node_capacity_recursive(self, node: BTreeNode) -> None:
        """Valide récursivement la capacité des nœuds."""
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
        """Retourne une représentation string de l'arbre B."""
        if self.root is None:
            return f"BTree(order={self.order}, empty)"
        
        return f"BTree(order={self.order}, size={self.size}, height={self.height})"
    
    def __repr__(self) -> str:
        """Retourne une représentation détaillée de l'arbre B."""
        return (
            f"BTree(order={self.order}, size={self.size}, "
            f"height={self.height}, root={'present' if self.root else 'None'})"
        )