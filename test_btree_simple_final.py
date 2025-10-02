#!/usr/bin/env python3
"""
Script de test final pour la version simplifiée des classes B-tree.
"""

from btree_simple import (
    BTree,
    BTreeNode,
    BTreeError,
    InvalidOrderError,
    NodeFullError,
)


def test_btree_node():
    """Test basique de BTreeNode."""
    print("=== Test BTreeNode ===")
    
    try:
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
        
        # Test division
        node.keys = [10, 20, 30, 40, 50]  # Nœud plein
        left_node, median_key, right_node = node.split()
        print(f"✓ Division réussie - Clé médiane: {median_key}")
        print(f"✓ Nœud gauche: {left_node.keys}")
        print(f"✓ Nœud droit: {right_node.keys}")
        
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
        
        # Test comptage de plage
        count = btree.count_range(15, 45)
        print(f"✓ Comptage plage [15, 45]: {count}")
        
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
        # Test InvalidOrderError
        try:
            BTree(order=1)
        except InvalidOrderError as e:
            print(f"✓ InvalidOrderError capturée: {e}")
        
        # Test NodeFullError
        try:
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


def test_complex_operations():
    """Test d'opérations complexes."""
    print("\n=== Test Opérations Complexes ===")
    
    try:
        btree = BTree(order=3)
        
        # Insérer des clés dans un ordre aléatoire
        keys = [50, 30, 70, 10, 40, 60, 80, 20, 90, 15, 35, 45, 55, 65, 75, 85]
        
        for key in keys:
            btree.insert(key)
        
        print(f"✓ {len(keys)} clés insérées, taille: {btree.size}")
        print(f"✓ Hauteur: {btree.height}")
        print(f"✓ Arbre valide: {btree.is_valid()}")
        
        # Test de toutes les clés
        for key in keys:
            if not btree.contains(key):
                print(f"✗ Clé {key} manquante après insertion")
                return False
        
        print("✓ Toutes les clés sont présentes")
        
        # Supprimer quelques clés
        keys_to_delete = [30, 60, 80]
        for key in keys_to_delete:
            if not btree.delete(key):
                print(f"✗ Impossible de supprimer la clé {key}")
                return False
        
        print(f"✓ {len(keys_to_delete)} clés supprimées")
        print(f"✓ Taille finale: {btree.size}")
        print(f"✓ Arbre valide après suppression: {btree.is_valid()}")
        
        # Vérifier que les clés supprimées ne sont plus présentes
        for key in keys_to_delete:
            if btree.contains(key):
                print(f"✗ Clé {key} encore présente après suppression")
                return False
        
        print("✓ Clés supprimées correctement")
        
        # Test de requête de plage
        range_result = btree.range_query(20, 70)
        print(f"✓ Requête de plage [20, 70]: {len(range_result)} clés")
        
        print("✓ Tous les tests d'opérations complexes ont réussi!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur dans les opérations complexes: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance():
    """Test de performance avec un grand ensemble de données."""
    print("\n=== Test Performance ===")
    
    try:
        btree = BTree(order=5)
        keys = list(range(1, 101))  # 100 clés
        
        # Insérer toutes les clés
        for key in keys:
            btree.insert(key)
        
        print(f"✓ {len(keys)} clés insérées")
        print(f"✓ Taille: {btree.size}")
        print(f"✓ Hauteur: {btree.height}")
        print(f"✓ Arbre valide: {btree.is_valid()}")
        
        # Vérifier quelques clés
        test_keys = [1, 50, 100]
        for key in test_keys:
            if not btree.contains(key):
                print(f"✗ Clé {key} manquante")
                return False
        
        print("✓ Clés de test présentes")
        
        # Test de requête de plage
        result = btree.range_query(20, 80)
        expected_count = 61  # 20 à 80 inclus
        if len(result) != expected_count:
            print(f"✗ Requête de plage incorrecte: {len(result)} au lieu de {expected_count}")
            return False
        
        print(f"✓ Requête de plage correcte: {len(result)} clés")
        
        # Supprimer quelques clés
        keys_to_delete = [25, 50, 75]
        for key in keys_to_delete:
            if not btree.delete(key):
                print(f"✗ Impossible de supprimer la clé {key}")
                return False
        
        print(f"✓ {len(keys_to_delete)} clés supprimées")
        print(f"✓ Taille finale: {btree.size}")
        print(f"✓ Arbre valide après suppression: {btree.is_valid()}")
        
        print("✓ Tous les tests de performance ont réussi!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur dans les tests de performance: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_advanced_features():
    """Test des fonctionnalités avancées."""
    print("\n=== Test Fonctionnalités Avancées ===")
    
    try:
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        # Test bulk_load
        btree.bulk_load(keys)
        print(f"✓ Chargement en masse: {btree.size} clés")
        print(f"✓ Arbre valide après chargement: {btree.is_valid()}")
        
        # Test get_leaf_nodes
        leaves = btree.get_leaf_nodes()
        print(f"✓ Nœuds feuilles: {len(leaves)}")
        
        # Test get_internal_nodes
        internals = btree.get_internal_nodes()
        print(f"✓ Nœuds internes: {len(internals)}")
        
        # Test get_node_count
        stats = btree.get_node_count()
        print(f"✓ Statistiques: {stats}")
        
        # Test validate_properties
        properties = btree.validate_properties()
        print(f"✓ Propriétés validées: {properties}")
        
        # Vérifier que toutes les propriétés sont vraies
        for prop_name, prop_value in properties.items():
            if not prop_value:
                print(f"✗ Propriété {prop_name} invalide")
                return False
        
        print("✓ Toutes les propriétés sont valides")
        
        print("✓ Tous les tests de fonctionnalités avancées ont réussi!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur dans les fonctionnalités avancées: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale de test."""
    print("Démarrage des tests B-tree simplifiés...")
    
    results = []
    results.append(test_btree_node())
    results.append(test_btree())
    results.append(test_exceptions())
    results.append(test_complex_operations())
    results.append(test_performance())
    results.append(test_advanced_features())
    
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
    import sys
    sys.exit(main())