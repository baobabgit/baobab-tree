"""
Classe SplayNode pour les arbres Splay.

Ce module implémente la classe SplayNode, spécialisée pour les arbres Splay.
Elle hérite de BinaryTreeNode et ajoute les fonctionnalités spécifiques
aux nœuds Splay (opérations de splay, métadonnées de performance).
"""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from ..core.exceptions import SplayNodeError, SplayOperationError
from ..core.interfaces import T
from ..binary.binary_tree_node import BinaryTreeNode

if TYPE_CHECKING:
    from .splay_node import SplayNode


class SplayNode(BinaryTreeNode):
    """
    Nœud spécialisé pour les arbres Splay.

    Cette classe étend BinaryTreeNode pour fournir des fonctionnalités spécifiques
    aux arbres Splay, incluant les opérations de splay et le suivi des métadonnées
    de performance.

    :param value: Valeur stockée dans le nœud
    :type value: T
    :param parent: Nœud parent (optionnel)
    :type parent: Optional[SplayNode], optional
    :param left: Nœud enfant gauche (optionnel)
    :type left: Optional[SplayNode], optional
    :param right: Nœud enfant droit (optionnel)
    :type right: Optional[SplayNode], optional
    :param metadata: Dictionnaire de métadonnées (optionnel)
    :type metadata: Optional[dict], optional
    """

    def __init__(
        self,
        value: T,
        parent: Optional["SplayNode"] = None,
        left: Optional["SplayNode"] = None,
        right: Optional["SplayNode"] = None,
        metadata: Optional[dict] = None,
    ):
        """
        Initialise un nouveau nœud Splay.

        :param value: Valeur stockée dans le nœud
        :type value: T
        :param parent: Nœud parent (optionnel)
        :type parent: Optional[SplayNode], optional
        :param left: Nœud enfant gauche (optionnel)
        :type left: Optional[SplayNode], optional
        :param right: Nœud enfant droit (optionnel)
        :type right: Optional[SplayNode], optional
        :param metadata: Dictionnaire de métadonnées (optionnel)
        :type metadata: Optional[dict], optional
        :raises SplayNodeError: Si l'initialisation du nœud Splay échoue
        """
        super().__init__(value, parent, left, right, metadata)
        
        # Métadonnées spécifiques aux Splay
        self._access_count = 0
        self._last_accessed = None
        self._splay_count = 0

    @property
    def access_count(self) -> int:
        """
        Retourne le nombre d'accès au nœud.

        :return: Nombre d'accès au nœud
        :rtype: int
        """
        return self._access_count

    @property
    def last_accessed(self) -> Optional[float]:
        """
        Retourne le timestamp du dernier accès au nœud.

        :return: Timestamp du dernier accès ou None
        :rtype: Optional[float]
        """
        return self._last_accessed

    @property
    def splay_count(self) -> int:
        """
        Retourne le nombre de fois que le nœud a été splayé.

        :return: Nombre de splay du nœud
        :rtype: int
        """
        return self._splay_count

    def increment_access(self) -> None:
        """
        Incrémente le compteur d'accès et met à jour le timestamp.

        :raises SplayNodeError: Si l'incrémentation échoue
        """
        try:
            import time
            self._access_count += 1
            self._last_accessed = time.time()
        except Exception as e:
            raise SplayNodeError(f"Failed to increment access count: {e}", self)

    def increment_splay(self) -> None:
        """
        Incrémente le compteur de splay.

        :raises SplayNodeError: Si l'incrémentation échoue
        """
        try:
            self._splay_count += 1
        except Exception as e:
            raise SplayNodeError(f"Failed to increment splay count: {e}", self)

    def reset_metrics(self) -> None:
        """
        Remet à zéro toutes les métriques du nœud.

        :raises SplayNodeError: Si la remise à zéro échoue
        """
        try:
            self._access_count = 0
            self._last_accessed = None
            self._splay_count = 0
        except Exception as e:
            raise SplayNodeError(f"Failed to reset metrics: {e}", self)

    def get_metrics(self) -> dict:
        """
        Retourne toutes les métriques du nœud.

        :return: Dictionnaire contenant les métriques
        :rtype: dict
        :raises SplayNodeError: Si la récupération des métriques échoue
        """
        try:
            return {
                "access_count": self._access_count,
                "last_accessed": self._last_accessed,
                "splay_count": self._splay_count,
                "value": self.value,
                "is_leaf": self.is_leaf,
                "height": self.get_height(),
            }
        except Exception as e:
            raise SplayNodeError(f"Failed to get metrics: {e}", self)

    def is_zig_case(self) -> bool:
        """
        Vérifie si le nœud est dans un cas de rotation simple (zig).

        :return: True si c'est un cas zig, False sinon
        :rtype: bool
        :raises SplayNodeError: Si la vérification échoue
        """
        try:
            if self._parent is None:
                return False
            
            # Cas zig : le parent est la racine
            return self._parent._parent is None
        except Exception as e:
            raise SplayNodeError(f"Failed to check zig case: {e}", self)

    def is_zig_zig_case(self) -> bool:
        """
        Vérifie si le nœud est dans un cas de rotation double zig-zig.

        :return: True si c'est un cas zig-zig, False sinon
        :rtype: bool
        :raises SplayNodeError: Si la vérification échoue
        """
        try:
            if self._parent is None or self._parent._parent is None:
                return False
            
            # Cas zig-zig : même direction pour nœud->parent et parent->grandparent
            parent = self._parent
            grandparent = parent._parent
            
            # Vérifier si nœud et parent sont tous les deux enfants gauches ou droits
            return (self == parent.left and parent == grandparent.left) or \
                   (self == parent.right and parent == grandparent.right)
        except Exception as e:
            raise SplayNodeError(f"Failed to check zig-zig case: {e}", self)

    def is_zig_zag_case(self) -> bool:
        """
        Vérifie si le nœud est dans un cas de rotation double zig-zag.

        :return: True si c'est un cas zig-zag, False sinon
        :rtype: bool
        :raises SplayNodeError: Si la vérification échoue
        """
        try:
            if self._parent is None or self._parent._parent is None:
                return False
            
            # Cas zig-zag : directions opposées pour nœud->parent et parent->grandparent
            parent = self._parent
            grandparent = parent._parent
            
            # Vérifier si nœud et parent sont dans des directions opposées
            return (self == parent.left and parent == grandparent.right) or \
                   (self == parent.right and parent == grandparent.left)
        except Exception as e:
            raise SplayNodeError(f"Failed to check zig-zag case: {e}", self)

    def get_rotation_type(self) -> str:
        """
        Détermine le type de rotation nécessaire pour ce nœud.

        :return: Type de rotation ('zig', 'zig-zig', 'zig-zag', ou 'none')
        :rtype: str
        :raises SplayNodeError: Si la détermination échoue
        """
        try:
            if self._parent is None:
                return "none"
            
            if self.is_zig_case():
                return "zig"
            elif self.is_zig_zig_case():
                return "zig-zig"
            elif self.is_zig_zag_case():
                return "zig-zag"
            else:
                return "none"
        except Exception as e:
            raise SplayNodeError(f"Failed to determine rotation type: {e}", self)

    def get_splay_path(self) -> list["SplayNode"]:
        """
        Retourne le chemin complet du nœud à la racine.

        :return: Liste des nœuds du chemin (du nœud à la racine)
        :rtype: list[SplayNode]
        :raises SplayNodeError: Si la récupération du chemin échoue
        """
        try:
            path = []
            current = self
            
            while current is not None:
                path.append(current)
                current = current._parent
            
            return path
        except Exception as e:
            raise SplayNodeError(f"Failed to get splay path: {e}", self)

    def get_splay_depth(self) -> int:
        """
        Retourne la profondeur du nœud dans l'arbre (distance à la racine).

        :return: Profondeur du nœud
        :rtype: int
        :raises SplayNodeError: Si le calcul de la profondeur échoue
        """
        try:
            depth = 0
            current = self
            
            while current._parent is not None:
                depth += 1
                current = current._parent
            
            return depth
        except Exception as e:
            raise SplayNodeError(f"Failed to calculate splay depth: {e}", self)

    def to_string(self, indent: int = 0) -> str:
        """
        Retourne une représentation string du nœud avec indentation.

        :param indent: Niveau d'indentation
        :type indent: int
        :return: Représentation string du nœud
        :rtype: str
        :raises SplayNodeError: Si la conversion échoue
        """
        try:
            prefix = "  " * indent
            metrics = self.get_metrics()
            
            result = f"{prefix}SplayNode(value={self.value}, "
            result += f"access_count={metrics['access_count']}, "
            result += f"splay_count={metrics['splay_count']}, "
            result += f"height={metrics['height']})\n"
            
            if self.left is not None:
                result += f"{prefix}  Left: {self.left.to_string(indent + 1)}"
            if self.right is not None:
                result += f"{prefix}  Right: {self.right.to_string(indent + 1)}"
            
            return result
        except Exception as e:
            raise SplayNodeError(f"Failed to convert to string: {e}", self)

    def __str__(self) -> str:
        """
        Retourne une représentation string simple du nœud.

        :return: Représentation string du nœud
        :rtype: str
        """
        try:
            return f"SplayNode(value={self.value}, access_count={self._access_count}, splay_count={self._splay_count})"
        except Exception:
            return f"SplayNode(value={self.value})"

    def __repr__(self) -> str:
        """
        Retourne une représentation détaillée du nœud.

        :return: Représentation détaillée du nœud
        :rtype: str
        """
        try:
            return f"SplayNode(value={self.value!r}, parent={self.parent!r}, left={self.left!r}, right={self.right!r})"
        except Exception:
            return f"SplayNode(value={self.value!r})"