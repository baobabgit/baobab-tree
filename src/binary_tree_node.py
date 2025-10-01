"""
Classe BinaryTreeNode pour les arbres binaires.

Ce module implémente la classe BinaryTreeNode, spécialisée pour les arbres
binaires. Elle hérite de TreeNode et ajoute les fonctionnalités spécifiques
aux nœuds binaires (gauche/droite).
"""

from typing import Any, List, Optional, TYPE_CHECKING

from .exceptions import InvalidNodeOperationError, NodeValidationError
from .interfaces import T
from .tree_node import TreeNode

if TYPE_CHECKING:
    from .binary_tree_node import BinaryTreeNode


class BinaryTreeNode(TreeNode):
    """
    Nœud spécialisé pour les arbres binaires.

    Cette classe étend TreeNode pour fournir des fonctionnalités spécifiques
    aux arbres binaires, avec des enfants gauche et droit explicites.

    :param value: Valeur stockée dans le nœud
    :type value: T
    :param parent: Nœud parent (optionnel)
    :type parent: Optional[BinaryTreeNode], optional
    :param left: Nœud enfant gauche (optionnel)
    :type left: Optional[BinaryTreeNode], optional
    :param right: Nœud enfant droit (optionnel)
    :type right: Optional[BinaryTreeNode], optional
    :param metadata: Dictionnaire de métadonnées (optionnel)
    :type metadata: Optional[dict], optional
    """

    def __init__(
        self,
        value: T,
        parent: Optional["BinaryTreeNode"] = None,
        left: Optional["BinaryTreeNode"] = None,
        right: Optional["BinaryTreeNode"] = None,
        metadata: Optional[dict] = None,
    ):
        """
        Initialise un nouveau nœud d'arbre binaire.

        :param value: Valeur stockée dans le nœud
        :type value: T
        :param parent: Nœud parent (optionnel)
        :type parent: Optional[BinaryTreeNode], optional
        :param left: Nœud enfant gauche (optionnel)
        :type left: Optional[BinaryTreeNode], optional
        :param right: Nœud enfant droit (optionnel)
        :type right: Optional[BinaryTreeNode], optional
        :param metadata: Dictionnaire de métadonnées (optionnel)
        :type metadata: Optional[dict], optional
        :raises CircularReferenceError: Si une référence circulaire est détectée
        :raises NodeValidationError: Si la validation du nœud échoue
        """
        # Initialiser sans enfants d'abord
        super().__init__(value, parent, [], metadata)

        # Définir les enfants gauche et droit après initialisation
        self._left = None
        self._right = None

        if left is not None:
            self.set_left(left)
        if right is not None:
            self.set_right(right)

    @property
    def left(self) -> Optional["BinaryTreeNode"]:
        """
        Retourne le nœud enfant gauche.

        :return: Nœud enfant gauche ou None
        :rtype: Optional[BinaryTreeNode]
        """
        return self._left

    @property
    def right(self) -> Optional["BinaryTreeNode"]:
        """
        Retourne le nœud enfant droit.

        :return: Nœud enfant droit ou None
        :rtype: Optional[BinaryTreeNode]
        """
        return self._right

    def set_left(self, node: Optional["BinaryTreeNode"]) -> None:
        """
        Définit le nœud enfant gauche.

        :param node: Nouveau nœud enfant gauche ou None pour supprimer
        :type node: Optional[BinaryTreeNode]
        :raises CircularReferenceError: Si la définition créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, BinaryTreeNode):
            raise InvalidNodeOperationError(
                f"Left child must be a BinaryTreeNode, got {type(node).__name__}",
                "set_left",
                self,
            )

        # Retirer l'ancien enfant gauche
        if self._left is not None:
            self.remove_child(self._left)

        # Définir le nouveau enfant gauche
        self._left = node
        if node is not None:
            self.add_child(node)

    def set_right(self, node: Optional["BinaryTreeNode"]) -> None:
        """
        Définit le nœud enfant droit.

        :param node: Nouveau nœud enfant droit ou None pour supprimer
        :type node: Optional[BinaryTreeNode]
        :raises CircularReferenceError: Si la définition créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, BinaryTreeNode):
            raise InvalidNodeOperationError(
                f"Right child must be a BinaryTreeNode, got {type(node).__name__}",
                "set_right",
                self,
            )

        # Retirer l'ancien enfant droit
        if self._right is not None:
            self.remove_child(self._right)

        # Définir le nouveau enfant droit
        self._right = node
        if node is not None:
            self.add_child(node)

    def get_left(self) -> Optional["BinaryTreeNode"]:
        """
        Retourne le nœud enfant gauche.

        :return: Nœud enfant gauche ou None
        :rtype: Optional[BinaryTreeNode]
        """
        return self._left

    def get_right(self) -> Optional["BinaryTreeNode"]:
        """
        Retourne le nœud enfant droit.

        :return: Nœud enfant droit ou None
        :rtype: Optional[BinaryTreeNode]
        """
        return self._right

    def has_left(self) -> bool:
        """
        Vérifie la présence d'un enfant gauche.

        :return: True si le nœud a un enfant gauche, False sinon
        :rtype: bool
        """
        return self._left is not None

    def has_right(self) -> bool:
        """
        Vérifie la présence d'un enfant droit.

        :return: True si le nœud a un enfant droit, False sinon
        :rtype: bool
        """
        return self._right is not None

    def is_leaf(self) -> bool:
        """
        Vérifie si le nœud est une feuille (n'a pas d'enfants).

        :return: True si le nœud est une feuille, False sinon
        :rtype: bool
        """
        return self._left is None and self._right is None

    def is_root(self) -> bool:
        """
        Vérifie si le nœud est la racine (n'a pas de parent).

        :return: True si le nœud est la racine, False sinon
        :rtype: bool
        """
        return self._parent is None

    def get_height(self) -> int:
        """
        Calcule la hauteur du nœud.

        La hauteur d'un nœud est la longueur du chemin le plus long
        de ce nœud vers une feuille.

        :return: Hauteur du nœud
        :rtype: int
        """
        if self.is_leaf():
            return 0

        left_height = self._left.get_height() if self._left is not None else -1
        right_height = (
            self._right.get_height() if self._right is not None else -1
        )

        return 1 + max(left_height, right_height)

    def get_depth(self) -> int:
        """
        Calcule la profondeur du nœud.

        La profondeur d'un nœud est la longueur du chemin de la racine
        vers ce nœud.

        :return: Profondeur du nœud
        :rtype: int
        """
        if self.is_root():
            return 0

        return 1 + self._parent.get_depth()

    def validate(self) -> bool:
        """
        Valide les propriétés du nœud binaire.

        Cette méthode vérifie que le nœud respecte toutes les contraintes
        d'un nœud binaire valide.

        :return: True si le nœud est valide, False sinon
        :rtype: bool
        :raises NodeValidationError: Si la validation échoue
        """
        # Vérifier que les enfants sont des BinaryTreeNode
        for child in self._children:
            if not isinstance(child, BinaryTreeNode):
                raise NodeValidationError(
                    f"All children must be BinaryTreeNode instances, got {type(child).__name__}",
                    "binary_tree_node_children_type",
                    self,
                )

        # Vérifier que les enfants gauche et droit correspondent aux enfants
        expected_children = []
        if self._left is not None:
            expected_children.append(self._left)
        if self._right is not None:
            expected_children.append(self._right)

        if set(self._children) != set(expected_children):
            raise NodeValidationError(
                "Children list does not match left and right children",
                "binary_tree_node_children_consistency",
                self,
            )

        # Vérifier qu'il n'y a pas plus de 2 enfants
        if len(self._children) > 2:
            raise NodeValidationError(
                f"Binary tree node cannot have more than 2 children, got {len(self._children)}",
                "binary_tree_node_max_children",
                self,
            )

        # Vérifier que les enfants ont ce nœud comme parent
        for child in self._children:
            if child.parent is not self:
                raise NodeValidationError(
                    "Child does not have this node as parent",
                    "binary_tree_node_parent_consistency",
                    self,
                )

        return True

    def get_children(self) -> List["BinaryTreeNode"]:
        """
        Retourne la liste des nœuds enfants.

        :return: Liste des nœuds enfants (gauche, puis droite si présente)
        :rtype: List[BinaryTreeNode]
        """
        children = []
        if self._left is not None:
            children.append(self._left)
        if self._right is not None:
            children.append(self._right)
        return children

    def add_child(self, child: "BinaryTreeNode") -> None:
        """
        Ajoute un enfant au nœud binaire.

        Cette méthode est surchargée pour s'assurer que seuls des BinaryTreeNode
        peuvent être ajoutés comme enfants.

        :param child: Nœud enfant à ajouter
        :type child: BinaryTreeNode
        :raises CircularReferenceError: Si l'ajout créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if not isinstance(child, BinaryTreeNode):
            raise InvalidNodeOperationError(
                f"Child must be a BinaryTreeNode, got {type(child).__name__}",
                "add_child",
                self,
            )

        # Si on a déjà 2 enfants, on ne peut pas en ajouter d'autres
        if len(self._children) >= 2:
            raise InvalidNodeOperationError(
                "Binary tree node cannot have more than 2 children",
                "add_child",
                self,
            )

        super().add_child(child)

    def __str__(self) -> str:
        """
        Retourne la représentation string du nœud binaire.

        :return: Représentation string du nœud binaire
        :rtype: str
        """
        return f"BinaryTreeNode(value={self._value})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du nœud binaire.

        :return: Représentation détaillée du nœud binaire
        :rtype: str
        """
        return (
            f"BinaryTreeNode(value={self._value!r}, parent={self._parent}, "
            f"left={self._left}, right={self._right})"
        )

    def __eq__(self, other: Any) -> bool:
        """
        Teste l'égalité entre deux nœuds binaires.

        :param other: Autre objet à comparer
        :type other: Any
        :return: True si les nœuds sont égaux, False sinon
        :rtype: bool
        """
        if not isinstance(other, BinaryTreeNode):
            return False

        return (
            self._value == other._value
            and self._parent is other._parent
            and self._left is other._left
            and self._right is other._right
        )

    def __hash__(self) -> int:
        """
        Retourne le hash du nœud binaire.

        :return: Hash du nœud binaire
        :rtype: int
        """
        return hash(
            (self._value, id(self._parent), id(self._left), id(self._right))
        )
