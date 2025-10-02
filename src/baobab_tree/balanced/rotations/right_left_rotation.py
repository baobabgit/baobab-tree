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
        # Sauvegarder les références importantes
        parent = node.parent
        right_child_left = right_child.left
        right_child_right = right_child.right
        right_child_left_left = right_child_left.left
        right_child_left_right = right_child_left.right

        # Nettoyer toutes les relations
        node._right = None
        node._children = []
        node._parent = None

        right_child._left = None
        right_child._children = []
        right_child._parent = None

        right_child_left._left = None
        right_child_left._right = None
        right_child_left._children = []
        right_child_left._parent = None

        # Établir les nouvelles relations après rotation droite-gauche
        # right_child_left devient la nouvelle racine
        # node devient son enfant gauche
        # right_child devient son enfant droit

        # right_child_left.left = node
        right_child_left._left = node
        right_child_left._children.append(node)
        node._parent = right_child_left

        # node.left reste inchangé (préserver)
        # Mais nous devons mettre à jour les enfants de node
        if node.left is not None:
            node._children.append(node.left)

        # node.right = None (pas d'enfant droit après rotation)

        # right_child_left.right = right_child
        right_child_left._right = right_child
        right_child_left._children.append(right_child)
        right_child._parent = right_child_left

        # right_child.left = right_child_left_left (préserver)
        if right_child_left_left is not None:
            right_child._left = right_child_left_left
            right_child._children.append(right_child_left_left)
            right_child_left_left._parent = right_child

        # right_child.right = right_child_right (préserver)
        if right_child_right is not None:
            right_child._right = right_child_right
            right_child._children.append(right_child_right)
            right_child_right._parent = right_child

        # Mettre à jour les références parent
        if parent is not None:
            if parent.left is node:
                parent._left = right_child_left
            elif parent.right is node:
                parent._right = right_child_left
            parent._children = [child for child in parent._children if child is not node]
            parent._children.append(right_child_left)
            right_child_left._parent = parent

        new_root = right_child_left

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