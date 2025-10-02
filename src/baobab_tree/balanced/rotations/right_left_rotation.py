"""
Classe RightLeftRotation pour les rotations droite-gauche d'arbres équilibrés.

Ce module implémente la classe RightLeftRotation qui effectue des rotations
droite-gauche (double rotation) pour équilibrer les arbres binaires.
"""

from typing import TYPE_CHECKING

from ...core.exceptions import InvalidRotationError, MissingChildError
from .left_rotation import LeftRotation
from .right_rotation import RightRotation
from .tree_rotation import TreeRotation

if TYPE_CHECKING:
    from ...binary.binary_tree_node import BinaryTreeNode


class RightLeftRotation(TreeRotation):
    """
    Rotation droite-gauche (double rotation).

    Cette classe implémente la rotation droite-gauche, qui est une double rotation
    utilisée pour équilibrer les arbres binaires dans des cas spécifiques de déséquilibre.
    Elle combine une rotation droite sur l'enfant droit suivi d'une rotation gauche
    sur le nœud racine.

    Exemple de rotation droite-gauche :
    ```
    Avant :      A           Après :      C
                / \\                     / \\
               D   B                   A   B
                  / \\                 / \\ / \\
                 C   E               D   F G E
                / \\
               F   G
    ```
    """

    def __init__(self):
        """
        Initialise une nouvelle rotation droite-gauche.
        """
        super().__init__("right_left")
        self._left_rotation = LeftRotation()
        self._right_rotation = RightRotation()

    def rotate(self, node: "BinaryTreeNode") -> "BinaryTreeNode":
        """
        Effectue une rotation droite-gauche.

        Cette méthode effectue une rotation droite-gauche sur le nœud donné :
        1. Effectuer une rotation droite sur l'enfant droit
        2. Effectuer une rotation gauche sur le nœud
        3. Mettre à jour toutes les références
        4. Retourner la nouvelle racine

        :param node: Nœud sur lequel effectuer la rotation droite-gauche
        :type node: BinaryTreeNode
        :return: Nouvelle racine après la rotation droite-gauche
        :rtype: BinaryTreeNode
        :raises InvalidRotationError: Si la rotation droite-gauche ne peut pas être effectuée
        :raises MissingChildError: Si l'enfant droit est manquant
        """
        # Validation pré-rotation
        if not self.validate_before_rotation(node):
            raise InvalidRotationError(
                "Right-left rotation validation failed", self.rotation_type, node
            )

        # Vérifier que le nœud a un enfant droit
        if not node.has_right():
            raise MissingChildError(
                "Right-left rotation requires a right child", self.rotation_type, "right", node
            )

        right_child = node.right

        # Vérifier que l'enfant droit a un enfant gauche
        if not right_child.has_left():
            raise MissingChildError(
                "Right-left rotation requires right child to have a left child",
                self.rotation_type,
                "left",
                right_child,
            )

        # Effectuer la rotation droite-gauche
        # 1. Effectuer une rotation droite sur l'enfant droit
        new_right_child = self._right_rotation.rotate(right_child)

        # 2. Effectuer une rotation gauche sur le nœud
        new_root = self._left_rotation.rotate(node)

        # Validation post-rotation
        if not self.validate_after_rotation(new_root):
            raise InvalidRotationError(
                "Right-left rotation post-validation failed", self.rotation_type, new_root
            )

        return new_root

    def can_rotate(self, node: "BinaryTreeNode") -> bool:
        """
        Vérifie si une rotation droite-gauche peut être effectuée.

        Une rotation droite-gauche peut être effectuée si :
        1. Le nœud existe
        2. Le nœud a un enfant droit
        3. L'enfant droit a un enfant gauche
        4. Le nœud est valide

        :param node: Nœud à vérifier
        :type node: BinaryTreeNode
        :return: True si une rotation droite-gauche peut être effectuée, False sinon
        :rtype: bool
        """
        if node is None:
            return False

        # Vérifier que le nœud a un enfant droit
        if not node.has_right():
            return False

        right_child = node.right

        # Vérifier que l'enfant droit a un enfant gauche
        if not right_child.has_left():
            return False

        # Vérifier que le nœud est valide
        try:
            return node.validate()
        except Exception:
            return False

    def get_description(self) -> str:
        """
        Retourne la description de la rotation droite-gauche.

        :return: Description de la rotation droite-gauche
        :rtype: str
        """
        return "Rotation droite-gauche: double rotation (droite sur enfant droit, puis gauche sur racine)"

    def _predict_rotation_effect(self, node: "BinaryTreeNode") -> dict:
        """
        Prédit l'effet spécifique d'une rotation droite-gauche.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode
        :return: Prédiction de l'effet de la rotation droite-gauche
        :rtype: dict
        """
        base_prediction = super()._predict_rotation_effect(node)
        
        # Prédictions spécifiques à la rotation droite-gauche
        specific_prediction = {
            "new_root": node.right.left.value if node.has_right() and node.right.has_left() else None,
            "is_double_rotation": True,
            "first_rotation": "right",
            "second_rotation": "left",
            "complexity": "O(1)",  # Double rotation mais toujours O(1)
        }
        
        base_prediction.update(specific_prediction)
        return base_prediction

    def __str__(self) -> str:
        """
        Retourne la représentation string de la rotation droite-gauche.

        :return: Représentation string
        :rtype: str
        """
        return "RightLeftRotation()"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de la rotation droite-gauche.

        :return: Représentation détaillée
        :rtype: str
        """
        return "RightLeftRotation()"