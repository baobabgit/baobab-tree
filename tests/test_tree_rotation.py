"""
Tests unitaires pour la classe TreeRotation.

Ce module contient tous les tests unitaires pour la classe abstraite TreeRotation
et ses fonctionnalités communes.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_tree.balanced.rotations.tree_rotation import TreeRotation
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.exceptions import (
    RotationValidationError,
    TreeRotationError,
)


class ConcreteTreeRotation(TreeRotation):
    """Classe concrète pour tester TreeRotation."""
    
    def __init__(self):
        super().__init__("test")
    
    def rotate(self, node):
        return node
    
    def can_rotate(self, node):
        return node is not None and node.has_left()
    
    def get_description(self):
        return "Test rotation"


class TestTreeRotation:
    """Tests pour la classe TreeRotation."""

    def test_init(self):
        """Test de l'initialisation."""
        rotation = ConcreteTreeRotation()
        assert rotation.rotation_type == "test"

    def test_rotation_type_property(self):
        """Test de la propriété rotation_type."""
        rotation = ConcreteTreeRotation()
        assert rotation.rotation_type == "test"

    def test_validate_before_rotation_success(self):
        """Test de validation pré-rotation réussie."""
        rotation = ConcreteTreeRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        
        result = rotation.validate_before_rotation(node)
        assert result is True

    def test_validate_before_rotation_none_node(self):
        """Test de validation pré-rotation avec nœud None."""
        rotation = ConcreteTreeRotation()
        
        with pytest.raises(RotationValidationError) as exc_info:
            rotation.validate_before_rotation(None)
        
        assert "Cannot rotate None node" in str(exc_info.value)
        assert exc_info.value.validation_phase == "before"

    def test_validate_before_rotation_invalid_node(self):
        """Test de validation pré-rotation avec nœud invalide."""
        rotation = ConcreteTreeRotation()
        node = Mock()
        node.validate.return_value = False
        
        with pytest.raises(RotationValidationError) as exc_info:
            rotation.validate_before_rotation(node)
        
        assert "Node is not valid for rotation" in str(exc_info.value)

    def test_validate_before_rotation_cannot_rotate(self):
        """Test de validation pré-rotation quand la rotation n'est pas possible."""
        rotation = ConcreteTreeRotation()
        node = BinaryTreeNode(1)  # Pas d'enfant gauche
        
        with pytest.raises(RotationValidationError) as exc_info:
            rotation.validate_before_rotation(node)
        
        assert "cannot be performed on this node" in str(exc_info.value)

    def test_validate_after_rotation_success(self):
        """Test de validation post-rotation réussie."""
        rotation = ConcreteTreeRotation()
        node = BinaryTreeNode(1)
        
        result = rotation.validate_after_rotation(node)
        assert result is True

    def test_validate_after_rotation_none_node(self):
        """Test de validation post-rotation avec nœud None."""
        rotation = ConcreteTreeRotation()
        
        with pytest.raises(RotationValidationError) as exc_info:
            rotation.validate_after_rotation(None)
        
        assert "Rotation resulted in None node" in str(exc_info.value)
        assert exc_info.value.validation_phase == "after"

    def test_validate_after_rotation_invalid_node(self):
        """Test de validation post-rotation avec nœud invalide."""
        rotation = ConcreteTreeRotation()
        node = Mock()
        node.validate.return_value = False
        
        with pytest.raises(RotationValidationError) as exc_info:
            rotation.validate_after_rotation(node)
        
        assert "Node is not valid after rotation" in str(exc_info.value)

    def test_update_parent_references_success(self):
        """Test de mise à jour des références parent réussie."""
        rotation = ConcreteTreeRotation()
        parent = BinaryTreeNode(0)
        old_root = BinaryTreeNode(1)
        new_root = BinaryTreeNode(2)
        
        parent.set_left(old_root)
        
        rotation.update_parent_references(old_root, new_root)
        
        assert parent.left is new_root
        assert new_root.parent is parent

    def test_update_parent_references_none_nodes(self):
        """Test de mise à jour des références parent avec nœuds None."""
        rotation = ConcreteTreeRotation()
        
        with pytest.raises(TreeRotationError) as exc_info:
            rotation.update_parent_references(None, None)
        
        assert "Cannot update parent references with None nodes" in str(exc_info.value)

    def test_update_parent_references_invalid_parent_child_relationship(self):
        """Test de mise à jour des références parent avec relation parent-enfant invalide."""
        rotation = ConcreteTreeRotation()
        parent = BinaryTreeNode(0)
        old_root = BinaryTreeNode(1)
        new_root = BinaryTreeNode(2)
        
        # old_root n'est pas un enfant de parent
        with pytest.raises(TreeRotationError) as exc_info:
            rotation.update_parent_references(old_root, new_root)
        
        assert "Old root is not a child of its parent" in str(exc_info.value)

    def test_analyze_rotation_success(self):
        """Test d'analyse de rotation réussie."""
        rotation = ConcreteTreeRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        
        analysis = rotation.analyze_rotation(node)
        
        assert analysis["rotation_type"] == "test"
        assert analysis["node_value"] == 1
        assert analysis["can_rotate"] is True
        assert analysis["node_height"] == 1
        assert analysis["node_depth"] == 0
        assert analysis["is_leaf"] is False
        assert analysis["is_root"] is True
        assert analysis["has_left"] is True
        assert analysis["has_right"] is True

    def test_analyze_rotation_none_node(self):
        """Test d'analyse de rotation avec nœud None."""
        rotation = ConcreteTreeRotation()
        
        analysis = rotation.analyze_rotation(None)
        assert analysis["error"] == "Cannot analyze None node"

    def test_get_rotation_stats_success(self):
        """Test de statistiques de rotation réussies."""
        rotation = ConcreteTreeRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        
        stats = rotation.get_rotation_stats(node)
        
        assert stats["rotation_type"] == "test"
        assert stats["subtree_size"] == 3
        assert stats["subtree_height"] == 1
        assert stats["leaf_count"] == 2
        assert stats["internal_nodes"] == 1
        assert stats["balance_factor"] == 0

    def test_get_rotation_stats_none_node(self):
        """Test de statistiques de rotation avec nœud None."""
        rotation = ConcreteTreeRotation()
        
        stats = rotation.get_rotation_stats(None)
        assert stats["error"] == "Cannot get stats for None node"

    def test_validate_consistency_success(self):
        """Test de validation de cohérence réussie."""
        rotation = ConcreteTreeRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        
        result = rotation.validate_consistency(node)
        assert result is True

    def test_validate_consistency_none_node(self):
        """Test de validation de cohérence avec nœud None."""
        rotation = ConcreteTreeRotation()
        
        result = rotation.validate_consistency(None)
        assert result is False

    def test_validate_properties_success(self):
        """Test de validation des propriétés réussie."""
        rotation = ConcreteTreeRotation()
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        
        properties = rotation.validate_properties(node)
        
        assert properties["node_valid"] is True
        assert properties["parent_child_consistency"] is True
        assert properties["subtree_valid"] is True
        assert properties["height_consistent"] is True
        assert properties["structure_valid"] is True

    def test_validate_properties_none_node(self):
        """Test de validation des propriétés avec nœud None."""
        rotation = ConcreteTreeRotation()
        
        properties = rotation.validate_properties(None)
        assert properties["error"] is True

    def test_count_subtree_nodes(self):
        """Test du comptage des nœuds de sous-arbre."""
        rotation = ConcreteTreeRotation()
        
        # Test avec nœud None
        assert rotation._count_subtree_nodes(None) == 0
        
        # Test avec un seul nœud
        node = BinaryTreeNode(1)
        assert rotation._count_subtree_nodes(node) == 1
        
        # Test avec sous-arbre
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        assert rotation._count_subtree_nodes(node) == 3

    def test_count_leaves(self):
        """Test du comptage des feuilles."""
        rotation = ConcreteTreeRotation()
        
        # Test avec nœud None
        assert rotation._count_leaves(None) == 0
        
        # Test avec feuille
        node = BinaryTreeNode(1)
        assert rotation._count_leaves(node) == 1
        
        # Test avec sous-arbre
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        assert rotation._count_leaves(node) == 2

    def test_count_internal_nodes(self):
        """Test du comptage des nœuds internes."""
        rotation = ConcreteTreeRotation()
        
        # Test avec nœud None
        assert rotation._count_internal_nodes(None) == 0
        
        # Test avec feuille
        node = BinaryTreeNode(1)
        assert rotation._count_internal_nodes(node) == 0
        
        # Test avec sous-arbre
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        assert rotation._count_internal_nodes(node) == 1

    def test_calculate_balance_factor(self):
        """Test du calcul du facteur d'équilibre."""
        rotation = ConcreteTreeRotation()
        
        # Test avec nœud None
        assert rotation._calculate_balance_factor(None) == 0
        
        # Test avec feuille
        node = BinaryTreeNode(1)
        assert rotation._calculate_balance_factor(node) == 0
        
        # Test avec enfants
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        assert rotation._calculate_balance_factor(node) == 0

    def test_calculate_real_height(self):
        """Test du calcul de la hauteur réelle."""
        rotation = ConcreteTreeRotation()
        
        # Test avec nœud None
        assert rotation._calculate_real_height(None) == -1
        
        # Test avec feuille
        node = BinaryTreeNode(1)
        assert rotation._calculate_real_height(node) == 0
        
        # Test avec sous-arbre
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        assert rotation._calculate_real_height(node) == 1

    def test_has_circular_references(self):
        """Test de détection des références circulaires."""
        rotation = ConcreteTreeRotation()
        
        # Test avec nœud None
        assert rotation._has_circular_references(None) is False
        
        # Test sans références circulaires
        node = BinaryTreeNode(1)
        node.set_left(BinaryTreeNode(2))
        node.set_right(BinaryTreeNode(3))
        assert rotation._has_circular_references(node) is False

    def test_str_representation(self):
        """Test de la représentation string."""
        rotation = ConcreteTreeRotation()
        str_repr = str(rotation)
        assert "ConcreteTreeRotation" in str_repr
        assert "test" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        rotation = ConcreteTreeRotation()
        repr_str = repr(rotation)
        assert "ConcreteTreeRotation" in repr_str
        assert "test" in repr_str