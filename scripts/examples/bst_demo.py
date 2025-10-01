#!/usr/bin/env python3
"""
Démonstration de l'utilisation de BinarySearchTree.

Ce script montre comment utiliser la classe BinarySearchTree
en important depuis le package principal.
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Importer depuis le package principal
from binary_search_tree import BinarySearchTree


def main():
    """Fonction principale de démonstration."""
    print("=== Démonstration de BinarySearchTree ===\n")
    
    # 1. Création d'un BST
    print("1. Création d'un BST vide")
    bst = BinarySearchTree()
    print(f"   BST vide : {bst}")
    print(f"   Taille : {len(bst)}")
    print(f"   Est vide : {bst.is_empty()}")
    print()
    
    # 2. Insertion de valeurs
    print("2. Insertion de valeurs")
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    print(f"   Insertion des valeurs : {values}")
    
    for value in values:
        success = bst.insert(value)
        print(f"   Insertion de {value} : {'✓' if success else '✗ (déjà présent)'}")
    
    print(f"   Taille finale : {len(bst)}")
    print(f"   Hauteur : {bst.get_height()}")
    print()
    
    # 3. Recherche de valeurs
    print("3. Recherche de valeurs")
    search_values = [50, 25, 100, 30]
    for value in search_values:
        found = bst.contains(value)
        print(f"   {value} : {'✓ trouvé' if found else '✗ non trouvé'}")
    print()
    
    # 4. Parcours de l'arbre
    print("4. Parcours de l'arbre")
    print(f"   Parcours préfixe : {bst.preorder_traversal()}")
    print(f"   Parcours infixe  : {bst.inorder_traversal()}")
    print(f"   Parcours postfixe: {bst.postorder_traversal()}")
    print(f"   Parcours par niveaux: {bst.level_order_traversal()}")
    print()
    
    # 5. Valeurs min/max
    print("5. Valeurs extrêmes")
    print(f"   Valeur minimale : {bst.get_min()}")
    print(f"   Valeur maximale : {bst.get_max()}")
    print()
    
    # 6. Validation et équilibre
    print("6. Validation et équilibre")
    print(f"   Arbre valide : {'✓' if bst.is_valid() else '✗'}")
    print(f"   Arbre équilibré : {'✓' if bst.is_balanced() else '✗'}")
    print(f"   Facteur d'équilibre : {bst.get_balance_factor()}")
    print()
    
    # 7. Recherche de successeur/prédécesseur
    print("7. Successeur et prédécesseur")
    test_values = [20, 30, 50, 70, 80]
    for value in test_values:
        try:
            successor = bst.find_successor(value)
            predecessor = bst.find_predecessor(value)
            print(f"   {value} : prédécesseur={predecessor}, successeur={successor}")
        except Exception as e:
            print(f"   {value} : erreur - {e}")
    print()
    
    # 8. Recherche de plancher/plafond
    print("8. Plancher et plafond")
    test_values = [15, 25, 35, 55, 75, 90]
    for value in test_values:
        floor = bst.find_floor(value)
        ceiling = bst.find_ceiling(value)
        print(f"   {value} : plancher={floor}, plafond={ceiling}")
    print()
    
    # 9. Requêtes de plage
    print("9. Requêtes de plage")
    ranges = [(20, 40), (50, 70), (10, 30), (80, 100)]
    for min_val, max_val in ranges:
        range_values = bst.range_query(min_val, max_val)
        count = bst.count_range(min_val, max_val)
        print(f"   Plage [{min_val}, {max_val}] : {len(range_values)} valeurs = {sorted(range_values)}")
    print()
    
    # 10. Itérateurs
    print("10. Utilisation des itérateurs")
    print("    Parcours infixe avec itérateur :")
    for i, value in enumerate(bst.inorder_iter()):
        if i < 5:  # Afficher seulement les 5 premières valeurs
            print(f"      {value}")
        elif i == 5:
            print("      ...")
            break
    print()
    
    # 11. Suppression de valeurs
    print("11. Suppression de valeurs")
    to_delete = [20, 50, 70, 100]
    for value in to_delete:
        success = bst.delete(value)
        print(f"   Suppression de {value} : {'✓' if success else '✗ (non trouvé)'}")
    
    print(f"   Taille après suppression : {len(bst)}")
    print(f"   Parcours infixe après suppression : {bst.inorder_traversal()}")
    print()
    
    # 12. Test avec comparateur personnalisé
    print("12. Test avec comparateur personnalisé")
    
    def reverse_comparator(a: int, b: int) -> int:
        """Comparateur qui inverse l'ordre."""
        if a > b:
            return -1
        elif a == b:
            return 0
        else:
            return 1
    
    reverse_bst = BinarySearchTree(reverse_comparator)
    reverse_values = [50, 30, 70, 20, 40]
    for value in reverse_values:
        reverse_bst.insert(value)
    
    print(f"   BST avec comparateur inversé : {reverse_bst.inorder_traversal()}")
    print(f"   Valeur min (max avec comparateur inversé) : {reverse_bst.get_min()}")
    print(f"   Valeur max (min avec comparateur inversé) : {reverse_bst.get_max()}")
    print()
    
    print("=== Fin de la démonstration ===")


if __name__ == "__main__":
    main()