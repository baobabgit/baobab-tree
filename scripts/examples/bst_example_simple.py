#!/usr/bin/env python3
"""
Exemple d'utilisation simple de la classe BinarySearchTree.

Ce script démontre les principales fonctionnalités de la classe
BinarySearchTree avec des exemples pratiques.
"""

import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Imports directs des modules
from binary_tree_node import BinaryTreeNode
from exceptions import BSTError, ValueNotFoundError


class BinarySearchTree:
    """
    Version simplifiée de BinarySearchTree pour l'exemple.
    """
    
    def __init__(self):
        self._root = None
        self._size = 0
    
    def insert(self, value):
        """Insère une valeur dans l'arbre."""
        if self._root is None:
            self._root = BinaryTreeNode(value)
            self._size = 1
            return True
        
        return self._insert_recursive(self._root, value)
    
    def _insert_recursive(self, node, value):
        """Insère récursivement une valeur."""
        if value < node.value:
            if node.left is None:
                new_node = BinaryTreeNode(value)
                node.set_left(new_node)
                self._size += 1
                return True
            else:
                return self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                new_node = BinaryTreeNode(value)
                node.set_right(new_node)
                self._size += 1
                return True
            else:
                return self._insert_recursive(node.right, value)
        else:
            return False  # Valeur déjà présente
    
    def contains(self, value):
        """Vérifie si une valeur existe dans l'arbre."""
        return self._search_recursive(self._root, value) is not None
    
    def _search_recursive(self, node, value):
        """Recherche récursivement une valeur."""
        if node is None:
            return None
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        elif value > node.value:
            return self._search_recursive(node.right, value)
        else:
            return node
    
    def inorder_traversal(self):
        """Effectue le parcours infixe de l'arbre."""
        if self._root is None:
            return []
        return self._inorder_recursive(self._root)
    
    def _inorder_recursive(self, node):
        """Parcours infixe récursif."""
        if node is None:
            return []
        
        result = []
        result.extend(self._inorder_recursive(node.left))
        result.append(node.value)
        result.extend(self._inorder_recursive(node.right))
        return result
    
    def get_min(self):
        """Trouve la valeur minimale."""
        if self._root is None:
            return None
        
        current = self._root
        while current.left is not None:
            current = current.left
        return current.value
    
    def get_max(self):
        """Trouve la valeur maximale."""
        if self._root is None:
            return None
        
        current = self._root
        while current.right is not None:
            current = current.right
        return current.value
    
    def size(self):
        """Retourne la taille de l'arbre."""
        return self._size
    
    def is_empty(self):
        """Vérifie si l'arbre est vide."""
        return self._root is None


def main():
    """Fonction principale démontrant l'utilisation du BST."""
    print("=== Exemple d'utilisation de BinarySearchTree ===\n")
    
    # 1. Création d'un BST
    print("1. Création d'un BST vide")
    bst = BinarySearchTree()
    print(f"   BST vide : taille={bst.size()}, vide={bst.is_empty()}")
    print()
    
    # 2. Insertion de valeurs
    print("2. Insertion de valeurs")
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    print(f"   Insertion des valeurs : {values}")
    
    for value in values:
        success = bst.insert(value)
        print(f"   Insertion de {value} : {'✓' if success else '✗ (déjà présent)'}")
    
    print(f"   Taille finale : {bst.size()}")
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
    inorder = bst.inorder_traversal()
    print(f"   Parcours infixe (trié) : {inorder}")
    print()
    
    # 5. Valeurs min/max
    print("5. Valeurs extrêmes")
    print(f"   Valeur minimale : {bst.get_min()}")
    print(f"   Valeur maximale : {bst.get_max()}")
    print()
    
    # 6. Test avec des chaînes
    print("6. Test avec des chaînes")
    string_bst = BinarySearchTree()
    words = ["banana", "apple", "cherry", "date", "elderberry"]
    for word in words:
        string_bst.insert(word)
    
    print(f"   Mots insérés : {words}")
    print(f"   Parcours trié : {string_bst.inorder_traversal()}")
    print()
    
    print("=== Fin de l'exemple ===")


if __name__ == "__main__":
    main()