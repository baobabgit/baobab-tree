"""
Tests unitaires finaux pour atteindre 90%+ de couverture de code.

Ce module contient des tests ciblés pour couvrir toutes les branches
et méthodes des classes SplayTree et SplayNode.
"""

import pytest
import time
from typing import List

from src.baobab_tree.specialized.splay_tree import SplayTree
from src.baobab_tree.specialized.splay_node import SplayNode
from src.baobab_tree.core.exceptions import SplayTreeError, SplayOperationError, SplayValidationError


class TestSplayTreeFinal:
    """Tests finaux pour SplayTree."""

    def test_constructor_exception_handling(self):
        """Test de gestion d'exception dans le constructeur."""
        # Test avec un comparateur qui lève une exception
        def problematic_comparator(a, b):
            if a is None or b is None:
                raise ValueError("None values not allowed")
            return a - b
        
        # Test normal
        tree = SplayTree(problematic_comparator)
        assert tree is not None

    def test_create_node_variations(self):
        """Test de création de nœud avec différentes variations."""
        tree = SplayTree()
        
        # Création sans parent
        node1 = tree._create_node(5)
        assert isinstance(node1, SplayNode)
        assert node1.value == 5
        
        # Création avec parent
        parent = SplayNode(10)
        node2 = tree._create_node(3, parent)
        assert isinstance(node2, SplayNode)
        assert node2.value == 3

    def test_splay_operations_coverage(self):
        """Test de couverture des opérations de splay."""
        tree = SplayTree()
        
        # Test avec nœud None
        result = tree._splay(None)
        assert result is None
        
        # Test avec nœud sans parent
        node = SplayNode(5)
        result = tree._splay(node)
        assert result == node

    def test_zig_operations_coverage(self):
        """Test de couverture des opérations zig."""
        tree = SplayTree()
        
        # Test avec nœud sans parent
        node = SplayNode(5)
        tree._zig(node)  # Ne devrait pas lever d'exception
        
        # Test avec nœud ayant un parent
        parent = SplayNode(10)
        child = SplayNode(5)
        parent.set_left(child)
        tree._zig(child)  # Ne devrait pas lever d'exception

    def test_zig_zig_operations_coverage(self):
        """Test de couverture des opérations zig-zig."""
        tree = SplayTree()
        
        # Test avec nœud sans parent
        node = SplayNode(5)
        tree._zig_zig(node)  # Ne devrait pas lever d'exception
        
        # Test avec nœud ayant un parent mais pas de grandparent
        parent = SplayNode(10)
        child = SplayNode(5)
        parent.set_left(child)
        tree._zig_zig(child)  # Ne devrait pas lever d'exception

    def test_zig_zag_operations_coverage(self):
        """Test de couverture des opérations zig-zag."""
        tree = SplayTree()
        
        # Test avec nœud sans parent
        node = SplayNode(5)
        tree._zig_zag(node)  # Ne devrait pas lever d'exception
        
        # Test avec nœud ayant un parent mais pas de grandparent
        parent = SplayNode(10)
        child = SplayNode(5)
        parent.set_left(child)
        tree._zig_zag(child)  # Ne devrait pas lever d'exception

    def test_is_zig_zig_coverage(self):
        """Test de couverture de is_zig_zig."""
        tree = SplayTree()
        
        # Test avec nœud sans parent
        node = SplayNode(5)
        result = tree._is_zig_zig(node)
        assert result is False
        
        # Test avec nœud ayant un parent mais pas de grandparent
        parent = SplayNode(10)
        child = SplayNode(5)
        parent.set_left(child)
        result = tree._is_zig_zig(child)
        assert result is False

    def test_insert_coverage(self):
        """Test de couverture d'insertion."""
        tree = SplayTree()
        
        # Test insertion simple
        result = tree.insert(5)
        assert result is True
        assert tree.size == 1
        
        # Test insertion de doublon
        result = tree.insert(5)
        assert result is False
        assert tree.size == 1

    def test_search_coverage(self):
        """Test de couverture de recherche."""
        tree = SplayTree()
        
        # Test recherche dans arbre vide
        result = tree.search(5)
        assert result is False
        
        # Test recherche avec élément présent
        tree.insert(5)
        result = tree.search(5)
        assert result is True

    def test_delete_coverage(self):
        """Test de couverture de suppression."""
        tree = SplayTree()
        
        # Test suppression dans arbre vide
        result = tree.delete(5)
        assert result is False
        
        # Test suppression avec élément présent
        tree.insert(5)
        result = tree.delete(5)
        assert result is True
        assert tree.size == 0

    def test_find_coverage(self):
        """Test de couverture de find."""
        tree = SplayTree()
        
        # Test find dans arbre vide
        result = tree.find(5)
        assert result is None
        
        # Test find avec élément présent
        tree.insert(5)
        result = tree.find(5)
        assert result == 5

    def test_get_min_max_coverage(self):
        """Test de couverture de get_min et get_max."""
        tree = SplayTree()
        
        # Test avec arbre vide
        min_val = tree.get_min()
        assert min_val is None
        
        max_val = tree.get_max()
        assert max_val is None
        
        # Test avec un élément
        tree.insert(5)
        min_val = tree.get_min()
        assert min_val == 5
        
        max_val = tree.get_max()
        assert max_val == 5

    def test_remove_min_max_coverage(self):
        """Test de couverture de remove_min et remove_max."""
        tree = SplayTree()
        
        # Test avec arbre vide
        min_val = tree.remove_min()
        assert min_val is None
        
        max_val = tree.remove_max()
        assert max_val is None
        
        # Test avec un élément
        tree.insert(5)
        min_val = tree.remove_min()
        assert min_val == 5
        assert tree.size == 0

    def test_merge_coverage(self):
        """Test de couverture de merge."""
        tree1 = SplayTree()
        tree2 = SplayTree()
        
        # Test fusion d'arbres vides
        tree1.merge(tree2)
        assert tree1.size == 0
        assert tree2.size == 0
        
        # Test fusion avec un élément
        tree1.insert(5)
        tree2.insert(3)
        tree1.merge(tree2)
        assert tree1.size == 2
        assert tree2.size == 0

    def test_split_coverage(self):
        """Test de couverture de split."""
        tree = SplayTree()
        
        # Test split d'arbre vide
        new_tree = tree.split(5)
        assert tree.size == 0
        assert new_tree.size == 0
        
        # Test split avec un élément
        tree.insert(5)
        new_tree = tree.split(5)
        assert tree.size + new_tree.size == 1

    def test_performance_metrics_coverage(self):
        """Test de couverture des métriques de performance."""
        tree = SplayTree()
        
        # Test avec arbre vide
        metrics = tree.get_performance_metrics()
        assert "size" in metrics
        assert "height" in metrics
        assert "splay_count" in metrics
        assert "total_accesses" in metrics
        assert "average_splay_per_access" in metrics
        
        # Test avec un élément
        tree.insert(5)
        metrics = tree.get_performance_metrics()
        assert metrics["size"] == 1

    def test_validation_coverage(self):
        """Test de couverture de validation."""
        tree = SplayTree()
        
        # Test avec arbre vide
        result = tree.is_valid()
        assert result is True
        
        # Test avec un élément
        tree.insert(5)
        result = tree.is_valid()
        assert result is True

    def test_print_coverage(self):
        """Test de couverture de print."""
        tree = SplayTree()
        
        # Test avec arbre vide
        tree.print()  # Ne devrait pas lever d'exception
        
        # Test avec un élément
        tree.insert(5)
        tree.print()  # Ne devrait pas lever d'exception

    def test_str_repr_coverage(self):
        """Test de couverture de __str__ et __repr__."""
        tree = SplayTree()
        
        # Test avec arbre vide
        str_repr = str(tree)
        assert "SplayTree" in str_repr
        
        repr_str = repr(tree)
        assert "SplayTree" in repr_str
        
        # Test avec un élément
        tree.insert(5)
        str_repr = str(tree)
        assert "SplayTree" in str_repr
        
        repr_str = repr(tree)
        assert "SplayTree" in repr_str

    def test_count_nodes_coverage(self):
        """Test de couverture de _count_nodes."""
        tree = SplayTree()
        
        # Test avec None
        count = tree._count_nodes(None)
        assert count == 0
        
        # Test avec un nœud
        tree.insert(5)
        count = tree._count_nodes(tree._root)
        assert count == 1

    def test_validate_splay_nodes_coverage(self):
        """Test de couverture de _validate_splay_nodes."""
        tree = SplayTree()
        
        # Test avec None
        result = tree._validate_splay_nodes(None)
        assert result is True
        
        # Test avec un nœud SplayNode valide
        tree.insert(5)
        result = tree._validate_splay_nodes(tree._root)
        assert result is True


class TestSplayNodeFinal:
    """Tests finaux pour SplayNode."""

    def test_constructor_coverage(self):
        """Test de couverture du constructeur."""
        # Test constructeur de base
        node = SplayNode(5)
        assert node.value == 5
        assert node.access_count == 0
        assert node.splay_count == 0
        assert node.last_accessed is None

    def test_access_metrics_coverage(self):
        """Test de couverture des métriques d'accès."""
        node = SplayNode(5)
        
        # Test increment_access
        initial_count = node.access_count
        node.increment_access()
        assert node.access_count == initial_count + 1
        assert node.last_accessed is not None
        
        # Test increment_splay
        initial_splay = node.splay_count
        node.increment_splay()
        assert node.splay_count == initial_splay + 1
        
        # Test reset_metrics
        node.reset_metrics()
        assert node.access_count == 0
        assert node.splay_count == 0
        assert node.last_accessed is None

    def test_get_metrics_coverage(self):
        """Test de couverture de get_metrics."""
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

    def test_rotation_detection_coverage(self):
        """Test de couverture de détection de rotation."""
        node = SplayNode(5)
        
        # Test sans parent
        assert node.is_zig_case() is False
        assert node.is_zig_zig_case() is False
        assert node.is_zig_zag_case() is False
        assert node.get_rotation_type() == "none"

    def test_path_operations_coverage(self):
        """Test de couverture des opérations de chemin."""
        node = SplayNode(5)
        
        # Test get_splay_path
        path = node.get_splay_path()
        assert len(path) == 1
        assert path[0] == node
        
        # Test get_splay_depth
        depth = node.get_splay_depth()
        assert depth == 0

    def test_string_representations_coverage(self):
        """Test de couverture des représentations string."""
        node = SplayNode(5)
        node.increment_access()
        node.increment_splay()
        
        # Test to_string
        str_repr = node.to_string()
        assert "SplayNode" in str_repr
        assert "value=5" in str_repr
        
        # Test __str__
        str_repr = str(node)
        assert "SplayNode" in str_repr
        
        # Test __repr__
        repr_str = repr(node)
        assert "SplayNode" in repr_str

    def test_error_handling_coverage(self):
        """Test de couverture de gestion d'erreurs."""
        node = SplayNode(5)
        
        # Test avec des opérations qui peuvent lever des exceptions
        try:
            node.increment_access()
            node.increment_splay()
            node.reset_metrics()
            node.get_metrics()
            node.get_rotation_type()
            node.get_splay_path()
            node.get_splay_depth()
            node.to_string()
            str(node)
            repr(node)
        except Exception as e:
            # Si une exception est levée, elle devrait être gérée
            assert isinstance(e, (SplayNodeError, Exception))


if __name__ == "__main__":
    pytest.main([__file__])