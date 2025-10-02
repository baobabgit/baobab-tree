#!/usr/bin/env python3
"""
Version autonome des classes B-tree pour éviter les problèmes d'import.
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


class NodeUnderflowError(BTreeError):
    """Exception levée lors d'un nœud avec trop peu de clés."""
    
    def __init__(self, message: str, node, key_count: int, minimum_required: int):
        super().__init__(message, "underflow_check", node)
        self.key_count = key_count
        self.minimum_required = minimum_required
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        return f"{base_msg} (Current: {self.key_count}, Required: {self.minimum_required})"


class SplitError(BTreeError):
    """Exception levée lors d'une erreur de division d'un nœud."""
    
    def __init__(self, message: str, node, reason: str):
        super().__init__(message, "node_split", node)
        self.reason = reason
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        return f"{base_msg} (Reason: {self.reason})"


class MergeError(BTreeError):
    """Exception levée lors d'une erreur de fusion de nœuds."""
    
    def __init__(self, message: str, node1, node2, reason: str):
        super().__init__(message, "node_merge", node1)
        self.node2 = node2
        self.reason = reason
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        return f"{base_msg} (Node2: {self.node2}, Reason: {self.reason})"


class RedistributionError(BTreeError):
    """Exception levée lors d'une erreur de redistribution des clés."""
    
    def __init__(self, message: str, source_node, target_node, reason: str):
        super().__init__(message, "key_redistribution", source_node)
        self.target_node = target_node
        self.reason = reason
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        return f"{base_msg} (Target: {self.target_node}, Reason: {self.reason})"


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
            raise SplitError(
                "Impossible de diviser un nœud qui n'est pas plein",
                self,
                "node_not_full",
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
        """Supprime une clé de l'arbre B."""
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
    
    def _delete_key(self, node: BTreeNode, key: Any) -> bool:
        """Supprime une clé d'un nœud."""
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
    
    def _delete_internal_key(self, node: BTreeNode, key_index: int) -> bool:
        """Supprime une clé d'un nœud interne."""
        if key_index >= len(node.children) - 1:
            # Pas d'enfant droit, utiliser seulement l'enfant gauche
            left_child = node.children[key_index]
            if left_child is None:
                raise BTreeError(
                    f"Enfant manquant pour la suppression interne à l'index {key_index}",
                    "delete_internal_key",
                    node,
                )
            
            # Supprimer la clé et utiliser le prédécesseur
            predecessor = self._get_predecessor(left_child)
            node.keys[key_index] = predecessor
            return self._delete_key(left_child, predecessor)
        
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
    
    def _get_predecessor(self, node: BTreeNode) -> Any:
        """Retourne le prédécesseur d'un nœud."""
        while not node.is_leaf:
            node = node.children[-1]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du prédécesseur", "get_predecessor")
        return node.keys[-1]
    
    def _get_successor(self, node: BTreeNode) -> Any:
        """Retourne le successeur d'un nœud."""
        while not node.is_leaf:
            node = node.children[0]
            if node is None:
                raise BTreeError("Enfant manquant lors de la recherche du successeur", "get_successor")
        return node.keys[0]
    
    def _ensure_minimum_keys(self, parent: BTreeNode, child_index: int) -> None:
        """Garantit qu'un enfant a au moins le minimum de clés."""
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
    
    def _merge_children(self, parent: BTreeNode, key_index: int) -> None:
        """Fusionne deux enfants d'un nœud parent."""
        if key_index >= len(parent.children) - 1:
            # Pas d'enfant droit, fusionner avec l'enfant gauche précédent
            if key_index > 0:
                left_child = parent.children[key_index - 1]
                right_child = parent.children[key_index]
                separator_key = parent.keys[key_index - 1]
                
                if left_child is None or right_child is None:
                    raise BTreeError(
                        f"Enfant manquant pour la fusion à l'index {key_index}",
                        "merge_children",
                        parent,
                    )
                
                left_child.merge_with(right_child, separator_key)
                parent.keys.pop(key_index - 1)
                parent.children.pop(key_index)
            else:
                raise BTreeError(
                    f"Impossible de fusionner à l'index {key_index}",
                    "merge_children",
                    parent,
                )
        else:
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


# Ajouter les méthodes manquantes à BTreeNode
def borrow_from_left(self) -> bool:
    """Emprunte une clé au nœud frère gauche."""
    if self.parent is None:
        return False
    
    # Trouver l'index de ce nœud dans les enfants du parent
    parent_index = self.parent.children.index(self)
    if parent_index == 0:  # Pas de frère gauche
        return False
    
    left_sibling = self.parent.children[parent_index - 1]
    if left_sibling is None or left_sibling.is_minimum():
        return False
    
    # Emprunter la dernière clé du frère gauche
    borrowed_key = left_sibling.keys.pop()
    separator_key = self.parent.keys[parent_index - 1]
    
    # Insérer la clé séparatrice dans ce nœud
    self.keys.insert(0, separator_key)
    
    # Mettre à jour la clé séparatrice dans le parent
    self.parent.keys[parent_index - 1] = borrowed_key
    
    # Gérer les enfants si nécessaire
    if not self.is_leaf:
        borrowed_child = left_sibling.children.pop()
        if borrowed_child is not None:
            borrowed_child.parent = self
        self.children.insert(0, borrowed_child)
    
    return True


def borrow_from_right(self) -> bool:
    """Emprunte une clé au nœud frère droit."""
    if self.parent is None:
        return False
    
    # Trouver l'index de ce nœud dans les enfants du parent
    parent_index = self.parent.children.index(self)
    if parent_index >= len(self.parent.children) - 1:  # Pas de frère droit
        return False
    
    right_sibling = self.parent.children[parent_index + 1]
    if right_sibling is None or right_sibling.is_minimum():
        return False
    
    # Emprunter la première clé du frère droit
    borrowed_key = right_sibling.keys.pop(0)
    separator_key = self.parent.keys[parent_index]
    
    # Ajouter la clé séparatrice à ce nœud
    self.keys.append(separator_key)
    
    # Mettre à jour la clé séparatrice dans le parent
    self.parent.keys[parent_index] = borrowed_key
    
    # Gérer les enfants si nécessaire
    if not self.is_leaf:
        borrowed_child = right_sibling.children.pop(0)
        if borrowed_child is not None:
            borrowed_child.parent = self
        self.children.append(borrowed_child)
    
    return True


def merge_with(self, other: 'BTreeNode', separator_key: Any) -> None:
    """Fusionne ce nœud avec un autre nœud."""
    if self.parent != other.parent:
        raise MergeError(
            "Impossible de fusionner des nœuds avec des parents différents",
            self,
            other,
            "different_parents",
        )
    
    if len(self.keys) + len(other.keys) + 1 > 2 * self.order - 1:
        raise MergeError(
            "Impossible de fusionner: résultat dépasserait la capacité maximale",
            self,
            other,
            "capacity_exceeded",
        )
    
    # Ajouter la clé séparatrice et les clés de l'autre nœud
    self.keys.append(separator_key)
    self.keys.extend(other.keys)
    
    # Fusionner les enfants si nécessaire
    if not self.is_leaf:
        self.children.extend(other.children)
        # Mettre à jour les références parent
        for child in other.children:
            if child is not None:
                child.parent = self


# Ajouter les méthodes à la classe BTreeNode
BTreeNode.borrow_from_left = borrow_from_left
BTreeNode.borrow_from_right = borrow_from_right
BTreeNode.merge_with = merge_with