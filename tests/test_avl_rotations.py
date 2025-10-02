"""
Tests unitaires pour la classe AVLRotations.

Ce module contient tous les tests unitaires pour la classe AVLRotations,
incluant les tests de rotation simple, double et de validation.
"""

import pytest
from src.baobab_tree.balanced.avl_node import AVLNode
from src.baobab_tree.balanced.avl_rotations import AVLRotations
from src.baobab_tree.core.exceptions import RotationError


class TestAVLRotations:
    """Tests pour la classe AVLRotations."""

    def test_rotate_left_success(self):
        """Test de rotation gauche réussie."""
        # Créer un arbre déséquilibré vers la droite
        root = AVLNode(50)
        right_child = AVLNode(70)
        right_left_child = AVLNode(60)
        right_right_child = AVLNode(80)

        root.set_right(right_child)
        right_child.set_left(right_left_child)
        right_child.set_right(right_right_child)

        # Effectuer la rotation gauche
        new_root = AVLRotations.rotate_left(root)

        # Vérifier le résultat
        assert new_root is right_child
        assert new_root.left is root
        assert new_root.right is right_right_child
        assert root.right is right_left_child
        assert root.parent is right_child

    def test_rotate_left_with_null_node(self):
        """Test de rotation gauche avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_left(None)

        assert "Cannot rotate a null node" in str(exc_info.value)

    def test_rotate_left_without_right_child(self):
        """Test de rotation gauche sans enfant droit."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))

        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_left(node)

        assert "Cannot perform left rotation: node has no right child" in str(
            exc_info.value
        )

    def test_rotate_right_success(self):
        """Test de rotation droite réussie."""
        # Créer un arbre déséquilibré vers la gauche
        root = AVLNode(50)
        left_child = AVLNode(30)
        left_left_child = AVLNode(20)
        left_right_child = AVLNode(40)

        root.set_left(left_child)
        left_child.set_left(left_left_child)
        left_child.set_right(left_right_child)

        # Effectuer la rotation droite
        new_root = AVLRotations.rotate_right(root)

        # Vérifier le résultat
        assert new_root is left_child
        assert new_root.right is root
        assert new_root.left is left_left_child
        assert root.left is left_right_child
        assert root.parent is left_child

    def test_rotate_right_with_null_node(self):
        """Test de rotation droite avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_right(None)

        assert "Cannot rotate a null node" in str(exc_info.value)

    def test_rotate_right_without_left_child(self):
        """Test de rotation droite sans enfant gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))

        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_right(node)

        assert "Cannot perform right rotation: node has no left child" in str(
            exc_info.value
        )

    def test_rotate_left_right_success(self):
        """Test de rotation gauche-droite réussie."""
        # Créer un arbre avec déséquilibre gauche-droite
        root = AVLNode(50)
        left_child = AVLNode(30)
        left_right_child = AVLNode(40)
        left_right_left_child = AVLNode(35)
        left_right_right_child = AVLNode(45)

        root.set_left(left_child)
        left_child.set_right(left_right_child)
        left_right_child.set_left(left_right_left_child)
        left_right_child.set_right(left_right_right_child)

        # Effectuer la rotation gauche-droite
        new_root = AVLRotations.rotate_left_right(root)

        # Vérifier le résultat
        assert new_root is left_right_child
        assert new_root.left is left_child
        assert new_root.right is root
        assert left_child.right is left_right_left_child
        assert root.left is left_right_right_child

    def test_rotate_left_right_with_null_node(self):
        """Test de rotation gauche-droite avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_left_right(None)

        assert "Cannot rotate a null node" in str(exc_info.value)

    def test_rotate_left_right_without_left_child(self):
        """Test de rotation gauche-droite sans enfant gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))

        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_left_right(node)

        assert "Cannot perform left-right rotation: node has no left child" in str(
            exc_info.value
        )

    def test_rotate_right_left_success(self):
        """Test de rotation droite-gauche réussie."""
        # Créer un arbre avec déséquilibre droite-gauche
        root = AVLNode(50)
        right_child = AVLNode(70)
        right_left_child = AVLNode(60)
        right_left_left_child = AVLNode(55)
        right_left_right_child = AVLNode(65)

        root.set_right(right_child)
        right_child.set_left(right_left_child)
        right_left_child.set_left(right_left_left_child)
        right_left_child.set_right(right_left_right_child)

        # Effectuer la rotation droite-gauche
        new_root = AVLRotations.rotate_right_left(root)

        # Vérifier le résultat
        assert new_root is right_left_child
        assert new_root.left is root
        assert new_root.right is right_child
        assert root.right is right_left_left_child
        assert right_child.left is right_left_right_child

    def test_rotate_right_left_with_null_node(self):
        """Test de rotation droite-gauche avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_right_left(None)

        assert "Cannot rotate a null node" in str(exc_info.value)

    def test_rotate_right_left_without_right_child(self):
        """Test de rotation droite-gauche sans enfant droit."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))

        with pytest.raises(RotationError) as exc_info:
            AVLRotations.rotate_right_left(node)

        assert "Cannot perform right-left rotation: node has no right child" in str(
            exc_info.value
        )

    def test_get_rotation_type_balanced(self):
        """Test de détermination du type de rotation pour un nœud équilibré."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        rotation_type = AVLRotations.get_rotation_type(node)
        assert rotation_type == "none"

    def test_get_rotation_type_left(self):
        """Test de détermination du type de rotation gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_right(AVLNode(80))

        rotation_type = AVLRotations.get_rotation_type(node)
        assert rotation_type == "left"

    def test_get_rotation_type_right(self):
        """Test de détermination du type de rotation droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_left(AVLNode(20))

        rotation_type = AVLRotations.get_rotation_type(node)
        assert rotation_type == "right"

    def test_get_rotation_type_left_right(self):
        """Test de détermination du type de rotation gauche-droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_right(AVLNode(40))
        node.left.right.set_right(AVLNode(45))

        rotation_type = AVLRotations.get_rotation_type(node)
        assert rotation_type == "left_right"

    def test_get_rotation_type_right_left(self):
        """Test de détermination du type de rotation droite-gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_left(AVLNode(60))
        node.right.left.set_left(AVLNode(55))

        rotation_type = AVLRotations.get_rotation_type(node)
        assert rotation_type == "right_left"

    def test_get_rotation_type_with_null_node(self):
        """Test de détermination du type de rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.get_rotation_type(None)

        assert "Cannot determine rotation type for null node" in str(exc_info.value)

    def test_perform_rotation_left(self):
        """Test de performance de rotation gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_right(AVLNode(80))

        new_root = AVLRotations.perform_rotation(node)
        assert new_root is node.right
        assert new_root.left is node

    def test_perform_rotation_right(self):
        """Test de performance de rotation droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_left(AVLNode(20))

        new_root = AVLRotations.perform_rotation(node)
        assert new_root is node.left
        assert new_root.right is node

    def test_perform_rotation_left_right(self):
        """Test de performance de rotation gauche-droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_right(AVLNode(40))
        node.left.right.set_right(AVLNode(45))

        new_root = AVLRotations.perform_rotation(node)
        assert new_root is node.left.right
        assert new_root.left is node.left
        assert new_root.right is node

    def test_perform_rotation_right_left(self):
        """Test de performance de rotation droite-gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_left(AVLNode(60))
        node.right.left.set_left(AVLNode(55))

        new_root = AVLRotations.perform_rotation(node)
        assert new_root is node.right.left
        assert new_root.left is node
        assert new_root.right is node.right

    def test_perform_rotation_none(self):
        """Test de performance de rotation quand aucune n'est nécessaire."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        new_root = AVLRotations.perform_rotation(node)
        assert new_root is node

    def test_perform_rotation_with_null_node(self):
        """Test de performance de rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.perform_rotation(None)

        assert "Cannot perform rotation on null node" in str(exc_info.value)

    def test_validate_rotation_result_success(self):
        """Test de validation de résultat de rotation réussie."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        result = AVLRotations.validate_rotation_result(node)
        assert result is True

    def test_validate_rotation_result_with_null_node(self):
        """Test de validation de résultat de rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.validate_rotation_result(None)

        assert "Cannot validate rotation result for null node" in str(exc_info.value)

    def test_validate_rotation_result_with_invalid_node(self):
        """Test de validation de résultat de rotation avec nœud invalide."""
        node = AVLNode(50)
        # Forcer un état invalide
        node._balance_factor = 2

        with pytest.raises(RotationError) as exc_info:
            AVLRotations.validate_rotation_result(node)

        assert "Rotation validation failed" in str(exc_info.value)

    def test_complex_rotation_sequence(self):
        """Test d'une séquence complexe de rotations."""
        # Créer un arbre déséquilibré
        root = AVLNode(50)
        root.set_right(AVLNode(70))
        root.right.set_right(AVLNode(80))
        root.right.right.set_right(AVLNode(90))

        # Effectuer une rotation gauche
        new_root = AVLRotations.rotate_left(root)
        assert new_root.value == 70
        assert new_root.left.value == 50
        assert new_root.right.value == 80

        # Vérifier que l'arbre est maintenant équilibré
        assert new_root.is_balanced()
        assert new_root.left.is_balanced()
        assert new_root.right.is_balanced()

    def test_rotation_preserves_values(self):
        """Test que les rotations préservent les valeurs."""
        # Créer un arbre avec des valeurs spécifiques
        root = AVLNode(50)
        left = AVLNode(30)
        right = AVLNode(70)
        left_left = AVLNode(20)
        left_right = AVLNode(40)

        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        # Effectuer une rotation droite
        new_root = AVLRotations.rotate_right(root)

        # Vérifier que toutes les valeurs sont préservées
        values = []

        def collect_values(node):
            if node:
                values.append(node.value)
                collect_values(node.left)
                collect_values(node.right)

        collect_values(new_root)
        assert set(values) == {50, 30, 70, 20, 40}

    def test_rotation_updates_parent_references(self):
        """Test que les rotations mettent à jour les références parent."""
        root = AVLNode(50)
        right_child = AVLNode(70)
        right_left_child = AVLNode(60)

        root.set_right(right_child)
        right_child.set_left(right_left_child)

        # Effectuer une rotation gauche
        new_root = AVLRotations.rotate_left(root)

        # Vérifier les références parent
        assert new_root.parent is None  # Nouvelle racine
        assert root.parent is new_root
        assert right_left_child.parent is root
        assert right_child.right.parent is new_root

    def test_rotation_with_parent(self):
        """Test de rotation avec un nœud qui a un parent."""
        grandparent = AVLNode(100)
        parent = AVLNode(50)
        child = AVLNode(30)
        grandchild = AVLNode(20)

        grandparent.set_left(parent)
        parent.set_left(child)
        child.set_left(grandchild)

        # Effectuer une rotation droite sur parent
        new_parent = AVLRotations.rotate_right(parent)

        # Vérifier que grandparent pointe vers le nouveau parent
        assert grandparent.left is new_parent
        assert new_parent.parent is grandparent
        assert new_parent.right is parent
        assert parent.parent is new_parent

    def test_select_rotation_left(self):
        """Test de sélection de rotation gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_right(AVLNode(80))

        rotation_func = AVLRotations.select_rotation(node)
        assert rotation_func == AVLRotations.rotate_left

    def test_select_rotation_right(self):
        """Test de sélection de rotation droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_left(AVLNode(20))

        rotation_func = AVLRotations.select_rotation(node)
        assert rotation_func == AVLRotations.rotate_right

    def test_select_rotation_left_right(self):
        """Test de sélection de rotation gauche-droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_right(AVLNode(40))
        node.left.right.set_right(AVLNode(45))

        rotation_func = AVLRotations.select_rotation(node)
        assert rotation_func == AVLRotations.rotate_left_right

    def test_select_rotation_right_left(self):
        """Test de sélection de rotation droite-gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_left(AVLNode(60))
        node.right.left.set_left(AVLNode(55))

        rotation_func = AVLRotations.select_rotation(node)
        assert rotation_func == AVLRotations.rotate_right_left

    def test_select_rotation_none(self):
        """Test de sélection de rotation quand aucune n'est nécessaire."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        rotation_func = AVLRotations.select_rotation(node)
        # Devrait retourner une fonction identité
        result = rotation_func(node)
        assert result is node

    def test_select_rotation_with_null_node(self):
        """Test de sélection de rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.select_rotation(None)

        assert "Cannot select rotation for null node" in str(exc_info.value)

    def test_analyze_imbalance_balanced(self):
        """Test d'analyse de déséquilibre pour un nœud équilibré."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        analysis = AVLRotations.analyze_imbalance(node)
        
        assert analysis["node_value"] == 50
        assert analysis["balance_factor"] == 0
        assert analysis["is_balanced"] is True
        assert analysis["rotation_type"] == "none"
        assert analysis["left_child_info"] is not None
        assert analysis["right_child_info"] is not None

    def test_analyze_imbalance_left_heavy(self):
        """Test d'analyse de déséquilibre pour un nœud déséquilibré à gauche."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_left(AVLNode(20))

        analysis = AVLRotations.analyze_imbalance(node)
        
        assert analysis["node_value"] == 50
        assert analysis["is_left_heavy"] is True
        assert analysis["rotation_type"] == "right"
        assert analysis["left_child_info"] is not None
        assert analysis["right_child_info"] is None

    def test_analyze_imbalance_right_heavy(self):
        """Test d'analyse de déséquilibre pour un nœud déséquilibré à droite."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_right(AVLNode(80))

        analysis = AVLRotations.analyze_imbalance(node)
        
        assert analysis["node_value"] == 50
        assert analysis["is_right_heavy"] is True
        assert analysis["rotation_type"] == "left"
        assert analysis["left_child_info"] is None
        assert analysis["right_child_info"] is not None

    def test_analyze_imbalance_with_null_node(self):
        """Test d'analyse de déséquilibre avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.analyze_imbalance(None)

        assert "Cannot analyze imbalance for null node" in str(exc_info.value)

    def test_validate_before_rotation_left(self):
        """Test de validation pré-rotation gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))

        assert AVLRotations.validate_before_rotation(node, "left") is True

    def test_validate_before_rotation_right(self):
        """Test de validation pré-rotation droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))

        assert AVLRotations.validate_before_rotation(node, "right") is True

    def test_validate_before_rotation_left_right(self):
        """Test de validation pré-rotation gauche-droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.left.set_right(AVLNode(40))

        assert AVLRotations.validate_before_rotation(node, "left_right") is True

    def test_validate_before_rotation_right_left(self):
        """Test de validation pré-rotation droite-gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))
        node.right.set_left(AVLNode(60))

        assert AVLRotations.validate_before_rotation(node, "right_left") is True

    def test_validate_before_rotation_invalid(self):
        """Test de validation pré-rotation invalide."""
        node = AVLNode(50)

        assert AVLRotations.validate_before_rotation(node, "left") is False
        assert AVLRotations.validate_before_rotation(node, "right") is False

    def test_validate_before_rotation_with_null_node(self):
        """Test de validation pré-rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.validate_before_rotation(None, "left")

        assert "Cannot validate rotation for null node" in str(exc_info.value)

    def test_validate_after_rotation_valid(self):
        """Test de validation post-rotation valide."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        assert AVLRotations.validate_after_rotation(node) is True

    def test_validate_after_rotation_invalid(self):
        """Test de validation post-rotation invalide."""
        node = AVLNode(50)
        # Créer un état invalide en cassant les références parent
        left_child = AVLNode(30)
        node.set_left(left_child)
        left_child.parent = None  # Casser la référence parent

        assert AVLRotations.validate_after_rotation(node) is False

    def test_validate_after_rotation_with_null_node(self):
        """Test de validation post-rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.validate_after_rotation(None)

        assert "Cannot validate rotation result for null node" in str(exc_info.value)

    def test_update_avl_properties(self):
        """Test de mise à jour des propriétés AVL."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        # Forcer un état incohérent
        node._balance_factor = 999

        AVLRotations.update_avl_properties(node)

        # Vérifier que les propriétés ont été mises à jour
        assert node.get_balance_factor() == 0

    def test_update_avl_properties_with_parent(self):
        """Test de mise à jour des propriétés AVL avec parent."""
        parent = AVLNode(100)
        child = AVLNode(50)
        parent.set_left(child)

        # Forcer un état incohérent
        parent._balance_factor = 999
        child._balance_factor = 999

        AVLRotations.update_avl_properties(child)

        # Vérifier que les propriétés ont été mises à jour pour l'enfant et le parent
        assert child.get_balance_factor() == 0
        assert parent.get_balance_factor() == 1  # Parent avec un enfant gauche

    def test_update_avl_properties_with_null_node(self):
        """Test de mise à jour des propriétés AVL avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.update_avl_properties(None)

        assert "Cannot update AVL properties for null node" in str(exc_info.value)

    def test_update_parent_references(self):
        """Test de mise à jour des références parent."""
        grandparent = AVLNode(100)
        old_root = AVLNode(50)
        new_root = AVLNode(70)

        grandparent.set_left(old_root)
        old_root.set_right(new_root)

        AVLRotations.update_parent_references(old_root, new_root)

        # Vérifier que grandparent pointe maintenant vers new_root
        assert grandparent.left is new_root
        assert new_root.parent is grandparent

    def test_update_parent_references_root_node(self):
        """Test de mise à jour des références parent pour un nœud racine."""
        old_root = AVLNode(50)
        new_root = AVLNode(70)

        old_root.set_right(new_root)

        AVLRotations.update_parent_references(old_root, new_root)

        # Vérifier que new_root n'a plus de parent (est devenu la racine)
        assert new_root.parent is None

    def test_update_parent_references_with_null_nodes(self):
        """Test de mise à jour des références parent avec nœuds null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.update_parent_references(None, None)

        assert "Cannot update parent references for null nodes" in str(exc_info.value)

    def test_get_rotation_stats(self):
        """Test de récupération des statistiques de rotation."""
        root = AVLNode(50)
        root.set_left(AVLNode(30))
        root.set_right(AVLNode(70))
        root.left.set_left(AVLNode(20))
        root.right.set_right(AVLNode(80))

        stats = AVLRotations.get_rotation_stats(root)

        assert stats["total_nodes"] == 5
        assert stats["balanced_nodes"] >= 0
        assert stats["left_heavy_nodes"] >= 0
        assert stats["right_heavy_nodes"] >= 0
        assert "nodes_needing_left_rotation" in stats
        assert "nodes_needing_right_rotation" in stats
        assert "nodes_needing_left_right_rotation" in stats
        assert "nodes_needing_right_left_rotation" in stats

    def test_get_rotation_stats_single_node(self):
        """Test de récupération des statistiques de rotation pour un seul nœud."""
        node = AVLNode(50)

        stats = AVLRotations.get_rotation_stats(node)

        assert stats["total_nodes"] == 1
        assert stats["balanced_nodes"] == 1
        assert stats["left_heavy_nodes"] == 0
        assert stats["right_heavy_nodes"] == 0

    def test_get_rotation_stats_with_null_node(self):
        """Test de récupération des statistiques de rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.get_rotation_stats(None)

        assert "Cannot get rotation stats for null node" in str(exc_info.value)

    def test_diagnose_rotation_left(self):
        """Test de diagnostic de rotation gauche."""
        node = AVLNode(50)
        node.set_right(AVLNode(70))

        diagnosis = AVLRotations.diagnose_rotation(node, "left")

        assert diagnosis["node_value"] == 50
        assert diagnosis["rotation_type"] == "left"
        assert diagnosis["can_perform_rotation"] is True
        assert diagnosis["predicted_effect"] is not None
        assert diagnosis["predicted_effect"]["new_root"] == 70
        assert diagnosis["predicted_effect"]["balance_improvement"] is True
        assert len(diagnosis["recommendations"]) > 0

    def test_diagnose_rotation_right(self):
        """Test de diagnostic de rotation droite."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))

        diagnosis = AVLRotations.diagnose_rotation(node, "right")

        assert diagnosis["node_value"] == 50
        assert diagnosis["rotation_type"] == "right"
        assert diagnosis["can_perform_rotation"] is True
        assert diagnosis["predicted_effect"] is not None
        assert diagnosis["predicted_effect"]["new_root"] == 30
        assert diagnosis["predicted_effect"]["balance_improvement"] is True

    def test_diagnose_rotation_invalid(self):
        """Test de diagnostic de rotation invalide."""
        node = AVLNode(50)

        diagnosis = AVLRotations.diagnose_rotation(node, "left")

        assert diagnosis["node_value"] == 50
        assert diagnosis["rotation_type"] == "left"
        assert diagnosis["can_perform_rotation"] is False
        assert diagnosis["predicted_effect"] is None
        assert "Cannot perform left rotation" in diagnosis["recommendations"][0]

    def test_diagnose_rotation_with_null_node(self):
        """Test de diagnostic de rotation avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.diagnose_rotation(None, "left")

        assert "Cannot diagnose rotation for null node" in str(exc_info.value)

    def test_analyze_rotation_performance(self):
        """Test d'analyse de performance des rotations."""
        node = AVLNode(50)
        node.set_left(AVLNode(30))
        node.set_right(AVLNode(70))

        performance = AVLRotations.analyze_rotation_performance(node)

        assert performance["node_value"] == 50
        assert "rotation_times" in performance
        assert "average_rotation_time" in performance
        assert "fastest_rotation" in performance
        assert "slowest_rotation" in performance
        assert "recommendations" in performance
        assert len(performance["recommendations"]) > 0

    def test_analyze_rotation_performance_with_null_node(self):
        """Test d'analyse de performance des rotations avec nœud null."""
        with pytest.raises(RotationError) as exc_info:
            AVLRotations.analyze_rotation_performance(None)

        assert "Cannot analyze rotation performance for null node" in str(exc_info.value)

    def test_complex_rotation_workflow(self):
        """Test d'un workflow complexe de rotation."""
        # Créer un arbre déséquilibré
        root = AVLNode(50)
        root.set_right(AVLNode(70))
        root.right.set_right(AVLNode(80))
        root.right.right.set_right(AVLNode(90))

        # Analyser le déséquilibre
        analysis = AVLRotations.analyze_imbalance(root)
        assert analysis["rotation_type"] == "left"

        # Diagnostiquer la rotation
        diagnosis = AVLRotations.diagnose_rotation(root, "left")
        assert diagnosis["can_perform_rotation"] is True

        # Valider avant rotation
        assert AVLRotations.validate_before_rotation(root, "left") is True

        # Effectuer la rotation
        new_root = AVLRotations.rotate_left(root)

        # Valider après rotation
        assert AVLRotations.validate_after_rotation(new_root) is True

        # Vérifier les statistiques
        stats = AVLRotations.get_rotation_stats(new_root)
        assert stats["total_nodes"] == 4

        # Analyser la performance
        performance = AVLRotations.analyze_rotation_performance(new_root)
        assert performance["node_value"] == 70  # Nouvelle racine

    def test_rotation_error_handling(self):
        """Test de gestion d'erreurs dans les rotations."""
        # Test avec nœud null
        with pytest.raises(RotationError):
            AVLRotations.rotate_left(None)

        with pytest.raises(RotationError):
            AVLRotations.rotate_right(None)

        with pytest.raises(RotationError):
            AVLRotations.rotate_left_right(None)

        with pytest.raises(RotationError):
            AVLRotations.rotate_right_left(None)

        # Test avec enfants manquants
        node = AVLNode(50)
        with pytest.raises(RotationError):
            AVLRotations.rotate_left(node)

        with pytest.raises(RotationError):
            AVLRotations.rotate_right(node)

    def test_rotation_preserves_tree_structure(self):
        """Test que les rotations préservent la structure de l'arbre."""
        # Créer un arbre complexe
        root = AVLNode(50)
        root.set_left(AVLNode(30))
        root.set_right(AVLNode(70))
        root.left.set_left(AVLNode(20))
        root.left.set_right(AVLNode(40))
        root.right.set_left(AVLNode(60))
        root.right.set_right(AVLNode(80))

        # Collecter toutes les valeurs avant rotation
        values_before = []

        def collect_values(node):
            if node:
                values_before.append(node.value)
                collect_values(node.left)
                collect_values(node.right)

        collect_values(root)

        # Effectuer une rotation droite
        new_root = AVLRotations.rotate_right(root)

        # Collecter toutes les valeurs après rotation
        values_after = []
        collect_values(new_root)

        # Vérifier que toutes les valeurs sont préservées
        assert set(values_before) == set(values_after)
        assert len(values_before) == len(values_after)
