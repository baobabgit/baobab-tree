#!/usr/bin/env python3
"""
Exemple d'utilisation de la classe AVLNode.

Ce script démontre toutes les fonctionnalités de la classe AVLNode,
incluant la création, la manipulation, la validation, la sérialisation
et la visualisation des nœuds AVL.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.avl_node import AVLNode


def main():
    """Fonction principale démontrant l'utilisation d'AVLNode."""
    print("=== Exemple d'utilisation de la classe AVLNode ===\n")

    # 1. Création d'un nœud AVL simple
    print("1. Création d'un nœud AVL simple")
    node = AVLNode(50)
    print(f"Nœud créé: {node}")
    print(f"Facteur d'équilibre: {node.get_balance_factor()}")
    print(f"Hauteur: {node.get_height()}")
    print(f"Est équilibré: {node.is_balanced()}")
    print(f"Représentation compacte: {node.to_compact_string()}")
    print()

    # 2. Ajout d'enfants et mise à jour automatique
    print("2. Ajout d'enfants et mise à jour automatique")
    left_child = AVLNode(30)
    right_child = AVLNode(70)
    
    node.set_left(left_child)
    print(f"Après ajout de l'enfant gauche: {node}")
    print(f"Facteur d'équilibre: {node.get_balance_factor()}")
    print(f"Hauteur gauche: {node.get_left_height()}")
    
    node.set_right(right_child)
    print(f"Après ajout de l'enfant droit: {node}")
    print(f"Facteur d'équilibre: {node.get_balance_factor()}")
    print(f"Hauteur droite: {node.get_right_height()}")
    print()

    # 3. Validation des propriétés AVL
    print("3. Validation des propriétés AVL")
    print(f"Est valide AVL: {node.is_avl_valid()}")
    print(f"Validation des hauteurs: {node.validate_heights()}")
    print(f"Validation du facteur d'équilibre: {node.validate_balance_factor()}")
    print()

    # 4. Informations détaillées du nœud
    print("4. Informations détaillées du nœud")
    info = node.get_node_info()
    print("Informations du nœud:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()

    # 5. Diagnostic du nœud
    print("5. Diagnostic du nœud")
    diagnosis = node.diagnose()
    print(f"Diagnostic valide: {diagnosis['is_valid']}")
    print(f"Problèmes détectés: {diagnosis['issues']}")
    print(f"Avertissements: {diagnosis['warnings']}")
    print(f"Structure: {diagnosis['structure']}")
    print()

    # 6. Création d'un arbre plus complexe
    print("6. Création d'un arbre plus complexe")
    root = AVLNode(50)
    left = AVLNode(30)
    right = AVLNode(70)
    left_left = AVLNode(20)
    left_right = AVLNode(40)
    right_left = AVLNode(60)
    right_right = AVLNode(80)
    
    # Construction de l'arbre
    root.set_left(left)
    root.set_right(right)
    left.set_left(left_left)
    left.set_right(left_right)
    right.set_left(right_left)
    right.set_right(right_right)
    
    print("Arbre construit avec 7 nœuds")
    print(f"Racine: {root}")
    print(f"Est valide AVL: {root.is_avl_valid()}")
    print()

    # 7. Visualisation de l'arbre
    print("7. Visualisation de l'arbre")
    print("Structure complète:")
    print(root.to_string())
    print()

    # 8. Copie de l'arbre
    print("8. Copie de l'arbre")
    copy_root = AVLNode.from_copy(root)
    print(f"Copie créée: {copy_root}")
    print(f"Copie indépendante: {copy_root is not root}")
    print(f"Copie valide AVL: {copy_root.is_avl_valid()}")
    print()

    # 9. Comparaison de nœuds
    print("9. Comparaison de nœuds")
    comparison = root.compare_with(copy_root)
    print("Comparaison racine vs copie:")
    for key, value in comparison.items():
        print(f"  {key}: {value}")
    print()

    # 10. Sérialisation et désérialisation
    print("10. Sérialisation et désérialisation")
    serialized_data = root.to_dict()
    print("Données sérialisées:")
    print(f"  Valeur racine: {serialized_data['value']}")
    print(f"  Facteur d'équilibre: {serialized_data['balance_factor']}")
    print(f"  Hauteur: {serialized_data['height']}")
    print(f"  Enfant gauche: {serialized_data['left']['value']}")
    print(f"  Enfant droit: {serialized_data['right']['value']}")
    
    # Désérialisation
    restored_root = AVLNode.from_dict(serialized_data)
    print(f"Nœud restauré: {restored_root}")
    print(f"Restauré valide AVL: {restored_root.is_avl_valid()}")
    print()

    # 11. Test avec nœud déséquilibré (pour démonstration)
    print("11. Test avec nœud déséquilibré")
    unbalanced_node = AVLNode(50)
    unbalanced_node._balance_factor = 2  # Facteur invalide
    
    print(f"Nœud déséquilibré: {unbalanced_node}")
    print(f"Est équilibré: {unbalanced_node.is_balanced()}")
    print(f"Est valide AVL: {unbalanced_node.is_avl_valid()}")
    
    diagnosis_unbalanced = unbalanced_node.diagnose()
    print(f"Diagnostic valide: {diagnosis_unbalanced['is_valid']}")
    print(f"Problèmes: {diagnosis_unbalanced['issues']}")
    print(f"Avertissements: {diagnosis_unbalanced['warnings']}")
    print(f"Recommandations: {diagnosis_unbalanced['recommendations']}")
    print()

    print("=== Fin de l'exemple ===")


if __name__ == "__main__":
    main()