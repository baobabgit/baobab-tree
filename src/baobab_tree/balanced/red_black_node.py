"""
Classe RedBlackNode pour les nœuds d'arbres rouge-noir.

Ce module implémente la classe RedBlackNode, spécialisée pour les arbres rouge-noir.
Elle hérite de BinaryTreeNode et ajoute les fonctionnalités spécifiques
aux nœuds rouge-noir (couleur, propriétés rouge-noir).
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional, TYPE_CHECKING

from ..binary.binary_tree_node import BinaryTreeNode
from ..core.exceptions import (
    ColorViolationError,
    InvalidNodeOperationError,
    NodeValidationError,
    RedBlackTreeError,
)
from ..core.interfaces import T

if TYPE_CHECKING:
    pass  # Forward reference handled by string annotations


class Color(Enum):
    """
    Énumération des couleurs pour les nœuds rouge-noir.

    Les nœuds rouge-noir peuvent être soit rouges, soit noirs.
    """

    RED = "red"
    BLACK = "black"


class RedBlackNode(BinaryTreeNode):
    """
    Nœud spécialisé pour les arbres rouge-noir avec gestion des couleurs.

    Cette classe étend BinaryTreeNode pour fournir des fonctionnalités spécifiques
    aux arbres rouge-noir, avec gestion automatique des couleurs et validation
    des propriétés rouge-noir.

    :param value: Valeur stockée dans le nœud
    :type value: T
    :param color: Couleur du nœud (par défaut RED)
    :type color: Color, optional
    :param parent: Nœud parent (optionnel)
    :type parent: Optional[RedBlackNode], optional
    :param left: Nœud enfant gauche (optionnel)
    :type left: Optional[RedBlackNode], optional
    :param right: Nœud enfant droit (optionnel)
    :type right: Optional[RedBlackNode], optional
    :param metadata: Dictionnaire de métadonnées (optionnel)
    :type metadata: Optional[dict], optional
    """

    def __init__(
        self,
        value: T,
        color: Color = Color.RED,
        parent: Optional["RedBlackNode"] = None,
        left: Optional["RedBlackNode"] = None,
        right: Optional["RedBlackNode"] = None,
        metadata: Optional[dict] = None,
    ):
        """
        Initialise un nouveau nœud rouge-noir.

        :param value: Valeur stockée dans le nœud
        :type value: T
        :param color: Couleur du nœud (par défaut RED)
        :type color: Color, optional
        :param parent: Nœud parent (optionnel)
        :type parent: Optional[RedBlackNode], optional
        :param left: Nœud enfant gauche (optionnel)
        :type left: Optional[RedBlackNode], optional
        :param right: Nœud enfant droit (optionnel)
        :type right: Optional[RedBlackNode], optional
        :param metadata: Dictionnaire de métadonnées (optionnel)
        :type metadata: Optional[dict], optional
        :raises CircularReferenceError: Si une référence circulaire est détectée
        :raises NodeValidationError: Si la validation échoue
        """
        super().__init__(value, parent, left, right, metadata)

        # Couleur du nœud
        self._color: Color = color
        # Hauteur noire mise en cache
        self._black_height: Optional[int] = None
        # Indicateur si le nœud est une sentinelle
        self._is_nil: bool = False

    @property
    def color(self) -> Color:
        """
        Retourne la couleur du nœud.

        :return: Couleur du nœud (RED ou BLACK)
        :rtype: Color
        """
        return self._color

    @color.setter
    def color(self, color: Color) -> None:
        """
        Définit la couleur du nœud.

        :param color: Nouvelle couleur du nœud
        :type color: Color
        :raises ColorViolationError: Si la couleur n'est pas valide
        """
        if not isinstance(color, Color):
            raise ColorViolationError(
                f"Invalid color type: {type(color).__name__}, expected Color",
                "color_type",
                self,
            )
        self._color = color

    def is_red(self) -> bool:
        """
        Vérifie si le nœud est rouge.

        :return: True si le nœud est rouge, False sinon
        :rtype: bool
        """
        return self._color == Color.RED

    def is_black(self) -> bool:
        """
        Vérifie si le nœud est noir.

        :return: True si le nœud est noir, False sinon
        :rtype: bool
        """
        return self._color == Color.BLACK

    def set_red(self) -> None:
        """
        Définit le nœud comme rouge.

        :return: None
        :rtype: None
        """
        self._color = Color.RED

    def set_black(self) -> None:
        """
        Définit le nœud comme noir.

        :return: None
        :rtype: None
        """
        self._color = Color.BLACK

    def toggle_color(self) -> None:
        """
        Inverse la couleur du nœud.

        :return: None
        :rtype: None
        """
        self._color = Color.BLACK if self._color == Color.RED else Color.RED

    def set_left(self, node: Optional["RedBlackNode"]) -> None:
        """
        Définit le nœud enfant gauche et valide les propriétés rouge-noir.

        :param node: Nouveau nœud enfant gauche ou None pour supprimer
        :type node: Optional[RedBlackNode]
        :raises CircularReferenceError: Si la définition créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, RedBlackNode):
            raise InvalidNodeOperationError(
                f"Left child must be a RedBlackNode, got {type(node).__name__}",
                "set_left",
                self,
            )

        super().set_left(node)

    def set_right(self, node: Optional["RedBlackNode"]) -> None:
        """
        Définit le nœud enfant droit et valide les propriétés rouge-noir.

        :param node: Nouveau nœud enfant droit ou None pour supprimer
        :type node: Optional[RedBlackNode]
        :raises CircularReferenceError: Si la définition créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if node is not None and not isinstance(node, RedBlackNode):
            raise InvalidNodeOperationError(
                f"Right child must be a RedBlackNode, got {type(node).__name__}",
                "set_right",
                self,
            )

        super().set_right(node)

    def add_child(self, child: "RedBlackNode") -> None:
        """
        Ajoute un enfant au nœud rouge-noir.

        Cette méthode est surchargée pour s'assurer que seuls des RedBlackNode
        peuvent être ajoutés comme enfants.

        :param child: Nœud enfant à ajouter
        :type child: RedBlackNode
        :raises CircularReferenceError: Si l'ajout créerait une référence circulaire
        :raises InvalidNodeOperationError: Si l'opération n'est pas valide
        """
        if not isinstance(child, RedBlackNode):
            raise InvalidNodeOperationError(
                f"Child must be a RedBlackNode, got {type(child).__name__}",
                "add_child",
                self,
            )

        super().add_child(child)

    def validate(self) -> bool:
        """
        Valide les propriétés du nœud rouge-noir.

        Cette méthode vérifie que le nœud respecte toutes les contraintes
        d'un nœud rouge-noir valide, y compris les propriétés BST et rouge-noir.

        :return: True si le nœud est valide, False sinon
        :rtype: bool
        :raises NodeValidationError: Si la validation échoue
        """
        # Valider les propriétés BST de base
        super().validate()

        # Vérifier que les enfants sont des RedBlackNode
        for child in self._children:
            if not isinstance(child, RedBlackNode):
                raise NodeValidationError(
                    f"All children must be RedBlackNode instances, got {type(child).__name__}",
                    "red_black_node_children_type",
                    self,
                )

        # Vérifier que la couleur est valide
        if not isinstance(self._color, Color):
            raise NodeValidationError(
                f"RedBlackNode color must be Color enum, got {type(self._color).__name__}",
                "red_black_node_color_type",
                self,
            )

        return True

    def is_red_black_valid(self) -> bool:
        """
        Valide que le nœud respecte les propriétés rouge-noir.

        Cette méthode vérifie récursivement que tous les nœuds du sous-arbre
        respectent les propriétés rouge-noir.

        :return: True si le nœud est valide rouge-noir, False sinon
        :rtype: bool
        """
        try:
            # Vérifier que la couleur est valide
            if not isinstance(self._color, Color):
                return False

            # Vérifier la propriété rouge (si le nœud est rouge, ses enfants sont noirs)
            if self.is_red():
                if self._left is not None and self._left.is_red():
                    return False
                if self._right is not None and self._right.is_red():
                    return False

            # Vérifier récursivement les enfants
            if self._left is not None and not self._left.is_red_black_valid():
                return False

            if self._right is not None and not self._right.is_red_black_valid():
                return False

            return True
        except Exception:
            return False

    def validate_colors(self) -> bool:
        """
        Valide que les couleurs sont correctement assignées.

        Cette méthode vérifie que chaque nœud a une couleur valide et que
        la propriété rouge est respectée.

        :return: True si les couleurs sont valides, False sinon
        :rtype: bool
        """
        try:
            # Vérifier que la couleur est valide
            if not isinstance(self._color, Color):
                return False

            # Vérifier la propriété rouge
            if self.is_red():
                if self._left is not None and self._left.is_red():
                    return False
                if self._right is not None and self._right.is_red():
                    return False

            # Vérifier récursivement les enfants
            if self._left is not None and not self._left.validate_colors():
                return False

            if self._right is not None and not self._right.validate_colors():
                return False

            return True
        except Exception:
            return False

    def validate_paths(self) -> bool:
        """
        Valide que tous les chemins ont le même nombre de nœuds noirs.

        Cette méthode vérifie la propriété de chemin des arbres rouge-noir :
        tous les chemins de la racine aux feuilles ont le même nombre de nœuds noirs.

        :return: True si tous les chemins ont le même nombre de nœuds noirs, False sinon
        :rtype: bool
        """
        try:
            # Calculer le nombre de nœuds noirs sur chaque chemin
            black_counts = self._get_black_counts()

            # Vérifier que tous les chemins ont le même nombre
            return len(set(black_counts)) <= 1
        except Exception:
            return False

    def _get_black_counts(self) -> list[int]:
        """
        Calcule le nombre de nœuds noirs sur chaque chemin vers les feuilles.

        :return: Liste des nombres de nœuds noirs par chemin
        :rtype: list[int]
        """
        if self.is_leaf():
            return [1 if self.is_black() else 0]

        counts = []

        # Compter les nœuds noirs sur les chemins des enfants
        if self._left is not None:
            left_counts = self._left._get_black_counts()
            counts.extend(left_counts)

        if self._right is not None:
            right_counts = self._right._get_black_counts()
            counts.extend(right_counts)

        # Ajouter 1 si ce nœud est noir
        if self.is_black():
            counts = [count + 1 for count in counts]

        return counts

    def get_color_info(self) -> dict[str, Any]:
        """
        Retourne les informations de couleur du nœud.

        Cette méthode collecte toutes les propriétés de couleur du nœud
        et calcule les statistiques associées.

        :return: Dictionnaire contenant les informations de couleur
        :rtype: dict[str, Any]
        """
        info = {
            "color": self._color.value,
            "is_red": self.is_red(),
            "is_black": self.is_black(),
            "is_leaf": self.is_leaf(),
            "is_root": self.is_root(),
            "depth": self.get_depth(),
            "has_left_child": self._left is not None,
            "has_right_child": self._right is not None,
            "children_count": len(self._children),
        }

        # Ajouter les informations des enfants si présents
        if self._left is not None:
            info["left_child_color"] = self._left._color.value
        if self._right is not None:
            info["right_child_color"] = self._right._color.value

        return info

    def get_black_height(self) -> int:
        """
        Calcule la hauteur noire du nœud.

        La hauteur noire est le nombre de nœuds noirs sur le chemin
        de ce nœud vers une feuille.

        :return: Hauteur noire du nœud
        :rtype: int
        """
        if self.is_leaf():
            return 1 if self.is_black() else 0

        # Calculer la hauteur noire des enfants
        left_height = self._left.get_black_height() if self._left is not None else 0
        right_height = self._right.get_black_height() if self._right is not None else 0

        # Ajouter 1 si ce nœud est noir
        black_addition = 1 if self.is_black() else 0

        return black_addition + max(left_height, right_height)

    def to_dict(self) -> dict[str, Any]:
        """
        Sérialise le nœud en dictionnaire.

        Cette méthode convertit le nœud rouge-noir et tous ses descendants en
        un dictionnaire sérialisable.

        :return: Dictionnaire représentant le nœud et ses descendants
        :rtype: dict[str, Any]
        """
        data = {
            "value": self._value,
            "color": self._color.value,
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
    def from_dict(cls, data: dict[str, Any]) -> "RedBlackNode[T]":
        """
        Désérialise un nœud depuis un dictionnaire.

        Cette méthode reconstruit un nœud rouge-noir et tous ses descendants
        à partir d'un dictionnaire sérialisé.

        :param data: Dictionnaire contenant les données sérialisées
        :type data: dict[str, Any]
        :return: Nouveau nœud rouge-noir reconstruit
        :rtype: RedBlackNode[T]
        :raises RedBlackTreeError: Si la désérialisation échoue
        """
        if not isinstance(data, dict):
            raise RedBlackTreeError(
                f"Expected dict for deserialization, got {type(data).__name__}",
                "from_dict",
            )

        # Vérifier les champs requis
        required_fields = ["value", "color"]
        for field in required_fields:
            if field not in data:
                raise RedBlackTreeError(
                    f"Missing required field '{field}' in serialized data",
                    "from_dict",
                )

        # Créer le nœud avec la valeur et la couleur
        color = Color(data["color"])
        node = cls(
            value=data["value"],
            color=color,
            metadata=data.get("metadata", {}),
        )

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
        color_symbol = "R" if self.is_red() else "B"
        result = f"{indent_str}RedBlackNode(value={self._value}, color={color_symbol})"

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
        "value(R/B)" où R indique rouge et B noir.

        :return: Représentation compacte du nœud
        :rtype: str
        """
        color_symbol = "R" if self.is_red() else "B"
        return f"{self._value}({color_symbol})"

    def __str__(self) -> str:
        """
        Retourne la représentation string du nœud rouge-noir.

        :return: Représentation string du nœud rouge-noir
        :rtype: str
        """
        color_symbol = "R" if self.is_red() else "B"
        return f"RedBlackNode(value={self._value}, color={color_symbol})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du nœud rouge-noir.

        :return: Représentation détaillée du nœud rouge-noir
        :rtype: str
        """
        color_symbol = "R" if self.is_red() else "B"
        return (
            f"RedBlackNode(value={self._value!r}, parent={self._parent}, "
            f"left={self._left}, right={self._right}, color={color_symbol})"
        )

    def __eq__(self, other: Any) -> bool:
        """
        Teste l'égalité entre deux nœuds rouge-noir.

        :param other: Autre objet à comparer
        :type other: Any
        :return: True si les nœuds sont égaux, False sinon
        :rtype: bool
        """
        if not isinstance(other, RedBlackNode):
            return False

        return (
            self._value == other._value
            and self._parent is other._parent
            and self._left is other._left
            and self._right is other._right
            and self._color == other._color
        )

    def __hash__(self) -> int:
        """
        Retourne le hash du nœud rouge-noir.

        :return: Hash du nœud rouge-noir
        :rtype: int
        """
        return hash(
            (
                self._value,
                id(self._parent),
                id(self._left),
                id(self._right),
                self._color,
            )
        )

    @classmethod
    def create_nil_node(cls) -> "RedBlackNode[T]":
        """
        Crée un nœud sentinelle (NIL) noir.

        Cette méthode crée un nœud spécial utilisé comme sentinelle dans
        les arbres rouge-noir. Les nœuds sentinelles sont toujours noirs
        et ont une valeur None.

        :return: Nouveau nœud sentinelle noir
        :rtype: RedBlackNode[T]
        """
        nil_node = cls(value=None, color=Color.BLACK)
        nil_node._is_nil = True
        nil_node._black_height = 0
        return nil_node

    @classmethod
    def from_copy(cls, other: "RedBlackNode[T]") -> "RedBlackNode[T]":
        """
        Crée une copie profonde d'un nœud rouge-noir.

        Cette méthode crée une copie complètement indépendante du nœud
        et de tous ses descendants, avec les mêmes valeurs et couleurs
        mais sans références partagées.

        :param other: Nœud rouge-noir à copier
        :type other: RedBlackNode[T]
        :return: Nouveau nœud rouge-noir copié
        :rtype: RedBlackNode[T]
        :raises RedBlackTreeError: Si la copie échoue
        """
        if not isinstance(other, RedBlackNode):
            raise RedBlackTreeError(
                f"Cannot copy non-RedBlackNode: {type(other).__name__}",
                "from_copy",
            )

        # Créer le nœud avec la même valeur et couleur
        new_node = cls(
            value=other._value,
            color=other._color,
            metadata=other._metadata.copy() if other._metadata else None,
        )

        # Copier les propriétés spéciales
        new_node._is_nil = other._is_nil
        new_node._black_height = other._black_height

        # Copier récursivement les enfants
        if other._left is not None:
            left_copy = cls.from_copy(other._left)
            new_node.set_left(left_copy)

        if other._right is not None:
            right_copy = cls.from_copy(other._right)
            new_node.set_right(right_copy)

        return new_node

    @property
    def is_nil(self) -> bool:
        """
        Vérifie si le nœud est une sentinelle.

        :return: True si le nœud est une sentinelle, False sinon
        :rtype: bool
        """
        return self._is_nil

    @property
    def black_height(self) -> int:
        """
        Retourne la hauteur noire du nœud.

        :return: Hauteur noire du nœud
        :rtype: int
        """
        if self._black_height is None:
            self._black_height = self.get_black_height()
        return self._black_height

    def set_color(self, color: Color) -> None:
        """
        Définit la couleur du nœud et met à jour les propriétés.

        Cette méthode définit la couleur du nœud et invalide le cache
        de la hauteur noire pour forcer un recalcul.

        :param color: Nouvelle couleur du nœud
        :type color: Color
        :raises ColorViolationError: Si la couleur n'est pas valide
        """
        if not isinstance(color, Color):
            raise ColorViolationError(
                f"Invalid color type: {type(color).__name__}, expected Color",
                "color_type",
                self,
            )

        self._color = color
        # Invalider le cache de la hauteur noire
        self._black_height = None

    def flip_color(self) -> None:
        """
        Inverse la couleur du nœud.

        Cette méthode inverse la couleur du nœud (rouge ↔ noir) et
        invalide le cache de la hauteur noire.

        :raises InvalidNodeOperationError: Si le nœud est une sentinelle
        """
        if self._is_nil:
            raise InvalidNodeOperationError(
                "Cannot flip color of NIL node",
                "flip_color",
                self,
            )

        self._color = Color.BLACK if self._color == Color.RED else Color.RED
        # Invalider le cache de la hauteur noire
        self._black_height = None

    def update_black_height(self) -> None:
        """
        Met à jour la hauteur noire du nœud.

        Cette méthode recalcule et met en cache la hauteur noire du nœud
        et propage la mise à jour vers le parent si nécessaire.

        :raises RedBlackTreeError: Si le calcul échoue
        """
        try:
            # Calculer la hauteur noire des enfants
            left_height = self._left.black_height if self._left is not None else 0
            right_height = self._right.black_height if self._right is not None else 0

            # Vérifier la cohérence
            if left_height != right_height:
                raise RedBlackTreeError(
                    f"Black heights inconsistent: left={left_height}, right={right_height}",
                    "update_black_height",
                    self,
                )

            # Ajouter 1 si le nœud est noir
            new_height = left_height + (1 if self.is_black() else 0)
            self._black_height = new_height

            # Propager vers le parent si nécessaire
            if self._parent is not None:
                self._parent.update_black_height()

        except Exception as e:
            if isinstance(e, RedBlackTreeError):
                raise
            raise RedBlackTreeError(
                f"Failed to update black height: {str(e)}",
                "update_black_height",
                self,
            ) from e

    def validate_black_height(self) -> bool:
        """
        Valide que la hauteur noire est correctement calculée.

        Cette méthode vérifie que la hauteur noire mise en cache correspond
        à la hauteur noire calculée récursivement.

        :return: True si la hauteur noire est valide, False sinon
        :rtype: bool
        """
        try:
            # Calculer la hauteur noire réelle
            calculated_height = self.get_black_height()

            # Comparer avec la hauteur mise en cache
            cached_height = self._black_height

            # Si pas de cache, mettre à jour
            if cached_height is None:
                self._black_height = calculated_height
                return True

            # Vérifier la cohérence
            return calculated_height == cached_height
        except Exception:
            return False

    def get_node_info(self) -> dict[str, Any]:
        """
        Retourne les informations complètes du nœud.

        Cette méthode collecte toutes les propriétés du nœud et calcule
        les statistiques de couleur et de structure.

        :return: Dictionnaire contenant toutes les informations du nœud
        :rtype: dict[str, Any]
        """
        info = {
            "value": self._value,
            "color": self._color.value,
            "is_red": self.is_red(),
            "is_black": self.is_black(),
            "is_nil": self._is_nil,
            "is_leaf": self.is_leaf(),
            "is_root": self.is_root(),
            "depth": self.get_depth(),
            "height": self.get_height(),
            "black_height": self.black_height,
            "has_left_child": self._left is not None,
            "has_right_child": self._right is not None,
            "children_count": len(self._children),
            "metadata": self._metadata.copy() if self._metadata else {},
        }

        # Ajouter les informations des enfants si présents
        if self._left is not None:
            info["left_child"] = {
                "value": self._left._value,
                "color": self._left._color.value,
            }
        if self._right is not None:
            info["right_child"] = {
                "value": self._right._value,
                "color": self._right._color.value,
            }

        return info

    def compare_with(self, other: "RedBlackNode[T]") -> dict[str, Any]:
        """
        Compare ce nœud avec un autre nœud rouge-noir.

        Cette méthode effectue une comparaison détaillée entre deux nœuds
        rouge-noir et retourne un rapport de comparaison.

        :param other: Autre nœud rouge-noir à comparer
        :type other: RedBlackNode[T]
        :return: Dictionnaire contenant le rapport de comparaison
        :rtype: dict[str, Any]
        :raises RedBlackTreeError: Si la comparaison échoue
        """
        if not isinstance(other, RedBlackNode):
            raise RedBlackTreeError(
                f"Cannot compare with non-RedBlackNode: {type(other).__name__}",
                "compare_with",
            )

        comparison = {
            "values_equal": self._value == other._value,
            "colors_equal": self._color == other._color,
            "structures_equal": (
                (self._left is None) == (other._left is None)
                and (self._right is None) == (other._right is None)
            ),
            "black_heights_equal": self.black_height == other.black_height,
            "depths_equal": self.get_depth() == other.get_depth(),
            "heights_equal": self.get_height() == other.get_height(),
            "is_nil_equal": self._is_nil == other._is_nil,
            "metadata_equal": self._metadata == other._metadata,
        }

        # Comparer les valeurs
        comparison["value_comparison"] = {
            "self": self._value,
            "other": other._value,
            "difference": self._value != other._value,
        }

        # Comparer les couleurs
        comparison["color_comparison"] = {
            "self": self._color.value,
            "other": other._color.value,
            "difference": self._color != other._color,
        }

        # Comparer les structures
        comparison["structure_comparison"] = {
            "self_has_left": self._left is not None,
            "other_has_left": other._left is not None,
            "self_has_right": self._right is not None,
            "other_has_right": other._right is not None,
        }

        return comparison

    def diagnose(self) -> dict[str, Any]:
        """
        Effectue un diagnostic complet du nœud.

        Cette méthode analyse le nœud et détecte les problèmes potentiels
        en validant toutes les propriétés rouge-noir.

        :return: Dictionnaire contenant le rapport de diagnostic
        :rtype: dict[str, Any]
        """
        diagnosis = {
            "node_info": self.get_node_info(),
            "validations": {},
            "issues": [],
            "recommendations": [],
        }

        # Valider les propriétés rouge-noir
        try:
            diagnosis["validations"]["is_red_black_valid"] = self.is_red_black_valid()
        except Exception as e:
            diagnosis["validations"]["is_red_black_valid"] = False
            diagnosis["issues"].append(f"Red-black validation failed: {str(e)}")

        try:
            diagnosis["validations"]["validate_colors"] = self.validate_colors()
        except Exception as e:
            diagnosis["validations"]["validate_colors"] = False
            diagnosis["issues"].append(f"Color validation failed: {str(e)}")

        try:
            diagnosis["validations"]["validate_paths"] = self.validate_paths()
        except Exception as e:
            diagnosis["validations"]["validate_paths"] = False
            diagnosis["issues"].append(f"Path validation failed: {str(e)}")

        try:
            diagnosis["validations"][
                "validate_black_height"
            ] = self.validate_black_height()
        except Exception as e:
            diagnosis["validations"]["validate_black_height"] = False
            diagnosis["issues"].append(f"Black height validation failed: {str(e)}")

        # Analyser les problèmes potentiels
        if not diagnosis["validations"].get("is_red_black_valid", True):
            diagnosis["recommendations"].append("Fix red-black property violations")

        if not diagnosis["validations"].get("validate_colors", True):
            diagnosis["recommendations"].append("Fix color violations")

        if not diagnosis["validations"].get("validate_paths", True):
            diagnosis["recommendations"].append("Fix path property violations")

        if not diagnosis["validations"].get("validate_black_height", True):
            diagnosis["recommendations"].append("Recalculate black height")

        # Analyser la couleur
        if self.is_red():
            if self._left is not None and self._left.is_red():
                diagnosis["issues"].append("Red node has red left child")
            if self._right is not None and self._right.is_red():
                diagnosis["issues"].append("Red node has red right child")

        return diagnosis

    def to_colored_string(self) -> str:
        """
        Retourne une représentation colorée du nœud.

        Cette méthode génère une représentation avec des codes couleur ANSI
        pour afficher le nœud avec sa couleur réelle.

        :return: Représentation colorée du nœud
        :rtype: str
        """
        # Codes couleur ANSI
        RED_COLOR = "\033[91m"  # Rouge
        BLACK_COLOR = "\033[30m"  # Noir
        RESET_COLOR = "\033[0m"  # Reset

        if self.is_red():
            color_code = RED_COLOR
            color_name = "RED"
        else:
            color_code = BLACK_COLOR
            color_name = "BLACK"

        return f"{color_code}{self._value}({color_name}){RESET_COLOR}"
