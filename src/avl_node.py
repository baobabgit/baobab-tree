"""
Classe AVLNode pour les nœuds d'arbres AVL.

Ce module implémente la classe AVLNode, spécialisée pour les arbres AVL.
Elle hérite de BinaryTreeNode et ajoute les fonctionnalités spécifiques
aux nœuds AVL (facteur d'équilibre, hauteur).
"""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from .binary_tree_node import BinaryTreeNode
from .exceptions import (
    AVLNodeError,
    HeightCalculationError,
    HeightMismatchError,
    InvalidBalanceFactorError,
    InvalidNodeOperationError,
    NodeValidationError,
)
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

        # Mettre à jour les métadonnées AVL après initialisation
        self._update_avl_metadata()

    @classmethod
    def from_copy(cls, other: "AVLNode[T]") -> "AVLNode[T]":
        """
        Crée une copie profonde d'un nœud AVL.

        :param other: Nœud AVL à copier
        :type other: AVLNode[T]
        :return: Nouveau nœud AVL copié
        :rtype: AVLNode[T]
        :raises AVLNodeError: Si la copie échoue
        """
        if not isinstance(other, AVLNode):
            raise AVLNodeError(
                f"Cannot copy non-AVLNode: {type(other).__name__}",
                "from_copy",
                other,
            )

        # Créer le nouveau nœud avec la même valeur
        new_node = cls(other._value, metadata=other._metadata.copy() if other._metadata else None)

        # Copier les propriétés AVL
        new_node._balance_factor = other._balance_factor
        new_node._cached_height = other._cached_height

        # Copier récursivement les enfants
        if other._left is not None:
            new_left = cls.from_copy(other._left)
            new_node.set_left(new_left)

        if other._right is not None:
            new_right = cls.from_copy(other._right)
            new_node.set_right(new_right)

        return new_node

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

    def get_balance_factor(self) -> int:
        """
        Retourne le facteur d'équilibre du nœud.

        :return: Facteur d'équilibre (-1, 0, ou 1 pour un nœud équilibré)
        :rtype: int
        """
        return self._balance_factor

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

    def get_left_height(self) -> int:
        """
        Retourne la hauteur du sous-arbre gauche.

        :return: Hauteur du sous-arbre gauche (-1 si pas d'enfant gauche)
        :rtype: int
        """
        if self._left is None:
            return -1
        return self._left._cached_height

    def get_right_height(self) -> int:
        """
        Retourne la hauteur du sous-arbre droit.

        :return: Hauteur du sous-arbre droit (-1 si pas d'enfant droit)
        :rtype: int
        """
        if self._right is None:
            return -1
        return self._right._cached_height

    def update_balance_factor(self) -> None:
        """
        Met à jour le facteur d'équilibre du nœud.

        Le facteur d'équilibre est calculé comme la différence entre
        la hauteur du sous-arbre droit et la hauteur du sous-arbre gauche.

        :return: None
        :rtype: None
        """
        left_height = self._left._cached_height if self._left is not None else -1
        right_height = self._right._cached_height if self._right is not None else -1

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
            left_height = self._left._cached_height if self._left is not None else -1
            right_height = self._right._cached_height if self._right is not None else -1
            self._cached_height = 1 + max(left_height, right_height)

    def update_all(self) -> None:
        """
        Met à jour toutes les propriétés AVL du nœud.

        Cette méthode met à jour la hauteur, le facteur d'équilibre et valide
        les propriétés AVL du nœud.

        :return: None
        :rtype: None
        :raises HeightCalculationError: Si le calcul de hauteur échoue
        :raises InvalidBalanceFactorError: Si le facteur d'équilibre est invalide
        """
        try:
            # Mettre à jour les hauteurs
            self.update_height()
            
            # Mettre à jour le facteur d'équilibre
            self.update_balance_factor()
            
            # Valider les propriétés AVL
            if not self.is_balanced():
                raise InvalidBalanceFactorError(
                    f"Balance factor {self._balance_factor} is not in valid range [-1, 1]",
                    self._balance_factor,
                    self,
                )
                
        except Exception as e:
            if isinstance(e, InvalidBalanceFactorError):
                raise
            raise HeightCalculationError(
                f"Failed to update AVL properties: {str(e)}",
                self,
            ) from e

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
        self._update_ancestors_metadata()

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
        self._update_ancestors_metadata()

    def _update_avl_metadata(self) -> None:
        """
        Met à jour les métadonnées AVL (hauteur et facteur d'équilibre).

        :return: None
        :rtype: None
        """
        self.update_height()
        self.update_balance_factor()

    def _update_ancestors_metadata(self) -> None:
        """
        Met à jour les métadonnées AVL pour tous les ancêtres.

        :return: None
        :rtype: None
        """
        current = self.parent
        while current is not None:
            current._update_avl_metadata()
            current = current.parent

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

    def is_avl_valid(self) -> bool:
        """
        Valide que le nœud respecte les propriétés AVL.

        Cette méthode vérifie récursivement que tous les nœuds du sous-arbre
        respectent les propriétés AVL.

        :return: True si le nœud est valide AVL, False sinon
        :rtype: bool
        """
        try:
            # Vérifier que balance_factor est dans [-1, 1]
            if not self.is_balanced():
                return False

            # Vérifier que height est cohérent
            if not self.validate_heights():
                return False

            # Vérifier récursivement les enfants
            if self._left is not None and not self._left.is_avl_valid():
                return False

            if self._right is not None and not self._right.is_avl_valid():
                return False

            return True
        except Exception:
            return False

    def validate_heights(self) -> bool:
        """
        Valide que les hauteurs sont correctement calculées.

        Cette méthode vérifie que les hauteurs stockées correspondent aux
        hauteurs réellement calculées.

        :return: True si les hauteurs sont cohérentes, False sinon
        :rtype: bool
        """
        try:
            # Calculer les hauteurs réelles des enfants
            left_height = self.get_left_height()
            right_height = self.get_right_height()

            # Calculer la hauteur attendue
            if self.is_leaf():
                expected_height = 0
            else:
                expected_height = 1 + max(left_height, right_height)

            # Comparer avec la hauteur stockée
            if self._cached_height != expected_height:
                return False

            # Vérifier la cohérence des enfants
            if self._left is not None and not self._left.validate_heights():
                return False

            if self._right is not None and not self._right.validate_heights():
                return False

            return True
        except Exception:
            return False

    def validate_balance_factor(self) -> bool:
        """
        Valide que le facteur d'équilibre est correct.

        Cette méthode vérifie que le facteur d'équilibre stocké correspond
        au facteur réellement calculé.

        :return: True si le facteur d'équilibre est correct, False sinon
        :rtype: bool
        """
        try:
            # Calculer le facteur réel
            left_height = self.get_left_height()
            right_height = self.get_right_height()
            expected_balance_factor = right_height - left_height

            # Comparer avec le facteur stocké
            if self._balance_factor != expected_balance_factor:
                return False

            # Vérifier qu'il est dans [-1, 1]
            if not self.is_balanced():
                return False

            return True
        except Exception:
            return False

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

    def get_node_info(self) -> dict[str, Any]:
        """
        Retourne les informations complètes du nœud.

        Cette méthode collecte toutes les propriétés du nœud et calcule
        les statistiques associées.

        :return: Dictionnaire contenant toutes les informations du nœud
        :rtype: dict[str, Any]
        """
        info = {
            "value": self._value,
            "balance_factor": self._balance_factor,
            "height": self._cached_height,
            "left_height": self.get_left_height(),
            "right_height": self.get_right_height(),
            "is_balanced": self.is_balanced(),
            "is_left_heavy": self.is_left_heavy(),
            "is_right_heavy": self.is_right_heavy(),
            "is_leaf": self.is_leaf(),
            "is_root": self.is_root(),
            "depth": self.get_depth(),
            "has_left_child": self._left is not None,
            "has_right_child": self._right is not None,
            "children_count": len(self._children),
            "metadata": self._metadata.copy() if self._metadata else {},
        }

        # Ajouter les informations des enfants si présents
        if self._left is not None:
            info["left_child_value"] = self._left._value
        if self._right is not None:
            info["right_child_value"] = self._right._value

        return info

    def compare_with(self, other: "AVLNode[T]") -> dict[str, Any]:
        """
        Compare ce nœud avec un autre nœud AVL.

        Cette méthode effectue une comparaison détaillée entre deux nœuds AVL
        et retourne un rapport de comparaison.

        :param other: Autre nœud AVL à comparer
        :type other: AVLNode[T]
        :return: Dictionnaire contenant le rapport de comparaison
        :rtype: dict[str, Any]
        :raises AVLNodeError: Si la comparaison échoue
        """
        if not isinstance(other, AVLNode):
            raise AVLNodeError(
                f"Cannot compare with non-AVLNode: {type(other).__name__}",
                "compare_with",
                self,
            )

        comparison = {
            "values_equal": self._value == other._value,
            "balance_factors_equal": self._balance_factor == other._balance_factor,
            "heights_equal": self._cached_height == other._cached_height,
            "both_balanced": self.is_balanced() and other.is_balanced(),
            "both_leaves": self.is_leaf() and other.is_leaf(),
            "both_roots": self.is_root() and other.is_root(),
            "depth_difference": self.get_depth() - other.get_depth(),
            "height_difference": self._cached_height - other._cached_height,
            "balance_factor_difference": self._balance_factor - other._balance_factor,
        }

        # Comparer les enfants
        comparison["left_children_equal"] = (
            self._left is None and other._left is None
        ) or (
            self._left is not None
            and other._left is not None
            and self._left._value == other._left._value
        )

        comparison["right_children_equal"] = (
            self._right is None and other._right is None
        ) or (
            self._right is not None
            and other._right is not None
            and self._right._value == other._right._value
        )

        return comparison

    def diagnose(self) -> dict[str, Any]:
        """
        Effectue un diagnostic complet du nœud.

        Cette méthode analyse le nœud et détecte les problèmes potentiels,
        retournant un rapport de diagnostic détaillé.

        :return: Dictionnaire contenant le rapport de diagnostic
        :rtype: dict[str, Any]
        """
        diagnosis = {
            "node_id": id(self),
            "value": self._value,
            "is_valid": True,
            "issues": [],
            "warnings": [],
            "recommendations": [],
        }

        # Vérifier la validité AVL
        try:
            if not self.is_avl_valid():
                diagnosis["is_valid"] = False
                diagnosis["issues"].append("Node does not satisfy AVL properties")
        except Exception as e:
            diagnosis["is_valid"] = False
            diagnosis["issues"].append(f"AVL validation failed: {str(e)}")

        # Vérifier les hauteurs
        try:
            if not self.validate_heights():
                diagnosis["is_valid"] = False
                diagnosis["issues"].append("Height validation failed")
        except Exception as e:
            diagnosis["is_valid"] = False
            diagnosis["issues"].append(f"Height validation error: {str(e)}")

        # Vérifier le facteur d'équilibre
        try:
            if not self.validate_balance_factor():
                diagnosis["is_valid"] = False
                diagnosis["issues"].append("Balance factor validation failed")
        except Exception as e:
            diagnosis["is_valid"] = False
            diagnosis["issues"].append(f"Balance factor validation error: {str(e)}")

        # Analyser les propriétés
        if not self.is_balanced():
            diagnosis["warnings"].append(
                f"Balance factor {self._balance_factor} is outside valid range [-1, 1]"
            )

        if self._balance_factor < -1:
            diagnosis["recommendations"].append("Consider right rotation")
        elif self._balance_factor > 1:
            diagnosis["recommendations"].append("Consider left rotation")

        # Analyser la structure
        if self.is_leaf():
            diagnosis["structure"] = "leaf"
        elif self._left is None:
            diagnosis["structure"] = "right_only"
        elif self._right is None:
            diagnosis["structure"] = "left_only"
        else:
            diagnosis["structure"] = "full"

        # Statistiques
        diagnosis["statistics"] = {
            "balance_factor": self._balance_factor,
            "height": self._cached_height,
            "depth": self.get_depth(),
            "children_count": len(self._children),
            "is_leaf": self.is_leaf(),
            "is_root": self.is_root(),
        }

        return diagnosis

    def to_dict(self) -> dict[str, Any]:
        """
        Sérialise le nœud en dictionnaire.

        Cette méthode convertit le nœud AVL et tous ses descendants en
        un dictionnaire sérialisable.

        :return: Dictionnaire représentant le nœud et ses descendants
        :rtype: dict[str, Any]
        """
        data = {
            "value": self._value,
            "balance_factor": self._balance_factor,
            "height": self._cached_height,
            "metadata": self._metadata.copy() if self._metadata else {},
            "left": None,
            "right": None,
        }

        # Sérialiser récursivement les enfants
        if self._left is not None:
            data["left"] = self._left.to_dict()

        if self._right is not None:
            data["right"] = self._right.to_dict()

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AVLNode[T]":
        """
        Désérialise un nœud depuis un dictionnaire.

        Cette méthode reconstruit un nœud AVL et tous ses descendants
        à partir d'un dictionnaire sérialisé.

        :param data: Dictionnaire contenant les données sérialisées
        :type data: dict[str, Any]
        :return: Nouveau nœud AVL reconstruit
        :rtype: AVLNode[T]
        :raises AVLNodeError: Si la désérialisation échoue
        """
        if not isinstance(data, dict):
            raise AVLNodeError(
                f"Expected dict for deserialization, got {type(data).__name__}",
                "from_dict",
            )

        # Vérifier les champs requis
        required_fields = ["value", "balance_factor", "height"]
        for field in required_fields:
            if field not in data:
                raise AVLNodeError(
                    f"Missing required field '{field}' in serialized data",
                    "from_dict",
                )

        # Créer le nœud avec la valeur
        node = cls(
            value=data["value"],
            metadata=data.get("metadata", {}),
        )

        # Restaurer les propriétés AVL
        node._balance_factor = data["balance_factor"]
        node._cached_height = data["height"]

        # Désérialiser récursivement les enfants
        if data.get("left") is not None:
            left_child = cls.from_dict(data["left"])
            node.set_left(left_child)

        if data.get("right") is not None:
            right_child = cls.from_dict(data["right"])
            node.set_right(right_child)

        return node

    def to_string(self, indent: int = 0) -> str:
        """
        Retourne une représentation textuelle du nœud.

        Cette méthode génère une représentation textuelle structurée du nœud
        avec indentation pour montrer la hiérarchie.

        :param indent: Niveau d'indentation (par défaut 0)
        :type indent: int
        :return: Représentation textuelle du nœud
        :rtype: str
        """
        indent_str = "  " * indent
        result = f"{indent_str}AVLNode(value={self._value}, balance={self._balance_factor}, height={self._cached_height})"

        # Ajouter les enfants avec indentation
        if self._left is not None:
            result += "\n" + self._left.to_string(indent + 1)
        else:
            result += f"\n{indent_str}  [No left child]"

        if self._right is not None:
            result += "\n" + self._right.to_string(indent + 1)
        else:
            result += f"\n{indent_str}  [No right child]"

        return result

    def to_compact_string(self) -> str:
        """
        Retourne une représentation compacte du nœud.

        Cette méthode génère une représentation compacte au format
        "value(bf:h)" où bf est le facteur d'équilibre et h la hauteur.

        :return: Représentation compacte du nœud
        :rtype: str
        """
        return f"{self._value}(bf:{self._balance_factor}:h:{self._cached_height})"

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
