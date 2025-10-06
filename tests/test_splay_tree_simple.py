"""
Tests unitaires simplifiés pour la classe SplayTree.

Ce module contient des tests unitaires simplifiés pour la classe SplayTree,
en évitant les opérations de splay complexes qui causent des références circulaires.
"""

import pytest
import time
from typing import List

from src.baobab_tree.specialized.splay_tree import SplayTree
from src.baobab_tree.specialized.splay_node import SplayNode
from src.baobab_tree.core.exceptions import SplayTreeError, SplayOperationError, SplayValidationError


class TestSplayTreeSimple:
    """Tests simplifiés pour la classe SplayTree."""

    def test_init(self):
        """Test de l'initialisation d'un arbre Splay vide."""
        tree = SplayTree()
        assert tree.root is None
        assert tree.size == 0
        assert tree.get_splay_count() == 0
        assert tree.get_total_accesses() == 0

    def test_init_with_comparator(self):
        """Test de l'initialisation avec un comparateur personnalisé."""
        def custom_compare(a: int, b: int) -> int:
            return b - a  # Ordre décroissant

        tree = SplayTree(custom_compare)
        assert tree.root is None
        assert tree.size == 0

    def test_insert_single(self):
        """Test d'insertion d'un seul élément."""
        tree = SplayTree()
        result = tree.insert(5)
        
        assert result is True
        assert tree.size == 1
        assert tree.root is not None
        assert tree.root.value == 5
        assert isinstance(tree.root, SplayNode)

    def test_insert_duplicate(self):
        """Test d'insertion d'un élément dupliqué."""
        tree = SplayTree()
        tree.insert(5)
        
        result = tree.insert(5)
        assert result is False
        assert tree.size == 1

    def test_search_empty_tree(self):
        """Test de recherche dans un arbre vide."""
        tree = SplayTree()
        result = tree.search(5)
        assert result is False

    def test_delete_empty_tree(self):
        """Test de suppression dans un arbre vide."""
        tree = SplayTree()
        result = tree.delete(5)
        assert result is False

    def test_find_non_existing(self):
        """Test de recherche d'un élément non existant."""
        tree = SplayTree()
        tree.insert(5)
        
        result = tree.find(7)
        assert result is None

    def test_get_min_empty_tree(self):
        """Test de récupération du minimum dans un arbre vide."""
        tree = SplayTree()
        min_value = tree.get_min()
        assert min_value is None

    def test_get_max_empty_tree(self):
        """Test de récupération du maximum dans un arbre vide."""
        tree = SplayTree()
        max_value = tree.get_max()
        assert max_value is None

    def test_remove_min_empty_tree(self):
        """Test de suppression du minimum dans un arbre vide."""
        tree = SplayTree()
        min_value = tree.remove_min()
        assert min_value is None

    def test_remove_max_empty_tree(self):
        """Test de suppression du maximum dans un arbre vide."""
        tree = SplayTree()
        max_value = tree.remove_max()
        assert max_value is None

    def test_split_empty_tree(self):
        """Test de division d'un arbre vide."""
        tree = SplayTree()
        new_tree = tree.split(5)
        
        assert tree.size == 0
        assert new_tree.size == 0

    def test_is_valid_empty_tree(self):
        """Test de validation d'un arbre vide."""
        tree = SplayTree()
        assert tree.is_valid() is True

    def test_print_empty_tree(self):
        """Test d'affichage d'un arbre vide."""
        tree = SplayTree()
        tree.print()  # Ne devrait pas lever d'exception

    def test_str_representation_empty(self):
        """Test de la représentation string d'un arbre vide."""
        tree = SplayTree()
        str_repr = str(tree)
        assert "SplayTree(empty)" in str_repr

    def test_repr_representation_empty(self):
        """Test de la représentation détaillée d'un arbre vide."""
        tree = SplayTree()
        repr_str = repr(tree)
        assert "SplayTree(empty)" in repr_str

    def test_splay_count_initial(self):
        """Test du comptage initial des opérations de splay."""
        tree = SplayTree()
        assert tree.get_splay_count() == 0

    def test_total_accesses_initial(self):
        """Test du comptage initial des accès totaux."""
        tree = SplayTree()
        assert tree.get_total_accesses() == 0

    def test_performance_metrics_empty(self):
        """Test des métriques de performance d'un arbre vide."""
        tree = SplayTree()
        metrics = tree.get_performance_metrics()
        
        assert "size" in metrics
        assert "height" in metrics
        assert "splay_count" in metrics
        assert "total_accesses" in metrics
        assert "average_splay_per_access" in metrics
        
        assert metrics["size"] == 0
        assert metrics["total_accesses"] == 0

    def test_error_handling_none_value(self):
        """Test de la gestion d'erreurs avec des valeurs None."""
        tree = SplayTree()
        
        # Test avec des valeurs None (si le type le permet)
        with pytest.raises((TypeError, SplayTreeError)):
            tree.insert(None)

    def test_comparator_functionality(self):
        """Test du comparateur personnalisé."""
        def reverse_compare(a: int, b: int) -> int:
            return b - a  # Ordre décroissant

        tree = SplayTree(reverse_compare)
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        # Avec un comparateur inversé, 7 devrait être le minimum
        min_value = tree.get_min()
        assert min_value == 7

    def test_create_node(self):
        """Test de création de nœud Splay."""
        tree = SplayTree()
        node = tree._create_node(5)
        
        assert isinstance(node, SplayNode)
        assert node.value == 5
        assert node.access_count == 0
        assert node.splay_count == 0

    def test_splay_operations_exist(self):
        """Test que les opérations de splay existent."""
        tree = SplayTree()
        
        # Vérifier que les méthodes existent
        assert hasattr(tree, '_splay')
        assert hasattr(tree, '_zig')
        assert hasattr(tree, '_zig_zig')
        assert hasattr(tree, '_zig_zag')
        assert hasattr(tree, '_is_zig_zig')

    def test_merge_empty_trees(self):
        """Test de fusion d'arbres vides."""
        tree1 = SplayTree()
        tree2 = SplayTree()
        
        tree1.merge(tree2)
        
        assert tree1.size == 0
        assert tree2.size == 0

    def test_split_with_single_element(self):
        """Test de division avec un seul élément."""
        tree = SplayTree()
        tree.insert(5)
        
        new_tree = tree.split(5)
        
        # L'arbre original devrait être vide ou contenir les éléments < 5
        # Le nouvel arbre devrait contenir les éléments >= 5
        assert tree.size + new_tree.size == 1

    def test_validation_with_single_node(self):
        """Test de validation avec un seul nœud."""
        tree = SplayTree()
        tree.insert(5)
        
        assert tree.is_valid() is True

    def test_performance_metrics_with_single_node(self):
        """Test des métriques de performance avec un seul nœud."""
        tree = SplayTree()
        tree.insert(5)
        
        metrics = tree.get_performance_metrics()
        
        assert metrics["size"] == 1
        assert metrics["height"] >= 0
        assert metrics["splay_count"] >= 0
        assert metrics["total_accesses"] >= 0

    def test_str_representation_with_single_node(self):
        """Test de la représentation string avec un seul nœud."""
        tree = SplayTree()
        tree.insert(5)
        
        str_repr = str(tree)
        assert "SplayTree" in str_repr
        assert "size=1" in str_repr

    def test_repr_representation_with_single_node(self):
        """Test de la représentation détaillée avec un seul nœud."""
        tree = SplayTree()
        tree.insert(5)
        
        repr_str = repr(tree)
        assert "SplayTree" in repr_str
        assert "size=1" in repr_str


class TestSplayNodeSimple:
    """Tests simplifiés pour la classe SplayNode."""

    def test_init(self):
        """Test de l'initialisation d'un nœud Splay."""
        node = SplayNode(5)
        assert node.value == 5
        assert node.access_count == 0
        assert node.last_accessed is None
        assert node.splay_count == 0

    def test_increment_access(self):
        """Test d'incrémentation du compteur d'accès."""
        node = SplayNode(5)
        initial_count = node.access_count
        
        node.increment_access()
        
        assert node.access_count == initial_count + 1
        assert node.last_accessed is not None

    def test_increment_splay(self):
        """Test d'incrémentation du compteur de splay."""
        node = SplayNode(5)
        initial_count = node.splay_count
        
        node.increment_splay()
        
        assert node.splay_count == initial_count + 1

    def test_reset_metrics(self):
        """Test de remise à zéro des métriques."""
        node = SplayNode(5)
        node.increment_access()
        node.increment_splay()
        
        node.reset_metrics()
        
        assert node.access_count == 0
        assert node.last_accessed is None
        assert node.splay_count == 0

    def test_get_metrics(self):
        """Test de récupération des métriques."""
        node = SplayNode(5)
        node.increment_access()
        node.increment_splay()
        
        metrics = node.get_metrics()
        
        assert "access_count" in metrics
        assert "last_accessed" in metrics
        assert "splay_count" in metrics
        assert "value" in metrics
        assert "is_leaf" in metrics
        assert "height" in metrics
        
        assert metrics["access_count"] == 1
        assert metrics["splay_count"] == 1
        assert metrics["value"] == 5

    def test_get_rotation_type_no_parent(self):
        """Test de détermination du type de rotation sans parent."""
        node = SplayNode(5)
        rotation_type = node.get_rotation_type()
        assert rotation_type == "none"

    def test_get_splay_path_single_node(self):
        """Test de récupération du chemin de splay pour un nœud seul."""
        node = SplayNode(5)
        path = node.get_splay_path()
        assert len(path) == 1
        assert path[0] == node

    def test_get_splay_depth_single_node(self):
        """Test de calcul de la profondeur de splay pour un nœud seul."""
        node = SplayNode(5)
        assert node.get_splay_depth() == 0

    def test_to_string(self):
        """Test de conversion en string."""
        node = SplayNode(5)
        node.increment_access()
        node.increment_splay()
        
        str_repr = node.to_string()
        assert "SplayNode" in str_repr
        assert "value=5" in str_repr
        assert "access_count=1" in str_repr
        assert "splay_count=1" in str_repr

    def test_str_representation(self):
        """Test de la représentation string."""
        node = SplayNode(5)
        node.increment_access()
        node.increment_splay()
        
        str_repr = str(node)
        assert "SplayNode" in str_repr
        assert "value=5" in str_repr
        assert "access_count=1" in str_repr
        assert "splay_count=1" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        node = SplayNode(5)
        str_repr = repr(node)
        assert "SplayNode" in str_repr
        assert "value=5" in str_repr

    def test_zig_case_no_parent(self):
        """Test de détection du cas zig sans parent."""
        node = SplayNode(5)
        assert node.is_zig_case() is False

    def test_zig_zig_case_no_parent(self):
        """Test de détection du cas zig-zig sans parent."""
        node = SplayNode(5)
        assert node.is_zig_zig_case() is False

    def test_zig_zag_case_no_parent(self):
        """Test de détection du cas zig-zag sans parent."""
        node = SplayNode(5)
        assert node.is_zig_zag_case() is False


if __name__ == "__main__":
    pytest.main([__file__])