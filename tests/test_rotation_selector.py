"""
Tests unitaires pour la classe RotationSelector.

Ce module contient tous les tests unitaires pour la classe RotationSelector.
"""

import pytest

from src.baobab_tree.balanced.rotations.rotation_selector import RotationSelector
from src.baobab_tree.balanced.rotations.left_rotation import LeftRotation
from src.baobab_tree.balanced.rotations.right_rotation import RightRotation
from src.baobab_tree.balanced.rotations.left_right_rotation import LeftRightRotation
from src.baobab_tree.balanced.rotations.right_left_rotation import RightLeftRotation
from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode
from src.baobab_tree.core.exceptions import InvalidRotationError


class TestRotationSelector:
    """Tests pour la classe RotationSelector."""

    def test_select_rotation_left_heavy(self):
        """Test de sélection de rotation pour déséquilibre gauche."""
        selector = RotationSelector()
        
        # Créer un nœud avec déséquilibre gauche
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        node.set_left(left_child)
        
        context = {"balance_factor": 2}
        
        rotation = selector.select_rotation(node, context)
        assert isinstance(rotation, RightRotation)

    def test_select_rotation_right_heavy(self):
        """Test de sélection de rotation pour déséquilibre droit."""
        selector = RotationSelector()
        
        # Créer un nœud avec déséquilibre droit
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        node.set_right(right_child)
        
        context = {"balance_factor": -2}
        
        rotation = selector.select_rotation(node, context)
        assert isinstance(rotation, LeftRotation)

    def test_select_rotation_left_right_heavy(self):
        """Test de sélection de rotation pour déséquilibre gauche-droite."""
        selector = RotationSelector()
        
        # Créer un nœud avec déséquilibre gauche-droite
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        context = {"balance_factor": 2}
        
        rotation = selector.select_rotation(node, context)
        assert isinstance(rotation, LeftRightRotation)

    def test_select_rotation_right_left_heavy(self):
        """Test de sélection de rotation pour déséquilibre droite-gauche."""
        selector = RotationSelector()
        
        # Créer un nœud avec déséquilibre droite-gauche
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        context = {"balance_factor": -2}
        
        rotation = selector.select_rotation(node, context)
        assert isinstance(rotation, RightLeftRotation)

    def test_select_rotation_none_node(self):
        """Test de sélection de rotation avec nœud None."""
        selector = RotationSelector()
        
        with pytest.raises(InvalidRotationError) as exc_info:
            selector.select_rotation(None, {})
        
        assert "Cannot select rotation for None node" in str(exc_info.value)

    def test_select_rotation_invalid_context(self):
        """Test de sélection de rotation avec contexte invalide."""
        selector = RotationSelector()
        node = BinaryTreeNode(1)
        
        with pytest.raises(InvalidRotationError) as exc_info:
            selector.select_rotation(node, "invalid_context")
        
        assert "Context must be a dictionary" in str(exc_info.value)

    def test_select_rotation_balanced(self):
        """Test de sélection de rotation pour nœud équilibré."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_child = BinaryTreeNode(3)
        
        node.set_left(left_child)
        node.set_right(right_child)
        
        context = {"balance_factor": 0}
        
        with pytest.raises(InvalidRotationError) as exc_info:
            selector.select_rotation(node, context)
        
        assert "No rotation needed" in str(exc_info.value)

    def test_analyze_imbalance_success(self):
        """Test d'analyse de déséquilibre réussie."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_child = BinaryTreeNode(3)
        
        node.set_left(left_child)
        node.set_right(right_child)
        
        analysis = selector.analyze_imbalance(node)
        
        assert analysis["node_value"] == 1
        assert analysis["has_left"] is True
        assert analysis["has_right"] is True
        assert analysis["is_leaf"] is False
        assert analysis["is_root"] is True
        assert analysis["left_height"] == 0
        assert analysis["right_height"] == 0
        assert analysis["height_difference"] == 0
        assert analysis["balance_factor"] == 0
        assert analysis["imbalance_type"] == "balanced"
        assert analysis["recommended_rotation"] is None

    def test_analyze_imbalance_left_heavy(self):
        """Test d'analyse de déséquilibre gauche."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_left(left_grandchild)
        
        analysis = selector.analyze_imbalance(node)
        
        assert analysis["imbalance_type"] == "left_heavy"
        assert analysis["recommended_rotation"] == "right"

    def test_analyze_imbalance_right_heavy(self):
        """Test d'analyse de déséquilibre droit."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_right(right_grandchild)
        
        analysis = selector.analyze_imbalance(node)
        
        assert analysis["imbalance_type"] == "right_heavy"
        assert analysis["recommended_rotation"] == "left"

    def test_analyze_imbalance_left_right_heavy(self):
        """Test d'analyse de déséquilibre gauche-droite."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        analysis = selector.analyze_imbalance(node)
        
        assert analysis["imbalance_type"] == "left_right_heavy"
        assert analysis["recommended_rotation"] == "left_right"

    def test_analyze_imbalance_right_left_heavy(self):
        """Test d'analyse de déséquilibre droite-gauche."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        analysis = selector.analyze_imbalance(node)
        
        assert analysis["imbalance_type"] == "right_left_heavy"
        assert analysis["recommended_rotation"] == "right_left"

    def test_analyze_imbalance_none_node(self):
        """Test d'analyse de déséquilibre avec nœud None."""
        selector = RotationSelector()
        
        analysis = selector.analyze_imbalance(None)
        assert analysis["error"] == "Cannot analyze None node"

    def test_get_rotation_for_balance_factor_positive(self):
        """Test de récupération de rotation pour facteur d'équilibre positif."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        node.set_left(left_child)
        
        rotation_type = selector.get_rotation_for_balance_factor(2, node)
        assert rotation_type == "right"

    def test_get_rotation_for_balance_factor_negative(self):
        """Test de récupération de rotation pour facteur d'équilibre négatif."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        node.set_right(right_child)
        
        rotation_type = selector.get_rotation_for_balance_factor(-2, node)
        assert rotation_type == "left"

    def test_get_rotation_for_balance_factor_left_right_heavy(self):
        """Test de récupération de rotation pour déséquilibre gauche-droite."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_grandchild = BinaryTreeNode(3)
        
        node.set_left(left_child)
        left_child.set_right(right_grandchild)
        
        rotation_type = selector.get_rotation_for_balance_factor(2, node)
        assert rotation_type == "left_right"

    def test_get_rotation_for_balance_factor_right_left_heavy(self):
        """Test de récupération de rotation pour déséquilibre droite-gauche."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        right_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        
        node.set_right(right_child)
        right_child.set_left(left_grandchild)
        
        rotation_type = selector.get_rotation_for_balance_factor(-2, node)
        assert rotation_type == "right_left"

    def test_get_rotation_for_balance_factor_balanced(self):
        """Test de récupération de rotation pour nœud équilibré."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        right_child = BinaryTreeNode(3)
        
        node.set_left(left_child)
        node.set_right(right_child)
        
        rotation_type = selector.get_rotation_for_balance_factor(0, node)
        assert rotation_type == "none"

    def test_str_representation(self):
        """Test de la représentation string."""
        selector = RotationSelector()
        str_repr = str(selector)
        assert str_repr == "RotationSelector()"

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        selector = RotationSelector()
        repr_str = repr(selector)
        assert repr_str == "RotationSelector()"

    def test_complex_tree_analysis(self):
        """Test d'analyse d'arbre complexe."""
        selector = RotationSelector()
        
        # Créer un arbre complexe
        #        1
        #       /
        #      2
        #     / \\
        #    3   4
        #   /
        #  5
        root = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        left_grandchild = BinaryTreeNode(3)
        right_grandchild = BinaryTreeNode(4)
        left_great_grandchild = BinaryTreeNode(5)
        
        root.set_left(left_child)
        left_child.set_left(left_grandchild)
        left_child.set_right(right_grandchild)
        left_grandchild.set_left(left_great_grandchild)
        
        analysis = selector.analyze_imbalance(root)
        
        assert analysis["node_value"] == 1
        assert analysis["left_height"] == 2
        assert analysis["right_height"] == 0
        assert analysis["balance_factor"] == 2
        assert analysis["imbalance_type"] == "left_heavy"
        assert analysis["recommended_rotation"] == "right"

    def test_context_with_balance_factor(self):
        """Test de sélection avec contexte contenant le facteur d'équilibre."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        context = {"balance_factor": 2}
        
        rotation = selector.select_rotation(node, context)
        assert isinstance(rotation, RightRotation)

    def test_context_without_balance_factor(self):
        """Test de sélection sans facteur d'équilibre dans le contexte."""
        selector = RotationSelector()
        
        node = BinaryTreeNode(1)
        left_child = BinaryTreeNode(2)
        node.set_left(left_child)
        
        context = {"other_info": "value"}
        
        rotation = selector.select_rotation(node, context)
        assert isinstance(rotation, RightRotation)