"""
Sélecteur automatique de rotation selon le contexte.

Ce module implémente la classe RotationSelector qui permet de sélectionner
automatiquement la rotation appropriée selon le contexte et le type de déséquilibre.
"""

from typing import Any, Dict, Optional, TYPE_CHECKING

from ...core.exceptions import InvalidRotationError
from .rotation_factory import RotationFactory
from .tree_rotation import TreeRotation

if TYPE_CHECKING:
    from ...binary.binary_tree_node import BinaryTreeNode


class RotationSelector:
    """
    Sélecteur automatique de rotation selon le contexte.

    Cette classe fournit des méthodes statiques pour sélectionner automatiquement
    la rotation appropriée selon le contexte et le type de déséquilibre détecté.
    Elle analyse les propriétés du nœud et du contexte pour déterminer la meilleure
    rotation à appliquer.

    Types de déséquilibre supportés :
    - "left_heavy" : Sous-arbre gauche plus lourd
    - "right_heavy" : Sous-arbre droit plus lourd
    - "left_right_heavy" : Déséquilibre gauche-droite
    - "right_left_heavy" : Déséquilibre droite-gauche
    """

    @staticmethod
    def select_rotation(node: "BinaryTreeNode", context: Dict[str, Any]) -> TreeRotation:
        """
        Sélectionne la rotation appropriée selon le contexte.

        Cette méthode analyse le nœud et le contexte pour déterminer la rotation
        la plus appropriée à appliquer.

        :param node: Nœud sur lequel appliquer la rotation
        :type node: BinaryTreeNode
        :param context: Contexte contenant les informations sur le déséquilibre
        :type context: Dict[str, Any]
        :return: Rotation sélectionnée
        :rtype: TreeRotation
        :raises InvalidRotationError: Si aucune rotation appropriée ne peut être sélectionnée
        """
        if node is None:
            raise InvalidRotationError("Cannot select rotation for None node", "none", node)

        if not isinstance(context, dict):
            raise InvalidRotationError(
                f"Context must be a dictionary, got {type(context).__name__}", "none", node
            )

        # Analyser le déséquilibre
        imbalance_type = RotationSelector._analyze_imbalance(node, context)

        # Sélectionner la rotation appropriée
        rotation_type = RotationSelector._select_rotation_type(imbalance_type, context)

        # Créer et retourner la rotation
        return RotationFactory.create_rotation(rotation_type)

    @staticmethod
    def analyze_imbalance(node: "BinaryTreeNode") -> Dict[str, Any]:
        """
        Analyse le déséquilibre d'un nœud.

        Cette méthode analyse le nœud pour détecter le type de déséquilibre
        et retourne un rapport détaillé.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode
        :return: Rapport d'analyse du déséquilibre
        :rtype: Dict[str, Any]
        """
        if node is None:
            return {"error": "Cannot analyze None node"}

        analysis = {
            "node_value": node.value,
            "has_left": node.has_left(),
            "has_right": node.has_right(),
            "is_leaf": node.is_leaf(),
            "is_root": node.is_root(),
        }

        # Calculer les hauteurs des sous-arbres
        left_height = node.left.get_height() if node.has_left() else -1
        right_height = node.right.get_height() if node.has_right() else -1

        analysis.update({
            "left_height": left_height,
            "right_height": right_height,
            "height_difference": left_height - right_height,
            "balance_factor": left_height - right_height,
        })

        # Déterminer le type de déséquilibre
        imbalance_type = RotationSelector._determine_imbalance_type(
            left_height, right_height, node
        )
        analysis["imbalance_type"] = imbalance_type

        # Recommander une rotation
        recommended_rotation = RotationSelector._recommend_rotation(imbalance_type, node)
        analysis["recommended_rotation"] = recommended_rotation

        return analysis

    @staticmethod
    def get_rotation_for_balance_factor(balance_factor: int, node: "BinaryTreeNode") -> str:
        """
        Retourne le type de rotation recommandé selon le facteur d'équilibre.

        :param balance_factor: Facteur d'équilibre du nœud
        :type balance_factor: int
        :param node: Nœud concerné
        :type node: BinaryTreeNode
        :return: Type de rotation recommandé
        :rtype: str
        """
        if balance_factor > 1:
            # Sous-arbre gauche plus lourd
            if node.has_left() and node.left.has_right():
                return "left_right"  # Double rotation gauche-droite
            else:
                return "right"  # Rotation droite simple

        elif balance_factor < -1:
            # Sous-arbre droit plus lourd
            if node.has_right() and node.right.has_left():
                return "right_left"  # Double rotation droite-gauche
            else:
                return "left"  # Rotation gauche simple

        else:
            # Pas de déséquilibre significatif
            return "none"

    @staticmethod
    def _analyze_imbalance(node: "BinaryTreeNode", context: Dict[str, Any]) -> str:
        """
        Analyse le déséquilibre d'un nœud selon le contexte.

        :param node: Nœud à analyser
        :type node: BinaryTreeNode
        :param context: Contexte d'analyse
        :type context: Dict[str, Any]
        :return: Type de déséquilibre détecté
        :rtype: str
        """
        # Utiliser le facteur d'équilibre du contexte si disponible
        balance_factor = context.get("balance_factor")
        if balance_factor is not None:
            return RotationSelector._determine_imbalance_type_from_factor(
                balance_factor, node
            )

        # Calculer le facteur d'équilibre
        left_height = node.left.get_height() if node.has_left() else -1
        right_height = node.right.get_height() if node.has_right() else -1
        balance_factor = left_height - right_height

        return RotationSelector._determine_imbalance_type_from_factor(
            balance_factor, node
        )

    @staticmethod
    def _select_rotation_type(imbalance_type: str, context: Dict[str, Any]) -> str:
        """
        Sélectionne le type de rotation selon le type de déséquilibre.

        :param imbalance_type: Type de déséquilibre
        :type imbalance_type: str
        :param context: Contexte de sélection
        :type context: Dict[str, Any]
        :return: Type de rotation sélectionné
        :rtype: str
        """
        rotation_mapping = {
            "left_heavy": "right",
            "right_heavy": "left",
            "left_right_heavy": "left_right",
            "right_left_heavy": "right_left",
            "balanced": "none",
        }

        rotation_type = rotation_mapping.get(imbalance_type, "none")

        if rotation_type == "none":
            raise InvalidRotationError(
                f"No rotation needed for imbalance type '{imbalance_type}'", "none", None
            )

        return rotation_type

    @staticmethod
    def _determine_imbalance_type(
        left_height: int, right_height: int, node: "BinaryTreeNode"
    ) -> str:
        """
        Détermine le type de déséquilibre selon les hauteurs.

        :param left_height: Hauteur du sous-arbre gauche
        :type left_height: int
        :param right_height: Hauteur du sous-arbre droit
        :type right_height: int
        :param node: Nœud concerné
        :type node: BinaryTreeNode
        :return: Type de déséquilibre
        :rtype: str
        """
        balance_factor = left_height - right_height

        if balance_factor > 1:
            # Sous-arbre gauche plus lourd
            if node.has_left() and node.left.has_right():
                return "left_right_heavy"
            else:
                return "left_heavy"

        elif balance_factor < -1:
            # Sous-arbre droit plus lourd
            if node.has_right() and node.right.has_left():
                return "right_left_heavy"
            else:
                return "right_heavy"

        else:
            return "balanced"

    @staticmethod
    def _determine_imbalance_type_from_factor(
        balance_factor: int, node: "BinaryTreeNode"
    ) -> str:
        """
        Détermine le type de déséquilibre selon le facteur d'équilibre.

        :param balance_factor: Facteur d'équilibre
        :type balance_factor: int
        :param node: Nœud concerné
        :type node: BinaryTreeNode
        :return: Type de déséquilibre
        :rtype: str
        """
        if balance_factor > 1:
            # Sous-arbre gauche plus lourd
            if node.has_left() and node.left.has_right():
                return "left_right_heavy"
            else:
                return "left_heavy"

        elif balance_factor < -1:
            # Sous-arbre droit plus lourd
            if node.has_right() and node.right.has_left():
                return "right_left_heavy"
            else:
                return "right_heavy"

        else:
            return "balanced"

    @staticmethod
    def _recommend_rotation(imbalance_type: str, node: "BinaryTreeNode") -> Optional[str]:
        """
        Recommande une rotation selon le type de déséquilibre.

        :param imbalance_type: Type de déséquilibre
        :type imbalance_type: str
        :param node: Nœud concerné
        :type node: BinaryTreeNode
        :return: Type de rotation recommandé
        :rtype: Optional[str]
        """
        recommendations = {
            "left_heavy": "right",
            "right_heavy": "left",
            "left_right_heavy": "left_right",
            "right_left_heavy": "right_left",
            "balanced": None,
        }

        return recommendations.get(imbalance_type)

    def __str__(self) -> str:
        """
        Retourne la représentation string du sélecteur.

        :return: Représentation string
        :rtype: str
        """
        return "RotationSelector()"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du sélecteur.

        :return: Représentation détaillée
        :rtype: str
        """
        return "RotationSelector()"