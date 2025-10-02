"""
Tests unitaires pour la classe AVLRotations.

Ce module contient tous les tests unitaires pour la classe AVLRotations,
incluant les tests de rotation simple, double et de validation.
"""

import pytest
from src.avl_node import AVLNode
from src.avl_rotations import AVLRotations
from src.exceptions import RotationError


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
