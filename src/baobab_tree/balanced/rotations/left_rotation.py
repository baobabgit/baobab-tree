"""
Classe LeftRotation pour les rotations gauches d'arbres équilibrés.

Ce module implémente la classe LeftRotation qui effectue des rotations gauches
pour équilibrer les arbres binaires.
"""

from typing import TYPE_CHECKING

from ...core.exceptions import InvalidRotationError, MissingChildError
from .tree_rotation import TreeRotation

if TYPE_CHECKING:
    from ...binary.binary_tree_node import BinaryTreeNode


class LeftRotation(TreeRotation):
    """
    Rotation gauche pour équilibrer les arbres.

    Cette classe implémente la rotation gauche, qui est utilisée pour équilibrer
    les arbres binaires quand le sous-arbre droit est plus haut que le sous-arbre
    gauche. La rotation gauche fait que l'enfant droit devient la nouvelle racine.

    Exemple de rotation gauche :
    ```
    Avant :      A           Après :      B
                / \\                     / \\
               B   C                   D   A
              / \\                         / \\
             D   E                       E   C
    ```
    """

    def __init__(self):
        """
        Initialise une nouvelle rotation gauche.
        """
        super().__init__("left")

    def rotate(self, node: "BinaryTreeNode") -> "BinaryTreeNode":
        """
        Effectue une rotation gauche.

        Cette méthode effectue une rotation gauche sur le nœud donné :
        1. Sauvegarder l'enfant droit
        2. Remplacer l'enfant droit par l'enfant gauche de l'enfant droit
        3. Définir le nœud comme enfant gauche de l'enfant droit
        4. Mettre à jour les références parent
        5. Retourner la nouvelle racine

        :param node: Nœud sur lequel effectuer la rotation gauche
        :type node: BinaryTreeNode
        :return: Nouvelle racine après la rotation gauche
        :rtype: BinaryTreeNode
        :raises InvalidRotationError: Si la rotation gauche ne peut pas être effectuée
        :raises MissingChildError: Si l'enfant droit est manquant
        """
        # Validation pré-rotation
        if not self.validate_before_rotation(node):
            raise InvalidRotationError(
                "Left rotation validation failed", self.rotation_type, node
            )

        # Sauvegarder l'enfant droit
        right_child = node.right
        if right_child is None:
            raise MissingChildError(
                "Left rotation requires a right child", self.rotation_type, "right", node
            )

        # Effectuer la rotation
        # 1. Sauvegarder les références importantes
        parent = node.parent
        right_child_left = right_child.left
        right_child_right = right_child.right

        # 2. Nettoyer complètement toutes les relations
        # Nettoyer les relations de node
        node._right = None
        node._children = []
        node._parent = None

        # Nettoyer les relations de right_child
        right_child._left = None
        right_child._children = []
        right_child._parent = None

        # 3. Établir les nouvelles relations
        # node.right = right_child_left
        if right_child_left is not None:
            node._right = right_child_left
            node._children.append(right_child_left)
            right_child_left._parent = node

        # right_child.left = node
        right_child._left = node
        right_child._children.append(node)
        node._parent = right_child

        # right_child.right = right_child_right (préserver l'enfant droit)
        if right_child_right is not None:
            right_child._right = right_child_right
            right_child._children.append(right_child_right)
            right_child_right._parent = right_child

        # 4. Mettre à jour les références parent
        if parent is not None:
            if parent.left is node:
                parent._left = right_child
            elif parent.right is node:
                parent._right = right_child
            parent._children = [child for child in parent._children if child is not node]
            parent._children.append(right_child)
            right_child._parent = parent

        # Validation post-rotation
        if not self.validate_after_rotation(right_child):
            raise InvalidRotationError(
                "Left rotation post-validation failed", self.rotation_type, right_child
            )

        return right_child

    def can_rotate(self, node: "BinaryTreeNode") -> bool:
        """
        Vérifie si une rotation gauche peut être effectuée.

        Une rotation gauche peut être effectuée si :
        1. Le nœud existe
        2. Le nœud a un enfant droit
        3. Le nœud est valide

        :param node: Nœud à vérifier
        :type node: BinaryTreeNode
        :return: True si une rotation gauche peut être effectuée, False sinon
        :rtype: bool
        """
        if node is None:
            return False

        # Vérifier que le nœud a un enfant droit
        if not node.has_right():
            return False

        # Vérifier que le nœud est valide
        try:
            return node.validate()
        except Exception:
            return False

    def get_description(self) -> str:
        """
        Retourne la description de la rotation gauche.

        :return: Description de la rotation gauche
        :rtype: str
        """
        return "Rotation gauche: l'enfant droit devient la racine"

    def _predict_rotation_effect(self, node: "BinaryTreeNode") -> dict:
        """
        Prédit l'effet spécifique d'une rotation gauche.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode
        :return: Prédiction de l'effet de la rotation gauche
        :rtype: dict
        """
        base_prediction = super()._predict_rotation_effect(node)
        
        # Prédictions spécifiques à la rotation gauche
        specific_prediction = {
            "new_root": node.right.value if node.has_right() else None,
            "old_root_becomes_left_child": True,
            "right_subtree_height_decreases": True,
            "left_subtree_height_increases": True,
        }
        
        base_prediction.update(specific_prediction)
        return base_prediction

    def __str__(self) -> str:
        """
        Retourne la représentation string de la rotation gauche.

        :return: Représentation string
        :rtype: str
        """
        return "LeftRotation()"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de la rotation gauche.

        :return: Représentation détaillée
        :rtype: str
        """
        return "LeftRotation()"