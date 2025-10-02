"""
Tests unitaires pour la classe RightLeftRotation.

Ce module contient tous les tests unitaires pour la classe RightLeftRotation.
"""

import pytest
from unittest.mock import patch

from src.baobab_tree.balanced.rotations.right_left_rotation import RightLeftRotation
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.exceptions import (
    InvalidRotationError,
    MissingChildError,
    RotationValidationError,
)


class TestRightLeftRotation:
    """Tests pour la classe RightLeftRotation."""

    def test_init(self):
        """Test de l'initialisation."""
        rotation = RightLeftRotation()
        assert rotation.rotation_type == "right_left"

    def test_can_rotate_with_valid_node(self):
        """Test de can_rotate avec nœud valide."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        result = rotation.can_rotate(node)
        assert result is True

    def test_can_rotate_with_none_node(self):
        """Test de can_rotate avec nœud None."""
        rotation = RightLeftRotation()
        
        result = rotation.can_rotate(None)
        assert result is False

    def test_can_rotate_without_right_child(self):
        """Test de can_rotate sans enfant droit."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        
        result = rotation.can_rotate(node)
        assert result is False

    def test_can_rotate_without_right_child_left_child(self):
        """Test de can_rotate sans enfant gauche de l'enfant droit."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        
        node.set_right(right_child)
        # Pas d'enfant gauche pour right_child
        
        result = rotation.can_rotate(node)
        assert result is False

    def test_can_rotate_with_invalid_node(self):
        """Test de can_rotate avec nœud invalide."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        # Simuler un nœud invalide
        with patch.object(node, 'validate', side_effect=Exception("Invalid node")):
            result = rotation.can_rotate(node)
            assert result is False

    def test_get_description(self):
        """Test de get_description."""
        rotation = RightLeftRotation()
        description = rotation.get_description()
        assert "Rotation droite-gauche" in description
        assert "double rotation" in description

    def test_rotate_success(self):
        """Test de rotation réussie."""
        rotation = RightLeftRotation()
        
        # Créer l'arbre de test
        #    1
        #     \\
        #      2
        #     /
        #    3
        #   / \\
        #  4   5
        root = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        left_great_grandchild = BinaryTreeNode(4)
        right_great_grandchild = BinaryTreeNode(5)
        
        root.set_right(right_child)
        right_child.set_left(left_grandchild)
        left_grandchild.set_left(left_great_grandchild)
        left_grandchild.set_right(right_great_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(root)
        
        # Vérifier la structure après rotation
        #    3
        #   / \\
        #  1   2
        # / \\
        #4   5
        assert new_root.value == 3
        assert new_root.left.value == 1
        assert new_root.right.value == 2
        assert new_root.left.left.value == 4
        assert new_root.left.right.value == 5
        assert new_root.left.parent is new_root
        assert new_root.right.parent is new_root

    def test_rotate_with_parent(self):
        """Test de rotation avec nœud parent."""
        rotation = RightLeftRotation()
        
        # Créer l'arbre de test avec parent
        #    0
        #   /
        #  1
        #   \\
        #    2
        #   /
        #  3
        parent = BinaryTreeNode(0)
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        parent.set_left(node)
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(node)
        
        # Vérifier la structure après rotation
        assert parent.left is new_root
        assert new_root.value == 3
        assert new_root.left.value == 1
        assert new_root.right.value == 2
        assert new_root.parent is parent

    def test_rotate_validation_failure(self):
        """Test de rotation avec échec de validation."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        # Pas d'enfant droit
        
        with pytest.raises(RotationValidationError):
            rotation.rotate(node)

    def test_rotate_missing_right_child(self):
        """Test de rotation avec enfant droit manquant."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        
        # Simuler un nœud sans enfant droit mais qui passe la validation
        with patch.object(rotation, 'validate_before_rotation', return_value=True):
            with pytest.raises(MissingChildError) as exc_info:
                rotation.rotate(node)
            
            assert "Right-left rotation requires a right child" in str(exc_info.value)
            assert exc_info.value.child_type == "right"

    def test_rotate_missing_right_child_left_child(self):
        """Test de rotation avec enfant gauche de l'enfant droit manquant."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        
        node.set_right(right_child)
        # Pas d'enfant gauche pour right_child
        
        # Simuler un nœud qui passe la validation mais échoue sur l'enfant gauche
        with patch.object(rotation, 'validate_before_rotation', return_value=True):
            with pytest.raises(MissingChildError) as exc_info:
                rotation.rotate(node)
            
            assert "Right-left rotation requires right child to have a left child" in str(exc_info.value)
            assert exc_info.value.child_type == "left"

    def test_rotate_post_validation_failure(self):
        """Test de rotation avec échec de validation post-rotation."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        # Simuler un échec de validation post-rotation
        with patch.object(rotation, 'validate_after_rotation', return_value=False):
            with pytest.raises(InvalidRotationError) as exc_info:
                rotation.rotate(node)
            
            assert "Right-left rotation post-validation failed" in str(exc_info.value)

    def test_predict_rotation_effect(self):
        """Test de prédiction de l'effet de rotation."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        prediction = rotation._predict_rotation_effect(node)
        
        assert prediction["new_root"] == 3
        assert prediction["is_double_rotation"] is True
        assert prediction["first_rotation"] == "right"
        assert prediction["second_rotation"] == "left"
        assert prediction["complexity"] == "O(1)"

    def test_predict_rotation_effect_without_required_children(self):
        """Test de prédiction avec nœud sans enfants requis."""
        rotation = RightLeftRotation()
        node = BinaryTreeNode(1)
        
        prediction = rotation._predict_rotation_effect(node)
        
        assert prediction["new_root"] is None
        assert prediction["is_double_rotation"] is True

    def test_str_representation(self):
        """Test de la représentation string."""
        rotation = RightLeftRotation()
        str_repr = str(rotation)
        assert str_repr == "RightLeftRotation()"

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        rotation = RightLeftRotation()
        repr_str = repr(rotation)
        assert repr_str == "RightLeftRotation()"

    def test_rotate_complex_tree(self):
        """Test de rotation sur un arbre complexe."""
        rotation = RightLeftRotation()
        
        # Créer un arbre plus complexe
        #    1
        #     \\
        #      2
        #     /
        #    3
        #   / \\
        #  4   5
        # / \\
        #6   7
        root = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        left_great_grandchild = BinaryTreeNode(4)
        right_great_grandchild = BinaryTreeNode(5)
        left_great_great_grandchild = BinaryTreeNode(6)
        right_great_great_grandchild = BinaryTreeNode(7)
        
        root.set_right(right_child)
        right_child.set_left(left_grandchild)
        left_grandchild.set_left(left_great_grandchild)
        left_grandchild.set_right(right_great_grandchild)
        left_great_grandchild.set_left(left_great_great_grandchild)
        left_great_grandchild.set_right(right_great_great_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(root)
        
        # Vérifier la structure après rotation
        assert new_root.value == 3
        assert new_root.left.value == 1
        assert new_root.right.value == 2
        assert new_root.left.left.value == 4
        assert new_root.left.right.value == 5
        assert new_root.left.left.left.value == 6
        assert new_root.left.left.right.value == 7

    def test_rotate_with_metadata(self):
        """Test de rotation avec métadonnées."""
        rotation = RightLeftRotation()
        
        node = BinaryTreeNode(1, metadata={"test": "value"})
        right_child = BinaryTreeNode(2, metadata={"test2": "value2"})
        left_grandchild = BinaryTreeNode(3, metadata={"test3": "value3"})
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        new_root = rotation.rotate(node)
        
        # Vérifier que les métadonnées sont préservées
        assert new_root.metadata == {"test3": "value3"}
        assert new_root.left.metadata == {"test": "value"}
        assert new_root.right.metadata == {"test2": "value2"}