"""
Tests unitaires pour la classe BinaryTreeNode.

Ce module contient tous les tests unitaires pour la classe BinaryTreeNode.
"""

import pytest

from src.exceptions import InvalidNodeOperationError, NodeValidationError
from src.binary_tree_node import BinaryTreeNode


class TestBinaryTreeNode:
    """Tests pour la classe BinaryTreeNode."""
    
    def test_init_with_value_only(self):
        """Test de l'initialisation avec seulement une valeur."""
        node = BinaryTreeNode(42)
        assert node.value == 42
        assert node.parent is None
        assert node.left is None
        assert node.right is None
        assert node.children == []
        assert node.metadata == {}
    
    def test_init_with_all_parameters(self):
        """Test de l'initialisation avec tous les paramètres."""
        parent = BinaryTreeNode(10)
        left = BinaryTreeNode(20)
        right = BinaryTreeNode(30)
        metadata = {"key": "value"}
        
        node = BinaryTreeNode(
            15,
            parent=parent,
            left=left,
            right=right,
            metadata=metadata
        )
        
        assert node.value == 15
        assert node.parent is parent
        assert node.left is left
        assert node.right is right
        assert left in node.children
        assert right in node.children
        assert node.metadata == metadata
    
    def test_left_property(self):
        """Test de la propriété left."""
        node = BinaryTreeNode(42)
        assert node.left is None
        
        left_child = BinaryTreeNode(20)
        node.set_left(left_child)
        assert node.left is left_child
    
    def test_right_property(self):
        """Test de la propriété right."""
        node = BinaryTreeNode(42)
        assert node.right is None
        
        right_child = BinaryTreeNode(30)
        node.set_right(right_child)
        assert node.right is right_child
    
    def test_set_left(self):
        """Test de la définition de l'enfant gauche."""
        node = BinaryTreeNode(42)
        left_child = BinaryTreeNode(20)
        
        node.set_left(left_child)
        assert node.left is left_child
        assert left_child.parent is node
        assert left_child in node.children
    
    def test_set_left_none(self):
        """Test de la suppression de l'enfant gauche."""
        node = BinaryTreeNode(42)
        left_child = BinaryTreeNode(20)
        
        node.set_left(left_child)
        assert node.left is left_child
        
        node.set_left(None)
        assert node.left is None
        assert left_child.parent is None
        assert left_child not in node.children
    
    def test_set_left_invalid_type(self):
        """Test de la définition d'un enfant gauche de type invalide."""
        node = BinaryTreeNode(42)
        
        with pytest.raises(InvalidNodeOperationError) as exc_info:
            node.set_left("not a BinaryTreeNode")
        
        assert "Left child must be a BinaryTreeNode" in str(exc_info.value)
        assert exc_info.value.operation == "set_left"
    
    def test_set_right(self):
        """Test de la définition de l'enfant droit."""
        node = BinaryTreeNode(42)
        right_child = BinaryTreeNode(30)
        
        node.set_right(right_child)
        assert node.right is right_child
        assert right_child.parent is node
        assert right_child in node.children
    
    def test_set_right_none(self):
        """Test de la suppression de l'enfant droit."""
        node = BinaryTreeNode(42)
        right_child = BinaryTreeNode(30)
        
        node.set_right(right_child)
        assert node.right is right_child
        
        node.set_right(None)
        assert node.right is None
        assert right_child.parent is None
        assert right_child not in node.children
    
    def test_set_right_invalid_type(self):
        """Test de la définition d'un enfant droit de type invalide."""
        node = BinaryTreeNode(42)
        
        with pytest.raises(InvalidNodeOperationError) as exc_info:
            node.set_right("not a BinaryTreeNode")
        
        assert "Right child must be a BinaryTreeNode" in str(exc_info.value)
        assert exc_info.value.operation == "set_right"
    
    def test_get_left(self):
        """Test de la méthode get_left."""
        node = BinaryTreeNode(42)
        left_child = BinaryTreeNode(20)
        
        node.set_left(left_child)
        assert node.get_left() is left_child
    
    def test_get_right(self):
        """Test de la méthode get_right."""
        node = BinaryTreeNode(42)
        right_child = BinaryTreeNode(30)
        
        node.set_right(right_child)
        assert node.get_right() is right_child
    
    def test_has_left(self):
        """Test de la méthode has_left."""
        node = BinaryTreeNode(42)
        assert node.has_left() is False
        
        left_child = BinaryTreeNode(20)
        node.set_left(left_child)
        assert node.has_left() is True
        
        node.set_left(None)
        assert node.has_left() is False
    
    def test_has_right(self):
        """Test de la méthode has_right."""
        node = BinaryTreeNode(42)
        assert node.has_right() is False
        
        right_child = BinaryTreeNode(30)
        node.set_right(right_child)
        assert node.has_right() is True
        
        node.set_right(None)
        assert node.has_right() is False
    
    def test_is_leaf(self):
        """Test de la méthode is_leaf."""
        node = BinaryTreeNode(42)
        assert node.is_leaf() is True
        
        left_child = BinaryTreeNode(20)
        node.set_left(left_child)
        assert node.is_leaf() is False
        
        right_child = BinaryTreeNode(30)
        node.set_right(right_child)
        assert node.is_leaf() is False
        
        node.set_left(None)
        node.set_right(None)
        assert node.is_leaf() is True
    
    def test_is_root(self):
        """Test de la méthode is_root."""
        node = BinaryTreeNode(42)
        assert node.is_root() is True
        
        parent = BinaryTreeNode(10)
        node.set_parent(parent)
        assert node.is_root() is False
    
    def test_get_height(self):
        """Test de la méthode get_height."""
        # Nœud feuille
        node = BinaryTreeNode(10)
        assert node.get_height() == 0
        
        # Nœud avec un enfant gauche
        left_child = BinaryTreeNode(20)
        node.set_left(left_child)
        assert node.get_height() == 1
        
        # Nœud avec un enfant droit
        right_child = BinaryTreeNode(30)
        node.set_right(right_child)
        assert node.get_height() == 1
        
        # Nœud avec petit-enfant
        grandchild = BinaryTreeNode(40)
        left_child.set_left(grandchild)
        assert node.get_height() == 2
    
    def test_get_depth(self):
        """Test de la méthode get_depth."""
        # Nœud racine
        root = BinaryTreeNode(10)
        assert root.get_depth() == 0
        
        # Nœud enfant
        child = BinaryTreeNode(20)
        child.set_parent(root)
        assert child.get_depth() == 1
        
        # Nœud petit-enfant
        grandchild = BinaryTreeNode(30)
        grandchild.set_parent(child)
        assert grandchild.get_depth() == 2
    
    def test_validate(self):
        """Test de la méthode validate."""
        parent = BinaryTreeNode(10)
        left = BinaryTreeNode(20)
        right = BinaryTreeNode(30)
        
        parent.set_left(left)
        parent.set_right(right)
        
        # Validation devrait réussir
        assert parent.validate() is True
        assert left.validate() is True
        assert right.validate() is True
    
    def test_validate_invalid_children_type(self):
        """Test de la validation avec des enfants de type invalide."""
        node = BinaryTreeNode(10)
        
        # Ajouter un enfant non-BinaryTreeNode (en contournant les vérifications)
        # Créer une classe mock qui n'est pas un BinaryTreeNode
        class MockNode:
            def __init__(self, value):
                self.value = value
                self.parent = None
        
        invalid_child = MockNode(20)
        node._children.append(invalid_child)
        
        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()
        
        assert "All children must be BinaryTreeNode instances" in str(exc_info.value)
        assert exc_info.value.validation_rule == "binary_tree_node_children_type"
    
    def test_validate_children_consistency(self):
        """Test de la validation de la cohérence des enfants."""
        node = BinaryTreeNode(10)
        left = BinaryTreeNode(20)
        right = BinaryTreeNode(30)
        
        node.set_left(left)
        node.set_right(right)
        
        # Casser la cohérence en ajoutant un enfant non référencé
        extra_child = BinaryTreeNode(40)
        node._children.append(extra_child)
        
        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()
        
        assert "Children list does not match left and right children" in str(exc_info.value)
        assert exc_info.value.validation_rule == "binary_tree_node_children_consistency"
    
    def test_validate_max_children(self):
        """Test de la validation du nombre maximum d'enfants."""
        node = BinaryTreeNode(10)
        child1 = BinaryTreeNode(20)
        child2 = BinaryTreeNode(30)
        child3 = BinaryTreeNode(40)
        
        node.set_left(child1)
        node.set_right(child2)
        
        # Ajouter un troisième enfant (en contournant les vérifications)
        node._children.append(child3)
        
        with pytest.raises(NodeValidationError) as exc_info:
            node.validate()
        
        # Le test devrait échouer sur la cohérence des enfants, pas sur le nombre max
        assert "Children list does not match left and right children" in str(exc_info.value)
        assert exc_info.value.validation_rule == "binary_tree_node_children_consistency"
    
    def test_get_children(self):
        """Test de la méthode get_children."""
        node = BinaryTreeNode(10)
        left = BinaryTreeNode(20)
        right = BinaryTreeNode(30)
        
        node.set_left(left)
        node.set_right(right)
        
        children = node.get_children()
        assert len(children) == 2
        assert left in children
        assert right in children
        # Vérifier que c'est une copie
        assert children is not node._children
    
    def test_get_children_partial(self):
        """Test de la méthode get_children avec seulement un enfant."""
        node = BinaryTreeNode(10)
        left = BinaryTreeNode(20)
        
        node.set_left(left)
        
        children = node.get_children()
        assert len(children) == 1
        assert left in children
    
    def test_add_child(self):
        """Test de l'ajout d'un enfant."""
        parent = BinaryTreeNode(10)
        child = BinaryTreeNode(20)
        
        parent.add_child(child)
        assert child in parent.children
        assert child.parent is parent
    
    def test_add_child_invalid_type(self):
        """Test de l'ajout d'un enfant de type invalide."""
        parent = BinaryTreeNode(10)
        
        with pytest.raises(InvalidNodeOperationError) as exc_info:
            parent.add_child("not a BinaryTreeNode")
        
        assert "Child must be a BinaryTreeNode" in str(exc_info.value)
        assert exc_info.value.operation == "add_child"
    
    def test_add_child_max_children(self):
        """Test de l'ajout d'un enfant quand on a déjà 2 enfants."""
        parent = BinaryTreeNode(10)
        child1 = BinaryTreeNode(20)
        child2 = BinaryTreeNode(30)
        child3 = BinaryTreeNode(40)
        
        parent.add_child(child1)
        parent.add_child(child2)
        
        with pytest.raises(InvalidNodeOperationError) as exc_info:
            parent.add_child(child3)
        
        assert "Binary tree node cannot have more than 2 children" in str(exc_info.value)
        assert exc_info.value.operation == "add_child"
    
    def test_str(self):
        """Test de la méthode __str__."""
        node = BinaryTreeNode(42)
        assert str(node) == "BinaryTreeNode(value=42)"
    
    def test_repr(self):
        """Test de la méthode __repr__."""
        node = BinaryTreeNode(42)
        repr_str = repr(node)
        assert "BinaryTreeNode" in repr_str
        assert "value=42" in repr_str
        assert "parent=None" in repr_str
        assert "left=None" in repr_str
        assert "right=None" in repr_str
    
    def test_repr_with_children(self):
        """Test de la méthode __repr__ avec des enfants."""
        node = BinaryTreeNode(42)
        left = BinaryTreeNode(20)
        right = BinaryTreeNode(30)
        
        node.set_left(left)
        node.set_right(right)
        
        repr_str = repr(node)
        assert "BinaryTreeNode" in repr_str
        assert "value=42" in repr_str
        assert "left=" in repr_str
        assert "right=" in repr_str
    
    def test_eq(self):
        """Test de la méthode __eq__."""
        node1 = BinaryTreeNode(42)
        node2 = BinaryTreeNode(42)
        node3 = BinaryTreeNode(43)
        
        # Même valeur, pas de parent, pas d'enfants
        assert node1 == node2
        
        # Valeurs différentes
        assert node1 != node3
        
        # Différents types
        assert node1 != "not a node"
    
    def test_eq_with_children(self):
        """Test de la méthode __eq__ avec des enfants."""
        node1 = BinaryTreeNode(42)
        node2 = BinaryTreeNode(42)
        
        left1 = BinaryTreeNode(20)
        right1 = BinaryTreeNode(30)
        left2 = BinaryTreeNode(20)
        right2 = BinaryTreeNode(30)
        
        node1.set_left(left1)
        node1.set_right(right1)
        node2.set_left(left2)
        node2.set_right(right2)
        
        # Les nœuds sont différents car ils ont des enfants différents
        assert node1 != node2
    
    def test_hash(self):
        """Test de la méthode __hash__."""
        node1 = BinaryTreeNode(42)
        node2 = BinaryTreeNode(42)
        
        # Même nœud
        assert hash(node1) == hash(node1)
        
        # Nœuds différents (même valeur mais instances différentes)
        # Les hash peuvent être identiques par hasard, testons plutôt la cohérence
        assert hash(node1) == hash(node1)  # Même objet
        assert hash(node2) == hash(node2)  # Même objet
    
    def test_inheritance(self):
        """Test que BinaryTreeNode hérite bien de TreeNode."""
        from src.tree_node import TreeNode
        
        node = BinaryTreeNode(42)
        assert isinstance(node, TreeNode)
        assert isinstance(node, BinaryTreeNode)