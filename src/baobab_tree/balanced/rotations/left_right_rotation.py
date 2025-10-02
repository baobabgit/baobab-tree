"""
Classe LeftRightRotation pour les rotations gauche-droite d'arbres équilibrés.

Ce module implémente la classe LeftRightRotation qui effectue des rotations
gauche-droite (double rotation) pour équilibrer les arbres binaires.
"""

from typing import TYPE_CHECKING

from ...core.exceptions import InvalidRotationError, MissingChildError
from .left_rotation import LeftRotation
from .right_rotation import RightRotation
from .tree_rotation import TreeRotation

if TYPE_CHECKING:
    from ...binary.binary_tree_node import BinaryTreeNode


class LeftRightRotation(TreeRotation):
    """
    Rotation gauche-droite (double rotation).

    Cette classe implémente la rotation gauche-droite, qui est une double rotation
    utilisée pour équilibrer les arbres binaires dans des cas spécifiques de déséquilibre.
    Elle combine une rotation gauche sur l'enfant gauche suivi d'une rotation droite
    sur le nœud racine.

    Exemple de rotation gauche-droite :
    ```
    Avant :      A           Après :      C
                / \\                     / \\
               B   D                   B   A
              / \\                     / \\ / \\
             E   C                   E   F G D
                / \\
               F   G
    ```
    """

    def __init__(self):
        """
        Initialise une nouvelle rotation gauche-droite.
        """
        super().__init__("left_right")
        self._left_rotation = LeftRotation()
        self._right_rotation = RightRotation()

    def rotate(self, node: "BinaryTreeNode") -> "BinaryTreeNode":
        """
        Effectue une rotation gauche-droite.

        Cette méthode effectue une rotation gauche-droite sur le nœud donné :
        1. Effectuer une rotation gauche sur l'enfant gauche
        2. Effectuer une rotation droite sur le nœud
        3. Mettre à jour toutes les références
        4. Retourner la nouvelle racine

        :param node: Nœud sur lequel effectuer la rotation gauche-droite
        :type node: BinaryTreeNode
        :return: Nouvelle racine après la rotation gauche-droite
        :rtype: BinaryTreeNode
        :raises InvalidRotationError: Si la rotation gauche-droite ne peut pas être effectuée
        :raises MissingChildError: Si l'enfant gauche est manquant
        """
        # Validation pré-rotation
        if not self.validate_before_rotation(node):
            raise InvalidRotationError(
                "Left-right rotation validation failed", self.rotation_type, node
            )

        # Vérifier que le nœud a un enfant gauche
        if not node.has_left():
            raise MissingChildError(
                "Left-right rotation requires a left child", self.rotation_type, "left", node
            )

        left_child = node.left

        # Vérifier que l'enfant gauche a un enfant droit
        if not left_child.has_right():
            raise MissingChildError(
                "Left-right rotation requires left child to have a right child",
                self.rotation_type,
                "right",
                left_child,
            )

        # Effectuer la rotation gauche-droite
        # 1. Effectuer une rotation gauche sur l'enfant gauche
        new_left_child = self._left_rotation.rotate(left_child)

        # 2. Effectuer une rotation droite sur le nœud
        new_root = self._right_rotation.rotate(node)

        # Validation post-rotation
        if not self.validate_after_rotation(new_root):
            raise InvalidRotationError(
                "Left-right rotation post-validation failed", self.rotation_type, new_root
            )

        return new_root

    def can_rotate(self, node: "BinaryTreeNode") -> bool:
        """
        Vérifie si une rotation gauche-droite peut être effectuée.

        Une rotation gauche-droite peut être effectuée si :
        1. Le nœud existe
        2. Le nœud a un enfant gauche
        3. L'enfant gauche a un enfant droit
        4. Le nœud est valide

        :param node: Nœud à vérifier
        :type node: BinaryTreeNode
        :return: True si une rotation gauche-droite peut être effectuée, False sinon
        :rtype: bool
        """
        if node is None:
            return False

        # Vérifier que le nœud a un enfant gauche
        if not node.has_left():
            return False

        left_child = node.left

        # Vérifier que l'enfant gauche a un enfant droit
        if not left_child.has_right():
            return False

        # Vérifier que le nœud est valide
        try:
            return node.validate()
        except Exception:
            return False

    def get_description(self) -> str:
        """
        Retourne la description de la rotation gauche-droite.

        :return: Description de la rotation gauche-droite
        :rtype: str
        """
        return "Rotation gauche-droite: double rotation (gauche sur enfant gauche, puis droite sur racine)"

    def _predict_rotation_effect(self, node: "BinaryTreeNode") -> dict:
        """
        Prédit l'effet spécifique d'une rotation gauche-droite.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode
        :return: Prédiction de l'effet de la rotation gauche-droite
        :rtype: dict
        """
        base_prediction = super()._predict_rotation_effect(node)
        
        # Prédictions spécifiques à la rotation gauche-droite
        specific_prediction = {
            "new_root": node.left.right.value if node.has_left() and node.left.has_right() else None,
            "is_double_rotation": True,
            "first_rotation": "left",
            "second_rotation": "right",
            "complexity": "O(1)",  # Double rotation mais toujours O(1)
        }
        
        base_prediction.update(specific_prediction)
        return base_prediction

    def __str__(self) -> str:
        """
        Retourne la représentation string de la rotation gauche-droite.

        :return: Représentation string
        :rtype: str
        """
        return "LeftRightRotation()"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de la rotation gauche-droite.

        :return: Représentation détaillée
        :rtype: str
        """
        return "LeftRightRotation()"