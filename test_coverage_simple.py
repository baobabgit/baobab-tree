#!/usr/bin/env python3
"""
Test simple pour mesurer la couverture de code des modules SplayTree.
"""

from src.baobab_tree.specialized.splay_tree import SplayTree
from src.baobab_tree.specialized.splay_node import SplayNode

def test_splay_tree_coverage():
    """Test de couverture de code pour SplayTree."""
    
    # Test constructeur
    tree = SplayTree()
    tree_with_comp = SplayTree(lambda a, b: a - b)
    
    # Test insertion simple
    tree.insert(5)
    
    # Test méthodes de base
    tree.get_performance_metrics()
    tree.is_valid()
    tree.print()
    str(tree)
    repr(tree)
    
    # Test méthodes avec arbre vide
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
    
    # Test méthodes internes
    node = tree._create_node(10)
    tree._splay(None)
    tree._zig(node)
    tree._zig_zig(node)
    tree._zig_zag(node)
    tree._is_zig_zig(node)
    tree._count_nodes(None)
    tree._count_nodes(tree._root)
    tree._validate_splay_nodes(None)
    tree._validate_splay_nodes(tree._root)

def test_splay_node_coverage():
    """Test de couverture de code pour SplayNode."""
    
    # Test constructeur
    node = SplayNode(5)
    
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
    str(node)
    repr(node)

if __name__ == "__main__":
    test_splay_tree_coverage()
    test_splay_node_coverage()
    print("Coverage test completed successfully")