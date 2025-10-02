"""
Tests unitaires pour la classe BTree.

Ce module contient tous les tests unitaires pour la classe BTree,
incluant les tests de fonctionnalité, de validation et de gestion d'erreurs.
"""

import pytest
from typing import List, Optional

from src.baobab_tree.nary.btree import BTree
from src.baobab_tree.nary.btree_node import BTreeNode
from src.baobab_tree.core.exceptions import (
    BTreeError,
    InvalidOrderError,
    NodeFullError,
    NodeUnderflowError,
)


class TestBTree:
    """Tests pour la classe BTree."""

    def test_init_default_order(self):
        """Test de l'initialisation avec l'ordre par défaut."""
        btree = BTree()
        assert btree.order == 3
        assert btree.root is None
        assert btree.size == 0
        assert btree.height == 0

    def test_init_custom_order(self):
        """Test de l'initialisation avec un ordre personnalisé."""
        btree = BTree(order=5)
        assert btree.order == 5
        assert btree.root is None
        assert btree.size == 0
        assert btree.height == 0

    def test_init_invalid_order(self):
        """Test de l'initialisation avec un ordre invalide."""
        with pytest.raises(InvalidOrderError) as exc_info:
            BTree(order=1)
        assert "Ordre invalide" in str(exc_info.value)

    def test_insert_first_key(self):
        """Test de l'insertion de la première clé."""
        btree = BTree(order=3)
        btree.insert(10)
        
        assert btree.size == 1
        assert btree.height == 1
        assert btree.root is not None
        assert btree.root.keys == [10]
        assert btree.root.is_leaf is True

    def test_insert_multiple_keys(self):
        """Test de l'insertion de plusieurs clés."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        assert btree.size == 5
        assert btree.contains(10) is True
        assert btree.contains(30) is True
        assert btree.contains(50) is True

    def test_insert_causes_split(self):
        """Test de l'insertion qui cause une division."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60]  # Dépassera la capacité d'une feuille
        
        for key in keys:
            btree.insert(key)
        
        assert btree.size == 6
        assert btree.height > 1  # L'arbre a maintenant plusieurs niveaux

    def test_search_existing_key(self):
        """Test de la recherche d'une clé existante."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        result = btree.search(30)
        assert result is not None
        assert isinstance(result, BTreeNode)
        assert 30 in result.keys

    def test_search_non_existing_key(self):
        """Test de la recherche d'une clé non existante."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        result = btree.search(25)
        assert result is None

    def test_search_empty_tree(self):
        """Test de la recherche dans un arbre vide."""
        btree = BTree(order=3)
        
        result = btree.search(10)
        assert result is None

    def test_contains_existing_key(self):
        """Test de la vérification de présence d'une clé existante."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        assert btree.contains(30) is True
        assert btree.contains(50) is True

    def test_contains_non_existing_key(self):
        """Test de la vérification de présence d'une clé non existante."""
        btree = Btree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        assert btree.contains(25) is False
        assert btree.contains(60) is False

    def test_delete_existing_key(self):
        """Test de la suppression d'une clé existante."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        result = btree.delete(30)
        assert result is True
        assert btree.size == 4
        assert btree.contains(30) is False

    def test_delete_non_existing_key(self):
        """Test de la suppression d'une clé non existante."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        result = btree.delete(25)
        assert result is False
        assert btree.size == 5  # Taille inchangée

    def test_delete_all_keys(self):
        """Test de la suppression de toutes les clés."""
        btree = BTree(order=3)
        keys = [10, 20, 30]
        
        for key in keys:
            btree.insert(key)
        
        for key in keys:
            btree.delete(key)
        
        assert btree.size == 0
        assert btree.is_empty() is True
        assert btree.root is None

    def test_clear(self):
        """Test du vidage de l'arbre."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        btree.clear()
        
        assert btree.size == 0
        assert btree.height == 0
        assert btree.root is None
        assert btree.is_empty() is True

    def test_is_empty(self):
        """Test de la vérification si l'arbre est vide."""
        btree = BTree(order=3)
        assert btree.is_empty() is True
        
        btree.insert(10)
        assert btree.is_empty() is False
        
        btree.delete(10)
        assert btree.is_empty() is True

    def test_get_size(self):
        """Test de la récupération de la taille."""
        btree = BTree(order=3)
        assert btree.get_size() == 0
        
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            btree.insert(key)
        
        assert btree.get_size() == 5

    def test_get_height(self):
        """Test de la récupération de la hauteur."""
        btree = BTree(order=3)
        assert btree.get_height() == 0
        
        btree.insert(10)
        assert btree.get_height() == 1
        
        # Insérer assez de clés pour créer plusieurs niveaux
        keys = [20, 30, 40, 50, 60, 70, 80, 90]
        for key in keys:
            btree.insert(key)
        
        assert btree.get_height() > 1

    def test_get_min(self):
        """Test de la récupération de la clé minimale."""
        btree = BTree(order=3)
        assert btree.get_min() is None
        
        keys = [50, 30, 70, 10, 40, 60, 80]
        for key in keys:
            btree.insert(key)
        
        assert btree.get_min() == 10

    def test_get_max(self):
        """Test de la récupération de la clé maximale."""
        btree = BTree(order=3)
        assert btree.get_max() is None
        
        keys = [50, 30, 70, 10, 40, 60, 80]
        for key in keys:
            btree.insert(key)
        
        assert btree.get_max() == 80

    def test_is_valid(self):
        """Test de la validation de l'arbre."""
        btree = BTree(order=3)
        assert btree.is_valid() is True  # Arbre vide est valide
        
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            btree.insert(key)
        
        assert btree.is_valid() is True

    def test_range_query(self):
        """Test de la requête de plage."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for key in keys:
            btree.insert(key)
        
        result = btree.range_query(25, 75)
        expected = [30, 40, 50, 60, 70]
        assert result == expected

    def test_range_query_empty_range(self):
        """Test de la requête de plage vide."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        result = btree.range_query(60, 70)
        assert result == []

    def test_count_range(self):
        """Test du comptage dans une plage."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for key in keys:
            btree.insert(key)
        
        count = btree.count_range(25, 75)
        assert count == 5

    def test_bulk_load(self):
        """Test du chargement en masse."""
        btree = BTree(order=3)
        keys = [50, 30, 70, 10, 40, 60, 80, 20, 90]
        
        btree.bulk_load(keys)
        
        assert btree.size == len(keys)
        assert btree.is_valid() is True
        
        # Vérifier que toutes les clés sont présentes
        for key in keys:
            assert btree.contains(key) is True

    def test_bulk_load_empty(self):
        """Test du chargement en masse avec une liste vide."""
        btree = BTree(order=3)
        btree.bulk_load([])
        
        assert btree.size == 0
        assert btree.is_empty() is True

    def test_get_leaf_nodes(self):
        """Test de la récupération des nœuds feuilles."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for key in keys:
            btree.insert(key)
        
        leaves = btree.get_leaf_nodes()
        assert len(leaves) > 0
        
        # Vérifier que tous les nœuds retournés sont des feuilles
        for leaf in leaves:
            assert leaf.is_leaf is True

    def test_get_internal_nodes(self):
        """Test de la récupération des nœuds internes."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for key in keys:
            btree.insert(key)
        
        internals = btree.get_internal_nodes()
        
        # Vérifier que tous les nœuds retournés sont internes
        for internal in internals:
            assert internal.is_leaf is False

    def test_get_node_count(self):
        """Test de la récupération des statistiques de nœuds."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for key in keys:
            btree.insert(key)
        
        stats = btree.get_node_count()
        
        assert "total_nodes" in stats
        assert "leaf_nodes" in stats
        assert "internal_nodes" in stats
        assert "total_keys" in stats
        assert "height" in stats
        
        assert stats["total_keys"] == btree.size
        assert stats["height"] == btree.height
        assert stats["total_nodes"] == stats["leaf_nodes"] + stats["internal_nodes"]

    def test_validate_properties(self):
        """Test de la validation des propriétés."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for key in keys:
            btree.insert(key)
        
        properties = btree.validate_properties()
        
        assert "is_valid" in properties
        assert "height_consistent" in properties
        assert "size_consistent" in properties
        assert "keys_sorted" in properties
        assert "node_capacity" in properties
        
        # Toutes les propriétés doivent être vraies pour un arbre valide
        for prop_value in properties.values():
            assert prop_value is True

    def test_str_representation(self):
        """Test de la représentation string."""
        btree = BTree(order=3)
        str_repr = str(btree)
        assert "BTree(order=3, empty)" in str_repr
        
        btree.insert(10)
        str_repr = str(btree)
        assert "BTree(order=3, size=1, height=1)" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        btree = BTree(order=3)
        repr_str = repr(btree)
        assert "BTree(order=3, size=0, height=0" in repr_str
        assert "root=None" in repr_str
        
        btree.insert(10)
        repr_str = repr(btree)
        assert "root='present'" in repr_str

    def test_complex_insertion_deletion(self):
        """Test d'insertions et suppressions complexes."""
        btree = BTree(order=3)
        
        # Insérer des clés dans un ordre aléatoire
        keys = [50, 30, 70, 10, 40, 60, 80, 20, 90, 15, 35, 45, 55, 65, 75, 85]
        
        for key in keys:
            btree.insert(key)
        
        assert btree.size == len(keys)
        assert btree.is_valid() is True
        
        # Supprimer quelques clés
        keys_to_delete = [30, 60, 80]
        for key in keys_to_delete:
            btree.delete(key)
        
        assert btree.size == len(keys) - len(keys_to_delete)
        assert btree.is_valid() is True
        
        # Vérifier que les clés supprimées ne sont plus présentes
        for key in keys_to_delete:
            assert btree.contains(key) is False
        
        # Vérifier que les autres clés sont toujours présentes
        remaining_keys = [k for k in keys if k not in keys_to_delete]
        for key in remaining_keys:
            assert btree.contains(key) is True

    def test_edge_case_single_key(self):
        """Test du cas limite avec une seule clé."""
        btree = BTree(order=3)
        btree.insert(42)
        
        assert btree.size == 1
        assert btree.height == 1
        assert btree.contains(42) is True
        assert btree.get_min() == 42
        assert btree.get_max() == 42
        
        btree.delete(42)
        assert btree.size == 0
        assert btree.height == 0
        assert btree.is_empty() is True

    def test_edge_case_minimum_order(self):
        """Test du cas limite avec l'ordre minimum."""
        btree = BTree(order=2)
        keys = [10, 20, 30, 40, 50]
        
        for key in keys:
            btree.insert(key)
        
        assert btree.size == 5
        assert btree.is_valid() is True
        
        for key in keys:
            assert btree.contains(key) is True

    def test_performance_large_dataset(self):
        """Test de performance avec un grand ensemble de données."""
        btree = BTree(order=5)
        keys = list(range(1, 1001))  # 1000 clés
        
        # Insérer toutes les clés
        for key in keys:
            btree.insert(key)
        
        assert btree.size == 1000
        assert btree.is_valid() is True
        
        # Vérifier quelques clés
        assert btree.contains(1) is True
        assert btree.contains(500) is True
        assert btree.contains(1000) is True
        
        # Test de requête de plage
        result = btree.range_query(100, 200)
        assert len(result) == 101  # 100 à 200 inclus
        
        # Supprimer quelques clés
        keys_to_delete = [100, 200, 300, 400, 500]
        for key in keys_to_delete:
            btree.delete(key)
        
        assert btree.size == 995
        assert btree.is_valid() is True