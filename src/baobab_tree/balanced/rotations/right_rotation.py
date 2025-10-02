"""
Classe RightRotation pour les rotations droites d'arbres équilibrés.

Ce module implémente la classe RightRotation qui effectue des rotations droites
pour équilibrer les arbres binaires.
"""

from typing import TYPE_CHECKING

from ...core.exceptions import InvalidRotationError, MissingChildError
from .tree_rotation import TreeRotation

if TYPE_CHECKING:
    from ...binary.binary_tree_node import BinaryTreeNode


class RightRotation(TreeRotation):
    """
    Rotation droite pour équilibrer les arbres.

    Cette classe implémente la rotation droite, qui est utilisée pour équilibrer
    les arbres binaires quand le sous-arbre gauche est plus haut que le sous-arbre
    droit. La rotation droite fait que l'enfant gauche devient la nouvelle racine.

    Exemple de rotation droite :
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
        Initialise une nouvelle rotation droite.
        """
        super().__init__("right")

    def rotate(self, node: "BinaryTreeNode") -> "BinaryTreeNode":
        """
        Effectue une rotation droite.

        Cette méthode effectue une rotation droite sur le nœud donné :
        1. Sauvegarder l'enfant gauche
        2. Remplacer l'enfant gauche par l'enfant droit de l'enfant gauche
        3. Définir le nœud comme enfant droit de l'enfant gauche
        4. Mettre à jour les références parent
        5. Retourner la nouvelle racine

        :param node: Nœud sur lequel effectuer la rotation droite
        :type node: BinaryTreeNode
        :return: Nouvelle racine après la rotation droite
        :rtype: BinaryTreeNode
        :raises InvalidRotationError: Si la rotation droite ne peut pas être effectuée
        :raises MissingChildError: Si l'enfant gauche est manquant
        """
        # Validation pré-rotation
        if not self.validate_before_rotation(node):
            raise InvalidRotationError(
                "Right rotation validation failed", self.rotation_type, node
            )

        # Sauvegarder l'enfant gauche
        left_child = node.left
        if left_child is None:
            raise MissingChildError(
                "Right rotation requires a left child", self.rotation_type, "left", node
            )

        # Effectuer la rotation
        # 1. Sauvegarder les références importantes
        parent = node.parent
        left_child_left = left_child.left
        left_child_right = left_child.right

        # 2. Nettoyer complètement toutes les relations
        # Nettoyer les relations de node
        node._left = None
        node._children = []
        node._parent = None

        # Nettoyer les relations de left_child
        left_child._right = None
        left_child._children = []
        left_child._parent = None

        # 3. Établir les nouvelles relations
        # node.left = left_child_right
        if left_child_right is not None:
            node._left = left_child_right
            node._children.append(left_child_right)
            left_child_right._parent = node

        # left_child.right = node
        left_child._right = node
        left_child._children.append(node)
        node._parent = left_child

        # left_child.left = left_child_left (préserver l'enfant gauche)
        if left_child_left is not None:
            left_child._left = left_child_left
            left_child._children.append(left_child_left)
            left_child_left._parent = left_child

        # 4. Mettre à jour les références parent
        if parent is not None:
            if parent.left is node:
                parent._left = left_child
            elif parent.right is node:
                parent._right = left_child
            parent._children = [child for child in parent._children if child is not node]
            parent._children.append(left_child)
            left_child._parent = parent

        # Validation post-rotation
        if not self.validate_after_rotation(left_child):
            raise InvalidRotationError(
                "Right rotation post-validation failed", self.rotation_type, left_child
            )

        return left_child

    def can_rotate(self, node: "BinaryTreeNode") -> bool:
        """
        Vérifie si une rotation droite peut être effectuée.

        Une rotation droite peut être effectuée si :
        1. Le nœud existe
        2. Le nœud a un enfant gauche
        3. Le nœud est valide

        :param node: Nœud à vérifier
        :type node: BinaryTreeNode
        :return: True si une rotation droite peut être effectuée, False sinon
        :rtype: bool
        """
        if node is None:
            return False

        # Vérifier que le nœud a un enfant gauche
        if not node.has_left():
            return False

        # Vérifier que le nœud est valide
        try:
            return node.validate()
        except Exception:
            return False

    def get_description(self) -> str:
        """
        Retourne la description de la rotation droite.

        :return: Description de la rotation droite
        :rtype: str
        """
        return "Rotation droite: l'enfant gauche devient la racine"

    def _predict_rotation_effect(self, node: "BinaryTreeNode") -> dict:
        """
        Prédit l'effet spécifique d'une rotation droite.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode
        :return: Prédiction de l'effet de la rotation droite
        :rtype: dict
        """
        base_prediction = super()._predict_rotation_effect(node)
        
        # Prédictions spécifiques à la rotation droite
        specific_prediction = {
            "new_root": node.left.value if node.has_left() else None,
            "old_root_becomes_right_child": True,
            "left_subtree_height_decreases": True,
            "right_subtree_height_increases": True,
        }
        
        base_prediction.update(specific_prediction)
        return base_prediction

    def __str__(self) -> str:
        """
        Retourne la représentation string de la rotation droite.

        :return: Représentation string
        :rtype: str
        """
        return "RightRotation()"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée de la rotation droite.

        :return: Représentation détaillée
        :rtype: str
        """
        return "RightRotation()"