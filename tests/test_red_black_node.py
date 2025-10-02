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
        assert exc_info.value.validation_rule == "binary_tree_node_children_type"

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


class TestRedBlackNodeEdgeCases:
    """Tests pour les cas limites de RedBlackNode."""

    def test_validate_invalid_color_type(self):
        """Test de validation avec couleur de type invalide."""
        node = RedBlackNode(42)
        # Simuler une couleur de type invalide
        node._color = "invalid_color"

        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()

        assert "RedBlackNode color must be Color enum" in str(exc_info.value)
        assert exc_info.value.validation_rule == "red_black_node_color_type"

    def test_validate_red_black_children_type(self):
        """Test de validation avec enfants de type invalide pour RedBlackNode."""
        node = RedBlackNode(42)
        # Simuler un enfant de type invalide
        node._children = [RedBlackNode(1), "invalid_child"]

        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()

        assert "All children must be BinaryTreeNode instances" in str(exc_info.value)
        assert exc_info.value.validation_rule == "binary_tree_node_children_type"

    def test_color_property_setter_invalid_type(self):
        """Test du setter de couleur avec type invalide."""
        node = RedBlackNode(42)

        with pytest.raises(ColorViolationError) as exc_info:
            node.color = "invalid_color"

        assert "Invalid color type" in str(exc_info.value)

    def test_validate_colors_with_none_children(self):
        """Test de validation des couleurs avec enfants None."""
        node = RedBlackNode(42, Color.RED)
        node._left = None
        node._right = None

        # Ne devrait pas lever d'exception
        assert node.validate_colors() is True

    def test_validate_paths_with_none_children(self):
        """Test de validation des chemins avec enfants None."""
        node = RedBlackNode(42, Color.BLACK)
        node._left = None
        node._right = None

        # Ne devrait pas lever d'exception
        assert node.validate_paths() is True

    def test_get_color_info_edge_cases(self):
        """Test des cas limites de get_color_info."""
        node = RedBlackNode(42, Color.RED)

        # Test des informations de couleur
        color_info = node.get_color_info()
        assert color_info["color"] == "red"
        assert color_info["is_red"] is True
        assert color_info["is_black"] is False

    def test_get_black_height_edge_cases(self):
        """Test des cas limites de get_black_height."""
        node = RedBlackNode(42, Color.BLACK)

        # Test avec enfants None
        node._left = None
        node._right = None
        height = node.get_black_height()
        assert height == 1

    def test_to_dict_with_metadata(self):
        """Test de sérialisation avec métadonnées."""
        node = RedBlackNode(42, Color.RED)
        node._metadata = {"test": "value"}

        data = node.to_dict()
        assert data["metadata"]["test"] == "value"

    def test_from_dict_with_metadata(self):
        """Test de désérialisation avec métadonnées."""
        data = {"value": 42, "color": "red", "metadata": {"test": "value"}}

        node = RedBlackNode.from_dict(data)
        assert node._metadata["test"] == "value"


class TestRedBlackNodeAdvancedFeatures:
    """Tests pour les fonctionnalités avancées de RedBlackNode."""

    def test_create_nil_node(self):
        """Test de création d'un nœud sentinelle."""
        nil_node = RedBlackNode.create_nil_node()

        assert nil_node.value is None
        assert nil_node.color == Color.BLACK
        assert nil_node.is_nil is True
        assert nil_node._black_height == 0

    def test_from_copy_simple(self):
        """Test de copie d'un nœud simple."""
        original = RedBlackNode(42, Color.RED)
        copy = RedBlackNode.from_copy(original)

        # Vérifier que c'est une copie indépendante
        assert copy.value == original.value
        assert copy.color == original.color
        assert copy is not original
        assert copy._parent is None  # Pas de parent dans la copie

    def test_from_copy_with_children(self):
        """Test de copie d'un nœud avec enfants."""
        parent = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        right = RedBlackNode(15, Color.RED)

        parent.set_left(left)
        parent.set_right(right)

        copy = RedBlackNode.from_copy(parent)

        # Vérifier la structure copiée
        assert copy.value == 10
        assert copy.color == Color.BLACK
        assert copy.left.value == 5
        assert copy.left.color == Color.RED
        assert copy.right.value == 15
        assert copy.right.color == Color.RED

        # Vérifier l'indépendance
        assert copy is not parent
        assert copy.left is not left
        assert copy.right is not right

    def test_from_copy_invalid_type(self):
        """Test de copie avec type invalide."""
        with pytest.raises(RedBlackTreeError) as exc_info:
            RedBlackNode.from_copy("invalid")

        assert "Cannot copy non-RedBlackNode" in str(exc_info.value)
        assert exc_info.value.operation == "from_copy"

    def test_is_nil_property(self):
        """Test de la propriété is_nil."""
        node = RedBlackNode(42)
        assert node.is_nil is False

        nil_node = RedBlackNode.create_nil_node()
        assert nil_node.is_nil is True

    def test_black_height_property(self):
        """Test de la propriété black_height."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        right = RedBlackNode(15, Color.RED)

        root.set_left(left)
        root.set_right(right)

        # Test du cache
        assert root.black_height == 1
        assert root._black_height == 1  # Doit être mis en cache

    def test_set_color_method(self):
        """Test de la méthode set_color."""
        node = RedBlackNode(42, Color.RED)

        # Test changement de couleur
        node.set_color(Color.BLACK)
        assert node.color == Color.BLACK
        assert node._black_height is None  # Cache invalidé

    def test_set_color_invalid_type(self):
        """Test de set_color avec type invalide."""
        node = RedBlackNode(42)

        with pytest.raises(ColorViolationError) as exc_info:
            node.set_color("invalid")

        assert "Invalid color type" in str(exc_info.value)

    def test_flip_color(self):
        """Test de flip_color."""
        node = RedBlackNode(42, Color.RED)

        node.flip_color()
        assert node.color == Color.BLACK

        node.flip_color()
        assert node.color == Color.RED

    def test_flip_color_nil_node(self):
        """Test de flip_color sur nœud sentinelle."""
        nil_node = RedBlackNode.create_nil_node()

        with pytest.raises(InvalidNodeOperationError) as exc_info:
            nil_node.flip_color()

        assert "Cannot flip color of NIL node" in str(exc_info.value)
        assert exc_info.value.operation == "flip_color"

    def test_update_black_height(self):
        """Test de update_black_height."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        right = RedBlackNode(15, Color.RED)

        root.set_left(left)
        root.set_right(right)

        # Mettre à jour la hauteur noire
        root.update_black_height()

        assert root._black_height == 1

    def test_update_black_height_inconsistent(self):
        """Test de update_black_height avec hauteurs incohérentes."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.BLACK)  # Noir
        right = RedBlackNode(15, Color.RED)  # Rouge

        root.set_left(left)
        root.set_right(right)

        # Forcer des hauteurs incohérentes
        left._black_height = 2
        right._black_height = 1

        with pytest.raises(RedBlackTreeError) as exc_info:
            root.update_black_height()

        assert "Black heights inconsistent" in str(exc_info.value)
        assert exc_info.value.operation == "update_black_height"

    def test_validate_black_height(self):
        """Test de validate_black_height."""
        node = RedBlackNode(42, Color.BLACK)

        # Test sans cache
        assert node.validate_black_height() is True
        assert node._black_height is not None

    def test_get_node_info(self):
        """Test de get_node_info."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)

        root.set_left(left)

        info = root.get_node_info()

        assert info["value"] == 10
        assert info["color"] == "black"
        assert info["is_red"] is False
        assert info["is_black"] is True
        assert info["is_nil"] is False
        assert info["is_leaf"] is False
        assert info["is_root"] is True
        assert info["has_left_child"] is True
        assert info["has_right_child"] is False
        assert info["left_child"]["value"] == 5
        assert info["left_child"]["color"] == "red"

    def test_compare_with(self):
        """Test de compare_with."""
        node1 = RedBlackNode(42, Color.RED)
        node2 = RedBlackNode(42, Color.RED)
        node3 = RedBlackNode(43, Color.RED)
        node4 = RedBlackNode(42, Color.BLACK)

        # Comparaison identique
        comparison = node1.compare_with(node2)
        assert comparison["values_equal"] is True
        assert comparison["colors_equal"] is True

        # Comparaison différente valeur
        comparison = node1.compare_with(node3)
        assert comparison["values_equal"] is False

        # Comparaison différente couleur
        comparison = node1.compare_with(node4)
        assert comparison["colors_equal"] is False

    def test_compare_with_invalid_type(self):
        """Test de compare_with avec type invalide."""
        node = RedBlackNode(42)

        with pytest.raises(RedBlackTreeError) as exc_info:
            node.compare_with("invalid")

        assert "Cannot compare with non-RedBlackNode" in str(exc_info.value)
        assert exc_info.value.operation == "compare_with"

    def test_diagnose(self):
        """Test de diagnose."""
        root = RedBlackNode(10, Color.BLACK)
        left = RedBlackNode(5, Color.RED)
        right = RedBlackNode(15, Color.RED)

        root.set_left(left)
        root.set_right(right)

        diagnosis = root.diagnose()

        assert "node_info" in diagnosis
        assert "validations" in diagnosis
        assert "issues" in diagnosis
        assert "recommendations" in diagnosis

        # Vérifier les validations
        assert diagnosis["validations"]["is_red_black_valid"] is True
        assert diagnosis["validations"]["validate_colors"] is True
        assert diagnosis["validations"]["validate_paths"] is True

    def test_diagnose_with_violations(self):
        """Test de diagnose avec violations."""
        parent = RedBlackNode(10, Color.RED)
        left = RedBlackNode(5, Color.RED)  # Violation : parent rouge avec enfant rouge

        parent.set_left(left)

        diagnosis = parent.diagnose()

        # Doit détecter les violations
        assert diagnosis["validations"]["is_red_black_valid"] is False
        assert diagnosis["validations"]["validate_colors"] is False
        assert len(diagnosis["issues"]) > 0
        assert len(diagnosis["recommendations"]) > 0

    def test_to_colored_string(self):
        """Test de to_colored_string."""
        red_node = RedBlackNode(42, Color.RED)
        black_node = RedBlackNode(42, Color.BLACK)

        red_str = red_node.to_colored_string()
        black_str = black_node.to_colored_string()

        # Vérifier que les codes couleur sont présents
        assert "\033[91m" in red_str  # Code couleur rouge
        assert "RED" in red_str
        assert "\033[0m" in red_str  # Reset

        assert "\033[30m" in black_str  # Code couleur noir
        assert "BLACK" in black_str
        assert "\033[0m" in black_str  # Reset
