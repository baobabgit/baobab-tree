"""
Tests unitaires pour la classe BTreeNode.

Ce module contient tous les tests unitaires pour la classe BTreeNode,
incluant les tests de fonctionnalité, de validation et de gestion d'erreurs.
"""

import pytest
from typing import List, Optional

from src.baobab_tree.nary.btree_node import BTreeNode
from src.baobab_tree.core.exceptions import (
    BTreeError,
    NodeFullError,
    NodeUnderflowError,
    SplitError,
    MergeError,
    RedistributionError,
)


class TestBTreeNode:
    """Tests pour la classe BTreeNode."""

    def test_init_basic(self):
        """Test de l'initialisation basique d'un nœud B-tree."""
        node = BTreeNode(order=3, is_leaf=True)
        assert node.order == 3
        assert node.is_leaf is True
        assert node.keys == []
        assert node.children == []
        assert node.parent is None

    def test_init_with_parameters(self):
        """Test de l'initialisation avec paramètres."""
        keys = [10, 20, 30]
        children = [None, None, None, None]
        parent = BTreeNode(order=3, is_leaf=False)
        
        node = BTreeNode(
            order=3,
            is_leaf=False,
            keys=keys,
            children=children,
            parent=parent
        )
        
        assert node.order == 3
        assert node.is_leaf is False
        assert node.keys == keys
        assert node.children == children
        assert node.parent == parent

    def test_init_invalid_order(self):
        """Test de l'initialisation avec un ordre invalide."""
        with pytest.raises(BTreeError) as exc_info:
            BTreeNode(order=1)
        assert "Ordre invalide" in str(exc_info.value)

    def test_get_key_count(self):
        """Test du comptage des clés."""
        node = BTreeNode(order=3, is_leaf=True)
        assert node.get_key_count() == 0
        
        node.keys = [10, 20, 30]
        assert node.get_key_count() == 3

    def test_get_child_count(self):
        """Test du comptage des enfants."""
        node = BTreeNode(order=3, is_leaf=True)
        assert node.get_child_count() == 0
        
        node.children = [None, None, None, None]
        assert node.get_child_count() == 4

    def test_is_full(self):
        """Test de la vérification si le nœud est plein."""
        node = BTreeNode(order=3, is_leaf=True)
        
        # Ordre 3 -> maximum 5 clés
        assert node.is_full() is False
        
        node.keys = [10, 20, 30, 40, 50]
        assert node.is_full() is True

    def test_is_minimum(self):
        """Test de la vérification si le nœud contient le minimum de clés."""
        node = BTreeNode(order=3, is_leaf=True)
        
        # Ordre 3 -> minimum 2 clés
        assert node.is_minimum() is True
        
        node.keys = [10, 20]
        assert node.is_minimum() is True
        
        node.keys = [10, 20, 30]
        assert node.is_minimum() is False

    def test_search_key(self):
        """Test de la recherche de clé."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30, 40, 50]
        
        # Clé existante
        assert node.search_key(20) == 1
        assert node.search_key(40) == 3
        
        # Clé non existante
        assert node.search_key(15) == 1  # Position d'insertion
        assert node.search_key(5) == 0   # Position d'insertion
        assert node.search_key(60) == 5  # Position d'insertion

    def test_insert_key_success(self):
        """Test de l'insertion de clé réussie."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 30, 40, 50]
        
        index = node.insert_key(20)
        assert index == 1
        assert node.keys == [10, 20, 30, 40, 50]

    def test_insert_key_full_node(self):
        """Test de l'insertion dans un nœud plein."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30, 40, 50]  # Nœud plein
        
        with pytest.raises(NodeFullError) as exc_info:
            node.insert_key(60)
        assert "Nœud plein" in str(exc_info.value)

    def test_delete_key_success(self):
        """Test de la suppression de clé réussie."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30, 40, 50]
        
        result = node.delete_key(30)
        assert result is True
        assert node.keys == [10, 20, 40, 50]

    def test_delete_key_not_found(self):
        """Test de la suppression d'une clé non trouvée."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30, 40, 50]
        
        result = node.delete_key(25)
        assert result is False
        assert node.keys == [10, 20, 30, 40, 50]

    def test_get_child_index_leaf(self):
        """Test de la récupération de l'index enfant pour une feuille."""
        node = BTreeNode(order=3, is_leaf=True)
        
        with pytest.raises(BTreeError) as exc_info:
            node.get_child_index(20)
        assert "Impossible de récupérer l'enfant d'une feuille" in str(exc_info.value)

    def test_get_child_index_internal(self):
        """Test de la récupération de l'index enfant pour un nœud interne."""
        node = BTreeNode(order=3, is_leaf=False)
        node.keys = [20, 40, 60]
        
        assert node.get_child_index(10) == 0
        assert node.get_child_index(30) == 1
        assert node.get_child_index(50) == 2
        assert node.get_child_index(70) == 3

    def test_split_success(self):
        """Test de la division réussie d'un nœud."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30, 40, 50]  # Nœud plein
        
        left_node, median_key, right_node = node.split()
        
        assert median_key == 30
        assert left_node.keys == [10, 20]
        assert right_node.keys == [40, 50]
        assert left_node.parent == node.parent
        assert right_node.parent == node.parent

    def test_split_not_full(self):
        """Test de la division d'un nœud non plein."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30]  # Nœud non plein
        
        with pytest.raises(SplitError) as exc_info:
            node.split()
        assert "Impossible de diviser un nœud qui n'est pas plein" in str(exc_info.value)

    def test_split_internal_node(self):
        """Test de la division d'un nœud interne."""
        parent = BTreeNode(order=3, is_leaf=False)
        child1 = BTreeNode(order=3, is_leaf=True, keys=[10, 20])
        child2 = BTreeNode(order=3, is_leaf=True, keys=[40, 50])
        child3 = BTreeNode(order=3, is_leaf=True, keys=[70, 80])
        
        node = BTreeNode(order=3, is_leaf=False)
        node.keys = [30, 60, 90, 100, 110]  # Nœud plein
        node.children = [child1, child2, child3, None, None, None]
        node.parent = parent
        
        left_node, median_key, right_node = node.split()
        
        assert median_key == 60
        assert left_node.keys == [30, 90]
        assert right_node.keys == [100, 110]
        assert len(left_node.children) == 3
        assert len(right_node.children) == 3

    def test_merge_with_success(self):
        """Test de la fusion réussie de nœuds."""
        parent = BTreeNode(order=3, is_leaf=False)
        
        node1 = BTreeNode(order=3, is_leaf=True, keys=[10, 20], parent=parent)
        node2 = BTreeNode(order=3, is_leaf=True, keys=[40, 50], parent=parent)
        
        node1.merge_with(node2, 30)
        
        assert node1.keys == [10, 20, 30, 40, 50]
        assert node1.parent == parent

    def test_merge_with_different_parents(self):
        """Test de la fusion avec des parents différents."""
        parent1 = BTreeNode(order=3, is_leaf=False)
        parent2 = BTreeNode(order=3, is_leaf=False)
        
        node1 = BTreeNode(order=3, is_leaf=True, keys=[10, 20], parent=parent1)
        node2 = BTreeNode(order=3, is_leaf=True, keys=[40, 50], parent=parent2)
        
        with pytest.raises(MergeError) as exc_info:
            node1.merge_with(node2, 30)
        assert "Impossible de fusionner des nœuds avec des parents différents" in str(exc_info.value)

    def test_merge_with_capacity_exceeded(self):
        """Test de la fusion qui dépasse la capacité."""
        parent = BTreeNode(order=3, is_leaf=False)
        
        # Créer des nœuds qui, une fois fusionnés, dépasseraient la capacité
        node1 = BTreeNode(order=3, is_leaf=True, keys=[10, 20, 30, 40], parent=parent)
        node2 = BTreeNode(order=3, is_leaf=True, keys=[60, 70, 80, 90], parent=parent)
        
        with pytest.raises(MergeError) as exc_info:
            node1.merge_with(node2, 50)
        assert "Impossible de fusionner: résultat dépasserait la capacité maximale" in str(exc_info.value)

    def test_borrow_from_left_success(self):
        """Test de l'emprunt réussi au frère gauche."""
        parent = BTreeNode(order=3, is_leaf=False)
        parent.keys = [30, 60]
        
        left_sibling = BTreeNode(order=3, is_leaf=True, keys=[10, 20, 25], parent=parent)
        right_node = BTreeNode(order=3, is_leaf=True, keys=[40], parent=parent)
        
        parent.children = [left_sibling, right_node]
        
        result = right_node.borrow_from_left()
        
        assert result is True
        assert right_node.keys == [30, 40]
        assert left_sibling.keys == [10, 20]
        assert parent.keys == [25, 60]

    def test_borrow_from_left_no_sibling(self):
        """Test de l'emprunt quand il n'y a pas de frère gauche."""
        parent = BTreeNode(order=3, is_leaf=False)
        parent.keys = [30]
        
        node = BTreeNode(order=3, is_leaf=True, keys=[40], parent=parent)
        parent.children = [node]
        
        result = node.borrow_from_left()
        assert result is False

    def test_borrow_from_right_success(self):
        """Test de l'emprunt réussi au frère droit."""
        parent = BTreeNode(order=3, is_leaf=False)
        parent.keys = [30, 60]
        
        left_node = BTreeNode(order=3, is_leaf=True, keys=[10], parent=parent)
        right_sibling = BTreeNode(order=3, is_leaf=True, keys=[40, 50, 55], parent=parent)
        
        parent.children = [left_node, right_sibling]
        
        result = left_node.borrow_from_right()
        
        assert result is True
        assert left_node.keys == [10, 30]
        assert right_sibling.keys == [50, 55]
        assert parent.keys == [40, 60]

    def test_borrow_from_right_no_sibling(self):
        """Test de l'emprunt quand il n'y a pas de frère droit."""
        parent = BTreeNode(order=3, is_leaf=False)
        parent.keys = [30]
        
        node = BTreeNode(order=3, is_leaf=True, keys=[10], parent=parent)
        parent.children = [node]
        
        result = node.borrow_from_right()
        assert result is False

    def test_redistribute_keys_success(self):
        """Test de la redistribution réussie des clés."""
        parent = BTreeNode(order=3, is_leaf=False)
        parent.keys = [30, 60]
        
        left_sibling = BTreeNode(order=3, is_leaf=True, keys=[10, 20, 25], parent=parent)
        right_node = BTreeNode(order=3, is_leaf=True, keys=[40], parent=parent)
        
        parent.children = [left_sibling, right_node]
        
        right_node.redistribute_keys()
        
        assert right_node.keys == [30, 40]
        assert left_sibling.keys == [10, 20]
        assert parent.keys == [25, 60]

    def test_redistribute_keys_no_parent(self):
        """Test de la redistribution sans parent."""
        node = BTreeNode(order=3, is_leaf=True, keys=[10])
        
        with pytest.raises(RedistributionError) as exc_info:
            node.redistribute_keys()
        assert "Impossible de redistribuer: pas de parent" in str(exc_info.value)

    def test_get_predecessor(self):
        """Test de la récupération du prédécesseur."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30, 40, 50]
        
        assert node.get_predecessor(20) == 10
        assert node.get_predecessor(30) == 20
        assert node.get_predecessor(10) is None

    def test_get_successor(self):
        """Test de la récupération du successeur."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30, 40, 50]
        
        assert node.get_successor(20) == 30
        assert node.get_successor(30) == 40
        assert node.get_successor(50) is None

    def test_validate_node_success(self):
        """Test de la validation réussie d'un nœud."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30]
        
        assert node.validate_node() is True

    def test_validate_node_invalid(self):
        """Test de la validation d'un nœud invalide."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [30, 20, 10]  # Clés non triées
        
        assert node.validate_node() is False

    def test_to_string(self):
        """Test de la représentation textuelle."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30]
        
        result = node.to_string()
        assert "BTreeNode(order=3, is_leaf=True)" in result
        assert "Keys: [10, 20, 30]" in result

    def test_get_node_info(self):
        """Test de la récupération des informations du nœud."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30]
        
        info = node.get_node_info()
        
        assert info["order"] == 3
        assert info["is_leaf"] is True
        assert info["key_count"] == 3
        assert info["child_count"] == 0
        assert info["is_full"] is False
        assert info["is_minimum"] is False
        assert info["keys"] == [10, 20, 30]
        assert info["parent"] is False

    def test_str_representation(self):
        """Test de la représentation string."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30]
        
        str_repr = str(node)
        assert "BTreeNode(keys=[10, 20, 30], is_leaf=True)" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        node = BTreeNode(order=3, is_leaf=True)
        node.keys = [10, 20, 30]
        
        repr_str = repr(node)
        assert "BTreeNode(order=3" in repr_str
        assert "keys=[10, 20, 30]" in repr_str
        assert "is_leaf=True" in repr_str

    def test_validation_with_children(self):
        """Test de la validation avec des enfants."""
        parent = BTreeNode(order=3, is_leaf=False)
        child1 = BTreeNode(order=3, is_leaf=True, keys=[10, 20], parent=parent)
        child2 = BTreeNode(order=3, is_leaf=True, keys=[40, 50], parent=parent)
        
        parent.keys = [30]
        parent.children = [child1, child2]
        
        assert parent.validate_node() is True

    def test_validation_invalid_children_count(self):
        """Test de la validation avec un nombre invalide d'enfants."""
        parent = BTreeNode(order=3, is_leaf=False)
        parent.keys = [30]
        parent.children = [None]  # Pas assez d'enfants
        
        assert parent.validate_node() is False

    def test_validation_exceeds_max_keys(self):
        """Test de la validation avec trop de clés."""
        node = BTreeNode(order=3, is_leaf=True)
        # Ordre 3 -> maximum 5 clés
        node.keys = [10, 20, 30, 40, 50, 60]  # Trop de clés
        
        assert node.validate_node() is False

    def test_validation_exceeds_max_children(self):
        """Test de la validation avec trop d'enfants."""
        node = BTreeNode(order=3, is_leaf=False)
        # Ordre 3 -> maximum 6 enfants
        node.children = [None] * 7  # Trop d'enfants
        
        assert node.validate_node() is False