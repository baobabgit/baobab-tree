"""
Classe abstraite TreeRotation pour les rotations d'arbres équilibrés.

Ce module implémente la classe abstraite TreeRotation qui définit l'interface
commune pour toutes les rotations d'arbres équilibrés (AVL, Rouge-Noir, etc.).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TYPE_CHECKING

from ...core.exceptions import (
    InvalidRotationError,
    MissingChildError,
    RotationValidationError,
    TreeRotationError,
)
from ...core.interfaces import T

if TYPE_CHECKING:
    from ...binary.binary_tree_node import BinaryTreeNode


class TreeRotation(ABC, Generic[T]):
    """
    Classe abstraite pour les rotations d'arbres équilibrés.

    Cette classe définit l'interface commune pour toutes les rotations d'arbres
    équilibrés. Elle fournit les méthodes abstraites que chaque type de rotation
    doit implémenter, ainsi que des méthodes concrètes communes pour la validation
    et la gestion des références parent.

    :param rotation_type: Type de rotation (pour identification)
    :type rotation_type: str
    """

    def __init__(self, rotation_type: str):
        """
        Initialise une nouvelle rotation.

        :param rotation_type: Type de rotation (pour identification)
        :type rotation_type: str
        """
        self._rotation_type = rotation_type

    @property
    def rotation_type(self) -> str:
        """
        Retourne le type de rotation.

        :return: Type de rotation
        :rtype: str
        """
        return self._rotation_type

    @abstractmethod
    def rotate(self, node: "BinaryTreeNode[T]") -> "BinaryTreeNode[T]":
        """
        Effectue la rotation sur le nœud donné.

        Cette méthode abstraite doit être implémentée par chaque type de rotation
        pour effectuer la rotation spécifique.

        :param node: Nœud sur lequel effectuer la rotation
        :type node: BinaryTreeNode[T]
        :return: Nouvelle racine après la rotation
        :rtype: BinaryTreeNode[T]
        :raises InvalidRotationError: Si la rotation ne peut pas être effectuée
        :raises MissingChildError: Si un enfant requis est manquant
        :raises RotationValidationError: Si la validation échoue
        """
        pass

    @abstractmethod
    def can_rotate(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Vérifie si la rotation peut être effectuée sur le nœud donné.

        Cette méthode abstraite doit être implémentée par chaque type de rotation
        pour vérifier si les conditions nécessaires sont remplies.

        :param node: Nœud à vérifier
        :type node: BinaryTreeNode[T]
        :return: True si la rotation peut être effectuée, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Retourne une description de la rotation.

        Cette méthode abstraite doit être implémentée par chaque type de rotation
        pour fournir une description textuelle de ce que fait la rotation.

        :return: Description de la rotation
        :rtype: str
        """
        pass

    def validate_before_rotation(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Valide qu'une rotation peut être effectuée.

        Cette méthode effectue les validations communes avant une rotation :
        1. Vérifier que le nœud existe
        2. Vérifier que les enfants nécessaires existent
        3. Appeler can_rotate pour validation spécifique
        4. Retourner True si valide

        :param node: Nœud à valider
        :type node: BinaryTreeNode[T]
        :return: True si la rotation peut être effectuée, False sinon
        :rtype: bool
        :raises RotationValidationError: Si la validation échoue
        """
        if node is None:
            raise RotationValidationError(
                "Cannot rotate None node",
                self._rotation_type,
                "before",
                node,
            )

        # Vérifier que le nœud est valide
        if not node.validate():
            raise RotationValidationError(
                "Node is not valid for rotation",
                self._rotation_type,
                "before",
                node,
            )

        # Appeler la validation spécifique
        if not self.can_rotate(node):
            raise RotationValidationError(
                f"Rotation {self._rotation_type} cannot be performed on this node",
                self._rotation_type,
                "before",
                node,
            )

        return True

    def validate_after_rotation(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Valide qu'une rotation a été effectuée correctement.

        Cette méthode effectue les validations communes après une rotation :
        1. Vérifier la cohérence des références
        2. Vérifier les propriétés de l'arbre
        3. Vérifier la structure résultante
        4. Retourner True si valide

        :param node: Nouvelle racine après rotation
        :type node: BinaryTreeNode[T]
        :return: True si la rotation est valide, False sinon
        :rtype: bool
        :raises RotationValidationError: Si la validation échoue
        """
        if node is None:
            raise RotationValidationError(
                "Rotation resulted in None node",
                self._rotation_type,
                "after",
                node,
            )

        # Vérifier que le nœud est valide
        if not node.validate():
            raise RotationValidationError(
                "Node is not valid after rotation",
                self._rotation_type,
                "after",
                node,
            )

        # Vérifier la cohérence des références parent-enfant
        if not self._validate_parent_child_consistency(node):
            raise RotationValidationError(
                "Parent-child references are inconsistent after rotation",
                self._rotation_type,
                "after",
                node,
            )

        return True

    def update_parent_references(
        self, old_root: "BinaryTreeNode[T]", new_root: "BinaryTreeNode[T]"
    ) -> None:
        """
        Met à jour les références parent après une rotation.

        Cette méthode met à jour les références parent pour maintenir la cohérence
        de l'arbre après une rotation :
        1. Obtenir le parent de l'ancienne racine
        2. Mettre à jour la référence parent vers la nouvelle racine
        3. Mettre à jour la référence parent de la nouvelle racine
        4. Valider les références

        :param old_root: Ancienne racine avant la rotation
        :type old_root: BinaryTreeNode[T]
        :param new_root: Nouvelle racine après la rotation
        :type new_root: BinaryTreeNode[T]
        :raises TreeRotationError: Si la mise à jour des références échoue
        """
        if old_root is None or new_root is None:
            raise TreeRotationError(
                "Cannot update parent references with None nodes",
                self._rotation_type,
            )

        # Obtenir le parent de l'ancienne racine
        parent = old_root.parent

        # Mettre à jour la référence parent vers la nouvelle racine
        if parent is not None:
            if parent.left is old_root:
                # Mettre à jour directement les attributs pour éviter les références circulaires
                parent._left = new_root
                parent._children = [child for child in parent._children if child is not old_root]
                parent._children.append(new_root)
            elif parent.right is old_root:
                # Mettre à jour directement les attributs pour éviter les références circulaires
                parent._right = new_root
                parent._children = [child for child in parent._children if child is not old_root]
                parent._children.append(new_root)
            else:
                raise TreeRotationError(
                    "Old root is not a child of its parent",
                    self._rotation_type,
                    old_root,
                )

        # Mettre à jour la référence parent de la nouvelle racine
        new_root._parent = parent

    def analyze_rotation(self, node: "BinaryTreeNode[T]") -> Dict[str, Any]:
        """
        Analyse l'effet d'une rotation avant de l'effectuer.

        Cette méthode analyse l'état actuel du nœud et prédit l'effet de la rotation
        pour fournir des informations de diagnostic.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode[T]
        :return: Rapport d'analyse contenant les métriques et prédictions
        :rtype: Dict[str, Any]
        """
        if node is None:
            return {"error": "Cannot analyze None node"}

        analysis = {
            "rotation_type": self._rotation_type,
            "node_value": node.value,
            "can_rotate": self.can_rotate(node),
            "node_height": node.get_height(),
            "node_depth": node.get_depth(),
            "is_leaf": node.is_leaf(),
            "is_root": node.is_root(),
            "has_left": node.has_left(),
            "has_right": node.has_right(),
        }

        # Ajouter des informations sur les enfants si présents
        if node.has_left():
            analysis["left_child_height"] = node.left.get_height()
        if node.has_right():
            analysis["right_child_height"] = node.right.get_height()

        # Prédire l'effet de la rotation
        analysis["predicted_effect"] = self._predict_rotation_effect(node)

        return analysis

    def get_rotation_stats(self, node: "BinaryTreeNode[T]") -> Dict[str, Any]:
        """
        Retourne les statistiques de rotation du sous-arbre.

        Cette méthode calcule les statistiques de rotation pour le sous-arbre
        enraciné au nœud donné.

        :param node: Racine du sous-arbre à analyser
        :type node: BinaryTreeNode[T]
        :return: Statistiques de rotation
        :rtype: Dict[str, Any]
        """
        if node is None:
            return {"error": "Cannot get stats for None node"}

        stats = {
            "rotation_type": self._rotation_type,
            "subtree_size": self._count_subtree_nodes(node),
            "subtree_height": node.get_height(),
            "leaf_count": self._count_leaves(node),
            "internal_nodes": self._count_internal_nodes(node),
            "balance_factor": self._calculate_balance_factor(node),
        }

        return stats

    def validate_consistency(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Valide la cohérence de l'arbre après rotation.

        Cette méthode vérifie la cohérence générale de l'arbre après une rotation,
        incluant les références parent-enfant et les propriétés structurelles.

        :param node: Nœud racine à valider
        :type node: BinaryTreeNode[T]
        :return: True si l'arbre est cohérent, False sinon
        :rtype: bool
        """
        if node is None:
            return False

        # Vérifier la cohérence des références parent-enfant
        if not self._validate_parent_child_consistency(node):
            return False

        # Vérifier que tous les nœuds sont valides
        return self._validate_subtree(node)

    def validate_properties(self, node: "BinaryTreeNode[T]") -> Dict[str, bool]:
        """
        Valide les propriétés spécifiques de l'arbre après rotation.

        Cette méthode vérifie les propriétés spécifiques de l'arbre après rotation
        et retourne un rapport détaillé des validations.

        :param node: Nœud racine à valider
        :type node: BinaryTreeNode[T]
        :return: Rapport de validation des propriétés
        :rtype: Dict[str, bool]
        """
        if node is None:
            return {"error": True}

        properties = {
            "node_valid": node.validate(),
            "parent_child_consistency": self._validate_parent_child_consistency(node),
            "subtree_valid": self._validate_subtree(node),
            "height_consistent": self._validate_height_consistency(node),
            "structure_valid": self._validate_structure(node),
        }

        return properties

    def _validate_parent_child_consistency(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Valide la cohérence des références parent-enfant.

        :param node: Nœud à valider
        :type node: BinaryTreeNode[T]
        :return: True si cohérent, False sinon
        :rtype: bool
        """
        # Vérifier que les enfants ont ce nœud comme parent
        if node.has_left() and node.left.parent is not node:
            return False
        if node.has_right() and node.right.parent is not node:
            return False

        return True

    def _validate_subtree(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Valide récursivement un sous-arbre.

        :param node: Racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: True si valide, False sinon
        :rtype: bool
        """
        if not node.validate():
            return False

        if node.has_left() and not self._validate_subtree(node.left):
            return False
        if node.has_right() and not self._validate_subtree(node.right):
            return False

        return True

    def _validate_height_consistency(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Valide la cohérence des hauteurs.

        :param node: Nœud à valider
        :type node: BinaryTreeNode[T]
        :return: True si cohérent, False sinon
        :rtype: bool
        """
        # Calculer la hauteur réelle
        real_height = self._calculate_real_height(node)

        # Comparer avec la hauteur calculée
        return real_height == node.get_height()

    def _validate_structure(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Valide la structure générale de l'arbre.

        :param node: Nœud à valider
        :type node: BinaryTreeNode[T]
        :return: True si valide, False sinon
        :rtype: bool
        """
        # Vérifier qu'il n'y a pas de références circulaires
        return not self._has_circular_references(node)

    def _predict_rotation_effect(self, node: "BinaryTreeNode[T]") -> Dict[str, Any]:
        """
        Prédit l'effet d'une rotation.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode[T]
        :return: Prédiction de l'effet
        :rtype: Dict[str, Any]
        """
        return {
            "will_change_height": True,  # Généralement vrai pour les rotations
            "will_change_balance": True,  # Généralement vrai pour les rotations
            "complexity": "O(1)",  # Les rotations sont O(1)
        }

    def _count_subtree_nodes(self, node: "BinaryTreeNode[T]") -> int:
        """
        Compte le nombre de nœuds dans un sous-arbre.

        :param node: Racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Nombre de nœuds
        :rtype: int
        """
        if node is None:
            return 0

        count = 1
        if node.has_left():
            count += self._count_subtree_nodes(node.left)
        if node.has_right():
            count += self._count_subtree_nodes(node.right)

        return count

    def _count_leaves(self, node: "BinaryTreeNode[T]") -> int:
        """
        Compte le nombre de feuilles dans un sous-arbre.

        :param node: Racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Nombre de feuilles
        :rtype: int
        """
        if node is None:
            return 0

        if node.is_leaf():
            return 1

        count = 0
        if node.has_left():
            count += self._count_leaves(node.left)
        if node.has_right():
            count += self._count_leaves(node.right)

        return count

    def _count_internal_nodes(self, node: "BinaryTreeNode[T]") -> int:
        """
        Compte le nombre de nœuds internes dans un sous-arbre.

        :param node: Racine du sous-arbre
        :type node: BinaryTreeNode[T]
        :return: Nombre de nœuds internes
        :rtype: int
        """
        if node is None:
            return 0

        if node.is_leaf():
            return 0

        count = 1
        if node.has_left():
            count += self._count_internal_nodes(node.left)
        if node.has_right():
            count += self._count_internal_nodes(node.right)

        return count

    def _calculate_balance_factor(self, node: "BinaryTreeNode[T]") -> int:
        """
        Calcule le facteur d'équilibre d'un nœud.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode[T]
        :return: Facteur d'équilibre
        :rtype: int
        """
        if node is None:
            return 0

        left_height = node.left.get_height() if node.has_left() else -1
        right_height = node.right.get_height() if node.has_right() else -1

        return left_height - right_height

    def _calculate_real_height(self, node: "BinaryTreeNode[T]") -> int:
        """
        Calcule la hauteur réelle d'un nœud (sans cache).

        :param node: Nœud à analyser
        :type node: BinaryTreeNode[T]
        :return: Hauteur réelle
        :rtype: int
        """
        if node is None:
            return -1

        if node.is_leaf():
            return 0

        left_height = self._calculate_real_height(node.left)
        right_height = self._calculate_real_height(node.right)

        return 1 + max(left_height, right_height)

    def _has_circular_references(self, node: "BinaryTreeNode[T]") -> bool:
        """
        Vérifie s'il y a des références circulaires.

        :param node: Nœud à vérifier
        :type node: BinaryTreeNode[T]
        :return: True si des références circulaires existent
        :rtype: bool
        """
        visited = set()
        return self._check_circular_references(node, visited)

    def _check_circular_references(
        self, node: "BinaryTreeNode[T]", visited: set
    ) -> bool:
        """
        Vérifie récursivement les références circulaires.

        :param node: Nœud actuel
        :type node: BinaryTreeNode[T]
        :param visited: Ensemble des nœuds visités
        :type visited: set
        :return: True si des références circulaires existent
        :rtype: bool
        """
        if node is None:
            return False

        if id(node) in visited:
            return True

        visited.add(id(node))

        if node.has_left() and self._check_circular_references(node.left, visited):
            return True
        if node.has_right() and self._check_circular_references(node.right, visited):
            return True

        visited.remove(id(node))
        return False

    def __str__(self) -> str:
        """
        Retourne la représentation string de la rotation.

        :return: Représentation string
        :rtype: str
        """
        return f"{self.__class__.__name__}(type={self._rotation_type})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de la rotation.

        :return: Représentation détaillée
        :rtype: str
        """
        return f"{self.__class__.__name__}(rotation_type={self._rotation_type!r})"