"""
Classe AVLNode pour les nœuds d'arbres AVL.

Ce module implémente la classe AVLNode, spécialisée pour les arbres AVL.
Elle hérite de BinaryTreeNode et ajoute les fonctionnalités spécifiques
aux nœuds AVL (facteur d'équilibre, hauteur).
"""

from typing import Any, Optional, TYPE_CHECKING

from .binary_tree_node import BinaryTreeNode
from .exceptions import InvalidBalanceFactorError, NodeValidationError
from .interfaces import T

if TYPE_CHECKING:
    from .avl_node import AVLNode


class AVLNode(BinaryTreeNode):
    """
    Nœud spécialisé pour les arbres AVL avec facteur d'équilibre.

    Cette classe étend BinaryTreeNode pour fournir des fonctionnalités spécifiques
    aux arbres AVL, notamment le calcul et la gestion du facteur d'équilibre
    et de la hauteur.

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
        :raises CircularReferenceError: Si une référence circulaire est détectée
        :raises NodeValidationError: Si la validation du nœud échoue
        """
        super().__init__(value, parent, left, right, metadata)
        
        # Attributs spécifiques AVL
        self._height: int = 0
        self._balance_factor: int = 0
        
        # Calculer la hauteur et le facteur d'équilibre initiaux
        self.update_height()
        self.update_balance_factor()

    @property
    def height(self) -> int:
        """
        Retourne la hauteur du nœud AVL.

        :return: Hauteur du nœud
        :rtype: int
        """
        return self._height

    @property
    def balance_factor(self) -> int:
        """
        Retourne le facteur d'équilibre du nœud AVL.

        :return: Facteur d'équilibre (-1, 0, ou 1)
        :rtype: int
        """
        return self._balance_factor

    def update_height(self) -> None:
        """
        Met à jour la hauteur du nœud AVL.

        La hauteur d'un nœud AVL est calculée comme 1 + max(hauteur_gauche, hauteur_droite).
        Pour un nœud feuille, la hauteur est 0.

        :return: None
        :rtype: None
        """
        left_height = self._left.height if self._left is not None else -1
        right_height = self._right.height if self._right is not None else -1
        
        self._height = 1 + max(left_height, right_height)

    def update_balance_factor(self) -> None:
        """
        Met à jour le facteur d'équilibre du nœud AVL.

        Le facteur d'équilibre est calculé comme hauteur_droite - hauteur_gauche.
        Pour un arbre AVL valide, ce facteur doit être dans [-1, 0, 1].

        :return: None
        :rtype: None
        :raises InvalidBalanceFactorError: Si le facteur d'équilibre est invalide
        """
        left_height = self._left.height if self._left is not None else -1
        right_height = self._right.height if self._right is not None else -1
        
        self._balance_factor = right_height - left_height
        
        # Valider le facteur d'équilibre
        if abs(self._balance_factor) > 1:
            raise InvalidBalanceFactorError(
                f"Invalid balance factor: {self._balance_factor}. Must be in [-1, 0, 1]",
                self._balance_factor,
                "update_balance_factor"
            )

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

        Un nœud est équilibré si son facteur d'équilibre est dans [-1, 0, 1].

        :return: True si le nœud est équilibré, False sinon
        :rtype: bool
        """
        return abs(self._balance_factor) <= 1

    def set_left(self, node: Optional["AVLNode"]) -> None:
        """
        Définit le nœud enfant gauche et met à jour les métadonnées AVL.

        :param node: Nouveau nœud enfant gauche ou None pour supprimer
        :type node: Optional[AVLNode]
        :raises CircularReferenceError: Si la définition créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, AVLNode):
            raise InvalidNodeOperationError(
                f"Left child must be an AVLNode, got {type(node).__name__}",
                "set_left",
                self,
            )

        super().set_left(node)
        self.update_height()
        self.update_balance_factor()

    def set_right(self, node: Optional["AVLNode"]) -> None:
        """
        Définit le nœud enfant droit et met à jour les métadonnées AVL.

        :param node: Nouveau nœud enfant droit ou None pour supprimer
        :type node: Optional[AVLNode]
        :raises CircularReferenceError: Si la définition créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, AVLNode):
            raise InvalidNodeOperationError(
                f"Right child must be an AVLNode, got {type(node).__name__}",
                "set_right",
                self,
            )

        super().set_right(node)
        self.update_height()
        self.update_balance_factor()

    def get_height(self) -> int:
        """
        Retourne la hauteur du nœud AVL.

        Cette méthode surcharge la méthode de BinaryTreeNode pour utiliser
        la hauteur calculée et mise en cache.

        :return: Hauteur du nœud
        :rtype: int
        """
        return self._height

    def validate(self) -> bool:
        """
        Valide les propriétés du nœud AVL.

        Cette méthode vérifie que le nœud respecte toutes les contraintes
        d'un nœud AVL valide, y compris les propriétés de BinaryTreeNode.

        :return: True si le nœud est valide, False sinon
        :rtype: bool
        :raises NodeValidationError: Si la validation échoue
        :raises InvalidBalanceFactorError: Si le facteur d'équilibre est invalide
        """
        # Valider les propriétés de base du nœud binaire
        super().validate()

        # Vérifier que les enfants sont des AVLNode
        for child in self._children:
            if not isinstance(child, AVLNode):
                raise NodeValidationError(
                    f"All children must be AVLNode instances, got {type(child).__name__}",
                    "avl_node_children_type",
                    self,
                )

        # Vérifier que la hauteur calculée correspond à la hauteur stockée
        expected_height = super().get_height()
        if self._height != expected_height:
            raise NodeValidationError(
                f"Cached height {self._height} does not match calculated height {expected_height}",
                "avl_node_height_consistency",
                self,
            )

        # Vérifier que le facteur d'équilibre est valide
        if not self.is_balanced():
            raise InvalidBalanceFactorError(
                f"Invalid balance factor: {self._balance_factor}. Must be in [-1, 0, 1]",
                self._balance_factor,
                "validate"
            )

        return True

    def add_child(self, child: "AVLNode") -> None:
        """
        Ajoute un enfant au nœud AVL.

        Cette méthode est surchargée pour s'assurer que seuls des AVLNode
        peuvent être ajoutés comme enfants.

        :param child: Nœud enfant à ajouter
        :type child: AVLNode
        :raises CircularReferenceError: Si l'ajout créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if not isinstance(child, AVLNode):
            raise InvalidNodeOperationError(
                f"Child must be an AVLNode, got {type(child).__name__}",
                "add_child",
                self,
            )

        super().add_child(child)
        self.update_height()
        self.update_balance_factor()

    def __str__(self) -> str:
        """
        Retourne la représentation string du nœud AVL.

        :return: Représentation string du nœud AVL
        :rtype: str
        """
        return f"AVLNode(value={self._value}, height={self._height}, balance={self._balance_factor})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du nœud AVL.

        :return: Représentation détaillée du nœud AVL
        :rtype: str
        """
        return (
            f"AVLNode(value={self._value!r}, parent={self._parent}, "
            f"left={self._left}, right={self._right}, "
            f"height={self._height}, balance={self._balance_factor})"
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
            and self._height == other._height
            and self._balance_factor == other._balance_factor
        )

    def __hash__(self) -> int:
        """
        Retourne le hash du nœud AVL.

        :return: Hash du nœud AVL
        :rtype: int
        """
        return hash(
            (self._value, id(self._parent), id(self._left), id(self._right), self._height, self._balance_factor)
        )