"""
Tests unitaires pour les cas d'erreur de BinaryTreeNode.

Ce module contient les tests pour les cas d'erreur et les branches
exceptionnelles de la classe BinaryTreeNode.
"""

import unittest
from unittest.mock import patch, MagicMock

from src.binary_tree_node import BinaryTreeNode
from src.exceptions import (
    InvalidNodeOperationError,
    NodeValidationError,
    CircularReferenceError,
)


class TestBinaryTreeNodeErrorCases(unittest.TestCase):
    """
    Classe de tests pour les cas d'erreur de BinaryTreeNode.
    """

    def test_set_left_none(self):
        """Test de définition d'un enfant gauche None."""
        node = BinaryTreeNode(42)

        # Définir None comme enfant gauche doit fonctionner
        node.set_left(None)
        self.assertIsNone(node.left)
        self.assertIsNone(node._left)

    def test_set_right_none(self):
        """Test de définition d'un enfant droit None."""
        node = BinaryTreeNode(42)

        # Définir None comme enfant droit doit fonctionner
        node.set_right(None)
        self.assertIsNone(node.right)
        self.assertIsNone(node._right)

    def test_set_left_self(self):
        """Test de définition de soi-même comme enfant gauche."""
        node = BinaryTreeNode(42)

        with self.assertRaises(CircularReferenceError) as context:
            node.set_left(node)

        self.assertIn("Cannot add node as its own child", str(context.exception))

    def test_set_right_self(self):
        """Test de définition de soi-même comme enfant droit."""
        node = BinaryTreeNode(42)

        with self.assertRaises(CircularReferenceError) as context:
            node.set_right(node)

        self.assertIn("Cannot add node as its own child", str(context.exception))

    def test_set_left_circular_reference(self):
        """Test de définition d'un enfant gauche créant une référence circulaire."""
        parent = BinaryTreeNode(42)
        child = BinaryTreeNode(24)
        grandchild = BinaryTreeNode(12)

        # Créer une structure parent -> child -> grandchild
        parent.set_left(child)
        child.set_left(grandchild)

        # Essayer de définir parent comme enfant gauche de grandchild (circulaire)
        with self.assertRaises(CircularReferenceError) as context:
            grandchild.set_left(parent)

        self.assertIn(
            "Adding this child would create a circular reference",
            str(context.exception),
        )

    def test_set_right_circular_reference(self):
        """Test de définition d'un enfant droit créant une référence circulaire."""
        parent = BinaryTreeNode(42)
        child = BinaryTreeNode(24)
        grandchild = BinaryTreeNode(12)

        # Créer une structure parent -> child -> grandchild
        parent.set_right(child)
        child.set_right(grandchild)

        # Essayer de définir parent comme enfant droit de grandchild (circulaire)
        with self.assertRaises(CircularReferenceError) as context:
            grandchild.set_right(parent)

        self.assertIn(
            "Adding this child would create a circular reference",
            str(context.exception),
        )

    def test_add_child_too_many_children(self):
        """Test d'ajout d'un enfant quand il y en a déjà 2."""
        node = BinaryTreeNode(42)
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)
        child3 = BinaryTreeNode(6)

        # Ajouter les deux premiers enfants
        node.add_child(child1)
        node.add_child(child2)

        # Essayer d'ajouter un troisième enfant
        with self.assertRaises(InvalidNodeOperationError) as context:
            node.add_child(child3)

        self.assertIn(
            "Binary tree node cannot have more than 2 children", str(context.exception)
        )
        self.assertEqual(context.exception.operation, "add_child")

    def test_set_left_when_occupied(self):
        """Test de définition d'un enfant gauche quand la position est occupée."""
        node = BinaryTreeNode(42)
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)

        # Ajouter le premier enfant gauche
        node.set_left(child1)
        self.assertEqual(node.left, child1)

        # Remplacer par le deuxième enfant gauche
        node.set_left(child2)
        self.assertEqual(node.left, child2)
        self.assertIsNone(child1.parent)  # L'ancien enfant n'a plus de parent

    def test_set_right_when_occupied(self):
        """Test de définition d'un enfant droit quand la position est occupée."""
        node = BinaryTreeNode(42)
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)

        # Ajouter le premier enfant droit
        node.set_right(child1)
        self.assertEqual(node.right, child1)

        # Remplacer par le deuxième enfant droit
        node.set_right(child2)
        self.assertEqual(node.right, child2)
        self.assertIsNone(child1.parent)  # L'ancien enfant n'a plus de parent

    def test_remove_child_success(self):
        """Test de suppression réussie d'un enfant."""
        node = BinaryTreeNode(42)
        child = BinaryTreeNode(24)

        node.add_child(child)
        self.assertEqual(len(node._children), 1)
        self.assertEqual(child.parent, node)

        result = node.remove_child(child)
        self.assertTrue(result)
        self.assertEqual(len(node._children), 0)
        self.assertIsNone(child.parent)

    def test_remove_child_not_found(self):
        """Test de suppression d'un enfant non trouvé."""
        node = BinaryTreeNode(42)
        child = BinaryTreeNode(24)

        # Essayer de supprimer un enfant qui n'existe pas
        result = node.remove_child(child)
        self.assertFalse(result)

    def test_remove_child_wrong_node(self):
        """Test de suppression d'un enfant différent."""
        node = BinaryTreeNode(42)
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)

        # Ajouter le premier enfant
        node.add_child(child1)

        # Essayer de supprimer le deuxième enfant
        result = node.remove_child(child2)
        self.assertFalse(result)

        # Le premier enfant doit toujours être là
        self.assertIn(child1, node._children)

    def test_validate_binary_tree_property(self):
        """Test de validation de la propriété d'arbre binaire."""
        node = BinaryTreeNode(42)

        # Ajouter plus de 2 enfants via la liste _children
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)
        child3 = BinaryTreeNode(6)

        # Ajouter les enfants normalement
        node.add_child(child1)
        node.add_child(child2)

        # Ajouter un troisième enfant directement dans la liste (corruption)
        node._children.append(child3)

        # La validation doit échouer
        with self.assertRaises(NodeValidationError) as context:
            node.validate()

        # La validation échoue d'abord sur la cohérence des enfants
        self.assertIn(
            "Children list does not match left and right children",
            str(context.exception),
        )
        self.assertEqual(
            context.exception.validation_rule, "binary_tree_node_children_consistency"
        )

    def test_validate_left_child_consistency(self):
        """Test de validation de la cohérence de l'enfant gauche."""
        node = BinaryTreeNode(42)
        child = BinaryTreeNode(24)

        # Ajouter l'enfant à gauche
        node.set_left(child)

        # Corrompre la relation en retirant l'enfant de la liste
        node._children.remove(child)

        # La validation doit échouer
        with self.assertRaises(NodeValidationError) as context:
            node.validate()

        self.assertIn(
            "Children list does not match left and right children",
            str(context.exception),
        )
        self.assertEqual(
            context.exception.validation_rule, "binary_tree_node_children_consistency"
        )

    def test_validate_right_child_consistency(self):
        """Test de validation de la cohérence de l'enfant droit."""
        node = BinaryTreeNode(42)
        child = BinaryTreeNode(24)

        # Ajouter l'enfant à droite
        node.set_right(child)

        # Corrompre la relation en retirant l'enfant de la liste
        node._children.remove(child)

        # La validation doit échouer
        with self.assertRaises(NodeValidationError) as context:
            node.validate()

        self.assertIn(
            "Children list does not match left and right children",
            str(context.exception),
        )
        self.assertEqual(
            context.exception.validation_rule, "binary_tree_node_children_consistency"
        )

    def test_validate_children_list_consistency(self):
        """Test de validation de la cohérence de la liste des enfants."""
        node = BinaryTreeNode(42)
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)

        # Ajouter les enfants
        node.add_child(child1)
        node.add_child(child2)

        # Ajouter un enfant supplémentaire dans la liste (corruption)
        extra_child = BinaryTreeNode(6)
        node._children.append(extra_child)

        # La validation doit échouer
        with self.assertRaises(NodeValidationError) as context:
            node.validate()

        self.assertIn(
            "Children list does not match left and right children",
            str(context.exception),
        )
        self.assertEqual(
            context.exception.validation_rule, "binary_tree_node_children_consistency"
        )

    def test_validate_parent_child_consistency(self):
        """Test de validation de la cohérence parent-enfant."""
        node = BinaryTreeNode(42)
        child = BinaryTreeNode(24)

        # Ajouter l'enfant
        node.add_child(child)

        # Corrompre la relation parent-enfant
        child._parent = None

        # La validation doit échouer
        with self.assertRaises(NodeValidationError) as context:
            node.validate()

        # La validation échoue d'abord sur la cohérence des enfants
        self.assertIn(
            "Children list does not match left and right children",
            str(context.exception),
        )
        self.assertEqual(
            context.exception.validation_rule, "binary_tree_node_children_consistency"
        )

    def test_set_left_replaces_existing(self):
        """Test que set_left remplace l'enfant gauche existant."""
        node = BinaryTreeNode(42)
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)

        # Ajouter le premier enfant gauche
        node.set_left(child1)
        self.assertEqual(node.left, child1)
        self.assertEqual(child1.parent, node)

        # Remplacer par le deuxième enfant
        node.set_left(child2)
        self.assertEqual(node.left, child2)
        self.assertEqual(child2.parent, node)
        self.assertIsNone(child1.parent)  # L'ancien enfant n'a plus de parent

    def test_set_right_replaces_existing(self):
        """Test que set_right remplace l'enfant droit existant."""
        node = BinaryTreeNode(42)
        child1 = BinaryTreeNode(24)
        child2 = BinaryTreeNode(12)

        # Ajouter le premier enfant droit
        node.set_right(child1)
        self.assertEqual(node.right, child1)
        self.assertEqual(child1.parent, node)

        # Remplacer par le deuxième enfant
        node.set_right(child2)
        self.assertEqual(node.right, child2)
        self.assertEqual(child2.parent, node)
        self.assertIsNone(child1.parent)  # L'ancien enfant n'a plus de parent

    def test_has_left_and_right(self):
        """Test des méthodes has_left et has_right."""
        node = BinaryTreeNode(42)
        child = BinaryTreeNode(24)

        # Initialement, pas d'enfants
        self.assertFalse(node.has_left())
        self.assertFalse(node.has_right())

        # Ajouter un enfant gauche
        node.set_left(child)
        self.assertTrue(node.has_left())
        self.assertFalse(node.has_right())

        # Retirer l'enfant gauche
        node.set_left(None)
        self.assertFalse(node.has_left())
        self.assertFalse(node.has_right())

        # Ajouter un enfant droit
        node.set_right(child)
        self.assertFalse(node.has_left())
        self.assertTrue(node.has_right())

    def test_is_leaf_with_children(self):
        """Test de is_leaf avec des enfants."""
        node = BinaryTreeNode(42)
        child = BinaryTreeNode(24)

        # Initialement, c'est une feuille
        self.assertTrue(node.is_leaf())

        # Ajouter un enfant gauche
        node.set_left(child)
        self.assertFalse(node.is_leaf())

        # Retirer l'enfant gauche
        node.set_left(None)
        self.assertTrue(node.is_leaf())

        # Ajouter un enfant droit
        node.set_right(child)
        self.assertFalse(node.is_leaf())

    def test_get_height_with_children(self):
        """Test de get_height avec des enfants."""
        node = BinaryTreeNode(42)
        left_child = BinaryTreeNode(24)
        right_child = BinaryTreeNode(12)

        # Hauteur d'un nœud seul
        self.assertEqual(node.get_height(), 0)

        # Hauteur avec un enfant gauche
        node.set_left(left_child)
        self.assertEqual(node.get_height(), 1)

        # Hauteur avec deux enfants
        node.set_right(right_child)
        self.assertEqual(node.get_height(), 1)

        # Hauteur avec un petit-fils
        grandchild = BinaryTreeNode(6)
        left_child.set_left(grandchild)
        self.assertEqual(node.get_height(), 2)

    def test_get_depth_with_parent(self):
        """Test de get_depth avec un parent."""
        parent = BinaryTreeNode(42)
        child = BinaryTreeNode(24)
        grandchild = BinaryTreeNode(12)

        # Profondeur d'un nœud racine
        self.assertEqual(parent.get_depth(), 0)

        # Profondeur d'un enfant
        parent.set_left(child)
        self.assertEqual(child.get_depth(), 1)

        # Profondeur d'un petit-fils
        child.set_left(grandchild)
        self.assertEqual(grandchild.get_depth(), 2)


if __name__ == "__main__":
    unittest.main()
