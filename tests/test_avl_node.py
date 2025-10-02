"""
Tests unitaires pour la classe AVLNode.

Ce module contient tous les tests unitaires pour la classe AVLNode,
incluant les tests de base, les tests de validation et les tests d'erreurs.
"""

import pytest
from src.baobab_tree.balanced.avl_node import AVLNode
from src.baobab_tree.core.exceptions import (
    AVLNodeError,
    HeightCalculationError,
    HeightMismatchError,
    InvalidBalanceFactorError,
    InvalidNodeOperationError,
    NodeValidationError,
)


class TestAVLNode:
    """Tests pour la classe AVLNode."""

    def test_avl_node_creation(self):
        """Test de création d'un nœud AVL."""
        node = AVLNode(42)
        assert node.value == 42
        assert node.balance_factor == 0
        assert node.height == 0
        assert node.left is None
        assert node.right is None
        assert node.parent is None

    def test_avl_node_with_parent(self):
        """Test de création d'un nœud AVL avec parent."""
        parent = AVLNode(50)
        node = AVLNode(30, parent=parent)
        assert node.value == 30
        assert node.parent is parent
        assert parent.left is None  # Pas encore défini comme enfant

    def test_avl_node_with_children(self):
        """Test de création d'un nœud AVL avec enfants."""
        left_child = AVLNode(20)
        right_child = AVLNode(60)
        node = AVLNode(40, left=left_child, right=right_child)

        assert node.left is left_child
        assert node.right is right_child
        assert left_child.parent is node
        assert right_child.parent is node

    def test_balance_factor_property(self):
        """Test de la propriété balance_factor."""
        node = AVLNode(50)
        assert node.balance_factor == 0

        # Ajouter un enfant gauche
        left_child = AVLNode(30)
        node.set_left(left_child)
        assert node.balance_factor == -1  # Gauche plus lourd

        # Ajouter un enfant droit
        right_child = AVLNode(70)
        node.set_right(right_child)
        assert node.balance_factor == 0  # Équilibré

    def test_height_property(self):
        """Test de la propriété height."""
        node = AVLNode(50)
        assert node.height == 0

        # Ajouter un enfant
        child = AVLNode(30)
        node.set_left(child)
        assert node.height == 1

        # Ajouter un autre enfant
        child2 = AVLNode(70)
        node.set_right(child2)
        assert node.height == 1  # Toujours 1 car les enfants sont des feuilles

    def test_update_balance_factor(self):
        """Test de la mise à jour du facteur d'équilibre."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.update_balance_factor()
        assert node.balance_factor == -1

        node.set_right(right_child)
        node.update_balance_factor()
        assert node.balance_factor == 0

    def test_update_height(self):
        """Test de la mise à jour de la hauteur."""
        node = AVLNode(50)
        child = AVLNode(30)
        grandchild = AVLNode(20)

        node.set_left(child)
        node.update_height()
        assert node.height == 1

        child.set_left(grandchild)
        node.update_height()
        assert node.height == 2

    def test_is_left_heavy(self):
        """Test de la méthode is_left_heavy."""
        node = AVLNode(50)
        assert not node.is_left_heavy()

        left_child = AVLNode(30)
        node.set_left(left_child)
        assert node.is_left_heavy()

        right_child = AVLNode(70)
        node.set_right(right_child)
        assert not node.is_left_heavy()

    def test_is_right_heavy(self):
        """Test de la méthode is_right_heavy."""
        node = AVLNode(50)
        assert not node.is_right_heavy()

        right_child = AVLNode(70)
        node.set_right(right_child)
        assert node.is_right_heavy()

        left_child = AVLNode(30)
        node.set_left(left_child)
        assert not node.is_right_heavy()

    def test_is_balanced(self):
        """Test de la méthode is_balanced."""
        node = AVLNode(50)
        assert node.is_balanced()

        # Ajouter un enfant gauche
        left_child = AVLNode(30)
        node.set_left(left_child)
        assert node.is_balanced()  # -1 est valide

        # Ajouter un enfant droit
        right_child = AVLNode(70)
        node.set_right(right_child)
        assert node.is_balanced()  # 0 est valide

    def test_set_left_with_avl_node(self):
        """Test de set_left avec un AVLNode."""
        node = AVLNode(50)
        left_child = AVLNode(30)

        node.set_left(left_child)
        assert node.left is left_child
        assert left_child.parent is node
        assert node.balance_factor == -1

    def test_set_left_with_non_avl_node(self):
        """Test de set_left avec un nœud non-AVL."""
        node = AVLNode(50)

        with pytest.raises(InvalidNodeOperationError) as exc_info:
            node.set_left("not_a_node")

        assert "Left child must be an AVLNode" in str(exc_info.value)

    def test_set_right_with_avl_node(self):
        """Test de set_right avec un AVLNode."""
        node = AVLNode(50)
        right_child = AVLNode(70)

        node.set_right(right_child)
        assert node.right is right_child
        assert right_child.parent is node
        assert node.balance_factor == 1

    def test_set_right_with_non_avl_node(self):
        """Test de set_right avec un nœud non-AVL."""
        node = AVLNode(50)

        with pytest.raises(InvalidNodeOperationError) as exc_info:
            node.set_right("not_a_node")

        assert "Right child must be an AVLNode" in str(exc_info.value)

    def test_update_avl_metadata(self):
        """Test de la mise à jour des métadonnées AVL."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        # Les métadonnées doivent être mises à jour automatiquement
        assert node.balance_factor == 0
        assert node.height == 1

    def test_get_height_override(self):
        """Test de la surcharge de get_height."""
        node = AVLNode(50)
        child = AVLNode(30)
        grandchild = AVLNode(20)

        node.set_left(child)
        child.set_left(grandchild)

        # La hauteur mise en cache doit être utilisée
        assert node.get_height() == 2
        assert node.height == 2

    def test_validate_success(self):
        """Test de validation réussie."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        assert node.validate() is True

    def test_validate_with_non_avl_child(self):
        """Test de validation avec un enfant non-AVL."""
        node = AVLNode(50)
        # Créer un BinaryTreeNode au lieu d'un AVLNode
        from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode

        non_avl_child = BinaryTreeNode(30)

        # Forcer l'ajout de l'enfant non-AVL
        node._left = non_avl_child
        node._children = [non_avl_child]

        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()

        assert "All children must be AVLNode instances" in str(exc_info.value)

    def test_validate_with_invalid_balance_factor(self):
        """Test de validation avec un facteur d'équilibre invalide."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        # Forcer un facteur d'équilibre invalide
        node._balance_factor = 2

        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()

        assert "AVL node balance factor must be -1, 0, or 1" in str(exc_info.value)

    def test_validate_with_height_mismatch(self):
        """Test de validation avec une incohérence de hauteur."""
        node = AVLNode(50)
        child = AVLNode(30)

        node.set_left(child)

        # Forcer une hauteur mise en cache incorrecte
        node._cached_height = 5

        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()

        assert "Cached height" in str(
            exc_info.value
        ) and "does not match calculated height" in str(exc_info.value)

    def test_add_child_with_avl_node(self):
        """Test de add_child avec un AVLNode."""
        node = AVLNode(50)
        child = AVLNode(30)

        node.add_child(child)
        assert child in node._children
        assert child.parent is node

    def test_add_child_with_non_avl_node(self):
        """Test de add_child avec un nœud non-AVL."""
        node = AVLNode(50)

        with pytest.raises(InvalidNodeOperationError) as exc_info:
            node.add_child("not_a_node")

        assert "Child must be an AVLNode" in str(exc_info.value)

    def test_str_representation(self):
        """Test de la représentation string."""
        node = AVLNode(42)
        node._balance_factor = -1
        node._cached_height = 2

        str_repr = str(node)
        assert "AVLNode" in str_repr
        assert "value=42" in str_repr
        assert "balance=-1" in str_repr
        assert "height=2" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        node = AVLNode(42)
        node._balance_factor = 1
        node._cached_height = 1

        repr_str = repr(node)
        assert "AVLNode" in repr_str
        assert "value=42" in repr_str
        assert "balance=1" in repr_str
        assert "height=1" in repr_str

    def test_equality(self):
        """Test de l'égalité entre nœuds AVL."""
        node1 = AVLNode(42)
        node2 = AVLNode(42)
        node3 = AVLNode(43)

        assert node1 == node2
        assert node1 != node3
        assert node1 != "not_a_node"

    def test_hash(self):
        """Test du hash des nœuds AVL."""
        node1 = AVLNode(42)
        node2 = AVLNode(42)
        node3 = AVLNode(43)

        assert hash(node1) == hash(node2)
        assert hash(node1) != hash(node3)

    def test_complex_tree_structure(self):
        """Test avec une structure d'arbre complexe."""
        # Créer un arbre AVL complexe
        root = AVLNode(50)
        left = AVLNode(30)
        right = AVLNode(70)
        left_left = AVLNode(20)
        left_right = AVLNode(40)
        right_left = AVLNode(60)
        right_right = AVLNode(80)

        # Construire l'arbre
        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)
        right.set_left(right_left)
        right.set_right(right_right)

        # Vérifier les propriétés
        assert root.balance_factor == 0
        assert root.height == 2
        assert left.balance_factor == 0
        assert right.balance_factor == 0

        # Vérifier la validation
        assert root.validate() is True

    def test_avl_node_inheritance(self):
        """Test de l'héritage de BinaryTreeNode."""
        node = AVLNode(50)

        # Vérifier que les méthodes de base fonctionnent
        assert node.is_leaf() is True
        assert node.is_root() is True
        assert node.get_depth() == 0

        # Ajouter des enfants
        child = AVLNode(30)
        node.set_left(child)

        assert node.is_leaf() is False
        assert child.is_root() is False
        assert child.get_depth() == 1

    def test_from_copy(self):
        """Test du constructeur de copie."""
        # Créer un nœud original avec enfants
        original = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)
        original.set_left(left_child)
        original.set_right(right_child)

        # Créer une copie
        copy_node = AVLNode.from_copy(original)

        # Vérifier que la copie est indépendante
        assert copy_node.value == original.value
        assert copy_node.balance_factor == original.balance_factor
        assert copy_node.height == original.height
        assert copy_node is not original
        assert copy_node.left is not original.left
        assert copy_node.right is not original.right

        # Vérifier que les enfants sont copiés
        assert copy_node.left.value == original.left.value
        assert copy_node.right.value == original.right.value

    def test_from_copy_with_non_avl_node(self):
        """Test du constructeur de copie avec un nœud non-AVL."""
        from src.baobab_tree.binary.binary_tree_node import BinaryTreeNode

        non_avl_node = BinaryTreeNode(42)

        with pytest.raises(AVLNodeError) as exc_info:
            AVLNode.from_copy(non_avl_node)

        assert "Cannot copy non-AVLNode" in str(exc_info.value)

    def test_get_balance_factor(self):
        """Test de la méthode get_balance_factor."""
        node = AVLNode(50)
        assert node.get_balance_factor() == 0

        left_child = AVLNode(30)
        node.set_left(left_child)
        assert node.get_balance_factor() == -1

    def test_get_left_height(self):
        """Test de la méthode get_left_height."""
        node = AVLNode(50)
        assert node.get_left_height() == -1

        left_child = AVLNode(30)
        node.set_left(left_child)
        assert node.get_left_height() == 0

    def test_get_right_height(self):
        """Test de la méthode get_right_height."""
        node = AVLNode(50)
        assert node.get_right_height() == -1

        right_child = AVLNode(70)
        node.set_right(right_child)
        assert node.get_right_height() == 0

    def test_update_all_success(self):
        """Test de la méthode update_all avec succès."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        # update_all ne doit pas lever d'exception
        node.update_all()
        assert node.is_balanced()

    def test_update_all_with_invalid_balance(self):
        """Test de update_all avec facteur d'équilibre invalide."""
        node = AVLNode(50)
        # Forcer un facteur d'équilibre invalide
        node._balance_factor = 2

        with pytest.raises(InvalidBalanceFactorError) as exc_info:
            node.update_all()

        assert "Balance factor 2 is not in valid range" in str(exc_info.value)

    def test_is_avl_valid_success(self):
        """Test de la méthode is_avl_valid avec succès."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        assert node.is_avl_valid()

    def test_is_avl_valid_failure(self):
        """Test de la méthode is_avl_valid avec échec."""
        node = AVLNode(50)
        # Forcer un facteur d'équilibre invalide
        node._balance_factor = 2

        assert not node.is_avl_valid()

    def test_validate_heights_success(self):
        """Test de la méthode validate_heights avec succès."""
        node = AVLNode(50)
        child = AVLNode(30)
        node.set_left(child)

        assert node.validate_heights()

    def test_validate_heights_failure(self):
        """Test de la méthode validate_heights avec échec."""
        node = AVLNode(50)
        child = AVLNode(30)
        node.set_left(child)

        # Forcer une hauteur incorrecte
        node._cached_height = 5

        assert not node.validate_heights()

    def test_validate_balance_factor_success(self):
        """Test de la méthode validate_balance_factor avec succès."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        assert node.validate_balance_factor()

    def test_validate_balance_factor_failure(self):
        """Test de la méthode validate_balance_factor avec échec."""
        node = AVLNode(50)
        # Forcer un facteur d'équilibre incorrect
        node._balance_factor = 2

        assert not node.validate_balance_factor()

    def test_get_node_info(self):
        """Test de la méthode get_node_info."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        info = node.get_node_info()

        assert info["value"] == 50
        assert info["balance_factor"] == 0
        assert info["height"] == 1
        assert info["is_balanced"] is True
        assert info["is_leaf"] is False
        assert info["has_left_child"] is True
        assert info["has_right_child"] is True
        assert info["children_count"] == 2

    def test_compare_with_success(self):
        """Test de la méthode compare_with avec succès."""
        node1 = AVLNode(50)
        node2 = AVLNode(50)

        comparison = node1.compare_with(node2)

        assert comparison["values_equal"] is True
        assert comparison["balance_factors_equal"] is True
        assert comparison["heights_equal"] is True
        assert comparison["both_balanced"] is True

    def test_compare_with_different_values(self):
        """Test de la méthode compare_with avec valeurs différentes."""
        node1 = AVLNode(50)
        node2 = AVLNode(60)

        comparison = node1.compare_with(node2)

        assert comparison["values_equal"] is False
        assert comparison["balance_factors_equal"] is True

    def test_compare_with_non_avl_node(self):
        """Test de la méthode compare_with avec un nœud non-AVL."""
        node = AVLNode(50)

        with pytest.raises(AVLNodeError) as exc_info:
            node.compare_with("not_a_node")

        assert "Cannot compare with non-AVLNode" in str(exc_info.value)

    def test_diagnose_valid_node(self):
        """Test de la méthode diagnose avec un nœud valide."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        diagnosis = node.diagnose()

        assert diagnosis["is_valid"] is True
        assert diagnosis["value"] == 50
        assert len(diagnosis["issues"]) == 0
        assert "statistics" in diagnosis

    def test_diagnose_invalid_node(self):
        """Test de la méthode diagnose avec un nœud invalide."""
        node = AVLNode(50)
        # Forcer un facteur d'équilibre invalide
        node._balance_factor = 2

        diagnosis = node.diagnose()

        assert diagnosis["is_valid"] is False
        assert len(diagnosis["issues"]) > 0
        assert len(diagnosis["warnings"]) > 0

    def test_to_dict(self):
        """Test de la méthode to_dict."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        data = node.to_dict()

        assert data["value"] == 50
        assert data["balance_factor"] == 0
        assert data["height"] == 1
        assert data["left"]["value"] == 30
        assert data["right"]["value"] == 70

    def test_from_dict(self):
        """Test de la méthode from_dict."""
        data = {
            "value": 50,
            "balance_factor": 0,
            "height": 1,
            "metadata": {},
            "left": {
                "value": 30,
                "balance_factor": 0,
                "height": 0,
                "metadata": {},
                "left": None,
                "right": None,
            },
            "right": {
                "value": 70,
                "balance_factor": 0,
                "height": 0,
                "metadata": {},
                "left": None,
                "right": None,
            },
        }

        node = AVLNode.from_dict(data)

        assert node.value == 50
        assert node.balance_factor == 0
        assert node.height == 1
        assert node.left.value == 30
        assert node.right.value == 70

    def test_from_dict_invalid_data(self):
        """Test de from_dict avec des données invalides."""
        with pytest.raises(AVLNodeError) as exc_info:
            AVLNode.from_dict("not_a_dict")

        assert "Expected dict for deserialization" in str(exc_info.value)

    def test_from_dict_missing_field(self):
        """Test de from_dict avec un champ manquant."""
        data = {"value": 50}  # Manque balance_factor et height

        with pytest.raises(AVLNodeError) as exc_info:
            AVLNode.from_dict(data)

        assert "Missing required field" in str(exc_info.value)

    def test_to_string(self):
        """Test de la méthode to_string."""
        node = AVLNode(50)
        left_child = AVLNode(30)
        right_child = AVLNode(70)

        node.set_left(left_child)
        node.set_right(right_child)

        result = node.to_string()

        assert "AVLNode(value=50" in result
        assert "AVLNode(value=30" in result
        assert "AVLNode(value=70" in result

    def test_to_string_with_indent(self):
        """Test de la méthode to_string avec indentation."""
        node = AVLNode(50)
        child = AVLNode(30)
        node.set_left(child)

        result = node.to_string(indent=2)

        assert result.startswith("    AVLNode")  # 4 espaces d'indentation

    def test_to_compact_string(self):
        """Test de la méthode to_compact_string."""
        node = AVLNode(50)
        node._balance_factor = -1
        node._cached_height = 2

        result = node.to_compact_string()

        assert result == "50(bf:-1:h:2)"

    def test_serialization_round_trip(self):
        """Test de sérialisation/désérialisation complète."""
        # Créer un arbre complexe
        root = AVLNode(50)
        left = AVLNode(30)
        right = AVLNode(70)
        left_left = AVLNode(20)
        left_right = AVLNode(40)

        root.set_left(left)
        root.set_right(right)
        left.set_left(left_left)
        left.set_right(left_right)

        # Sérialiser
        data = root.to_dict()

        # Désérialiser
        restored = AVLNode.from_dict(data)

        # Vérifier que l'arbre est identique
        assert restored.value == root.value
        assert restored.left.value == root.left.value
        assert restored.right.value == root.right.value
        assert restored.left.left.value == root.left.left.value
        assert restored.left.right.value == root.left.right.value

        # Vérifier les propriétés AVL
        assert restored.is_avl_valid()
        assert restored.validate_heights()
        assert restored.validate_balance_factor()
