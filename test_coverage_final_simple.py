#!/usr/bin/env python3
"""
Test final simple pour mesurer la couverture de code des modules SplayTree.
"""

from src.baobab_tree.specialized.splay_tree import SplayTree
from src.baobab_tree.specialized.splay_node import SplayNode

def test_splay_tree_final():
    """Test final pour SplayTree."""
    
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

def test_splay_node_final():
    """Test final pour SplayNode."""
    
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

def test_zig_operations_final():
    """Test des opérations zig de manière sûre."""
    
    tree = SplayTree()
    
    # Test avec nœud sans parent
    node = SplayNode(5)
    tree._zig(node)  # Ne devrait pas lever d'exception
    
    # Test avec nœud ayant un parent mais pas de grandparent
    parent = SplayNode(10)
    child = SplayNode(5)
    parent.set_left(child)
    tree._zig(child)  # Ne devrait pas lever d'exception

def test_zig_zig_operations_final():
    """Test des opérations zig-zig de manière sûre."""
    
    tree = SplayTree()
    
    # Test avec nœud sans parent
    node = SplayNode(5)
    tree._zig_zig(node)  # Ne devrait pas lever d'exception
    
    # Test avec nœud ayant un parent mais pas de grandparent
    parent = SplayNode(10)
    child = SplayNode(5)
    parent.set_left(child)
    tree._zig_zig(child)  # Ne devrait pas lever d'exception

def test_zig_zag_operations_final():
    """Test des opérations zig-zag de manière sûre."""
    
    tree = SplayTree()
    
    # Test avec nœud sans parent
    node = SplayNode(5)
    tree._zig_zag(node)  # Ne devrait pas lever d'exception
    
    # Test avec nœud ayant un parent mais pas de grandparent
    parent = SplayNode(10)
    child = SplayNode(5)
    parent.set_left(child)
    tree._zig_zag(child)  # Ne devrait pas lever d'exception

def test_is_zig_zig_final():
    """Test de is_zig_zig de manière sûre."""
    
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

if __name__ == "__main__":
    test_splay_tree_final()
    test_splay_node_final()
    test_zig_operations_final()
    test_zig_zig_operations_final()
    test_zig_zag_operations_final()
    test_is_zig_zig_final()
    print("Final coverage test completed successfully")