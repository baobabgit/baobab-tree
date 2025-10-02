"""
Algorithmes de rotation pour les arbres AVL.

Ce module implémente tous les algorithmes de rotation nécessaires pour
maintenir l'équilibre des arbres AVL : rotations simples et doubles.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, TYPE_CHECKING

from .avl_node import AVLNode
from .exceptions import RotationError
from .interfaces import T

if TYPE_CHECKING:
    pass


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
        right_child.set_parent(node.parent)

        # 2. Mettre à jour les références du parent
        if node.parent is not None:
            if node.parent.left == node:
                node.parent.set_left(right_child)
            else:
                node.parent.set_right(right_child)

        # 3. Le nœud actuel devient l'enfant gauche du nœud droit
        right_child.set_left(node)

        # 4. L'ancien enfant gauche du nœud droit devient l'enfant droit
        # du nœud actuel
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
        left_child.set_parent(node.parent)

        # 2. Mettre à jour les références du parent
        if node.parent is not None:
            if node.parent.left == node:
                node.parent.set_left(left_child)
            else:
                node.parent.set_right(left_child)

        # 3. Le nœud actuel devient l'enfant droit du nœud gauche
        left_child.set_right(node)

        # 4. L'ancien enfant droit du nœud gauche devient l'enfant gauche
        # du nœud actuel
        node.set_left(left_right_child)

        # 5. Mettre à jour les métadonnées AVL
        node._update_avl_metadata()
        left_child._update_avl_metadata()

        return left_child

    @staticmethod
    def rotate_left_right(node: AVLNode[T]) -> AVLNode[T]:
        """
        Effectue une rotation gauche-droite (double rotation) sur le nœud
        donné.

        Une rotation gauche-droite est utilisée quand le sous-arbre gauche
        est plus lourd et que son enfant droit est plus lourd que son enfant
        gauche.
        Elle combine une rotation gauche sur l'enfant gauche suivi d'une
        rotation droite sur le nœud actuel.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation ne peut pas être effectuée
        """
        if node is None:
            raise RotationError(
                "Cannot rotate a null node", "rotate_left_right"
            )

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
        Effectue une rotation droite-gauche (double rotation) sur le nœud
        donné.

        Une rotation droite-gauche est utilisée quand le sous-arbre droit
        est plus lourd et que son enfant gauche est plus lourd que son enfant
        droit.
        Elle combine une rotation droite sur l'enfant droit suivi d'une
        rotation gauche sur le nœud actuel.

        :param node: Nœud autour duquel effectuer la rotation
        :type node: AVLNode[T]
        :return: Nouvelle racine du sous-arbre après rotation
        :rtype: AVLNode[T]
        :raises RotationError: Si la rotation ne peut pas être effectuée
        """
        if node is None:
            raise RotationError(
                "Cannot rotate a null node", "rotate_right_left"
            )

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
        :return: Type de rotation nécessaire ('left', 'right', 'left_right',
                'right_left', ou 'none')
        :rtype: str
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot determine rotation type for null node",
                "get_rotation_type",
            )

        if node.is_balanced():
            return "none"

        if node.is_right_heavy():
            # Sous-arbre droit plus lourd
            if node.right is not None and node.right.is_left_heavy():
                return "right_left"
            return "left"
        # Sous-arbre gauche plus lourd
        if node.left is not None and node.left.is_right_heavy():
            return "left_right"
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
        if rotation_type == "right":
            return AVLRotations.rotate_right(node)
        if rotation_type == "left_right":
            return AVLRotations.rotate_left_right(node)
        if rotation_type == "right_left":
            return AVLRotations.rotate_right_left(node)
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
            ) from e

    @staticmethod
    def select_rotation(
        node: AVLNode[T],
    ) -> Callable[[AVLNode[T]], AVLNode[T]]:
        """
        Sélectionne la rotation appropriée selon le facteur d'équilibre.

        Cette méthode analyse le facteur d'équilibre du nœud et de ses enfants
        pour déterminer quelle fonction de rotation utiliser.

        :param node: Nœud à analyser
        :type node: AVLNode[T]
        :return: Fonction de rotation appropriée
        :rtype: Callable[[AVLNode[T]], AVLNode[T]]
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot select rotation for null node", "select_rotation"
            )

        rotation_type = AVLRotations.get_rotation_type(node)

        if rotation_type == "left":
            return AVLRotations.rotate_left
        if rotation_type == "right":
            return AVLRotations.rotate_right
        if rotation_type == "left_right":
            return AVLRotations.rotate_left_right
        if rotation_type == "right_left":
            return AVLRotations.rotate_right_left
        # Aucune rotation nécessaire - retourner une fonction identité
        return lambda n: n

    @staticmethod
    def analyze_imbalance(node: AVLNode[T]) -> Dict[str, Any]:
        """
        Analyse le type de déséquilibre du nœud.

        Cette méthode collecte les facteurs d'équilibre et identifie
        le type de déséquilibre présent.

        :param node: Nœud à analyser
        :type node: AVLNode[T]
        :return: Rapport d'analyse du déséquilibre
        :rtype: Dict[str, Any]
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot analyze imbalance for null node", "analyze_imbalance"
            )

        analysis = {
            "node_value": node.value,
            "balance_factor": node.get_balance_factor(),
            "height": node.get_height(),
            "is_balanced": node.is_balanced(),
            "is_left_heavy": node.is_left_heavy(),
            "is_right_heavy": node.is_right_heavy(),
            "rotation_type": AVLRotations.get_rotation_type(node),
            "left_child_info": None,
            "right_child_info": None,
        }

        # Analyser l'enfant gauche
        if node.left is not None:
            analysis["left_child_info"] = {
                "value": node.left.value,
                "balance_factor": node.left.get_balance_factor(),
                "height": node.left.get_height(),
                "is_balanced": node.left.is_balanced(),
            }

        # Analyser l'enfant droit
        if node.right is not None:
            analysis["right_child_info"] = {
                "value": node.right.value,
                "balance_factor": node.right.get_balance_factor(),
                "height": node.right.get_height(),
                "is_balanced": node.right.is_balanced(),
            }

        return analysis

    @staticmethod
    def validate_before_rotation(node: AVLNode[T], rotation_type: str) -> bool:
        """
        Valide qu'une rotation peut être effectuée.

        Cette méthode vérifie que le nœud et les enfants nécessaires
        existent pour la rotation demandée.

        :param node: Nœud à valider
        :type node: AVLNode[T]
        :param rotation_type: Type de rotation à valider
        :type rotation_type: str
        :return: True si la rotation peut être effectuée, False sinon
        :rtype: bool
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot validate rotation for null node",
                "validate_before_rotation",
            )

        if rotation_type == "left":
            return node.right is not None
        if rotation_type == "right":
            return node.left is not None
        if rotation_type == "left_right":
            return node.left is not None and node.left.right is not None
        if rotation_type == "right_left":
            return node.right is not None and node.right.left is not None
        return False

    @staticmethod
    def validate_after_rotation(node: AVLNode[T]) -> bool:
        """
        Valide qu'une rotation a été effectuée correctement.

        Cette méthode vérifie la cohérence des références et des
        propriétés AVL après une rotation.

        :param node: Nœud à valider
        :type node: AVLNode[T]
        :return: True si la rotation est correcte, False sinon
        :rtype: bool
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot validate rotation result for null node",
                "validate_after_rotation",
            )

        try:
            # Vérifier la cohérence des références parent/enfant
            if node.left is not None and node.left.parent != node:
                return False
            if node.right is not None and node.right.parent != node:
                return False

            # Vérifier les propriétés AVL
            return node.validate()
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def update_avl_properties(node: AVLNode[T]) -> None:
        """
        Met à jour toutes les propriétés AVL après une rotation.

        Cette méthode met à jour les hauteurs et facteurs d'équilibre
        et propage les changements vers les ancêtres.

        :param node: Nœud à mettre à jour
        :type node: AVLNode[T]
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot update AVL properties for null node",
                "update_avl_properties",
            )

        # Mettre à jour les métadonnées AVL du nœud
        node._update_avl_metadata()

        # Propager les changements vers les ancêtres
        current = node.parent
        while current is not None:
            current._update_avl_metadata()
            current = current.parent

    @staticmethod
    def update_parent_references(
        old_root: AVLNode[T], new_root: AVLNode[T]
    ) -> None:
        """
        Met à jour les références parent après une rotation.

        Cette méthode met à jour la référence parent vers la nouvelle racine
        et la référence parent de la nouvelle racine.

        :param old_root: Ancienne racine du sous-arbre
        :type old_root: AVLNode[T]
        :param new_root: Nouvelle racine du sous-arbre
        :type new_root: AVLNode[T]
        :raises RotationError: Si l'un des nœuds est null
        """
        if old_root is None or new_root is None:
            raise RotationError(
                "Cannot update parent references for null nodes",
                "update_parent_references",
            )

        # Obtenir le parent de l'ancienne racine
        parent = old_root.parent

        # Mettre à jour la référence parent vers la nouvelle racine
        if parent is not None:
            if parent.left == old_root:
                parent.set_left(new_root)
            else:
                parent.set_right(new_root)
        else:
            # L'ancienne racine était la racine de l'arbre
            new_root.set_parent(None)

    @staticmethod
    def get_rotation_stats(node: AVLNode[T]) -> Dict[str, int]:
        """
        Retourne les statistiques de rotation du sous-arbre.

        Cette méthode compte les rotations effectuées et analyse
        les types de rotations dans le sous-arbre.

        :param node: Nœud racine du sous-arbre à analyser
        :type node: AVLNode[T]
        :return: Statistiques de rotation
        :rtype: Dict[str, int]
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot get rotation stats for null node", "get_rotation_stats"
            )

        stats = {
            "total_nodes": 0,
            "balanced_nodes": 0,
            "left_heavy_nodes": 0,
            "right_heavy_nodes": 0,
            "nodes_needing_left_rotation": 0,
            "nodes_needing_right_rotation": 0,
            "nodes_needing_left_right_rotation": 0,
            "nodes_needing_right_left_rotation": 0,
        }

        def collect_stats(n: AVLNode[T]) -> None:
            if n is None:
                return

            stats["total_nodes"] += 1

            if n.is_balanced():
                stats["balanced_nodes"] += 1
            elif n.is_left_heavy():
                stats["left_heavy_nodes"] += 1
            elif n.is_right_heavy():
                stats["right_heavy_nodes"] += 1

            rotation_type = AVLRotations.get_rotation_type(n)
            if rotation_type == "left":
                stats["nodes_needing_left_rotation"] += 1
            elif rotation_type == "right":
                stats["nodes_needing_right_rotation"] += 1
            elif rotation_type == "left_right":
                stats["nodes_needing_left_right_rotation"] += 1
            elif rotation_type == "right_left":
                stats["nodes_needing_right_left_rotation"] += 1

            collect_stats(n.left)
            collect_stats(n.right)

        collect_stats(node)
        return stats

    @staticmethod
    def diagnose_rotation(
        node: AVLNode[T], rotation_type: str
    ) -> Dict[str, Any]:
        """
        Effectue un diagnostic avant une rotation.

        Cette méthode analyse l'état actuel du nœud et prédit
        l'effet de la rotation.

        :param node: Nœud à diagnostiquer
        :type node: AVLNode[T]
        :param rotation_type: Type de rotation à diagnostiquer
        :type rotation_type: str
        :return: Rapport de diagnostic
        :rtype: Dict[str, Any]
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot diagnose rotation for null node", "diagnose_rotation"
            )

        diagnosis = {
            "node_value": node.value,
            "current_state": AVLRotations.analyze_imbalance(node),
            "rotation_type": rotation_type,
            "can_perform_rotation": AVLRotations.validate_before_rotation(
                node, rotation_type
            ),
            "predicted_effect": None,
            "recommendations": [],
        }

        # Prédire l'effet de la rotation
        if diagnosis["can_perform_rotation"]:
            if rotation_type == "left":
                diagnosis["predicted_effect"] = {
                    "new_root": node.right.value if node.right else None,
                    "height_change": "Decrease",
                    "balance_improvement": True,
                }
            elif rotation_type == "right":
                diagnosis["predicted_effect"] = {
                    "new_root": node.left.value if node.left else None,
                    "height_change": "Decrease",
                    "balance_improvement": True,
                }
            elif rotation_type == "left_right":
                diagnosis["predicted_effect"] = {
                    "new_root": (
                        node.left.right.value
                        if node.left and node.left.right
                        else None
                    ),
                    "height_change": "Decrease",
                    "balance_improvement": True,
                }
            elif rotation_type == "right_left":
                diagnosis["predicted_effect"] = {
                    "new_root": (
                        node.right.left.value
                        if node.right and node.right.left
                        else None
                    ),
                    "height_change": "Decrease",
                    "balance_improvement": True,
                }

        # Ajouter des recommandations
        if not diagnosis["can_perform_rotation"]:
            diagnosis["recommendations"].append(
                f"Cannot perform {rotation_type} rotation: "
                f"missing required children"
            )
        else:
            diagnosis["recommendations"].append(
                f"{rotation_type} rotation is safe to perform"
            )

        return diagnosis

    @staticmethod
    def analyze_rotation_performance(node: AVLNode[T]) -> Dict[str, Any]:
        """
        Analyse la performance des rotations sur un nœud.

        Cette méthode mesure le temps d'exécution et analyse
        l'efficacité des rotations.

        :param node: Nœud à analyser
        :type node: AVLNode[T]
        :return: Métriques de performance
        :rtype: Dict[str, Any]
        :raises RotationError: Si le nœud est null
        """
        if node is None:
            raise RotationError(
                "Cannot analyze rotation performance for null node",
                "analyze_rotation_performance",
            )

        performance = {
            "node_value": node.value,
            "rotation_times": {},
            "average_rotation_time": 0.0,
            "fastest_rotation": None,
            "slowest_rotation": None,
            "recommendations": [],
        }

        # Mesurer le temps d'exécution pour chaque type de rotation
        rotation_types = ["left", "right", "left_right", "right_left"]

        for rotation_type in rotation_types:
            if AVLRotations.validate_before_rotation(node, rotation_type):
                # Effectuer plusieurs rotations pour obtenir une moyenne
                times = []
                for _ in range(5):  # 5 itérations pour une moyenne
                    start_time = time.perf_counter()

                    try:
                        if rotation_type == "left":
                            AVLRotations.rotate_left(node)
                        elif rotation_type == "right":
                            AVLRotations.rotate_right(node)
                        elif rotation_type == "left_right":
                            AVLRotations.rotate_left_right(node)
                        elif rotation_type == "right_left":
                            AVLRotations.rotate_right_left(node)

                        end_time = time.perf_counter()
                        times.append(end_time - start_time)
                    except (ValueError, AttributeError):
                        # Ignorer les erreurs de rotation pour les tests de
                        # performance
                        pass

                if times:
                    avg_time = sum(times) / len(times)
                    performance["rotation_times"][rotation_type] = avg_time

        # Calculer les statistiques
        if performance["rotation_times"]:
            times = list(performance["rotation_times"].values())
            performance["average_rotation_time"] = sum(times) / len(times)

            fastest_type = min(
                performance["rotation_times"],
                key=performance["rotation_times"].get,
            )
            slowest_type = max(
                performance["rotation_times"],
                key=performance["rotation_times"].get,
            )

            performance["fastest_rotation"] = fastest_type
            performance["slowest_rotation"] = slowest_type

        # Ajouter des recommandations
        if performance["average_rotation_time"] > 0.001:  # Plus de 1ms
            performance["recommendations"].append(
                "Consider optimizing rotation algorithms for "
                "better performance"
            )
        else:
            performance["recommendations"].append(
                "Rotation performance is acceptable"
            )

        return performance
