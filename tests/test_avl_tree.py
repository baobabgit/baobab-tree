"""
Tests unitaires pour la classe AVLTree.

Ce module contient tous les tests unitaires pour la classe AVLTree,
incluant les tests de base, les tests d'équilibrage et les tests de validation.
"""

import math
import pytest
from src.avl_tree import AVLTree
from src.avl_node import AVLNode
from src.exceptions import AVLError


class TestAVLTree:
    """Tests pour la classe AVLTree."""

    def test_avl_tree_creation(self):
        """Test de création d'un arbre AVL."""
        tree = AVLTree()
        assert tree.root is None
        assert tree.size == 0
        assert tree.balance_threshold == 1
        assert tree.rotation_count == 0

    def test_avl_tree_with_comparator(self):
        """Test de création d'un arbre AVL avec comparateur personnalisé."""

        def custom_comparator(a, b):
            return -1 if a < b else (1 if a > b else 0)

        tree = AVLTree(custom_comparator)
        assert tree.comparator is custom_comparator

    def test_insert_single_value(self):
        """Test d'insertion d'une seule valeur."""
        tree = AVLTree()
        result = tree.insert(50)

        assert result is True
        assert tree.size == 1
        assert tree.root is not None
        assert tree.root.value == 50
        assert isinstance(tree.root, AVLNode)
        assert tree.root.is_balanced()

    def test_insert_duplicate_value(self):
        """Test d'insertion d'une valeur dupliquée."""
        tree = AVLTree()
        tree.insert(50)
        result = tree.insert(50)

        assert result is False
        assert tree.size == 1

    def test_insert_multiple_values(self):
        """Test d'insertion de plusieurs valeurs."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            result = tree.insert(value)
            assert result is True

        assert tree.size == len(values)
        assert tree.is_avl_valid()

    def test_insert_sequential_values(self):
        """Test d'insertion de valeurs séquentielles (cas de déséquilibre)."""
        tree = AVLTree()
        values = [1, 2, 3, 4, 5]

        for value in values:
            tree.insert(value)

        assert tree.size == len(values)
        assert tree.is_avl_valid()
        assert tree.get_height() <= 2 * math.log2(tree.size + 1)

    def test_insert_reverse_sequential_values(self):
        """Test d'insertion de valeurs en ordre décroissant."""
        tree = AVLTree()
        values = [5, 4, 3, 2, 1]

        for value in values:
            tree.insert(value)

        assert tree.size == len(values)
        assert tree.is_avl_valid()
        assert tree.get_height() <= 2 * math.log2(tree.size + 1)

    def test_delete_existing_value(self):
        """Test de suppression d'une valeur existante."""
        tree = AVLTree()
        tree.insert(50)
        tree.insert(30)
        tree.insert(70)

        result = tree.delete(30)

        assert result is True
        assert tree.size == 2
        assert tree.is_avl_valid()

    def test_delete_non_existing_value(self):
        """Test de suppression d'une valeur inexistante."""
        tree = AVLTree()
        tree.insert(50)

        result = tree.delete(30)

        assert result is False
        assert tree.size == 1

    def test_delete_root(self):
        """Test de suppression de la racine."""
        tree = AVLTree()
        tree.insert(50)
        tree.insert(30)
        tree.insert(70)

        result = tree.delete(50)

        assert result is True
        assert tree.size == 2
        assert tree.is_avl_valid()

    def test_delete_all_values(self):
        """Test de suppression de toutes les valeurs."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        for value in values:
            result = tree.delete(value)
            assert result is True
            assert tree.is_avl_valid()

        assert tree.size == 0
        assert tree.root is None

    def test_search_existing_value(self):
        """Test de recherche d'une valeur existante."""
        tree = AVLTree()
        tree.insert(50)
        tree.insert(30)
        tree.insert(70)

        result = tree.search(30)

        assert result is not None
        assert result.value == 30
        assert isinstance(result, AVLNode)

    def test_search_non_existing_value(self):
        """Test de recherche d'une valeur inexistante."""
        tree = AVLTree()
        tree.insert(50)

        result = tree.search(30)

        assert result is None

    def test_contains_existing_value(self):
        """Test de contains avec une valeur existante."""
        tree = AVLTree()
        tree.insert(50)

        result = tree.contains(50)

        assert result is True

    def test_contains_non_existing_value(self):
        """Test de contains avec une valeur inexistante."""
        tree = AVLTree()
        tree.insert(50)

        result = tree.contains(30)

        assert result is False

    def test_is_avl_valid_empty_tree(self):
        """Test de validation AVL d'un arbre vide."""
        tree = AVLTree()
        assert tree.is_avl_valid() is True

    def test_is_avl_valid_balanced_tree(self):
        """Test de validation AVL d'un arbre équilibré."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        assert tree.is_avl_valid() is True

    def test_check_balance_factors(self):
        """Test de vérification des facteurs d'équilibre."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        assert tree.check_balance_factors() is True

    def test_validate_heights(self):
        """Test de validation des hauteurs."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        assert tree.validate_heights() is True

    def test_get_balance_statistics(self):
        """Test d'obtention des statistiques d'équilibre."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        stats = tree.get_balance_statistics()

        assert "total_nodes" in stats
        assert "balanced_nodes" in stats
        assert "left_heavy_nodes" in stats
        assert "right_heavy_nodes" in stats
        assert "perfectly_balanced_nodes" in stats
        assert stats["total_nodes"] == len(values)
        assert stats["balanced_nodes"] == len(values)

    def test_get_rotation_count(self):
        """Test d'obtention du nombre de rotations."""
        tree = AVLTree()
        initial_count = tree.get_rotation_count()

        # Insérer des valeurs qui nécessitent des rotations
        values = [1, 2, 3, 4, 5]
        for value in values:
            tree.insert(value)

        final_count = tree.get_rotation_count()
        assert final_count >= initial_count

    def test_get_height_analysis(self):
        """Test d'analyse des hauteurs."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        analysis = tree.get_height_analysis()

        assert "actual_height" in analysis
        assert "optimal_height" in analysis
        assert "height_difference" in analysis
        assert "is_optimal" in analysis
        assert analysis["actual_height"] >= 0
        assert analysis["optimal_height"] >= 0

    def test_height_optimality(self):
        """Test de l'optimalité de la hauteur."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]

        for value in values:
            tree.insert(value)

        analysis = tree.get_height_analysis()
        # Pour un arbre AVL, la hauteur doit être proche de l'optimal
        assert analysis["height_difference"] <= 1

    def test_rotation_count_increases(self):
        """Test que le compteur de rotations augmente."""
        tree = AVLTree()
        initial_count = tree.rotation_count

        # Insérer des valeurs qui nécessitent des rotations
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for value in values:
            tree.insert(value)

        assert tree.rotation_count > initial_count

    def test_clear_tree(self):
        """Test de vidage de l'arbre."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        tree.clear()

        assert tree.size == 0
        assert tree.root is None
        assert tree.rotation_count == 0

    def test_tree_properties_after_operations(self):
        """Test des propriétés de l'arbre après diverses opérations."""
        tree = AVLTree()

        # Insérer des valeurs
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        for value in values:
            tree.insert(value)
            assert tree.is_avl_valid()

        # Supprimer des valeurs
        delete_values = [20, 40, 60, 80]
        for value in delete_values:
            tree.delete(value)
            assert tree.is_avl_valid()

        # Vérifier les propriétés finales
        assert tree.size == len(values) - len(delete_values)
        assert tree.is_avl_valid()
        assert tree.check_balance_factors()
        assert tree.validate_heights()

    def test_large_tree_performance(self):
        """Test de performance sur un grand arbre."""
        tree = AVLTree()

        # Insérer 1000 valeurs
        for i in range(1000):
            tree.insert(i)
            if i % 100 == 0:  # Vérifier périodiquement
                assert tree.is_avl_valid()

        # Vérifier les propriétés finales
        assert tree.size == 1000
        assert tree.is_avl_valid()

        # La hauteur doit être logarithmique
        optimal_height = int(math.log2(1000 + 1))
        actual_height = tree.get_height()
        assert actual_height <= optimal_height + 1

    def test_random_insertions_and_deletions(self):
        """Test d'insertions et suppressions aléatoires."""
        import random

        tree = AVLTree()
        values = list(range(1, 101))  # 1 à 100
        random.shuffle(values)

        # Insérer toutes les valeurs
        for value in values:
            tree.insert(value)
            assert tree.is_avl_valid()

        # Supprimer la moitié des valeurs
        to_delete = values[:50]
        random.shuffle(to_delete)

        for value in to_delete:
            tree.delete(value)
            assert tree.is_avl_valid()

        assert tree.size == 50

    def test_string_representation(self):
        """Test de la représentation string."""
        tree = AVLTree()
        tree.insert(50)
        tree.insert(30)

        str_repr = str(tree)
        assert "AVLTree" in str_repr
        assert "size=2" in str_repr
        assert "height=" in str_repr
        assert "rotations=" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        tree = AVLTree()
        tree.insert(50)

        repr_str = repr(tree)
        assert "AVLTree" in repr_str
        assert "root=" in repr_str
        assert "size=1" in repr_str
        assert "rotations=0" in repr_str

    def test_inheritance_from_binary_search_tree(self):
        """Test de l'héritage de BinarySearchTree."""
        tree = AVLTree()

        # Vérifier que les méthodes de base fonctionnent
        assert tree.is_empty() is True
        assert tree.get_min() is None
        assert tree.get_max() is None

        tree.insert(50)
        tree.insert(30)
        tree.insert(70)

        assert tree.get_min() == 30
        assert tree.get_max() == 70
        assert tree.is_empty() is False

    def test_traversal_methods(self):
        """Test des méthodes de parcours héritées."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        # Test des parcours
        preorder = tree.preorder_traversal()
        inorder = tree.inorder_traversal()
        postorder = tree.postorder_traversal()
        level_order = tree.level_order_traversal()

        assert len(preorder) == len(values)
        assert len(inorder) == len(values)
        assert len(postorder) == len(values)
        assert len(level_order) == len(values)

        # Vérifier que tous les éléments sont présents
        assert set(preorder) == set(values)
        assert set(inorder) == set(values)
        assert set(postorder) == set(values)
        assert set(level_order) == set(values)

    def test_iterator_methods(self):
        """Test des méthodes d'itérateurs héritées."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            tree.insert(value)

        # Test des itérateurs
        preorder_iter = tree.preorder_iter()
        inorder_iter = tree.inorder_iter()
        postorder_iter = tree.postorder_iter()
        level_order_iter = tree.level_order_iter()

        # Vérifier que les itérateurs fonctionnent
        preorder_list = list(preorder_iter)
        inorder_list = list(inorder_iter)
        postorder_list = list(postorder_iter)
        level_order_list = list(level_order_iter)

        assert len(preorder_list) == len(values)
        assert len(inorder_list) == len(values)
        assert len(postorder_list) == len(values)
        assert len(level_order_list) == len(values)

    def test_error_handling(self):
        """Test de la gestion d'erreurs."""
        tree = AVLTree()

        # Test avec des valeurs valides
        tree.insert(50)
        assert tree.is_avl_valid()

        # Test avec des valeurs None (devrait lever une exception)
        with pytest.raises(Exception):
            tree.insert(None)

    def test_avl_properties_maintained(self):
        """Test que les propriétés AVL sont maintenues."""
        tree = AVLTree()

        # Insérer des valeurs dans différents ordres
        sequences = [
            [1, 2, 3, 4, 5],  # Ordre croissant
            [5, 4, 3, 2, 1],  # Ordre décroissant
            [3, 1, 5, 2, 4],  # Ordre aléatoire
            [1, 3, 2, 5, 4],  # Autre ordre aléatoire
        ]

        for sequence in sequences:
            tree.clear()
            for value in sequence:
                tree.insert(value)
                assert tree.is_avl_valid()
                assert tree.check_balance_factors()
                assert tree.validate_heights()
