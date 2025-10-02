"""
Classe AVLNode pour les nœuds d'arbres AVL.

Ce module implémente la classe AVLNode, spécialisée pour les arbres AVL.
Elle hérite de BinaryTreeNode et ajoute les fonctionnalités spécifiques
aux nœuds AVL (facteur d'équilibre, hauteur).
"""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from .binary_tree_node import BinaryTreeNode
from .exceptions import InvalidNodeOperationError, NodeValidationError
from .interfaces import T

if TYPE_CHECKING:
    from .avl_node import AVLNode


class AVLNode(BinaryTreeNode):
    """
    Nœud spécialisé pour les arbres AVL avec facteur d'équilibre.

    Cette classe étend BinaryTreeNode pour fournir des fonctionnalités spécifiques
    aux arbres AVL, avec gestion automatique du facteur d'équilibre et de la hauteur.

    :param value: Valeur stockée dans le nœud
    :type value: T
    :param parent: Nœud parent (optionnel)
    :type parent: Optional[AVLNode], optional
    :param left: Nœud enfant gauche (optionnel)
    :type left: Optional[AVLNode], optional
    :param right: Nœud enfant droit (optionnel)
    :type right: Optional[AVLNode], optional
    :param metadata: Dictionnaire de métadonnées (optionnel)
    :type metadata: Optional[dict], optional
    """

    def __init__(
        self,
        value: T,
        parent: Optional["AVLNode"] = None,
        left: Optional["AVLNode"] = None,
        right: Optional["AVLNode"] = None,
        metadata: Optional[dict] = None,
    ):
        """
        Initialise un nouveau nœud AVL.

        :param value: Valeur stockée dans le nœud
        :type value: T
        :param parent: Nœud parent (optionnel)
        :type parent: Optional[AVLNode], optional
        :param left: Nœud enfant gauche (optionnel)
        :type left: Optional[AVLNode], optional
        :param right: Nœud enfant droit (optionnel)
        :type right: Optional[AVLNode], optional
        :param metadata: Dictionnaire de métadonnées (optionnel)
        :type metadata: Optional[dict], optional
        :raises CircularReferenceError: Si une référence est détectée
        :raises NodeValidationError: Si la validation échoue
        """
        super().__init__(value, parent, left, right, metadata)

        # Facteur d'équilibre (différence entre hauteur droite et gauche)
        self._balance_factor: int = 0

        # Hauteur mise en cache pour optimiser les calculs
        self._cached_height: int = 0

    @property
    def balance_factor(self) -> int:
        """
        Retourne le facteur d'équilibre du nœud.

        Le facteur d'équilibre est la différence entre la hauteur du
        sous-arbre droit et la hauteur du sous-arbre gauche.

        :return: Facteur d'équilibre (-1, 0, ou 1 pour un nœud équilibré)
        :rtype: int
        """
        return self._balance_factor

    @property
    def height(self) -> int:
        """
        Retourne la hauteur mise en cache du nœud.

        :return: Hauteur du nœud
        :rtype: int
        """
        return self._cached_height

    def update_balance_factor(self) -> None:
        """
        Met à jour le facteur d'équilibre du nœud.

        Le facteur d'équilibre est calculé comme la différence entre
        la hauteur du sous-arbre droit et la hauteur du sous-arbre gauche.

        :return: None
        :rtype: None
        """
        left_height = self._left.get_height() if self._left is not None else -1
        right_height = self._right.get_height() if self._right is not None else -1

        self._balance_factor = right_height - left_height

    def update_height(self) -> None:
        """
        Met à jour la hauteur mise en cache du nœud.

        La hauteur est calculée comme 1 + max(hauteur_gauche, hauteur_droite).

        :return: None
        :rtype: None
        """
        if self.is_leaf():
            self._cached_height = 0
        else:
            left_height = self._left.get_height() if self._left is not None else -1
            right_height = self._right.get_height() if self._right is not None else -1
            self._cached_height = 1 + max(left_height, right_height)

    def is_left_heavy(self) -> bool:
        """
        Vérifie si le nœud penche à gauche.

        Un nœud penche à gauche si son facteur d'équilibre est négatif.

        :return: True si le nœud penche à gauche, False sinon
        :rtype: bool
        """
        return self._balance_factor < 0

    def is_right_heavy(self) -> bool:
        """
        Vérifie si le nœud penche à droite.

        Un nœud penche à droite si son facteur d'équilibre est positif.

        :return: True si le nœud penche à droite, False sinon
        :rtype: bool
        """
        return self._balance_factor > 0

    def is_balanced(self) -> bool:
        """
        Vérifie si le nœud est équilibré.

        Un nœud est équilibré si son facteur d'équilibre est -1, 0, ou 1.

        :return: True si le nœud est équilibré, False sinon
        :rtype: bool
        """
        return abs(self._balance_factor) <= 1

    def set_left(self, node: Optional["AVLNode"]) -> None:
        """
        Définit le nœud enfant gauche et met à jour les métadonnées AVL.

        :param node: Nouveau nœud enfant gauche ou None pour supprimer
        :type node: Optional[AVLNode]
        :raises CircularReferenceError: Si la définition créerait une référence
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, AVLNode):
            raise InvalidNodeOperationError(
                f"Left child must be an AVLNode, got {type(node).__name__}",
                "set_left",
                self,
            )

        super().set_left(node)
        self._update_avl_metadata()

    def set_right(self, node: Optional["AVLNode"]) -> None:
        """
        Définit le nœud enfant droit et met à jour les métadonnées AVL.

        :param node: Nouveau nœud enfant droit ou None pour supprimer
        :type node: Optional[AVLNode]
        :raises CircularReferenceError: Si la définition créerait une référence
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, AVLNode):
            raise InvalidNodeOperationError(
                f"Right child must be an AVLNode, got {type(node).__name__}",
                "set_right",
                self,
            )

        super().set_right(node)
        self._update_avl_metadata()

    def _update_avl_metadata(self) -> None:
        """
        Met à jour les métadonnées AVL (hauteur et facteur d'équilibre).

        :return: None
        :rtype: None
        """
        self.update_height()
        self.update_balance_factor()

    def get_height(self) -> int:
        """
        Calcule la hauteur du nœud AVL.

        Cette méthode surcharge la méthode parente pour utiliser la hauteur
        mise en cache et la mettre à jour si nécessaire.

        :return: Hauteur du nœud
        :rtype: int
        """
        # Mettre à jour la hauteur si nécessaire
        self.update_height()
        return self._cached_height

    def validate(self) -> bool:
        """
        Valide les propriétés du nœud AVL.

        Cette méthode vérifie que le nœud respecte toutes les contraintes
        d'un nœud AVL valide, y compris les propriétés BST et AVL.

        :return: True si le nœud est valide, False sinon
        :rtype: bool
        :raises NodeValidationError: Si la validation échoue
        """
        # Valider les propriétés BST de base
        super().validate()

        # Vérifier que les enfants sont des AVLNode
        for child in self._children:
            if not isinstance(child, AVLNode):
                raise NodeValidationError(
                    f"All children must be AVLNode instances, got {type(child).__name__}",
                    "avl_node_children_type",
                    self,
                )

        # Vérifier que le facteur d'équilibre est valide
        if not self.is_balanced():
            raise NodeValidationError(
                f"AVL node balance factor must be -1, 0, or 1, got {self._balance_factor}",
                "avl_node_balance_factor",
                self,
            )

        # Vérifier que la hauteur mise en cache est cohérente
        expected_height = super().get_height()
        if self._cached_height != expected_height:
            raise NodeValidationError(
                f"Cached height {self._cached_height} does not match calculated height {expected_height}",
                "avl_node_height_consistency",
                self,
            )

        return True

    def add_child(self, child: "AVLNode") -> None:
        """
        Ajoute un enfant au nœud AVL.

        Cette méthode est surchargée pour s'assurer que seuls des AVLNode
        peuvent être ajoutés comme enfants.

        :param child: Nœud enfant à ajouter
        :type child: AVLNode
        :raises CircularReferenceError: Si l'ajout créerait une référence
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if not isinstance(child, AVLNode):
            raise InvalidNodeOperationError(
                f"Child must be an AVLNode, got {type(child).__name__}",
                "add_child",
                self,
            )

        super().add_child(child)
        self._update_avl_metadata()

    def __str__(self) -> str:
        """
        Retourne la représentation string du nœud AVL.

        :return: Représentation string du nœud AVL
        :rtype: str
        """
        return f"AVLNode(value={self._value}, balance={self._balance_factor}, height={self._cached_height})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du nœud AVL.

        :return: Représentation détaillée du nœud AVL
        :rtype: str
        """
        return (
            f"AVLNode(value={self._value!r}, parent={self._parent}, "
            f"left={self._left}, right={self._right}, "
            f"balance={self._balance_factor}, height={self._cached_height})"
        )

    def __eq__(self, other: Any) -> bool:
        """
        Teste l'égalité entre deux nœuds AVL.

        :param other: Autre objet à comparer
        :type other: Any
        :return: True si les nœuds sont égaux, False sinon
        :rtype: bool
        """
        if not isinstance(other, AVLNode):
            return False

        return (
            self._value == other._value
            and self._parent is other._parent
            and self._left is other._left
            and self._right is other._right
            and self._balance_factor == other._balance_factor
            and self._cached_height == other._cached_height
        )

    def __hash__(self) -> int:
        """
        Retourne le hash du nœud AVL.

        :return: Hash du nœud AVL
        :rtype: int
        """
        return hash(
            (
                self._value,
                id(self._parent),
                id(self._left),
                id(self._right),
                self._balance_factor,
                self._cached_height,
            )
        )
