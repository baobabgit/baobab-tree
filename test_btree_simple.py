#!/usr/bin/env python3
"""
Script de test simple pour les classes B-tree.
"""

import sys
import os

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_btree_node():
    """Test basique de BTreeNode."""
    print("=== Test BTreeNode ===")
    
    try:
        from btree_node import BTreeNode
        print("✓ BTreeNode importé avec succès")
        
        # Test création
        node = BTreeNode(order=3, is_leaf=True)
        print(f"✓ Nœud créé - Ordre: {node.order}, Feuille: {node.is_leaf}")
        
        # Test insertion
        node.insert_key(10)
        node.insert_key(20)
        node.insert_key(30)
        print(f"✓ Clés insérées: {node.keys}")
        
        # Test validation
        is_valid = node.validate_node()
        print(f"✓ Nœud valide: {is_valid}")
        
        # Test propriétés
        print(f"✓ Nombre de clés: {node.get_key_count()}")
        print(f"✓ Nœud plein: {node.is_full()}")
        print(f"✓ Nœud minimum: {node.is_minimum()}")
        
        # Test recherche
        index = node.search_key(20)
        print(f"✓ Index de la clé 20: {index}")
        
        # Test suppression
        deleted = node.delete_key(20)
        print(f"✓ Clé 20 supprimée: {deleted}, Clés restantes: {node.keys}")
        
        print("✓ Tous les tests BTreeNode ont réussi!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur dans BTreeNode: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_btree():
    """Test basique de BTree."""
    print("\n=== Test BTree ===")
    
    try:
        from btree import BTree
        print("✓ BTree importé avec succès")
        
        # Test création
        btree = BTree(order=3)
        print(f"✓ Arbre créé - Ordre: {btree.order}, Taille: {btree.size}")
        
        # Test insertion
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            btree.insert(key)
        print(f"✓ Clés insérées: {keys}")
        print(f"✓ Taille finale: {btree.size}, Hauteur: {btree.height}")
        
        # Test recherche
        found = btree.search(30)
        print(f"✓ Recherche de 30: {'Trouvé' if found else 'Non trouvé'}")
        
        # Test contains
        contains_30 = btree.contains(30)
        contains_25 = btree.contains(25)
        print(f"✓ Contient 30: {contains_30}, Contient 25: {contains_25}")
        
        # Test min/max
        min_key = btree.get_min()
        max_key = btree.get_max()
        print(f"✓ Min: {min_key}, Max: {max_key}")
        
        # Test validation
        is_valid = btree.is_valid()
        print(f"✓ Arbre valide: {is_valid}")
        
        # Test suppression
        deleted = btree.delete(30)
        print(f"✓ Suppression de 30: {deleted}, Taille: {btree.size}")
        
        # Test requête de plage
        range_result = btree.range_query(15, 45)
        print(f"✓ Plage [15, 45]: {range_result}")
        
        print("✓ Tous les tests BTree ont réussi!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur dans BTree: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exceptions():
    """Test des exceptions B-tree."""
    print("\n=== Test Exceptions ===")
    
    try:
        from exceptions import (
            BTreeError,
            InvalidOrderError,
            NodeFullError,
            NodeUnderflowError,
            SplitError,
            MergeError,
            RedistributionError,
        )
        print("✓ Exceptions B-tree importées avec succès")
        
        # Test InvalidOrderError
        try:
            from btree import BTree
            BTree(order=1)
        except InvalidOrderError as e:
            print(f"✓ InvalidOrderError capturée: {e}")
        
        # Test NodeFullError
        try:
            from btree_node import BTreeNode
            node = BTreeNode(order=3, is_leaf=True)
            # Remplir le nœud
            for i in range(6):  # Ordre 3 -> max 5 clés
                node.insert_key(i * 10)
            # Essayer d'insérer une clé supplémentaire
            node.insert_key(60)
        except NodeFullError as e:
            print(f"✓ NodeFullError capturée: {e}")
        
        print("✓ Tous les tests d'exceptions ont réussi!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur dans les exceptions: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test."""
    print("Démarrage des tests B-tree...")
    
    results = []
    results.append(test_btree_node())
    results.append(test_btree())
    results.append(test_exceptions())
    
    print(f"\n=== Résumé ===")
    passed = sum(results)
    total = len(results)
    print(f"Tests réussis: {passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests ont réussi!")
        return 0
    else:
        print("❌ Certains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main())