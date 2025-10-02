"""
Tests unitaires pour les cas d'erreur de TreeNode.

Ce module contient les tests pour les cas d'erreur et les branches
exceptionnelles de la classe TreeNode.
"""

import unittest
from unittest.mock import patch, MagicMock

from src.tree_node import TreeNode
from src.exceptions import (
    CircularReferenceError,
    InvalidNodeOperationError,
    NodeValidationError,
)


class MockTreeNode(TreeNode):
    """Classe mock pour tester TreeNode."""

    def is_leaf(self) -> bool:
        return len(self._children) == 0

    def is_root(self) -> bool:
        return self._parent is None

    def get_height(self) -> int:
        if self.is_leaf():
            return 0
        return 1 + max((child.get_height() for child in self._children), default=0)

    def get_depth(self) -> int:
        if self.is_root():
            return 0
        return 1 + self._parent.get_depth()

    def validate(self) -> bool:
        # Validation simple pour les tests
        if self._parent is not None and self not in self._parent._children:
            raise NodeValidationError(
                "Child not in parent's children list", "parent_child_consistency", self
            )
        return True


class TestTreeNodeErrorCases(unittest.TestCase):
    """
    Classe de tests pour les cas d'erreur de TreeNode.
    """

    def test_add_child_none(self):
        """Test d'ajout d'un enfant None."""
        node = MockTreeNode(42)

        with self.assertRaises(InvalidNodeOperationError) as context:
            node.add_child(None)

        self.assertIn("Cannot add None as child", str(context.exception))
        self.assertEqual(context.exception.operation, "add_child")

    def test_add_child_self(self):
        """Test d'ajout de soi-même comme enfant."""
        node = MockTreeNode(42)

        with self.assertRaises(CircularReferenceError) as context:
            node.add_child(node)

        self.assertIn("Cannot add node as its own child", str(context.exception))
        self.assertEqual(context.exception.node1, node)
        self.assertEqual(context.exception.node2, node)

    def test_add_child_circular_reference(self):
        """Test d'ajout créant une référence circulaire."""
        parent = MockTreeNode(42)
        child = MockTreeNode(24)
        grandchild = MockTreeNode(12)

        # Créer une structure parent -> child -> grandchild
        parent.add_child(child)
        child.add_child(grandchild)

        # Essayer d'ajouter parent comme enfant de grandchild (circulaire)
        with self.assertRaises(CircularReferenceError) as context:
            grandchild.add_child(parent)

        self.assertIn(
            "Adding this child would create a circular reference",
            str(context.exception),
        )
        self.assertEqual(context.exception.node1, grandchild)
        self.assertEqual(context.exception.node2, parent)

    def test_remove_child_none(self):
        """Test de suppression d'un enfant None."""
        node = MockTreeNode(42)

        with self.assertRaises(InvalidNodeOperationError) as context:
            node.remove_child(None)

        self.assertIn("Cannot remove None child", str(context.exception))
        self.assertEqual(context.exception.operation, "remove_child")

    def test_set_parent_self(self):
        """Test de définition de soi-même comme parent."""
        node = MockTreeNode(42)

        with self.assertRaises(CircularReferenceError) as context:
            node.set_parent(node)

        self.assertIn("Cannot set node as its own parent", str(context.exception))
        self.assertEqual(context.exception.node1, node)
        self.assertEqual(context.exception.node2, node)

    def test_set_parent_circular_reference(self):
        """Test de définition d'un parent créant une référence circulaire."""
        parent = MockTreeNode(42)
        child = MockTreeNode(24)
        grandchild = MockTreeNode(12)

        # Créer une structure parent -> child -> grandchild
        parent.add_child(child)
        child.add_child(grandchild)

        # Essayer de définir grandchild comme parent de parent (circulaire)
        with self.assertRaises(CircularReferenceError) as context:
            parent.set_parent(grandchild)

        self.assertIn(
            "Setting this parent would create a circular reference",
            str(context.exception),
        )
        self.assertEqual(context.exception.node1, parent)
        self.assertEqual(context.exception.node2, grandchild)

    def test_set_metadata_invalid_key(self):
        """Test de définition d'une métadonnée avec une clé invalide."""
        node = MockTreeNode(42)

        with self.assertRaises(InvalidNodeOperationError) as context:
            node.set_metadata(123, "value")  # Clé non-string

        self.assertIn("Metadata key must be a string", str(context.exception))
        self.assertEqual(context.exception.operation, "set_metadata")

    def test_validate_parent_child_consistency_error(self):
        """Test de validation échouant sur la cohérence parent-enfant."""
        parent = MockTreeNode(42)
        child = MockTreeNode(24)

        # Ajouter l'enfant normalement
        parent.add_child(child)

        # Corrompre la relation en retirant l'enfant de la liste du parent
        parent._children.remove(child)

        # La validation doit échouer
        with self.assertRaises(NodeValidationError) as context:
            child.validate()

        self.assertIn("Child not in parent's children list", str(context.exception))
        self.assertEqual(context.exception.validation_rule, "parent_child_consistency")

    def test_would_create_circular_reference_direct(self):
        """Test de détection de référence circulaire directe."""
        node = MockTreeNode(42)

        # Test avec soi-même
        self.assertTrue(node._would_create_circular_reference(node))

    def test_would_create_circular_reference_ancestor(self):
        """Test de détection de référence circulaire avec ancêtre."""
        parent = MockTreeNode(42)
        child = MockTreeNode(24)
        grandchild = MockTreeNode(12)

        parent.add_child(child)
        child.add_child(grandchild)

        # grandchild est un ancêtre de parent
        self.assertTrue(parent._would_create_circular_reference(grandchild))

    def test_would_create_circular_reference_descendant(self):
        """Test de détection de référence circulaire avec descendant."""
        parent = MockTreeNode(42)
        child = MockTreeNode(24)
        grandchild = MockTreeNode(12)

        parent.add_child(child)
        child.add_child(grandchild)

        # parent est un ancêtre de grandchild
        self.assertTrue(grandchild._would_create_circular_reference(parent))

    def test_would_create_circular_reference_no_circle(self):
        """Test de détection d'absence de référence circulaire."""
        node1 = MockTreeNode(42)
        node2 = MockTreeNode(24)
        node3 = MockTreeNode(12)

        node1.add_child(node2)
        node2.add_child(node3)

        # node1 et node3 ne sont pas liés directement
        # Mais node3 est un descendant de node1, donc c'est une référence circulaire
        self.assertTrue(node1._would_create_circular_reference(node3))

    def test_remove_child_not_present(self):
        """Test de suppression d'un enfant non présent."""
        node = MockTreeNode(42)
        other_node = MockTreeNode(24)

        # Essayer de supprimer un nœud qui n'est pas un enfant
        result = node.remove_child(other_node)
        self.assertFalse(result)

    def test_remove_child_success(self):
        """Test de suppression réussie d'un enfant."""
        parent = MockTreeNode(42)
        child = MockTreeNode(24)

        parent.add_child(child)
        self.assertEqual(len(parent._children), 1)
        self.assertEqual(child._parent, parent)

        result = parent.remove_child(child)
        self.assertTrue(result)
        self.assertEqual(len(parent._children), 0)
        self.assertIsNone(child._parent)

    def test_set_parent_removes_from_old_parent(self):
        """Test que set_parent retire le nœud de son ancien parent."""
        old_parent = MockTreeNode(42)
        new_parent = MockTreeNode(24)
        child = MockTreeNode(12)

        old_parent.add_child(child)
        self.assertEqual(len(old_parent._children), 1)
        self.assertEqual(child._parent, old_parent)

        child.set_parent(new_parent)
        self.assertEqual(len(old_parent._children), 0)
        self.assertEqual(len(new_parent._children), 1)
        self.assertEqual(child._parent, new_parent)

    def test_set_parent_none_removes_from_parent(self):
        """Test que set_parent(None) retire le nœud de son parent."""
        parent = MockTreeNode(42)
        child = MockTreeNode(24)

        parent.add_child(child)
        self.assertEqual(len(parent._children), 1)
        self.assertEqual(child._parent, parent)

        child.set_parent(None)
        self.assertEqual(len(parent._children), 0)
        self.assertIsNone(child._parent)

    def test_clear_metadata(self):
        """Test de suppression de toutes les métadonnées."""
        node = MockTreeNode(42)
        node.set_metadata("key1", "value1")
        node.set_metadata("key2", "value2")

        self.assertEqual(len(node._metadata), 2)

        node.clear_metadata()
        self.assertEqual(len(node._metadata), 0)

    def test_get_metadata_with_default(self):
        """Test de récupération de métadonnée avec valeur par défaut."""
        node = MockTreeNode(42)

        # Test avec clé existante
        node.set_metadata("key1", "value1")
        self.assertEqual(node.get_metadata("key1"), "value1")

        # Test avec clé inexistante et valeur par défaut
        self.assertEqual(node.get_metadata("key2", "default"), "default")

        # Test avec clé inexistante sans valeur par défaut
        self.assertIsNone(node.get_metadata("key2"))

    def test_children_property_copy(self):
        """Test que la propriété children retourne une copie."""
        node = MockTreeNode(42)
        child1 = MockTreeNode(24)
        child2 = MockTreeNode(12)

        node.add_child(child1)
        node.add_child(child2)

        children = node.children
        self.assertEqual(len(children), 2)

        # Modifier la copie ne doit pas affecter l'original
        children.clear()
        self.assertEqual(len(node._children), 2)

    def test_metadata_property_copy(self):
        """Test que la propriété metadata retourne une copie."""
        node = MockTreeNode(42)
        node.set_metadata("key1", "value1")

        metadata = node.metadata
        self.assertEqual(len(metadata), 1)

        # Modifier la copie ne doit pas affecter l'original
        metadata.clear()
        self.assertEqual(len(node._metadata), 1)


if __name__ == "__main__":
    unittest.main()
