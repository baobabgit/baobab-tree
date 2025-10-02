"""
Tests unitaires pour la classe RightRotation.

Ce module contient tous les tests unitaires pour la classe RightRotation.
"""

import pytest
from unittest.mock import patch

from src.baobab_tree.balanced.rotations.right_rotation import RightRotation
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.exceptions import (
    InvalidRotationError,
    MissingChildError,
    RotationValidationError,
)


class TestRightRotation:
    """Tests pour la classe RightRotation."""

    def test_init(self):
        """Test de l'initialisation."""
        rotation = RightRotation()
        assert rotation.rotation_type == "right"

    def test_can_rotate_with_valid_node(self):
        """Test de can_rotate avec nœud valide."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        
        result = rotation.can_rotate(node)
        assert result is True

    def test_can_rotate_with_none_node(self):
        """Test de can_rotate avec nœud None."""
        rotation = RightRotation()
        
        result = rotation.can_rotate(None)
        assert result is False

    def test_can_rotate_without_left_child(self):
        """Test de can_rotate sans enfant gauche."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        node.set_right(BinaryTreeNode(2))
        
        result = rotation.can_rotate(node)
        assert result is False

    def test_can_rotate_with_invalid_node(self):
        """Test de can_rotate avec nœud invalide."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        
        # Simuler un nœud invalide
        with patch.object(node, 'validate', side_effect=Exception("Invalid node")):
            result = rotation.can_rotate(node)
            assert result is False

    def test_get_description(self):
        """Test de get_description."""
        rotation = RightRotation()
        description = rotation.get_description()
        assert description == "Rotation droite: l'enfant gauche devient la racine"

    def test_rotate_success(self):
        """Test de rotation réussie."""
        rotation = RightRotation()
        
        # Créer l'arbre de test
        #      1
        #     /
        #    2
        #   / \\
        #  3   4
        root = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        right_grandchild = BinaryTreeNode(4)
        
        root.set_left(left_child)
        left_child.set_left(left_grandchild)
        left_child.set_right(right_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(root)
        
        # Vérifier la structure après rotation
        #    2
        #   / \\
        #  3   1
        #     /
        #    4
        assert new_root.value == 2
        assert new_root.left.value == 3
        assert new_root.right.value == 1
        assert new_root.right.left.value == 4
        assert new_root.left.parent is new_root
        assert new_root.right.parent is new_root

    def test_rotate_with_parent(self):
        """Test de rotation avec nœud parent."""
        rotation = RightRotation()
        
        # Créer l'arbre de test avec parent
        #    0
        #     \\
        #      1
        #     /
        #    2
        parent = BinaryTreeNode(0)
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        
        parent.set_right(node)
        node.set_left(left_child)
        
        # Effectuer la rotation
        new_root = rotation.rotate(node)
        
        # Vérifier la structure après rotation
        assert parent.right is new_root
        assert new_root.value == 2
        assert new_root.right.value == 1
        assert new_root.parent is parent

    def test_rotate_validation_failure(self):
        """Test de rotation avec échec de validation."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        # Pas d'enfant gauche
        
        with pytest.raises(RotationValidationError):
            rotation.rotate(node)

    def test_rotate_missing_left_child(self):
        """Test de rotation avec enfant gauche manquant."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        
        # Simuler un nœud sans enfant gauche mais qui passe la validation
        with patch.object(rotation, 'validate_before_rotation', return_value=True):
            with pytest.raises(MissingChildError) as exc_info:
                rotation.rotate(node)
            
            assert "Right rotation requires a left child" in str(exc_info.value)
            assert exc_info.value.child_type == "left"

    def test_rotate_post_validation_failure(self):
        """Test de rotation avec échec de validation post-rotation."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        
        # Simuler un échec de validation post-rotation
        with patch.object(rotation, 'validate_after_rotation', return_value=False):
            with pytest.raises(InvalidRotationError) as exc_info:
                rotation.rotate(node)
            
            assert "Right rotation post-validation failed" in str(exc_info.value)

    def test_predict_rotation_effect(self):
        """Test de prédiction de l'effet de rotation."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        
        prediction = rotation._predict_rotation_effect(node)
        
        assert prediction["new_root"] == 2
        assert prediction["old_root_becomes_right_child"] is True
        assert prediction["left_subtree_height_decreases"] is True
        assert prediction["right_subtree_height_increases"] is True

    def test_predict_rotation_effect_without_left_child(self):
        """Test de prédiction avec nœud sans enfant gauche."""
        rotation = RightRotation()
        node = BinaryTreeNode(1)
        
        prediction = rotation._predict_rotation_effect(node)
        
        assert prediction["new_root"] is None
        assert prediction["old_root_becomes_right_child"] is True

    def test_str_representation(self):
        """Test de la représentation string."""
        rotation = RightRotation()
        str_repr = str(rotation)
        assert str_repr == "RightRotation()"

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        rotation = RightRotation()
        repr_str = repr(rotation)
        assert repr_str == "RightRotation()"

    def test_rotate_complex_tree(self):
        """Test de rotation sur un arbre complexe."""
        rotation = RightRotation()
        
        # Créer un arbre plus complexe
        #        1
        #       /
        #      2
        #     / \\
        #    3   4
        #   / \\
        #  5   6
        root = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        right_grandchild = BinaryTreeNode(4)
        left_great_grandchild = BinaryTreeNode(5)
        right_great_grandchild = BinaryTreeNode(6)
        
        root.set_left(left_child)
        left_child.set_left(left_grandchild)
        left_child.set_right(right_grandchild)
        left_grandchild.set_left(left_great_grandchild)
        left_grandchild.set_right(right_great_grandchild)
        
        # Effectuer la rotation
        new_root = rotation.rotate(root)
        
        # Vérifier la structure après rotation
        assert new_root.value == 2
        assert new_root.left.value == 3
        assert new_root.right.value == 1
        assert new_root.left.left.value == 5
        assert new_root.left.right.value == 6
        assert new_root.right.left.value == 4

    def test_rotate_with_metadata(self):
        """Test de rotation avec métadonnées."""
        rotation = RightRotation()
        
        node = BinaryTreeNode(1, metadata={"test": "value"})
        left_child = BinaryTreeNode(2, metadata={"test2": "value2"})
        node.set_left(left_child)
        
        new_root = rotation.rotate(node)
        
        # Vérifier que les métadonnées sont préservées
        assert new_root.metadata == {"test2": "value2"}
        assert new_root.right.metadata == {"test": "value"}