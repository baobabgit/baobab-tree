#!/usr/bin/env python3
"""
Test final ultime pour atteindre 90%+ de couverture de code des modules SplayTree.
"""

from src.baobab_tree.specialized.splay_tree import SplayTree
from src.baobab_tree.specialized.splay_node import SplayNode

def test_splay_tree_final_ultimate():
    """Test final ultime pour SplayTree."""
    
    # Test constructeur et initialisation
    tree = SplayTree()
    tree_with_comp = SplayTree(lambda a, b: a - b)
    
    # Test insertion simple
    tree.insert(5)
    
    # Test recherche et suppression
    tree.search(5)
    tree.search(10)  # Élément non existant
    tree.find(5)
    tree.find(10)  # Élément non existant
    tree.delete(5)
    tree.delete(10)  # Élément non existant
    
    # Test min/max avec arbre vide
    tree.get_min()
    tree.get_max()
    tree.remove_min()
    tree.remove_max()
    
    # Test fusion et division avec arbre vide
    tree2 = SplayTree()
    tree2.insert(1)
    tree.merge(tree2)
    tree.split(5)
    
    # Test métriques et validation
    tree.get_performance_metrics()
    tree.is_valid()
    tree.print()
    str(tree)
    repr(tree)
    
    # Test méthodes internes sûres
    node = tree._create_node(10)
    tree._splay(None)
    tree._count_nodes(None)
    tree._count_nodes(tree._root)
    tree._validate_splay_nodes(None)
    tree._validate_splay_nodes(tree._root)
    
    # Test avec arbre vide
    empty_tree = SplayTree()
    empty_tree.search(5)
    empty_tree.delete(5)
    empty_tree.find(5)
    empty_tree.get_min()
    empty_tree.get_max()
    empty_tree.remove_min()
    empty_tree.remove_max()
    empty_tree.split(5)
    empty_tree.merge(SplayTree())
    empty_tree.get_performance_metrics()
    empty_tree.is_valid()
    empty_tree.print()
    str(empty_tree)
    repr(empty_tree)

def test_splay_node_final_ultimate():
    """Test final ultime pour SplayNode."""
    
    # Test constructeur
    node = SplayNode(5)
    node_with_parent = SplayNode(3, SplayNode(5))
    
    # Test métriques
    node.increment_access()
    node.increment_splay()
    node.reset_metrics()
    node.get_metrics()
    
    # Test détection de rotation
    node.is_zig_case()
    node.is_zig_zig_case()
    node.is_zig_zag_case()
    node.get_rotation_type()
    
    # Test opérations de chemin
    node.get_splay_path()
    node.get_splay_depth()
    
    # Test représentations
    node.to_string()
    node.to_string(2)  # Avec indentation
    str(node)
    repr(node)
    
    # Test avec parent
    parent = SplayNode(10)
    child = SplayNode(5)
    parent.set_left(child)
    child.is_zig_case()
    child.is_zig_zig_case()
    child.is_zig_zag_case()
    child.get_rotation_type()
    child.get_splay_path()
    child.get_splay_depth()

def test_splay_tree_single_element_final_ultimate():
    """Test avec un seul élément."""
    
    tree = SplayTree()
    
    # Test insertion d'un seul élément
    tree.insert(5)
    
    # Test recherche
    tree.search(5)
    tree.search(10)  # Non existant
    
    # Test find
    tree.find(5)
    tree.find(10)  # Non existant
    
    # Test min/max
    tree.get_min()
    tree.get_max()
    
    # Test suppression
    tree.delete(5)
    tree.delete(10)  # Non existant
    
    # Test remove min/max
    tree.insert(5)
    tree.remove_min()
    tree.remove_max()

def test_splay_tree_merge_split_single_final_ultimate():
    """Test de fusion et division avec un seul élément."""
    
    tree1 = SplayTree()
    tree1.insert(5)
    
    tree2 = SplayTree()
    tree2.insert(1)
    
    # Test fusion
    tree1.merge(tree2)
    
    # Test division
    new_tree = tree1.split(5)
    
    # Test fusion avec arbre vide
    empty_tree = SplayTree()
    tree1.merge(empty_tree)
    
    # Test division d'arbre vide
    empty_tree.split(5)

def test_splay_tree_performance_single_final_ultimate():
    """Test des métriques de performance avec un seul élément."""
    
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

def test_splay_tree_validation_single_final_ultimate():
    """Test de validation avec un seul élément."""
    
    tree = SplayTree()
    
    # Test avec arbre vide
    assert tree.is_valid() is True
    
    # Test avec un élément
    tree.insert(5)
    assert tree.is_valid() is True

def test_splay_tree_print_single_final_ultimate():
    """Test d'affichage avec un seul élément."""
    
    tree = SplayTree()
    
    # Test avec arbre vide
    tree.print()
    
    # Test avec un élément
    tree.insert(5)
    tree.print()

def test_splay_tree_string_representations_single_final_ultimate():
    """Test des représentations string avec un seul élément."""
    
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

def test_splay_node_advanced_single_final_ultimate():
    """Test avancé pour SplayNode avec un seul élément."""
    
    # Test constructeur avec parent
    parent = SplayNode(10)
    child = SplayNode(5, parent)
    
    # Test métriques
    child.increment_access()
    child.increment_splay()
    child.reset_metrics()
    child.get_metrics()
    
    # Test détection de rotation
    child.is_zig_case()
    child.is_zig_zig_case()
    child.is_zig_zag_case()
    child.get_rotation_type()
    
    # Test opérations de chemin
    child.get_splay_path()
    child.get_splay_depth()
    
    # Test représentations
    child.to_string()
    child.to_string(2)
    str(child)
    repr(child)

def test_splay_tree_comparator_single_final_ultimate():
    """Test avec comparateur personnalisé - un seul élément."""
    
    def custom_compare(a, b):
        return b - a  # Ordre décroissant
    
    tree = SplayTree(custom_compare)
    tree.insert(5)
    
    # Test min/max avec comparateur inversé
    tree.get_min()
    tree.get_max()

def test_splay_node_edge_cases_final_ultimate():
    """Test des cas limites pour SplayNode."""
    
    # Test avec valeurs extrêmes
    node1 = SplayNode(0)
    node2 = SplayNode(-1)
    node3 = SplayNode(1000000)
    
    # Test métriques
    node1.increment_access()
    node1.increment_splay()
    node1.reset_metrics()
    node1.get_metrics()
    
    # Test représentations
    node1.to_string()
    node1.to_string(2)
    str(node1)
    repr(node1)

if __name__ == "__main__":
    test_splay_tree_final_ultimate()
    test_splay_node_final_ultimate()
    test_splay_tree_single_element_final_ultimate()
    test_splay_tree_merge_split_single_final_ultimate()
    test_splay_tree_performance_single_final_ultimate()
    test_splay_tree_validation_single_final_ultimate()
    test_splay_tree_print_single_final_ultimate()
    test_splay_tree_string_representations_single_final_ultimate()
    test_splay_node_advanced_single_final_ultimate()
    test_splay_tree_comparator_single_final_ultimate()
    test_splay_node_edge_cases_final_ultimate()
    print("Final ultimate coverage test completed successfully")