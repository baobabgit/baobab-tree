"""
Tests unitaires pour la classe RedBlackNode.

Ce module contient tous les tests unitaires pour la classe RedBlackNode,
incluant les tests de base, de validation, de sérialisation et de diagnostic.
"""

import pytest
from src.baobab_tree.balanced.red_black_node import Color, RedBlackNode
from src.baobab_tree.core.exceptions import (
    ColorViolationError,
    InvalidNodeOperationError,
    NodeValidationError,
    RedBlackTreeError,
)


class TestRedBlackNode:
    """Tests pour la classe RedBlackNode."""

    def test_init_default_color(self):
        """Test de l'initialisation avec couleur par défaut."""
        node = RedBlackNode(42)
        assert node.value == 42
        assert node.color == Color.RED
        assert node.is_red()
        assert not node.is_black()

    def test_init_custom_color(self):
        """Test de l'initialisation avec couleur personnalisée."""
        node = RedBlackNode(42, Color.BLACK)
        assert node.value == 42
        assert node.color == Color.BLACK
        assert not node.is_red()
        assert node.is_black()

    def test_color_property(self):
        """Test de la propriété color."""
        node = RedBlackNode(42)
        
        # Test getter
        assert node.color == Color.RED
        
        # Test setter
        node.color = Color.BLACK
        assert node.color == Color.BLACK
        assert node.is_black()

    def test_color_property_invalid_type(self):
        """Test de la propriété color avec type invalide."""
        node = RedBlackNode(42)
        
        with pytest.raises(ColorViolationError) as exc_info:
            node.color = "red"
        
        assert "Invalid color type" in str(exc_info.value)
        assert exc_info.value.color_property == "color_type"

    def test_color_methods(self):
        """Test des méthodes de couleur."""
        node = RedBlackNode(42, Color.RED)
        
        # Test set_red
        node.set_red()
        assert node.is_red()
        assert not node.is_black()
        
        # Test set_black
        node.set_black()
        assert node.is_black()
        assert not node.is_red()
        
        # Test toggle_color
        node.toggle_color()
        assert node.is_red()
        node.toggle_color()
        assert node.is_black()

    def test_set_left_valid(self):
        """Test de set_left avec nœud valide."""
        parent = RedBlackNode(10)
        child = RedBlackNode(5)
        
        parent.set_left(child)
        
        assert parent.left == child
        assert child.parent == parent

    def test_set_left_invalid_type(self):
        """Test de set_left avec type invalide."""
        parent = RedBlackNode(10)
        
        with pytest.raises(InvalidNodeOperationError) as exc_info:
            parent.set_left("invalid")
        
        assert "Left child must be a RedBlackNode" in str(exc_info.value)
        assert exc_info.value.operation == "set_left"

    def test_set_right_valid(self):
        """Test de set_right avec nœud valide."""
        parent = RedBlackNode(10)
        child = RedBlackNode(15)
        
        parent.set_right(child)
        
        assert parent.right == child
        assert child.parent == parent

    def test_set_right_invalid_type(self):
        """Test de set_right avec type invalide."""
        parent = RedBlackNode(10)
        
        with pytest.raises(InvalidNodeOperationError) as exc_info:
            parent.set_right("invalid")
        
        assert "Right child must be a RedBlackNode" in str(exc_info.value)
        assert exc_info.value.operation == "set_right"

    def test_add_child_valid(self):
        """Test de add_child avec nœud valide."""
        parent = RedBlackNode(10)
        child = RedBlackNode(5)
        
        parent.add_child(child)
        
        assert child in parent.children
        assert child.parent == parent

    def test_add_child_invalid_type(self):
        """Test de add_child avec type invalide."""
        parent = RedBlackNode(10)
        
        with pytest.raises(InvalidNodeOperationError) as exc_info:
            parent.add_child("invalid")
        
        assert "Child must be a RedBlackNode" in str(exc_info.value)
        assert exc_info.value.operation == "add_child"

    def test_validate_valid_node(self):
        """Test de validation d'un nœud valide."""
        node = RedBlackNode(42, Color.RED)
        assert node.validate() is True

    def test_validate_invalid_children_type(self):
        """Test de validation avec enfants de type invalide."""
        node = RedBlackNode(42)
        # Simuler un enfant de type invalide
        node._children = ["invalid"]
        
        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()
        
        assert "All children must be BinaryTreeNode instances" in str(exc_info.value)
        assert exc_info.value.validation_rule == "red_black_node_children_type"

    def test_is_red_black_valid_single_node(self):
        """Test de validation rouge-noir pour un nœud seul."""
        node = RedBlackNode(42, Color.RED)
        assert node.is_red_black_valid() is True
        
        node = RedBlackNode(42, Color.BLACK)
        assert node.is_red_black_valid() is True

    def test_is_red_black_valid_with_children(self):
        """Test de validation rouge-noir avec enfants."""
        parent = RedBlackNode(10, Color.BLACK)
        left_child = RedBlackNode(5, Color.RED)
        right_child = RedBlackNode(15, Color.RED)
        
        parent.set_left(left_child)
        parent.set_right(right_child)
        
        assert parent.is_red_black_valid() is True

    def test_is_red_black_valid_violation(self):
        """Test de validation rouge-noir avec violation."""
        parent = RedBlackNode(10, Color.RED)
        left_child = RedBlackNode(5, Color.RED)
        
        parent.set_left(left_child)
        
        # Violation : parent rouge avec enfant rouge
        assert parent.is_red_black_valid() is False

    def test_validate_colors_valid(self):
        """Test de validation des couleurs valides."""
        parent = RedBlackNode(10, Color.BLACK)
        left_child = RedBlackNode(5, Color.RED)
        right_child = RedBlackNode(15, Color.RED)
        
        parent.set_left(left_child)
        parent.set_right(right_child)
        
        assert parent.validate_colors() is True

    def test_validate_colors_violation(self):
        """Test de validation des couleurs avec violation."""
        parent = RedBlackNode(10, Color.RED)
        left_child = RedBlackNode(5, Color.RED)
        
        parent.set_left(left_child)
        
        # Violation : parent rouge avec enfant rouge
        assert parent.validate_colors() is False

    def test_validate_paths_valid(self):
        """Test de validation des chemins valides."""
        # Créer un arbre simple avec même nombre de nœuds noirs sur tous les chemins
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        right = RedBlackNode(15, Color.RED)
        
        root.set_left(left)
        root.set_right(right)
        
        assert root.validate_paths() is True

    def test_validate_paths_invalid(self):
        """Test de validation des chemins avec violation."""
        # Créer un arbre avec nombre différent de nœuds noirs sur les chemins
        root = RedBlackNode(10, Color.RED)
        left = RedBlackNode(5, Color.BLACK)
        right = RedBlackNode(15, Color.RED)
        
        root.set_left(left)
        root.set_right(right)
        
        # Les chemins n'ont pas le même nombre de nœuds noirs
        assert root.validate_paths() is False

    def test_get_color_info(self):
        """Test de get_color_info."""
        node = RedBlackNode(42, Color.RED)
        info = node.get_color_info()
        
        assert info["color"] == "red"
        assert info["is_red"] is True
        assert info["is_black"] is False
        assert info["is_leaf"] is True
        assert info["is_root"] is True

    def test_get_black_height(self):
        """Test de get_black_height."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        right = RedBlackNode(15, Color.RED)
        
        root.set_left(left)
        root.set_right(right)
        
        # Hauteur noire : 1 (racine noire) + 0 (enfants rouges) = 1
        assert root.get_black_height() == 1
        assert left.get_black_height() == 0
        assert right.get_black_height() == 0

    def test_to_dict(self):
        """Test de sérialisation en dictionnaire."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        right = RedBlackNode(15, Color.RED)
        
        root.set_left(left)
        root.set_right(right)
        
        data = root.to_dict()
        
        assert data["value"] == 10
        assert data["color"] == "black"
        assert data["left"]["value"] == 5
        assert data["left"]["color"] == "red"
        assert data["right"]["value"] == 15
        assert data["right"]["color"] == "red"

    def test_from_dict(self):
        """Test de désérialisation depuis dictionnaire."""
        data = {
            "value": 10,
            "color": "black",
            "left": {
                "value": 5,
                "color": "red",
                "left": None,
                "right": None,
            },
            "right": {
                "value": 15,
                "color": "red",
                "left": None,
                "right": None,
            },
        }
        
        node = RedBlackNode.from_dict(data)
        
        assert node.value == 10
        assert node.color == Color.BLACK
        assert node.left.value == 5
        assert node.left.color == Color.RED
        assert node.right.value == 15
        assert node.right.color == Color.RED

    def test_from_dict_invalid_data(self):
        """Test de désérialisation avec données invalides."""
        with pytest.raises(RedBlackTreeError) as exc_info:
            RedBlackNode.from_dict("invalid")
        
        assert "Expected dict for deserialization" in str(exc_info.value)
        assert exc_info.value.operation == "from_dict"

    def test_from_dict_missing_field(self):
        """Test de désérialisation avec champ manquant."""
        data = {"value": 10}  # Manque "color"
        
        with pytest.raises(RedBlackTreeError) as exc_info:
            RedBlackNode.from_dict(data)
        
        assert "Missing required field 'color'" in str(exc_info.value)
        assert exc_info.value.operation == "from_dict"

    def test_to_string(self):
        """Test de représentation textuelle."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        
        root.set_left(left)
        
        result = root.to_string()
        
        assert "RedBlackNode(value=10, color=B)" in result
        assert "RedBlackNode(value=5, color=R)" in result

    def test_to_compact_string(self):
        """Test de représentation compacte."""
        node = RedBlackNode(42, Color.RED)
        assert node.to_compact_string() == "42(R)"
        
        node = RedBlackNode(42, Color.BLACK)
        assert node.to_compact_string() == "42(B)"

    def test_str(self):
        """Test de __str__."""
        node = RedBlackNode(42, Color.RED)
        assert str(node) == "RedBlackNode(value=42, color=R)"
        
        node = RedBlackNode(42, Color.BLACK)
        assert str(node) == "RedBlackNode(value=42, color=B)"

    def test_repr(self):
        """Test de __repr__."""
        node = RedBlackNode(42, Color.RED)
        repr_str = repr(node)
        
        assert "RedBlackNode(value=42" in repr_str
        assert "color=R)" in repr_str

    def test_eq(self):
        """Test de __eq__."""
        node1 = RedBlackNode(42, Color.RED)
        node2 = RedBlackNode(42, Color.RED)
        node3 = RedBlackNode(42, Color.BLACK)
        node4 = RedBlackNode(43, Color.RED)
        
        assert node1 == node2
        assert node1 != node3
        assert node1 != node4
        assert node1 != "not a node"

    def test_hash(self):
        """Test de __hash__."""
        node1 = RedBlackNode(42, Color.RED)
        node2 = RedBlackNode(42, Color.RED)
        node3 = RedBlackNode(42, Color.BLACK)
        
        assert hash(node1) == hash(node2)
        assert hash(node1) != hash(node3)


class TestColor:
    """Tests pour l'énumération Color."""

    def test_color_values(self):
        """Test des valeurs de couleur."""
        assert Color.RED.value == "red"
        assert Color.BLACK.value == "black"

    def test_color_comparison(self):
        """Test de comparaison des couleurs."""
        assert Color.RED != Color.BLACK
        assert Color.RED == Color.RED
        assert Color.BLACK == Color.BLACK