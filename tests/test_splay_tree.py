"""
Tests unitaires pour la classe SplayTree.

Ce module contient tous les tests unitaires pour la classe SplayTree,
incluant les tests de fonctionnalité de base, les tests d'opérations
de splay, et les tests de performance.
"""

import pytest
import time
from typing import List

from src.baobab_tree.specialized.splay_tree import SplayTree
from src.baobab_tree.specialized.splay_node import SplayNode
from src.baobab_tree.core.exceptions import SplayTreeError, SplayOperationError, SplayValidationError


class TestSplayTree:
    """Tests pour la classe SplayTree."""

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

    def test_insert_multiple(self):
        """Test d'insertion de plusieurs éléments."""
        tree = SplayTree()
        values = [5, 3, 7, 1, 9]
        
        for value in values:
            result = tree.insert(value)
            assert result is True
        
        assert tree.size == len(values)
        assert tree.root is not None

    def test_insert_duplicate(self):
        """Test d'insertion d'un élément dupliqué."""
        tree = SplayTree()
        tree.insert(5)
        
        result = tree.insert(5)
        assert result is False
        assert tree.size == 1

    def test_search_existing(self):
        """Test de recherche d'un élément existant."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        result = tree.search(3)
        assert result is True
        assert tree.root.value == 3  # L'élément recherché devient la racine

    def test_search_non_existing(self):
        """Test de recherche d'un élément non existant."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        
        result = tree.search(7)
        assert result is False

    def test_search_empty_tree(self):
        """Test de recherche dans un arbre vide."""
        tree = SplayTree()
        result = tree.search(5)
        assert result is False

    def test_delete_existing(self):
        """Test de suppression d'un élément existant."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        result = tree.delete(3)
        assert result is True
        assert tree.size == 2

    def test_delete_non_existing(self):
        """Test de suppression d'un élément non existant."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        
        result = tree.delete(7)
        assert result is False
        assert tree.size == 2

    def test_delete_empty_tree(self):
        """Test de suppression dans un arbre vide."""
        tree = SplayTree()
        result = tree.delete(5)
        assert result is False

    def test_find_existing(self):
        """Test de recherche et retour d'un élément existant."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        result = tree.find(3)
        assert result == 3
        assert tree.root.value == 3

    def test_find_non_existing(self):
        """Test de recherche d'un élément non existant."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        
        result = tree.find(7)
        assert result is None

    def test_get_min(self):
        """Test de récupération de l'élément minimum."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(9)
        
        min_value = tree.get_min()
        assert min_value == 1
        assert tree.root.value == 1  # Le minimum devient la racine

    def test_get_min_empty_tree(self):
        """Test de récupération du minimum dans un arbre vide."""
        tree = SplayTree()
        min_value = tree.get_min()
        assert min_value is None

    def test_get_max(self):
        """Test de récupération de l'élément maximum."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(9)
        
        max_value = tree.get_max()
        assert max_value == 9
        assert tree.root.value == 9  # Le maximum devient la racine

    def test_get_max_empty_tree(self):
        """Test de récupération du maximum dans un arbre vide."""
        tree = SplayTree()
        max_value = tree.get_max()
        assert max_value is None

    def test_remove_min(self):
        """Test de suppression et retour de l'élément minimum."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(9)
        
        min_value = tree.remove_min()
        assert min_value == 1
        assert tree.size == 4

    def test_remove_min_empty_tree(self):
        """Test de suppression du minimum dans un arbre vide."""
        tree = SplayTree()
        min_value = tree.remove_min()
        assert min_value is None

    def test_remove_max(self):
        """Test de suppression et retour de l'élément maximum."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(9)
        
        max_value = tree.remove_max()
        assert max_value == 9
        assert tree.size == 4

    def test_remove_max_empty_tree(self):
        """Test de suppression du maximum dans un arbre vide."""
        tree = SplayTree()
        max_value = tree.remove_max()
        assert max_value is None

    def test_merge(self):
        """Test de fusion de deux arbres Splay."""
        tree1 = SplayTree()
        tree1.insert(5)
        tree1.insert(3)
        tree1.insert(7)
        
        tree2 = SplayTree()
        tree2.insert(2)
        tree2.insert(8)
        tree2.insert(6)
        
        tree1.merge(tree2)
        
        assert tree1.size == 6
        assert tree2.size == 0
        assert tree2.root is None

    def test_merge_empty_tree(self):
        """Test de fusion avec un arbre vide."""
        tree1 = SplayTree()
        tree1.insert(5)
        tree1.insert(3)
        
        tree2 = SplayTree()
        
        tree1.merge(tree2)
        
        assert tree1.size == 2
        assert tree2.size == 0

    def test_merge_into_empty_tree(self):
        """Test de fusion d'un arbre dans un arbre vide."""
        tree1 = SplayTree()
        
        tree2 = SplayTree()
        tree2.insert(5)
        tree2.insert(3)
        
        tree1.merge(tree2)
        
        assert tree1.size == 2
        assert tree2.size == 0

    def test_split(self):
        """Test de division d'un arbre Splay."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(9)
        
        new_tree = tree.split(5)
        
        assert tree.size <= 3  # Arbre original contient les valeurs < 5
        assert new_tree.size >= 2  # Nouvel arbre contient les valeurs >= 5

    def test_split_empty_tree(self):
        """Test de division d'un arbre vide."""
        tree = SplayTree()
        new_tree = tree.split(5)
        
        assert tree.size == 0
        assert new_tree.size == 0

    def test_splay_count(self):
        """Test du comptage des opérations de splay."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        initial_count = tree.get_splay_count()
        
        tree.search(3)  # Devrait déclencher un splay
        tree.search(7)  # Devrait déclencher un splay
        
        assert tree.get_splay_count() > initial_count

    def test_total_accesses(self):
        """Test du comptage des accès totaux."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        initial_accesses = tree.get_total_accesses()
        
        tree.search(3)
        tree.search(7)
        tree.search(5)
        
        assert tree.get_total_accesses() == initial_accesses + 3

    def test_performance_metrics(self):
        """Test des métriques de performance."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.search(3)
        tree.search(7)
        
        metrics = tree.get_performance_metrics()
        
        assert "size" in metrics
        assert "height" in metrics
        assert "splay_count" in metrics
        assert "total_accesses" in metrics
        assert "average_splay_per_access" in metrics
        
        assert metrics["size"] == 3
        assert metrics["total_accesses"] == 2

    def test_is_valid(self):
        """Test de validation d'un arbre Splay valide."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        assert tree.is_valid() is True

    def test_is_valid_empty_tree(self):
        """Test de validation d'un arbre vide."""
        tree = SplayTree()
        assert tree.is_valid() is True

    def test_print(self):
        """Test d'affichage de l'arbre."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        # Ne devrait pas lever d'exception
        tree.print()

    def test_print_empty_tree(self):
        """Test d'affichage d'un arbre vide."""
        tree = SplayTree()
        tree.print()  # Ne devrait pas lever d'exception

    def test_str_representation(self):
        """Test de la représentation string."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        
        str_repr = str(tree)
        assert "SplayTree" in str_repr
        assert "size=2" in str_repr

    def test_str_representation_empty(self):
        """Test de la représentation string d'un arbre vide."""
        tree = SplayTree()
        str_repr = str(tree)
        assert "SplayTree(empty)" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        tree = SplayTree()
        tree.insert(5)
        tree.insert(3)
        
        repr_str = repr(tree)
        assert "SplayTree" in repr_str
        assert "size=2" in repr_str

    def test_repr_representation_empty(self):
        """Test de la représentation détaillée d'un arbre vide."""
        tree = SplayTree()
        repr_str = repr(tree)
        assert "SplayTree(empty)" in repr_str

    def test_complex_operations(self):
        """Test d'opérations complexes."""
        tree = SplayTree()
        
        # Insertion de plusieurs éléments
        values = [10, 5, 15, 3, 7, 12, 18, 1, 9, 14, 20]
        for value in values:
            tree.insert(value)
        
        assert tree.size == len(values)
        
        # Recherche de plusieurs éléments
        for value in [5, 15, 1, 20]:
            assert tree.search(value) is True
        
        # Suppression de plusieurs éléments
        for value in [3, 7, 12, 18]:
            assert tree.delete(value) is True
        
        assert tree.size == len(values) - 4

    def test_splay_behavior(self):
        """Test du comportement de splay."""
        tree = SplayTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)
        
        # Rechercher un élément profond
        tree.search(3)
        assert tree.root.value == 3  # L'élément recherché devient la racine
        
        # Rechercher un autre élément
        tree.search(7)
        assert tree.root.value == 7  # Le nouvel élément devient la racine

    def test_error_handling(self):
        """Test de la gestion d'erreurs."""
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

    def test_large_dataset(self):
        """Test avec un grand ensemble de données."""
        tree = SplayTree()
        
        # Insérer 100 éléments
        for i in range(100):
            tree.insert(i)
        
        assert tree.size == 100
        
        # Rechercher des éléments aléatoires
        for i in [0, 25, 50, 75, 99]:
            assert tree.search(i) is True
            assert tree.root.value == i  # L'élément recherché devient la racine

    def test_sequential_access_pattern(self):
        """Test d'un pattern d'accès séquentiel."""
        tree = SplayTree()
        
        # Insérer des éléments
        for i in range(10):
            tree.insert(i)
        
        # Accès séquentiel
        for i in range(10):
            tree.search(i)
            assert tree.root.value == i

    def test_repeated_access_pattern(self):
        """Test d'un pattern d'accès répété."""
        tree = SplayTree()
        
        # Insérer des éléments
        for i in range(10):
            tree.insert(i)
        
        # Accès répété aux mêmes éléments
        for _ in range(5):
            tree.search(5)
            assert tree.root.value == 5

    def test_alternating_access_pattern(self):
        """Test d'un pattern d'accès alterné."""
        tree = SplayTree()
        
        # Insérer des éléments
        for i in range(10):
            tree.insert(i)
        
        # Accès alterné
        for _ in range(10):
            tree.search(0)
            tree.search(9)
        
        # L'un des deux éléments devrait être la racine
        assert tree.root.value in [0, 9]


class TestSplayNode:
    """Tests pour la classe SplayNode."""

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

    def test_zig_case(self):
        """Test de détection du cas zig."""
        parent = SplayNode(10)
        child = SplayNode(5, parent)
        parent.set_left(child)
        
        assert child.is_zig_case() is True

    def test_zig_zig_case(self):
        """Test de détection du cas zig-zig."""
        grandparent = SplayNode(20)
        parent = SplayNode(10, grandparent)
        child = SplayNode(5, parent)
        
        grandparent.set_left(parent)
        parent.set_left(child)
        
        assert child.is_zig_zig_case() is True

    def test_zig_zag_case(self):
        """Test de détection du cas zig-zag."""
        grandparent = SplayNode(20)
        parent = SplayNode(10, grandparent)
        child = SplayNode(15, parent)
        
        grandparent.set_left(parent)
        parent.set_right(child)
        
        assert child.is_zig_zag_case() is True

    def test_get_rotation_type(self):
        """Test de détermination du type de rotation."""
        parent = SplayNode(10)
        child = SplayNode(5, parent)
        parent.set_left(child)
        
        rotation_type = child.get_rotation_type()
        assert rotation_type == "zig"

    def test_get_splay_path(self):
        """Test de récupération du chemin de splay."""
        grandparent = SplayNode(20)
        parent = SplayNode(10, grandparent)
        child = SplayNode(5, parent)
        
        grandparent.set_left(parent)
        parent.set_left(child)
        
        path = child.get_splay_path()
        assert len(path) == 3
        assert path[0] == child
        assert path[1] == parent
        assert path[2] == grandparent

    def test_get_splay_depth(self):
        """Test de calcul de la profondeur de splay."""
        grandparent = SplayNode(20)
        parent = SplayNode(10, grandparent)
        child = SplayNode(5, parent)
        
        grandparent.set_left(parent)
        parent.set_left(child)
        
        assert child.get_splay_depth() == 2

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


if __name__ == "__main__":
    pytest.main([__file__])