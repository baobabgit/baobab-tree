"""
Classe abstraite TreeNode pour la librairie d'arbres.

Ce module implémente la classe TreeNode, classe abstraite de base pour tous
les nœuds d'arbres dans la librairie. Cette classe fournit les fonctionnalités
communes à tous les types de nœuds.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TYPE_CHECKING

from .exceptions import (
    CircularReferenceError,
    InvalidNodeOperationError,
    NodeValidationError,
)
from .interfaces import T

if TYPE_CHECKING:
    from .tree_node import TreeNode


class TreeNode(ABC, Generic[T]):
    """
    Classe abstraite de base pour tous les nœuds d'arbres.

    Cette classe définit l'interface commune pour tous les nœuds d'arbres
    dans la librairie. Elle fournit les fonctionnalités de base pour la
    gestion des relations parent-enfant et des métadonnées.

    :param value: Valeur stockée dans le nœud
    :type value: T
    :param parent: Nœud parent (optionnel)
    :type parent: Optional[TreeNode], optional
    :param children: Liste des nœuds enfants (optionnel)
    :type children: Optional[List[TreeNode]], optional
    :param metadata: Dictionnaire de métadonnées (optionnel)
    :type metadata: Optional[dict], optional
    """

    def __init__(
        self,
        value: T,
        parent: Optional["TreeNode"] = None,
        children: Optional[List["TreeNode"]] = None,
        metadata: Optional[dict] = None,
    ):
        """
        Initialise un nouveau nœud d'arbre.

        :param value: Valeur stockée dans le nœud
        :type value: T
        :param parent: Nœud parent (optionnel)
        :type parent: Optional[TreeNode], optional
        :param children: Liste des nœuds enfants (optionnel)
        :type children: Optional[List[TreeNode]], optional
        :param metadata: Dictionnaire de métadonnées (optionnel)
        :type metadata: Optional[dict], optional
        :raises CircularReferenceError: Si une référence circulaire est détectée
        :raises NodeValidationError: Si la validation du nœud échoue
        """
        self._value = value
        self._parent = None
        self._children = children or []
        self._metadata = metadata or {}

        # Définir le parent après initialisation pour éviter les références circulaires
        if parent is not None:
            self.set_parent(parent)

    @property
    def value(self) -> T:
        """
        Retourne la valeur stockée dans le nœud.

        :return: Valeur du nœud
        :rtype: T
        """
        return self._value

    @value.setter
    def value(self, new_value: T) -> None:
        """
        Définit la valeur du nœud.

        :param new_value: Nouvelle valeur pour le nœud
        :type new_value: T
        """
        self._value = new_value

    @property
    def parent(self) -> Optional["TreeNode"]:
        """
        Retourne le nœud parent.

        :return: Nœud parent ou None si pas de parent
        :rtype: Optional[TreeNode]
        """
        return self._parent

    @property
    def children(self) -> List["TreeNode"]:
        """
        Retourne la liste des nœuds enfants.

        :return: Liste des nœuds enfants
        :rtype: List[TreeNode]
        """
        return self._children.copy()

    @property
    def metadata(self) -> dict:
        """
        Retourne le dictionnaire des métadonnées.

        :return: Dictionnaire des métadonnées
        :rtype: dict
        """
        return self._metadata.copy()

    @abstractmethod
    def is_leaf(self) -> bool:
        """
        Vérifie si le nœud est une feuille (n'a pas d'enfants).

        :return: True si le nœud est une feuille, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_root(self) -> bool:
        """
        Vérifie si le nœud est la racine (n'a pas de parent).

        :return: True si le nœud est la racine, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_height(self) -> int:
        """
        Calcule la hauteur du nœud.

        La hauteur d'un nœud est la longueur du chemin le plus long
        de ce nœud vers une feuille.

        :return: Hauteur du nœud
        :rtype: int
        """
        pass

    @abstractmethod
    def get_depth(self) -> int:
        """
        Calcule la profondeur du nœud.

        La profondeur d'un nœud est la longueur du chemin de la racine
        vers ce nœud.

        :return: Profondeur du nœud
        :rtype: int
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Valide les propriétés du nœud.

        Cette méthode vérifie que le nœud respecte toutes les contraintes
        de sa structure et de ses relations.

        :return: True si le nœud est valide, False sinon
        :rtype: bool
        :raises NodeValidationError: Si la validation échoue
        """
        pass

    def add_child(self, child: "TreeNode") -> None:
        """
        Ajoute un enfant au nœud.

        :param child: Nœud enfant à ajouter
        :type child: TreeNode
        :raises CircularReferenceError: Si l'ajout créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if child is None:
            raise InvalidNodeOperationError(
                "Cannot add None as child", "add_child", self
            )

        if child is self:
            raise CircularReferenceError(
                "Cannot add node as its own child", self, child
            )

        # Vérifier les références circulaires
        if self._would_create_circular_reference(child):
            raise CircularReferenceError(
                "Adding this child would create a circular reference",
                self,
                child,
            )

        # Retirer l'enfant de son parent actuel s'il en a un
        if child.parent is not None:
            child.parent.remove_child(child)

        # Ajouter l'enfant
        self._children.append(child)
        child._parent = self

    def remove_child(self, child: "TreeNode") -> bool:
        """
        Supprime un enfant du nœud.

        :param child: Nœud enfant à supprimer
        :type child: TreeNode
        :return: True si l'enfant a été supprimé, False s'il n'était pas présent
        :rtype: bool
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if child is None:
            raise InvalidNodeOperationError(
                "Cannot remove None child", "remove_child", self
            )

        if child not in self._children:
            return False

        self._children.remove(child)
        child._parent = None
        return True

    def get_children(self) -> List["TreeNode"]:
        """
        Retourne la liste des nœuds enfants.

        :return: Copie de la liste des nœuds enfants
        :rtype: List[TreeNode]
        """
        return self._children.copy()

    def get_parent(self) -> Optional["TreeNode"]:
        """
        Retourne le nœud parent.

        :return: Nœud parent ou None si pas de parent
        :rtype: Optional[TreeNode]
        """
        return self._parent

    def set_parent(self, parent: Optional["TreeNode"]) -> None:
        """
        Définit le nœud parent.

        :param parent: Nouveau nœud parent ou None pour supprimer le parent
        :type parent: Optional[TreeNode]
        :raises CircularReferenceError: Si la définition créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if parent is self:
            raise CircularReferenceError(
                "Cannot set node as its own parent", self, parent
            )

        if parent is not None and self._would_create_circular_reference(parent):
            raise CircularReferenceError(
                "Setting this parent would create a circular reference",
                self,
                parent,
            )

        # Retirer ce nœud de son parent actuel
        if self._parent is not None:
            self._parent.remove_child(self)

        # Définir le nouveau parent
        self._parent = parent
        if parent is not None:
            parent._children.append(self)

    def clear_metadata(self) -> None:
        """
        Efface toutes les métadonnées du nœud.

        :return: None
        :rtype: None
        """
        self._metadata.clear()

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Définit une métadonnée pour le nœud.

        :param key: Clé de la métadonnée
        :type key: str
        :param value: Valeur de la métadonnée
        :type value: Any
        :raises InvalidNodeOperationError: Si la clé est invalide
        """
        if not isinstance(key, str):
            raise InvalidNodeOperationError(
                f"Metadata key must be a string, got {type(key).__name__}",
                "set_metadata",
                self,
            )

        self._metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Récupère une métadonnée du nœud.

        :param key: Clé de la métadonnée
        :type key: str
        :param default: Valeur par défaut si la clé n'existe pas
        :type default: Any, optional
        :return: Valeur de la métadonnée ou valeur par défaut
        :rtype: Any
        """
        return self._metadata.get(key, default)

    def _would_create_circular_reference(self, node: "TreeNode") -> bool:
        """
        Vérifie si l'ajout d'un nœud créerait une référence circulaire.

        :param node: Nœud à vérifier
        :type node: TreeNode
        :return: True si une référence circulaire serait créée, False sinon
        :rtype: bool
        """
        # Vérifier si le nœud est un ancêtre de self
        current = self
        while current is not None:
            if current is node:
                return True
            current = current.parent

        # Vérifier si self est un ancêtre du nœud
        current = node
        while current is not None:
            if current is self:
                return True
            current = current.parent

        return False

    def __str__(self) -> str:
        """
        Retourne la représentation string du nœud.

        :return: Représentation string du nœud
        :rtype: str
        """
        return f"TreeNode(value={self._value})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du nœud.

        :return: Représentation détaillée du nœud
        :rtype: str
        """
        return f"TreeNode(value={self._value!r}, parent={self._parent}, children_count={len(self._children)})"

    def __eq__(self, other: Any) -> bool:
        """
        Teste l'égalité entre deux nœuds.

        :param other: Autre objet à comparer
        :type other: Any
        :return: True si les nœuds sont égaux, False sinon
        :rtype: bool
        """
        if not isinstance(other, TreeNode):
            return False

        return (
            self._value == other._value
            and self._parent is other._parent
            and self._children == other._children
        )

    def __hash__(self) -> int:
        """
        Retourne le hash du nœud.

        :return: Hash du nœud
        :rtype: int
        """
        return hash(
            (
                self._value,
                id(self._parent),
                tuple(id(child) for child in self._children),
            )
        )
