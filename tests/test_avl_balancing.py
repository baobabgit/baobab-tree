"""
Tests unitaires pour la classe AVLBalancing.

Ce module contient tous les tests unitaires pour valider le fonctionnement
de la classe AVLBalancing et de ses algorithmes d'équilibrage.
"""

import pytest
import time
from typing import Any, Dict, List

from src.baobab_tree.balanced.avl_balancing import (
    AVLBalancing,
    BalancingError,
    CorrectionApplicationError,
    ImbalanceDetectionError,
    ValidationError,
)
from src.baobab_tree.balanced.avl_node import AVLNode
from src.baobab_tree.balanced.avl_rotations import AVLRotations
from src.baobab_tree.core.exceptions import AVLError


class TestAVLBalancing:
    """Tests pour la classe AVLBalancing."""

    def test_balance_node_none(self):
        """Test de balance_node avec un nœud None."""
        result = AVLBalancing.balance_node(None)
        assert result is None

    def test_balance_node_already_balanced(self):
        """Test de balance_node avec un nœud déjà équilibré."""
        # Créer un nœud équilibré
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        node.set_right(AVLNode(15))
        
        result = AVLBalancing.balance_node(node)
        assert result == node

    def test_balance_node_simple_left_imbalance(self):
        """Test de balance_node avec déséquilibre simple gauche."""
        # Créer un arbre déséquilibré à gauche
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.balance_node(root)
        assert result is not None
        assert result != root  # La racine devrait changer

    def test_balance_node_simple_right_imbalance(self):
        """Test de balance_node avec déséquilibre simple droit."""
        # Créer un arbre déséquilibré à droite
        root = AVLNode(10)
        right = AVLNode(15)
        right_right = AVLNode(20)
        
        root.set_right(right)
        right.set_right(right_right)
        
        # Forcer le déséquilibre
        root._balance_factor = 2
        root._cached_height = 2
        right._balance_factor = 1
        right._cached_height = 1
        
        result = AVLBalancing.balance_node(root)
        assert result is not None
        assert result != root  # La racine devrait changer

    def test_balance_node_double_left_right_imbalance(self):
        """Test de balance_node avec déséquilibre double gauche-droite."""
        # Créer un arbre avec déséquilibre double gauche-droite
        root = AVLNode(10)
        left = AVLNode(5)
        left_right = AVLNode(7)
        
        root.set_left(left)
        left.set_right(left_right)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = 1
        left._cached_height = 1
        
        result = AVLBalancing.balance_node(root)
        assert result is not None
        assert result != root  # La racine devrait changer

    def test_balance_node_double_right_left_imbalance(self):
        """Test de balance_node avec déséquilibre double droite-gauche."""
        # Créer un arbre avec déséquilibre double droite-gauche
        root = AVLNode(10)
        right = AVLNode(15)
        right_left = AVLNode(12)
        
        root.set_right(right)
        right.set_left(right_left)
        
        # Forcer le déséquilibre
        root._balance_factor = 2
        root._cached_height = 2
        right._balance_factor = -1
        right._cached_height = 1
        
        result = AVLBalancing.balance_node(root)
        assert result is not None
        assert result != root  # La racine devrait changer

    def test_rebalance_path_none(self):
        """Test de rebalance_path avec un nœud None."""
        result = AVLBalancing.rebalance_path(None)
        assert result is None

    def test_rebalance_path_single_node(self):
        """Test de rebalance_path avec un seul nœud."""
        node = AVLNode(10)
        result = AVLBalancing.rebalance_path(node)
        assert result == node

    def test_rebalance_path_multiple_nodes(self):
        """Test de rebalance_path avec plusieurs nœuds."""
        # Créer un arbre avec plusieurs niveaux
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.rebalance_path(left_left)
        assert result is not None

    def test_rebalance_tree_none(self):
        """Test de rebalance_tree avec une racine None."""
        result = AVLBalancing.rebalance_tree(None)
        assert result is None

    def test_rebalance_tree_already_balanced(self):
        """Test de rebalance_tree avec un arbre déjà équilibré."""
        # Créer un arbre équilibré
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.rebalance_tree(root)
        assert result == root

    def test_rebalance_tree_unbalanced(self):
        """Test de rebalance_tree avec un arbre déséquilibré."""
        # Créer un arbre déséquilibré
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.rebalance_tree(root)
        assert result is not None

    def test_detect_imbalance_none(self):
        """Test de detect_imbalance avec un nœud None."""
        with pytest.raises(ImbalanceDetectionError):
            AVLBalancing.detect_imbalance(None)

    def test_detect_imbalance_balanced(self):
        """Test de detect_imbalance avec un nœud équilibré."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        node.set_right(AVLNode(15))
        
        result = AVLBalancing.detect_imbalance(node)
        assert result["is_imbalanced"] is False
        assert result["type"] == "none"

    def test_detect_imbalance_simple_left(self):
        """Test de detect_imbalance avec déséquilibre simple gauche."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        
        # Forcer le déséquilibre
        node._balance_factor = -2
        
        result = AVLBalancing.detect_imbalance(node)
        assert result["is_imbalanced"] is True
        assert result["type"] == "simple_left"

    def test_detect_imbalance_simple_right(self):
        """Test de detect_imbalance avec déséquilibre simple droit."""
        node = AVLNode(10)
        node.set_right(AVLNode(15))
        
        # Forcer le déséquilibre
        node._balance_factor = 2
        
        result = AVLBalancing.detect_imbalance(node)
        assert result["is_imbalanced"] is True
        assert result["type"] == "simple_right"

    def test_detect_imbalance_double_left_right(self):
        """Test de detect_imbalance avec déséquilibre double gauche-droite."""
        node = AVLNode(10)
        left = AVLNode(5)
        left_right = AVLNode(7)
        
        node.set_left(left)
        left.set_right(left_right)
        
        # Forcer le déséquilibre
        node._balance_factor = -2
        left._balance_factor = 1
        
        result = AVLBalancing.detect_imbalance(node)
        assert result["is_imbalanced"] is True
        assert result["type"] == "double_left_right"

    def test_detect_imbalance_double_right_left(self):
        """Test de detect_imbalance avec déséquilibre double droite-gauche."""
        node = AVLNode(10)
        right = AVLNode(15)
        right_left = AVLNode(12)
        
        node.set_right(right)
        right.set_left(right_left)
        
        # Forcer le déséquilibre
        node._balance_factor = 2
        right._balance_factor = -1
        
        result = AVLBalancing.detect_imbalance(node)
        assert result["is_imbalanced"] is True
        assert result["type"] == "double_right_left"

    def test_detect_global_imbalance_none(self):
        """Test de detect_global_imbalance avec une racine None."""
        result = AVLBalancing.detect_global_imbalance(None)
        assert result == []

    def test_detect_global_imbalance_balanced_tree(self):
        """Test de detect_global_imbalance avec un arbre équilibré."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.detect_global_imbalance(root)
        assert result == []

    def test_detect_global_imbalance_unbalanced_tree(self):
        """Test de detect_global_imbalance avec un arbre déséquilibré."""
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.detect_global_imbalance(root)
        assert len(result) > 0
        assert result[0]["is_imbalanced"] is True

    def test_analyze_stability_none(self):
        """Test de analyze_stability avec une racine None."""
        result = AVLBalancing.analyze_stability(None)
        assert result["is_stable"] is True
        assert result["stability_score"] == 1.0
        assert result["risk_level"] == "low"

    def test_analyze_stability_stable_tree(self):
        """Test de analyze_stability avec un arbre stable."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.analyze_stability(root)
        assert result["is_stable"] is True
        assert result["risk_level"] == "low"

    def test_analyze_stability_unstable_tree(self):
        """Test de analyze_stability avec un arbre instable."""
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.analyze_stability(root)
        assert result["is_stable"] is False
        assert result["risk_level"] in ["medium", "high"]

    def test_apply_simple_correction_none(self):
        """Test de apply_simple_correction avec un nœud None."""
        result = AVLBalancing.apply_simple_correction(None)
        assert result is None

    def test_apply_simple_correction_balanced(self):
        """Test de apply_simple_correction avec un nœud équilibré."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        node.set_right(AVLNode(15))
        
        result = AVLBalancing.apply_simple_correction(node)
        assert result == node

    def test_apply_simple_correction_simple_left(self):
        """Test de apply_simple_correction avec déséquilibre simple gauche."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        
        # Forcer le déséquilibre
        node._balance_factor = -2
        
        result = AVLBalancing.apply_simple_correction(node)
        assert result is not None

    def test_apply_simple_correction_simple_right(self):
        """Test de apply_simple_correction avec déséquilibre simple droit."""
        node = AVLNode(10)
        node.set_right(AVLNode(15))
        
        # Forcer le déséquilibre
        node._balance_factor = 2
        
        result = AVLBalancing.apply_simple_correction(node)
        assert result is not None

    def test_apply_simple_correction_double_imbalance(self):
        """Test de apply_simple_correction avec déséquilibre double."""
        node = AVLNode(10)
        left = AVLNode(5)
        left_right = AVLNode(7)
        
        node.set_left(left)
        left.set_right(left_right)
        
        # Forcer le déséquilibre double
        node._balance_factor = -2
        left._balance_factor = 1
        
        with pytest.raises(CorrectionApplicationError):
            AVLBalancing.apply_simple_correction(node)

    def test_apply_double_correction_none(self):
        """Test de apply_double_correction avec un nœud None."""
        result = AVLBalancing.apply_double_correction(None)
        assert result is None

    def test_apply_double_correction_balanced(self):
        """Test de apply_double_correction avec un nœud équilibré."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        node.set_right(AVLNode(15))
        
        result = AVLBalancing.apply_double_correction(node)
        assert result == node

    def test_apply_double_correction_double_left_right(self):
        """Test de apply_double_correction avec déséquilibre double gauche-droite."""
        node = AVLNode(10)
        left = AVLNode(5)
        left_right = AVLNode(7)
        
        node.set_left(left)
        left.set_right(left_right)
        
        # Forcer le déséquilibre double
        node._balance_factor = -2
        left._balance_factor = 1
        
        result = AVLBalancing.apply_double_correction(node)
        assert result is not None

    def test_apply_double_correction_double_right_left(self):
        """Test de apply_double_correction avec déséquilibre double droite-gauche."""
        node = AVLNode(10)
        right = AVLNode(15)
        right_left = AVLNode(12)
        
        node.set_right(right)
        right.set_left(right_left)
        
        # Forcer le déséquilibre double
        node._balance_factor = 2
        right._balance_factor = -1
        
        result = AVLBalancing.apply_double_correction(node)
        assert result is not None

    def test_apply_double_correction_simple_imbalance(self):
        """Test de apply_double_correction avec déséquilibre simple."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        
        # Forcer le déséquilibre simple
        node._balance_factor = -2
        
        with pytest.raises(CorrectionApplicationError):
            AVLBalancing.apply_double_correction(node)

    def test_apply_cascade_correction_none(self):
        """Test de apply_cascade_correction avec un nœud None."""
        result = AVLBalancing.apply_cascade_correction(None)
        assert result is None

    def test_apply_cascade_correction_single_node(self):
        """Test de apply_cascade_correction avec un seul nœud."""
        node = AVLNode(10)
        result = AVLBalancing.apply_cascade_correction(node)
        assert result == node

    def test_apply_cascade_correction_multiple_nodes(self):
        """Test de apply_cascade_correction avec plusieurs nœuds."""
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.apply_cascade_correction(left_left)
        assert result is not None

    def test_validate_balance_none(self):
        """Test de validate_balance avec un nœud None."""
        result = AVLBalancing.validate_balance(None)
        assert result is True

    def test_validate_balance_valid_node(self):
        """Test de validate_balance avec un nœud valide."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        node.set_right(AVLNode(15))
        
        result = AVLBalancing.validate_balance(node)
        assert result is True

    def test_validate_balance_invalid_node(self):
        """Test de validate_balance avec un nœud invalide."""
        node = AVLNode(10)
        node.set_left(AVLNode(5))
        
        # Forcer un déséquilibre
        node._balance_factor = -2
        
        result = AVLBalancing.validate_balance(node)
        assert result is False

    def test_validate_global_balance_none(self):
        """Test de validate_global_balance avec une racine None."""
        result = AVLBalancing.validate_global_balance(None)
        assert result is True

    def test_validate_global_balance_valid_tree(self):
        """Test de validate_global_balance avec un arbre valide."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.validate_global_balance(root)
        assert result is True

    def test_validate_global_balance_invalid_tree(self):
        """Test de validate_global_balance avec un arbre invalide."""
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.validate_global_balance(root)
        assert result is False

    def test_validate_avl_properties_none(self):
        """Test de validate_avl_properties avec une racine None."""
        result = AVLBalancing.validate_avl_properties(None)
        assert result["overall_valid"] is True

    def test_validate_avl_properties_valid_tree(self):
        """Test de validate_avl_properties avec un arbre valide."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.validate_avl_properties(root)
        assert result["overall_valid"] is True

    def test_validate_avl_properties_invalid_tree(self):
        """Test de validate_avl_properties avec un arbre invalide."""
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.validate_avl_properties(root)
        assert result["overall_valid"] is False

    def test_monitor_balance_changes_none(self):
        """Test de monitor_balance_changes avec un nœud None."""
        callback_called = False
        
        def callback(data):
            nonlocal callback_called
            callback_called = True
        
        AVLBalancing.monitor_balance_changes(None, callback)
        assert callback_called is False

    def test_monitor_balance_changes_no_changes(self):
        """Test de monitor_balance_changes sans changements."""
        node = AVLNode(10)
        callback_called = False
        
        def callback(data):
            nonlocal callback_called
            callback_called = True
        
        AVLBalancing.monitor_balance_changes(node, callback)
        # Dans cette implémentation simplifiée, le callback n'est pas appelé
        # car il n'y a pas de changements détectés
        assert callback_called is False

    def test_get_balancing_stats_none(self):
        """Test de get_balancing_stats avec une racine None."""
        result = AVLBalancing.get_balancing_stats(None)
        assert result["total_nodes"] == 0
        assert result["balanced_nodes"] == 0
        assert result["stability_score"] == 1.0

    def test_get_balancing_stats_balanced_tree(self):
        """Test de get_balancing_stats avec un arbre équilibré."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.get_balancing_stats(root)
        assert result["total_nodes"] == 3
        assert result["balanced_nodes"] == 3
        assert result["stability_score"] == 1.0

    def test_get_balancing_stats_unbalanced_tree(self):
        """Test de get_balancing_stats avec un arbre déséquilibré."""
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.get_balancing_stats(root)
        assert result["total_nodes"] == 3
        assert result["balanced_nodes"] < 3
        assert result["stability_score"] < 1.0

    def test_get_balancing_history_none(self):
        """Test de get_balancing_history avec une racine None."""
        result = AVLBalancing.get_balancing_history(None)
        assert result == []

    def test_get_balancing_history_tree(self):
        """Test de get_balancing_history avec un arbre."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.get_balancing_history(root)
        assert len(result) == 3  # 3 nœuds dans l'arbre
        assert all("timestamp" in entry for entry in result)
        assert all("node_value" in entry for entry in result)

    def test_preventive_balancing_none(self):
        """Test de preventive_balancing avec une racine None."""
        result = AVLBalancing.preventive_balancing(None)
        assert result is None

    def test_preventive_balancing_stable_tree(self):
        """Test de preventive_balancing avec un arbre stable."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        result = AVLBalancing.preventive_balancing(root)
        assert result == root

    def test_preventive_balancing_unstable_tree(self):
        """Test de preventive_balancing avec un arbre instable."""
        root = AVLNode(10)
        left = AVLNode(5)
        left_left = AVLNode(3)
        
        root.set_left(left)
        left.set_left(left_left)
        
        # Forcer le déséquilibre
        root._balance_factor = -2
        root._cached_height = 2
        left._balance_factor = -1
        left._cached_height = 1
        
        result = AVLBalancing.preventive_balancing(root)
        assert result is not None

    def test_adaptive_balancing_none(self):
        """Test de adaptive_balancing avec une racine None."""
        usage_pattern = {"access_frequency": {}, "operation_types": {}}
        result = AVLBalancing.adaptive_balancing(None, usage_pattern)
        assert result is None

    def test_adaptive_balancing_stable_tree(self):
        """Test de adaptive_balancing avec un arbre stable."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        usage_pattern = {"access_frequency": {}, "operation_types": {}}
        result = AVLBalancing.adaptive_balancing(root, usage_pattern)
        assert result == root

    def test_adaptive_balancing_with_usage_pattern(self):
        """Test de adaptive_balancing avec un pattern d'usage."""
        root = AVLNode(10)
        root.set_left(AVLNode(5))
        root.set_right(AVLNode(15))
        
        usage_pattern = {
            "access_frequency": {10: 100, 5: 50, 15: 30},
            "operation_types": {"insertions": 10, "deletions": 5}
        }
        
        result = AVLBalancing.adaptive_balancing(root, usage_pattern)
        assert result is not None

    def test_error_handling_balance_node(self):
        """Test de gestion d'erreurs dans balance_node."""
        # Créer un nœud avec des propriétés invalides
        node = AVLNode(10)
        node._balance_factor = float('inf')  # Valeur invalide
        
        with pytest.raises(BalancingError):
            AVLBalancing.balance_node(node)

    def test_error_handling_detect_imbalance(self):
        """Test de gestion d'erreurs dans detect_imbalance."""
        # Créer un nœud avec des propriétés invalides
        node = AVLNode(10)
        node._balance_factor = float('inf')  # Valeur invalide
        
        with pytest.raises(ImbalanceDetectionError):
            AVLBalancing.detect_imbalance(node)

    def test_error_handling_validate_balance(self):
        """Test de gestion d'erreurs dans validate_balance."""
        # Créer un nœud avec des propriétés invalides
        node = AVLNode(10)
        node._balance_factor = float('inf')  # Valeur invalide
        
        with pytest.raises(ValidationError):
            AVLBalancing.validate_balance(node)

    def test_complex_tree_balancing(self):
        """Test d'équilibrage sur un arbre complexe."""
        # Créer un arbre complexe avec plusieurs niveaux
        root = AVLNode(50)
        
        # Sous-arbre gauche
        left = AVLNode(25)
        left_left = AVLNode(10)
        left_right = AVLNode(35)
        
        root.set_left(left)
        left.set_left(left_left)
        left.set_right(left_right)
        
        # Sous-arbre droit
        right = AVLNode(75)
        right_left = AVLNode(60)
        right_right = AVLNode(90)
        
        root.set_right(right)
        right.set_left(right_left)
        right.set_right(right_right)
        
        # Forcer des déséquilibres
        root._balance_factor = -1
        left._balance_factor = 0
        right._balance_factor = 0
        
        # Tester l'équilibrage
        result = AVLBalancing.balance_node(root)
        assert result is not None
        
        # Vérifier que l'arbre est maintenant équilibré
        assert AVLBalancing.validate_global_balance(result)

    def test_performance_large_tree(self):
        """Test de performance sur un grand arbre."""
        # Créer un arbre avec de nombreux nœuds
        root = AVLNode(100)
        
        # Ajouter des nœuds de manière séquentielle pour créer un déséquilibre
        for i in range(1, 100):
            node = AVLNode(i)
            if i < 50:
                # Ajouter à gauche pour créer un déséquilibre
                current = root
                while current.left is not None:
                    current = current.left
                current.set_left(node)
            else:
                # Ajouter à droite
                current = root
                while current.right is not None:
                    current = current.right
                current.set_right(node)
        
        # Mesurer le temps d'équilibrage
        start_time = time.time()
        result = AVLBalancing.rebalance_tree(root)
        end_time = time.time()
        
        # Vérifier que l'équilibrage a réussi
        assert result is not None
        assert AVLBalancing.validate_global_balance(result)
        
        # Vérifier que le temps d'exécution est raisonnable (moins de 1 seconde)
        assert end_time - start_time < 1.0

    def test_edge_cases(self):
        """Test des cas limites."""
        # Test avec un nœud sans enfants
        node = AVLNode(10)
        assert AVLBalancing.balance_node(node) == node
        assert AVLBalancing.validate_balance(node) is True
        
        # Test avec un nœud avec un seul enfant
        node.set_left(AVLNode(5))
        assert AVLBalancing.balance_node(node) == node
        assert AVLBalancing.validate_balance(node) is True
        
        # Test avec des valeurs extrêmes
        node._balance_factor = 0
        assert AVLBalancing.validate_balance(node) is True
        
        node._balance_factor = 1
        assert AVLBalancing.validate_balance(node) is True
        
        node._balance_factor = -1
        assert AVLBalancing.validate_balance(node) is True

    def test_statistics_accuracy(self):
        """Test de l'exactitude des statistiques."""
        # Créer un arbre avec des propriétés connues
        root = AVLNode(10)
        left = AVLNode(5)
        right = AVLNode(15)
        
        root.set_left(left)
        root.set_right(right)
        
        # Obtenir les statistiques
        stats = AVLBalancing.get_balancing_stats(root)
        
        # Vérifier l'exactitude
        assert stats["total_nodes"] == 3
        assert stats["balanced_nodes"] == 3
        assert stats["imbalanced_nodes"] == 0
        assert stats["stability_score"] == 1.0
        assert stats["max_imbalance"] == 0
        assert len(stats["balance_factors"]) == 3
        assert len(stats["heights"]) == 3

    def test_history_completeness(self):
        """Test de la complétude de l'historique."""
        # Créer un arbre
        root = AVLNode(10)
        left = AVLNode(5)
        right = AVLNode(15)
        
        root.set_left(left)
        root.set_right(right)
        
        # Obtenir l'historique
        history = AVLBalancing.get_balancing_history(root)
        
        # Vérifier la complétude
        assert len(history) == 3
        assert all("timestamp" in entry for entry in history)
        assert all("node_value" in entry for entry in history)
        assert all("balance_factor" in entry for entry in history)
        assert all("height" in entry for entry in history)
        assert all("is_balanced" in entry for entry in history)
        assert all("imbalance_type" in entry for entry in history)
        
        # Vérifier que les valeurs sont cohérentes
        node_values = [entry["node_value"] for entry in history]
        assert 10 in node_values
        assert 5 in node_values
        assert 15 in node_values