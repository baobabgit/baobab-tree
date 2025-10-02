"""
Tests unitaires pour la classe LeftRightRotation.

Ce module contient tous les tests unitaires pour la classe LeftRightRotation.
"""

import pytest
from unittest.mock import patch

from src.baobab_tree.balanced.rotations.left_right_rotation import LeftRightRotation
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.exceptions import (
    InvalidRotationError,
    MissingChildError,
    RotationValidationError,
)


class TestLeftRightRotation:
    """Tests pour la classe LeftRightRotation."""

    def test_init(self):
        """Test de l'initialisation."""
        rotation = LeftRightRotation()
        assert rotation.rotation_type == "left_right"

    def test_can_rotate_with_valid_node(self):
        """Test de can_rotate avec nœud valide."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        result = rotation.can_rotate(node)
        assert result is True

    def test_can_rotate_with_none_node(self):
        """Test de can_rotate avec nœud None."""
        rotation = LeftRightRotation()
        
        result = rotation.can_rotate(None)
        assert result is False

    def test_can_rotate_without_left_child(self):
        """Test de can_rotate sans enfant gauche."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        node.set_right(BinaryTreeNode(2))
        
        result = rotation.can_rotate(node)
        assert result is False

    def test_can_rotate_without_left_child_right_child(self):
        """Test de can_rotate sans enfant droit de l'enfant gauche."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        
        node.set_left(left_child)
        # Pas d'enfant droit pour left_child
        
        result = rotation.can_rotate(node)
        assert result is False

    def test_can_rotate_with_invalid_node(self):
        """Test de can_rotate avec nœud invalide."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        # Simuler un nœud invalide
        with patch.object(node, 'validate', side_effect=Exception("Invalid node")):
            result = rotation.can_rotate(node)
            assert result is False

    def test_get_description(self):
        """Test de get_description."""
        rotation = LeftRightRotation()
        description = rotation.get_description()
        assert "Rotation gauche-droite" in description
        assert "double rotation" in description

    def test_rotate_success(self):
        """Test de rotation réussie."""
        rotation = LeftRightRotation()
        
        # Créer l'arbre de test
        #      1
        #     /
        #    2
        #     \\
        #      3
        #     / \\
        #    4   5
        root = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        left_great_grandchild = BinaryTreeNode(4)
        right_great_grandchild = BinaryTreeNode(5)
        
        root.set_left(left_child)
        left_child.set_right(right_grandchild)
        right_grandchild.set_left(left_great_grandchild)
        right_grandchild.set_right(right_great_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(root)
        
        # Vérifier la structure après rotation
        #    3
        #   / \\
        #  2   1
        # / \\
        #4   5
        assert new_root.value == 3
        assert new_root.left.value == 2
        assert new_root.right.value == 1
        assert new_root.left.left.value == 4
        assert new_root.left.right.value == 5
        assert new_root.left.parent is new_root
        assert new_root.right.parent is new_root

    def test_rotate_with_parent(self):
        """Test de rotation avec nœud parent."""
        rotation = LeftRightRotation()
        
        # Créer l'arbre de test avec parent
        #    0
        #     \\
        #      1
        #     /
        #    2
        #     \\
        #      3
        parent = BinaryTreeNode(0)
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        parent.set_right(node)
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(node)
        
        # Vérifier la structure après rotation
        assert parent.right is new_root
        assert new_root.value == 3
        assert new_root.left.value == 2
        assert new_root.right.value == 1
        assert new_root.parent is parent

    def test_rotate_validation_failure(self):
        """Test de rotation avec échec de validation."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        # Pas d'enfant gauche
        
        with pytest.raises(RotationValidationError):
            rotation.rotate(node)

    def test_rotate_missing_left_child(self):
        """Test de rotation avec enfant gauche manquant."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        
        # Simuler un nœud sans enfant gauche mais qui passe la validation
        with patch.object(rotation, 'validate_before_rotation', return_value=True):
            with pytest.raises(MissingChildError) as exc_info:
                rotation.rotate(node)
            
            assert "Left-right rotation requires a left child" in str(exc_info.value)
            assert exc_info.value.child_type == "left"

    def test_rotate_missing_left_child_right_child(self):
        """Test de rotation avec enfant droit de l'enfant gauche manquant."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        
        node.set_left(left_child)
        # Pas d'enfant droit pour left_child
        
        # Simuler un nœud qui passe la validation mais échoue sur l'enfant droit
        with patch.object(rotation, 'validate_before_rotation', return_value=True):
            with pytest.raises(MissingChildError) as exc_info:
                rotation.rotate(node)
            
            assert "Left-right rotation requires left child to have a right child" in str(exc_info.value)
            assert exc_info.value.child_type == "right"

    def test_rotate_post_validation_failure(self):
        """Test de rotation avec échec de validation post-rotation."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        # Simuler un échec de validation post-rotation
        with patch.object(rotation, 'validate_after_rotation', return_value=False):
            with pytest.raises(InvalidRotationError) as exc_info:
                rotation.rotate(node)
            
            assert "Left-right rotation post-validation failed" in str(exc_info.value)

    def test_predict_rotation_effect(self):
        """Test de prédiction de l'effet de rotation."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        prediction = rotation._predict_rotation_effect(node)
        
        assert prediction["new_root"] == 3
        assert prediction["is_double_rotation"] is True
        assert prediction["first_rotation"] == "left"
        assert prediction["second_rotation"] == "right"
        assert prediction["complexity"] == "O(1)"

    def test_predict_rotation_effect_without_required_children(self):
        """Test de prédiction avec nœud sans enfants requis."""
        rotation = LeftRightRotation()
        node = BinaryTreeNode(1)
        
        prediction = rotation._predict_rotation_effect(node)
        
        assert prediction["new_root"] is None
        assert prediction["is_double_rotation"] is True

    def test_str_representation(self):
        """Test de la représentation string."""
        rotation = LeftRightRotation()
        str_repr = str(rotation)
        assert str_repr == "LeftRightRotation()"

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        rotation = LeftRightRotation()
        repr_str = repr(rotation)
        assert repr_str == "LeftRightRotation()"

    def test_rotate_complex_tree(self):
        """Test de rotation sur un arbre complexe."""
        rotation = LeftRightRotation()
        
        # Créer un arbre plus complexe
        #        1
        #       /
        #      2
        #       \\
        #        3
        #       / \\
        #      4   5
        #     / \\
        #    6   7
        root = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        left_great_grandchild = BinaryTreeNode(4)
        right_great_grandchild = BinaryTreeNode(5)
        left_great_great_grandchild = BinaryTreeNode(6)
        right_great_great_grandchild = BinaryTreeNode(7)
        
        root.set_left(left_child)
        left_child.set_right(right_grandchild)
        right_grandchild.set_left(left_great_grandchild)
        right_grandchild.set_right(right_great_grandchild)
        left_great_grandchild.set_left(left_great_great_grandchild)
        left_great_grandchild.set_right(right_great_great_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(root)
        
        # Vérifier la structure après rotation
        assert new_root.value == 3
        assert new_root.left.value == 2
        assert new_root.right.value == 1
        assert new_root.left.left.value == 4
        assert new_root.left.right.value == 5
        assert new_root.left.left.left.value == 6
        assert new_root.left.left.right.value == 7

    def test_rotate_with_metadata(self):
        """Test de rotation avec métadonnées."""
        rotation = LeftRightRotation()
        
        node = BinaryTreeNode(1, metadata={"test": "value"})
        left_child = BinaryTreeNode(2, metadata={"test2": "value2"})
        right_grandchild = BinaryTreeNode(3, metadata={"test3": "value3"})
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        new_root = rotation.rotate(node)
        
        # Vérifier que les métadonnées sont préservées
        assert new_root.metadata == {"test3": "value3"}
        assert new_root.left.metadata == {"test2": "value2"}
        assert new_root.right.metadata == {"test": "value"}