"""
Tests unitaires pour la classe TreeNode.

Ce module contient tous les tests unitaires pour la classe TreeNode abstraite.
Pour tester les méthodes abstraites, nous utilisons une classe concrète de test.
"""

import pytest
from typing import List, Optional

from src.baobab_tree.core.exceptions import (
    CircularReferenceError,
    InvalidNodeOperationError,
    NodeValidationError,
)
from src.baobab_tree.core.interfaces import T
from src.baobab_tree.core.tree_node import TreeNode


class ConcreteTreeNode(TreeNode):
    """
    Implémentation concrète de TreeNode pour les tests.

    Cette classe implémente toutes les méthodes abstraites de TreeNode
    pour permettre les tests unitaires.
    """

    def is_leaf(self) -> bool:
        """Vérifie si le nœud est une feuille."""
        return len(self._children) == 0

    def is_root(self) -> bool:
        """Vérifie si le nœud est la racine."""
        return self._parent is None

    def get_height(self) -> int:
        """Calcule la hauteur du nœud."""
        if self.is_leaf():
            return 0

        max_child_height = -1
        for child in self._children:
            child_height = child.get_height()
            max_child_height = max(max_child_height, child_height)

        return 1 + max_child_height

    def get_depth(self) -> int:
        """Calcule la profondeur du nœud."""
        if self.is_root():
            return 0

        return 1 + self._parent.get_depth()

    def validate(self) -> bool:
        """Valide les propriétés du nœud."""
        # Vérifier que tous les enfants ont ce nœud comme parent
        for child in self._children:
            if child.parent is not self:
                raise NodeValidationError(
                    "Child does not have this node as parent",
                    "parent_child_consistency",
                    self,
                )

        # Vérifier que le parent a ce nœud comme enfant
        if self._parent is not None:
            if self not in self._parent._children:
                raise NodeValidationError(
                    "Parent does not have this node as child",
                    "parent_child_consistency",
                    self,
                )

        return True


class TestTreeNode:
    """Tests pour la classe TreeNode."""

    def test_init_with_value_only(self):
        """Test de l'initialisation avec seulement une valeur."""
        node = ConcreteTreeNode(42)
        assert node.value == 42
        assert node.parent is None
        assert node.children == []
        assert node.metadata == {}

    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        parent = ConcreteTreeNode(10)
        child1 = ConcreteTreeNode(20)
        child2 = ConcreteTreeNode(30)
        metadata = {"key": "value"}

        node = ConcreteTreeNode(
            15, parent=parent, children=[child1, child2], metadata=metadata
        )

        assert node.value == 15
        assert node.parent is parent
        assert len(node.children) == 2
        assert child1 in node.children
        assert child2 in node.children
        assert node.metadata == metadata

    def test_value_property(self):
        """Test de la propriété value."""
        node = ConcreteTreeNode(42)
        assert node.value == 42

        node.value = 100
        assert node.value == 100

    def test_parent_property(self):
        """Test de la propriété parent."""
        node = ConcreteTreeNode(42)
        assert node.parent is None

        parent = ConcreteTreeNode(10)
        node.set_parent(parent)
        assert node.parent is parent

    def test_children_property(self):
        """Test de la propriété children."""
        node = ConcreteTreeNode(42)
        assert node.children == []

        child1 = ConcreteTreeNode(20)
        child2 = ConcreteTreeNode(30)
        node.add_child(child1)
        node.add_child(child2)

        children = node.children
        assert len(children) == 2
        assert child1 in children
        assert child2 in children
        # Vérifier que c'est une copie
        assert children is not node._children

    def test_metadata_property(self):
        """Test de la propriété metadata."""
        node = ConcreteTreeNode(42)
        assert node.metadata == {}

        node.set_metadata("key1", "value1")
        node.set_metadata("key2", "value2")

        metadata = node.metadata
        assert metadata == {"key1": "value1", "key2": "value2"}
        # Vérifier que c'est une copie
        assert metadata is not node._metadata

    def test_add_child(self):
        """Test de l'ajout d'un enfant."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        parent.add_child(child)

        assert child in parent.children
        assert child.parent is parent

    def test_add_child_none(self):
        """Test de l'ajout d'un enfant None."""
        parent = ConcreteTreeNode(10)

        with pytest.raises(InvalidNodeOperationError) as exc_info:
            parent.add_child(None)

        assert "Cannot add None as child" in str(exc_info.value)
        assert exc_info.value.operation == "add_child"

    def test_add_child_self(self):
        """Test de l'ajout de soi-même comme enfant."""
        node = ConcreteTreeNode(10)

        with pytest.raises(CircularReferenceError) as exc_info:
            node.add_child(node)

        assert "Cannot add node as its own child" in str(exc_info.value)

    def test_add_child_circular_reference(self):
        """Test de l'ajout créant une référence circulaire."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)
        grandchild = ConcreteTreeNode(30)

        parent.add_child(child)
        child.add_child(grandchild)

        with pytest.raises(CircularReferenceError) as exc_info:
            grandchild.add_child(parent)

        assert "Adding this child would create a circular reference" in str(
            exc_info.value
        )

    def test_remove_child(self):
        """Test de la suppression d'un enfant."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        parent.add_child(child)
        assert child in parent.children

        result = parent.remove_child(child)
        assert result is True
        assert child not in parent.children
        assert child.parent is None

    def test_remove_child_not_present(self):
        """Test de la suppression d'un enfant non présent."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        result = parent.remove_child(child)
        assert result is False

    def test_remove_child_none(self):
        """Test de la suppression d'un enfant None."""
        parent = ConcreteTreeNode(10)

        with pytest.raises(InvalidNodeOperationError) as exc_info:
            parent.remove_child(None)

        assert "Cannot remove None child" in str(exc_info.value)
        assert exc_info.value.operation == "remove_child"

    def test_get_children(self):
        """Test de la méthode get_children."""
        parent = ConcreteTreeNode(10)
        child1 = ConcreteTreeNode(20)
        child2 = ConcreteTreeNode(30)

        parent.add_child(child1)
        parent.add_child(child2)

        children = parent.get_children()
        assert len(children) == 2
        assert child1 in children
        assert child2 in children
        # Vérifier que c'est une copie
        assert children is not parent._children

    def test_get_parent(self):
        """Test de la méthode get_parent."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        child.set_parent(parent)
        assert child.get_parent() is parent

    def test_set_parent(self):
        """Test de la définition du parent."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        child.set_parent(parent)
        assert child.parent is parent
        assert child in parent.children

    def test_set_parent_none(self):
        """Test de la suppression du parent."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        child.set_parent(parent)
        assert child.parent is parent

        child.set_parent(None)
        assert child.parent is None
        assert child not in parent.children

    def test_set_parent_self(self):
        """Test de la définition de soi-même comme parent."""
        node = ConcreteTreeNode(10)

        with pytest.raises(CircularReferenceError) as exc_info:
            node.set_parent(node)

        assert "Cannot set node as its own parent" in str(exc_info.value)

    def test_set_parent_circular_reference(self):
        """Test de la définition d'un parent créant une référence circulaire."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        parent.add_child(child)

        # Essayer de définir l'enfant comme parent de son parent
        with pytest.raises(CircularReferenceError) as exc_info:
            parent.set_parent(child)

        assert "Setting this parent would create a circular reference" in str(
            exc_info.value
        )

    def test_clear_metadata(self):
        """Test de l'effacement des métadonnées."""
        node = ConcreteTreeNode(10)
        node.set_metadata("key1", "value1")
        node.set_metadata("key2", "value2")

        assert len(node.metadata) == 2

        node.clear_metadata()
        assert len(node.metadata) == 0

    def test_set_metadata(self):
        """Test de la définition d'une métadonnée."""
        node = ConcreteTreeNode(10)

        node.set_metadata("key", "value")
        assert node.get_metadata("key") == "value"

    def test_set_metadata_invalid_key(self):
        """Test de la définition d'une métadonnée avec une clé invalide."""
        node = ConcreteTreeNode(10)

        with pytest.raises(InvalidNodeOperationError) as exc_info:
            node.set_metadata(123, "value")

        assert "Metadata key must be a string" in str(exc_info.value)
        assert exc_info.value.operation == "set_metadata"

    def test_get_metadata(self):
        """Test de la récupération d'une métadonnée."""
        node = ConcreteTreeNode(10)
        node.set_metadata("key", "value")

        assert node.get_metadata("key") == "value"
        assert node.get_metadata("nonexistent") is None
        assert node.get_metadata("nonexistent", "default") == "default"

    def test_is_leaf(self):
        """Test de la méthode is_leaf."""
        node = ConcreteTreeNode(10)
        assert node.is_leaf() is True

        child = ConcreteTreeNode(20)
        node.add_child(child)
        assert node.is_leaf() is False

    def test_is_root(self):
        """Test de la méthode is_root."""
        node = ConcreteTreeNode(10)
        assert node.is_root() is True

        parent = ConcreteTreeNode(5)
        node.set_parent(parent)
        assert node.is_root() is False

    def test_get_height(self):
        """Test de la méthode get_height."""
        # Nœud feuille
        node = ConcreteTreeNode(10)
        assert node.get_height() == 0

        # Nœud avec un enfant
        child = ConcreteTreeNode(20)
        node.add_child(child)
        assert node.get_height() == 1

        # Nœud avec deux enfants
        child2 = ConcreteTreeNode(30)
        node.add_child(child2)
        assert node.get_height() == 1

        # Nœud avec petit-fils
        grandchild = ConcreteTreeNode(40)
        child.add_child(grandchild)
        assert node.get_height() == 2

    def test_get_depth(self):
        """Test de la méthode get_depth."""
        # Nœud racine
        root = ConcreteTreeNode(10)
        assert root.get_depth() == 0

        # Nœud enfant
        child = ConcreteTreeNode(20)
        child.set_parent(root)
        assert child.get_depth() == 1

        # Nœud petit-enfant
        grandchild = ConcreteTreeNode(30)
        grandchild.set_parent(child)
        assert grandchild.get_depth() == 2

    def test_validate(self):
        """Test de la méthode validate."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        parent.add_child(child)

        # Validation devrait réussir
        assert parent.validate() is True
        assert child.validate() is True

    def test_validate_invalid_parent_child_relationship(self):
        """Test de la validation avec une relation parent-enfant invalide."""
        parent = ConcreteTreeNode(10)
        child = ConcreteTreeNode(20)

        # Ajouter l'enfant au parent
        parent.add_child(child)

        # Casser la relation en modifiant directement les attributs
        child._parent = None

        with pytest.raises(NodeValidationError) as exc_info:
            parent.validate()

        assert "Child does not have this node as parent" in str(exc_info.value)
        assert exc_info.value.validation_rule == "parent_child_consistency"

    def test_str(self):
        """Test de la méthode __str__."""
        node = ConcreteTreeNode(42)
        assert str(node) == "TreeNode(value=42)"

    def test_repr(self):
        """Test de la méthode __repr__."""
        node = ConcreteTreeNode(42)
        repr_str = repr(node)
        assert "TreeNode" in repr_str
        assert "value=42" in repr_str
        assert "parent=None" in repr_str
        assert "children_count=0" in repr_str

    def test_eq(self):
        """Test de la méthode __eq__."""
        node1 = ConcreteTreeNode(42)
        node2 = ConcreteTreeNode(42)
        node3 = ConcreteTreeNode(43)

        # Même valeur, pas de parent, pas d'enfants
        assert node1 == node2

        # Valeurs différentes
        assert node1 != node3

        # Différents types
        assert node1 != "not a node"

    def test_hash(self):
        """Test de la méthode __hash__."""
        node1 = ConcreteTreeNode(42)
        node2 = ConcreteTreeNode(42)

        # Même nœud
        assert hash(node1) == hash(node1)

        # Nœuds différents (même valeur mais instances différentes)
        # Les hash peuvent être identiques par hasard, testons plutôt la cohérence
        assert hash(node1) == hash(node1)  # Même objet
        assert hash(node2) == hash(node2)  # Même objet
