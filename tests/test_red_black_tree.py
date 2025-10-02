"""
Tests unitaires pour la classe RedBlackTree.

Ce module contient tous les tests unitaires pour la classe RedBlackTree,
incluant les tests de base, d'équilibrage, de validation et de performance.
"""

import pytest
from src.baobab_tree.balanced.red_black_tree import RedBlackTree
from src.baobab_tree.balanced.red_black_node import Color, RedBlackNode
from src.baobab_tree.core.exceptions import (
    RedBlackTreeError,
    ColorViolationError,
    PathViolationError,
    RedBlackBalancingError,
)


class TestRedBlackTree:
    """Tests pour la classe RedBlackTree."""

    def test_init(self):
        """Test de l'initialisation."""
        tree = RedBlackTree()
        assert tree.size == 0
        assert tree.root is None
        assert tree.is_empty()
        assert tree._recolor_count == 0
        assert tree._rotation_count == 0

    def test_init_with_comparator(self):
        """Test de l'initialisation avec comparateur personnalisé."""
        def custom_comparator(a, b):
            return -1 if a < b else (1 if a > b else 0)
        
        tree = RedBlackTree(custom_comparator)
        assert tree.comparator == custom_comparator

    def test_insert_single_value(self):
        """Test d'insertion d'une seule valeur."""
        tree = RedBlackTree()
        
        result = tree.insert(42)
        
        assert result is True
        assert tree.size == 1
        assert tree.root is not None
        assert tree.root.value == 42
        assert tree.root.is_black()  # La racine doit être noire

    def test_insert_duplicate_value(self):
        """Test d'insertion de valeur dupliquée."""
        tree = RedBlackTree()
        tree.insert(42)
        
        result = tree.insert(42)
        
        assert result is False
        assert tree.size == 1

    def test_insert_multiple_values(self):
        """Test d'insertion de plusieurs valeurs."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            result = tree.insert(value)
            assert result is True
        
        assert tree.size == len(values)
        assert tree.is_red_black_valid()

    def test_insert_sequential_values(self):
        """Test d'insertion de valeurs séquentielles."""
        tree = RedBlackTree()
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for value in values:
            tree.insert(value)
        
        assert tree.size == len(values)
        assert tree.is_red_black_valid()
        assert tree.validate_colors()
        assert tree.validate_paths()

    def test_insert_reverse_order(self):
        """Test d'insertion en ordre décroissant."""
        tree = RedBlackTree()
        values = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        
        for value in values:
            tree.insert(value)
        
        assert tree.size == len(values)
        assert tree.is_red_black_valid()
        assert tree.validate_colors()
        assert tree.validate_paths()

    def test_delete_existing_value(self):
        """Test de suppression de valeur existante."""
        tree = RedBlackTree()
        tree.insert(50)
        tree.insert(30)
        tree.insert(70)
        
        result = tree.delete(30)
        
        assert result is True
        assert tree.size == 2
        assert tree.is_red_black_valid()

    def test_delete_non_existing_value(self):
        """Test de suppression de valeur inexistante."""
        tree = RedBlackTree()
        tree.insert(50)
        
        result = tree.delete(30)
        
        assert result is False
        assert tree.size == 1

    def test_delete_root(self):
        """Test de suppression de la racine."""
        tree = RedBlackTree()
        tree.insert(50)
        tree.insert(30)
        tree.insert(70)
        
        result = tree.delete(50)
        
        assert result is True
        assert tree.size == 2
        assert tree.is_red_black_valid()

    def test_delete_with_two_children(self):
        """Test de suppression d'un nœud avec deux enfants."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        result = tree.delete(50)
        
        assert result is True
        assert tree.size == len(values) - 1
        assert tree.is_red_black_valid()

    def test_delete_all_values(self):
        """Test de suppression de toutes les valeurs."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        for value in values:
            result = tree.delete(value)
            assert result is True
            assert tree.is_red_black_valid()
        
        assert tree.size == 0
        assert tree.root is None

    def test_search_existing_value(self):
        """Test de recherche de valeur existante."""
        tree = RedBlackTree()
        tree.insert(50)
        tree.insert(30)
        tree.insert(70)
        
        result = tree.search(30)
        
        assert result is not None
        assert result.value == 30

    def test_search_non_existing_value(self):
        """Test de recherche de valeur inexistante."""
        tree = RedBlackTree()
        tree.insert(50)
        
        result = tree.search(30)
        
        assert result is None

    def test_contains_existing_value(self):
        """Test de contains avec valeur existante."""
        tree = RedBlackTree()
        tree.insert(50)
        
        assert tree.contains(50) is True

    def test_contains_non_existing_value(self):
        """Test de contains avec valeur inexistante."""
        tree = RedBlackTree()
        tree.insert(50)
        
        assert tree.contains(30) is False

    def test_is_red_black_valid_empty_tree(self):
        """Test de validation rouge-noir pour arbre vide."""
        tree = RedBlackTree()
        assert tree.is_red_black_valid() is True

    def test_is_red_black_valid_single_node(self):
        """Test de validation rouge-noir pour nœud unique."""
        tree = RedBlackTree()
        tree.insert(42)
        assert tree.is_red_black_valid() is True

    def test_is_red_black_valid_complex_tree(self):
        """Test de validation rouge-noir pour arbre complexe."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            tree.insert(value)
        
        assert tree.is_red_black_valid() is True
        assert tree.validate_colors() is True
        assert tree.validate_paths() is True

    def test_validate_colors(self):
        """Test de validation des couleurs."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        assert tree.validate_colors() is True

    def test_validate_paths(self):
        """Test de validation des chemins."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        assert tree.validate_paths() is True

    def test_get_color_analysis(self):
        """Test d'analyse des couleurs."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        analysis = tree.get_color_analysis()
        
        assert "red_count" in analysis
        assert "black_count" in analysis
        assert "total_nodes" in analysis
        assert "red_percentage" in analysis
        assert "black_percentage" in analysis
        assert "color_distribution_by_level" in analysis
        assert analysis["total_nodes"] == len(values)

    def test_get_balancing_stats(self):
        """Test des statistiques d'équilibrage."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        stats = tree.get_balancing_stats()
        
        assert "recolor_count" in stats
        assert "rotation_count" in stats
        assert "total_operations" in stats
        assert stats["total_operations"] == stats["recolor_count"] + stats["rotation_count"]

    def test_get_performance_analysis(self):
        """Test d'analyse de performance."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        analysis = tree.get_performance_analysis()
        
        assert "size" in analysis
        assert "height" in analysis
        assert "is_balanced" in analysis
        assert "is_red_black_valid" in analysis
        assert "balancing_stats" in analysis
        assert "color_analysis" in analysis
        assert analysis["size"] == len(values)
        assert analysis["is_red_black_valid"] is True

    def test_find_red_nodes(self):
        """Test de recherche des nœuds rouges."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        red_nodes = tree.find_red_nodes()
        
        assert isinstance(red_nodes, list)
        for node in red_nodes:
            assert isinstance(node, RedBlackNode)
            assert node.is_red()

    def test_find_black_nodes(self):
        """Test de recherche des nœuds noirs."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        black_nodes = tree.find_black_nodes()
        
        assert isinstance(black_nodes, list)
        for node in black_nodes:
            assert isinstance(node, RedBlackNode)
            assert node.is_black()

    def test_get_structure_analysis(self):
        """Test d'analyse de structure."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        analysis = tree.get_structure_analysis()
        
        assert "size" in analysis
        assert "height" in analysis
        assert "is_balanced" in analysis
        assert "is_red_black_valid" in analysis
        assert "color_analysis" in analysis
        assert "balancing_stats" in analysis
        assert "root_color" in analysis
        assert "red_nodes_count" in analysis
        assert "black_nodes_count" in analysis

    def test_height_property(self):
        """Test de la propriété de hauteur."""
        tree = RedBlackTree()
        assert tree.get_height() == -1  # Arbre vide
        
        tree.insert(50)
        assert tree.get_height() == 0  # Un seul nœud
        
        tree.insert(30)
        tree.insert(70)
        height = tree.get_height()
        assert height >= 1  # Au moins 2 niveaux

    def test_min_max_values(self):
        """Test des valeurs min et max."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        assert tree.get_min() == min(values)
        assert tree.get_max() == max(values)

    def test_traversal_methods(self):
        """Test des méthodes de parcours."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        # Test parcours préfixe
        preorder = tree.preorder_traversal()
        assert len(preorder) == len(values)
        
        # Test parcours infixe
        inorder = tree.inorder_traversal()
        assert len(inorder) == len(values)
        assert inorder == sorted(values)  # BST property
        
        # Test parcours postfixe
        postorder = tree.postorder_traversal()
        assert len(postorder) == len(values)
        
        # Test parcours par niveaux
        level_order = tree.level_order_traversal()
        assert len(level_order) == len(values)

    def test_clear(self):
        """Test de vidage de l'arbre."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        tree.clear()
        
        assert tree.size == 0
        assert tree.root is None
        assert tree.is_empty()

    def test_str_and_repr(self):
        """Test de __str__ et __repr__."""
        tree = RedBlackTree()
        
        # Arbre vide
        assert "empty" in str(tree)
        
        # Arbre avec éléments
        tree.insert(50)
        tree.insert(30)
        
        str_repr = str(tree)
        assert "RedBlackTree" in str_repr
        assert "size=2" in str_repr
        
        repr_str = repr(tree)
        assert "RedBlackTree" in repr_str

    def test_len_and_bool(self):
        """Test de __len__ et __bool__."""
        tree = RedBlackTree()
        
        # Arbre vide
        assert len(tree) == 0
        assert bool(tree) is False
        
        # Arbre avec éléments
        tree.insert(50)
        assert len(tree) == 1
        assert bool(tree) is True

    def test_large_dataset(self):
        """Test avec un grand nombre d'éléments."""
        tree = RedBlackTree()
        values = list(range(1, 101))  # 1 à 100
        
        for value in values:
            tree.insert(value)
        
        assert tree.size == len(values)
        assert tree.is_red_black_valid()
        assert tree.validate_colors()
        assert tree.validate_paths()
        
        # Test de suppression
        for value in values[:50]:  # Supprimer la première moitié
            tree.delete(value)
        
        assert tree.size == len(values) - 50
        assert tree.is_red_black_valid()

    def test_random_insertions_and_deletions(self):
        """Test d'insertions et suppressions aléatoires."""
        import random
        
        tree = RedBlackTree()
        values = list(range(1, 51))  # 1 à 50
        random.shuffle(values)
        
        # Insertions aléatoires
        for value in values:
            tree.insert(value)
        
        assert tree.size == len(values)
        assert tree.is_red_black_valid()
        
        # Suppressions aléatoires
        random.shuffle(values)
        for value in values[:25]:  # Supprimer la moitié
            tree.delete(value)
        
        assert tree.size == len(values) - 25
        assert tree.is_red_black_valid()

    def test_error_handling(self):
        """Test de gestion d'erreurs."""
        tree = RedBlackTree()
        
        # Test avec des valeurs None (si le comparateur le permet)
        # Note: Cela dépend de l'implémentation du comparateur par défaut
        try:
            tree.insert(None)
            # Si l'insertion réussit, vérifier que l'arbre reste valide
            if tree.size > 0:
                assert tree.is_red_black_valid()
        except Exception:
            # Si une exception est levée, c'est acceptable
            pass

    def test_property_consistency(self):
        """Test de cohérence des propriétés rouge-noir."""
        tree = RedBlackTree()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            tree.insert(value)
            # Vérifier que les propriétés sont maintenues après chaque insertion
            assert tree.is_red_black_valid()
            assert tree.validate_colors()
            assert tree.validate_paths()
        
        # Vérifier que la racine est noire
        assert tree.root.is_black()
        
        # Vérifier qu'il n'y a pas de nœuds rouges consécutifs
        red_nodes = tree.find_red_nodes()
        for red_node in red_nodes:
            if red_node.left is not None:
                assert red_node.left.is_black()
            if red_node.right is not None:
                assert red_node.right.is_black()


class TestRedBlackTreeEdgeCases:
    """Tests pour les cas limites de RedBlackTree."""

    def test_insert_with_custom_comparator_error(self):
        """Test d'insertion avec comparateur personnalisé qui génère une erreur."""
        def bad_comparator(a, b):
            if a == 42:  # Valeur spéciale qui génère une erreur
                raise ValueError("Bad value")
            return 1 if a > b else -1 if a < b else 0
        
        tree = RedBlackTree(comparator=bad_comparator)
        
        # Insertion normale
        tree.insert(10)
        tree.insert(20)
        
        # Insertion qui génère une erreur
        with pytest.raises(RedBlackTreeError) as exc_info:
            tree.insert(42)
        
        assert "Error during insertion" in str(exc_info.value)

    def test_delete_with_custom_comparator_error(self):
        """Test de suppression avec comparateur personnalisé qui génère une erreur."""
        def bad_comparator(a, b):
            if a == 42:  # Valeur spéciale qui génère une erreur
                raise ValueError("Bad value")
            return 1 if a > b else -1 if a < b else 0
        
        tree = RedBlackTree(comparator=bad_comparator)
        tree.insert(10)
        tree.insert(20)
        # Ne pas insérer 42 car cela génère une erreur
        
        # Suppression qui génère une erreur lors de la recherche
        with pytest.raises(RedBlackTreeError) as exc_info:
            tree.delete(42)
        
        assert "Error during deletion" in str(exc_info.value)

    def test_fix_deletion_violations_empty_tree(self):
        """Test de correction des violations de suppression sur arbre vide."""
        tree = RedBlackTree()
        
        # Ne devrait pas lever d'exception
        tree._fix_deletion_violations(None)

    def test_fix_deletion_violations_root_node(self):
        """Test de correction des violations de suppression sur nœud racine."""
        tree = RedBlackTree()
        tree.insert(10)
        
        # Ne devrait pas lever d'exception
        tree._fix_deletion_violations(tree._root)

    def test_rotate_left_with_none_right_child(self):
        """Test de rotation gauche avec enfant droit None."""
        tree = RedBlackTree()
        tree.insert(10)
        node = tree._root
        
        with pytest.raises(RedBlackBalancingError) as exc_info:
            tree._rotate_left(node)
        
        assert "Cannot perform left rotation: no right child" in str(exc_info.value)

    def test_rotate_right_with_none_left_child(self):
        """Test de rotation droite avec enfant gauche None."""
        tree = RedBlackTree()
        tree.insert(10)
        node = tree._root
        
        with pytest.raises(RedBlackBalancingError) as exc_info:
            tree._rotate_right(node)
        
        assert "Cannot perform right rotation: no left child" in str(exc_info.value)

    def test_get_color_analysis_empty_tree(self):
        """Test d'analyse des couleurs sur arbre vide."""
        tree = RedBlackTree()
        analysis = tree.get_color_analysis()
        
        assert analysis["total_nodes"] == 0
        assert analysis["red_count"] == 0
        assert analysis["black_count"] == 0

    def test_get_performance_analysis_empty_tree(self):
        """Test d'analyse de performance sur arbre vide."""
        tree = RedBlackTree()
        analysis = tree.get_performance_analysis()
        
        assert analysis["size"] == 0
        assert analysis["balancing_stats"]["recolor_count"] == 0
        assert analysis["balancing_stats"]["rotation_count"] == 0

    def test_find_red_nodes_empty_tree(self):
        """Test de recherche de nœuds rouges sur arbre vide."""
        tree = RedBlackTree()
        red_nodes = tree.find_red_nodes()
        
        assert len(red_nodes) == 0

    def test_find_black_nodes_empty_tree(self):
        """Test de recherche de nœuds noirs sur arbre vide."""
        tree = RedBlackTree()
        black_nodes = tree.find_black_nodes()
        
        assert len(black_nodes) == 0

    def test_get_structure_analysis_empty_tree(self):
        """Test d'analyse de structure sur arbre vide."""
        tree = RedBlackTree()
        analysis = tree.get_structure_analysis()
        
        assert analysis["size"] == 0
        assert analysis["height"] == -1  # Arbre vide a une hauteur de -1
        assert analysis["is_balanced"] is True