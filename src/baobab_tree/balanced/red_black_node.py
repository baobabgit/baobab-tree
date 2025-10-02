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
    from .red_black_node import RedBlackNode


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