"""
Algorithmes de rotation pour les arbres AVL.

Ce module implémente tous les algorithmes de rotation nécessaires pour
maintenir l'équilibre des arbres AVL : rotations simples et doubles.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .avl_node import AVLNode
from .exceptions import RotationError
from .interfaces import T

if TYPE_CHECKING:
    from .avl_rotations import AVLRotations


class AVLRotations:
    """
    Classe contenant tous les algorithmes de rotation pour les arbres AVL.

    Cette classe fournit les méthodes pour effectuer les rotations simples
    (gauche, droite) et doubles (gauche-droite, droite-gauche) nécessaires
    pour maintenir l'équilibre des arbres AVL.
    """

    @staticmethod
    def rotate_left(node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation gauche sur le nœud donné.

        Une rotation gauche est utilisée quand le sous-arbre droit est plus
        lourd que le sous-arbre gauche. Elle réorganise les nœuds pour
        équilibrer l'arbre.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation ne peut pas être effectuée
        """
        if node is None:
            raise RotationError("Cannot rotate a null node", "rotate_left")

        if node.right is None:
            raise RotationError(
                "Cannot perform left rotation: node has no right child",
                "rotate_left",
                node,
            )

        # Sauvegarder les références importantes
        right_child = node.right
        right_left_child = right_child.left

        # Effectuer la rotation
        # 1. Le nœud droit devient le parent du nœud actuel
        right_child.parent = node.parent

        # 2. Mettre à jour les références du parent
        if node.parent is not None:
            if node.parent.left == node:
                node.parent.set_left(right_child)
            else:
                node.parent.set_right(right_child)

        # 3. Le nœud actuel devient l'enfant gauche du nœud droit
        right_child.set_left(node)

        # 4. L'ancien enfant gauche du nœud droit devient l'enfant droit du nœud actuel
        node.set_right(right_left_child)

        # 5. Mettre à jour les métadonnées AVL
        node._update_avl_metadata()
        right_child._update_avl_metadata()

        return right_child

    @staticmethod
    def rotate_right(node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation droite sur le nœud donné.

        Une rotation droite est utilisée quand le sous-arbre gauche est plus
        lourd que le sous-arbre droit. Elle réorganise les nœuds pour
        équilibrer l'arbre.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation ne peut pas être effectuée
        """
        if node is None:
            raise RotationError("Cannot rotate a null node", "rotate_right")

        if node.left is None:
            raise RotationError(
                "Cannot perform right rotation: node has no left child",
                "rotate_right",
                node,
            )

        # Sauvegarder les références importantes
        left_child = node.left
        left_right_child = left_child.right

        # Effectuer la rotation
        # 1. Le nœud gauche devient le parent du nœud actuel
        left_child.parent = node.parent

        # 2. Mettre à jour les références du parent
        if node.parent is not None:
            if node.parent.left == node:
                node.parent.set_left(left_child)
            else:
                node.parent.set_right(left_child)

        # 3. Le nœud actuel devient l'enfant droit du nœud gauche
        left_child.set_right(node)

        # 4. L'ancien enfant droit du nœud gauche devient l'enfant gauche du nœud actuel
        node.set_left(left_right_child)

        # 5. Mettre à jour les métadonnées AVL
        node._update_avl_metadata()
        left_child._update_avl_metadata()

        return left_child

    @staticmethod
    def rotate_left_right(node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation gauche-droite (double rotation) sur le nœud donné.

        Une rotation gauche-droite est utilisée quand le sous-arbre gauche
        est plus lourd et que son enfant droit est plus lourd que son enfant gauche.
        Elle combine une rotation gauche sur l'enfant gauche suivi d'une
        rotation droite sur le nœud actuel.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation ne peut pas être effectuée
        """
        if node is None:
            raise RotationError("Cannot rotate a null node", "rotate_left_right")

        if node.left is None:
            raise RotationError(
                "Cannot perform left-right rotation: node has no left child",
                "rotate_left_right",
                node,
            )

        # Effectuer la rotation gauche sur l'enfant gauche
        node.set_left(AVLRotations.rotate_left(node.left))

        # Effectuer la rotation droite sur le nœud actuel
        return AVLRotations.rotate_right(node)

    @staticmethod
    def rotate_right_left(node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation droite-gauche (double rotation) sur le nœud donné.

        Une rotation droite-gauche est utilisée quand le sous-arbre droit
        est plus lourd et que son enfant gauche est plus lourd que son enfant droit.
        Elle combine une rotation droite sur l'enfant droit suivi d'une
        rotation gauche sur le nœud actuel.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation ne peut pas être effectuée
        """
        if node is None:
            raise RotationError("Cannot rotate a null node", "rotate_right_left")

        if node.right is None:
            raise RotationError(
                "Cannot perform right-left rotation: node has no right child",
                "rotate_right_left",
                node,
            )

        # Effectuer la rotation droite sur l'enfant droit
        node.set_right(AVLRotations.rotate_right(node.right))

        # Effectuer la rotation gauche sur le nœud actuel
        return AVLRotations.rotate_left(node)

    @staticmethod
    def get_rotation_type(node: AVLNode[T]) -> str:
        """
        Détermine le type de rotation nécessaire pour équilibrer le nœud.

        Cette méthode analyse le facteur d'équilibre du nœud et de ses enfants
        pour déterminer quelle rotation est nécessaire.

        :param node: Nœud à analyser
        :type node: AVLNode[T]
        :return: Type de rotation nécessaire ('left', 'right', 'left_right', 'right_left', ou 'none')
        :rtype: str
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot determine rotation type for null node", "get_rotation_type"
            )

        if node.is_balanced():
            return "none"

        if node.is_right_heavy():
            # Sous-arbre droit plus lourd
            if node.right is not None and node.right.is_left_heavy():
                return "right_left"
            else:
                return "left"
        else:
            # Sous-arbre gauche plus lourd
            if node.left is not None and node.left.is_right_heavy():
                return "left_right"
            else:
                return "right"

    @staticmethod
    def perform_rotation(node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue la rotation appropriée pour équilibrer le nœud.

        Cette méthode détermine automatiquement le type de rotation nécessaire
        et l'effectue.

        :param node: Nœud à équilibrer
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si une erreur survient lors de la rotation
        """
        if node is None:
            raise RotationError(
                "Cannot perform rotation on null node", "perform_rotation"
            )

        rotation_type = AVLRotations.get_rotation_type(node)

        if rotation_type == "left":
            return AVLRotations.rotate_left(node)
        elif rotation_type == "right":
            return AVLRotations.rotate_right(node)
        elif rotation_type == "left_right":
            return AVLRotations.rotate_left_right(node)
        elif rotation_type == "right_left":
            return AVLRotations.rotate_right_left(node)
        else:
            # Aucune rotation nécessaire
            return node

    @staticmethod
    def validate_rotation_result(node: AVLNode[T]) -> bool:
        """
        Valide que le résultat d'une rotation est correct.

        Cette méthode vérifie que les propriétés AVL sont respectées
        après une rotation.

        :param node: Nœud à valider
        :type node: AVLNode[T]
        :return: True si la rotation est valide, False sinon
        :rtype: bool
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot validate rotation result for null node",
                "validate_rotation_result",
            )

        try:
            return node.validate()
        except Exception as e:
            raise RotationError(
                f"Rotation validation failed: {str(e)}",
                "validate_rotation_result",
                node,
            )
