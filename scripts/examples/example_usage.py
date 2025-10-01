#!/usr/bin/env python3
"""
Exemple d'utilisation de la librairie d'arbres - TreeNode et BinaryTreeNode.

Ce script démontre l'utilisation des classes TreeNode et BinaryTreeNode
implémentées dans la librairie d'arbres.
"""

from src import BinaryTreeNode, TreeNode


class ExampleTreeNode(TreeNode):
    """Exemple d'implémentation concrète de TreeNode pour la démonstration."""

    def is_leaf(self) -> bool:
        """Vérifie si le nœud est une feuille."""
        return len(self._children) == 0

    def is_root(self) -> bool:
        """Vérifie si le nœud est la racine."""
        return self._parent is None

    def get_height(self) -> int:
        """Calcule la hauteur du nœud."""
        if self.is_leaf():
            return 0

        max_child_height = -1
        for child in self._children:
            child_height = child.get_height()
            max_child_height = max(max_child_height, child_height)

        return 1 + max_child_height

    def get_depth(self) -> int:
        """Calcule la profondeur du nœud."""
        if self.is_root():
            return 0

        return 1 + self._parent.get_depth()

    def validate(self) -> bool:
        """Valide les propriétés du nœud."""
        # Vérifier que tous les enfants ont ce nœud comme parent
        for child in self._children:
            if child.parent is not self:
                return False

        # Vérifier que le parent a ce nœud comme enfant
        if self._parent is not None:
            if self not in self._parent._children:
                return False

        return True


def demonstrate_tree_node():
    """Démontre l'utilisation de la classe TreeNode."""
    print("=== Démonstration de TreeNode ===")

    # Créer des nœuds
    root = ExampleTreeNode("Racine")
    child1 = ExampleTreeNode("Enfant 1")
    child2 = ExampleTreeNode("Enfant 2")
    grandchild = ExampleTreeNode("Petit-enfant")

    # Construire l'arbre
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    # Afficher les propriétés
    print(f"Racine: {root.value}")
    print(f"  - Hauteur: {root.get_height()}")
    print(f"  - Profondeur: {root.get_depth()}")
    print(f"  - Est feuille: {root.is_leaf()}")
    print(f"  - Est racine: {root.is_root()}")
    print(f"  - Nombre d'enfants: {len(root.children)}")

    print(f"\nEnfant 1: {child1.value}")
    print(f"  - Hauteur: {child1.get_height()}")
    print(f"  - Profondeur: {child1.get_depth()}")
    print(f"  - Est feuille: {child1.is_leaf()}")
    print(f"  - Est racine: {child1.is_root()}")

    print(f"\nPetit-enfant: {grandchild.value}")
    print(f"  - Hauteur: {grandchild.get_height()}")
    print(f"  - Profondeur: {grandchild.get_depth()}")
    print(f"  - Est feuille: {grandchild.is_leaf()}")
    print(f"  - Est racine: {grandchild.is_root()}")

    # Tester la validation
    print(f"\nValidation de l'arbre: {root.validate()}")


def demonstrate_binary_tree_node():
    """Démontre l'utilisation de la classe BinaryTreeNode."""
    print("\n=== Démonstration de BinaryTreeNode ===")

    # Créer un arbre binaire simple
    root = BinaryTreeNode(10)
    left = BinaryTreeNode(5)
    right = BinaryTreeNode(15)
    left_left = BinaryTreeNode(3)
    left_right = BinaryTreeNode(7)

    # Construire l'arbre binaire
    root.set_left(left)
    root.set_right(right)
    left.set_left(left_left)
    left.set_right(left_right)

    # Afficher les propriétés
    print(f"Racine: {root.value}")
    print(f"  - Hauteur: {root.get_height()}")
    print(f"  - Profondeur: {root.get_depth()}")
    print(f"  - Est feuille: {root.is_leaf()}")
    print(f"  - A gauche: {root.has_left()}")
    print(f"  - A droite: {root.has_right()}")

    print(f"\nGauche: {left.value}")
    print(f"  - Hauteur: {left.get_height()}")
    print(f"  - Profondeur: {left.get_depth()}")
    print(f"  - Est feuille: {left.is_leaf()}")
    print(f"  - A gauche: {left.has_left()}")
    print(f"  - A droite: {left.has_right()}")

    print(f"\nDroite: {right.value}")
    print(f"  - Hauteur: {right.get_height()}")
    print(f"  - Profondeur: {right.get_depth()}")
    print(f"  - Est feuille: {right.is_leaf()}")
    print(f"  - A gauche: {right.has_left()}")
    print(f"  - A droite: {right.has_right()}")

    # Tester la validation
    print(f"\nValidation de l'arbre binaire: {root.validate()}")

    # Afficher la structure de l'arbre
    print("\nStructure de l'arbre binaire:")
    print("    10")
    print("   /  \\")
    print("  5    15")
    print(" / \\")
    print("3   7")


def demonstrate_metadata():
    """Démontre l'utilisation des métadonnées."""
    print("\n=== Démonstration des métadonnées ===")

    node = BinaryTreeNode(42)
    node.set_metadata("couleur", "rouge")
    node.set_metadata("taille", "grand")
    node.set_metadata("priorité", 1)

    print(f"Nœud: {node.value}")
    print(f"Métadonnées: {node.metadata}")
    print(f"Couleur: {node.get_metadata('couleur')}")
    print(f"Taille: {node.get_metadata('taille')}")
    print(f"Priorité: {node.get_metadata('priorité')}")
    print(f"Non existant: {node.get_metadata('inexistant', 'défaut')}")


def demonstrate_error_handling():
    """Démontre la gestion d'erreurs."""
    print("\n=== Démonstration de la gestion d'erreurs ===")

    try:
        node = BinaryTreeNode(10)
        # Essayer d'ajouter un enfant de type invalide
        node.set_left("pas un BinaryTreeNode")
    except Exception as e:
        print(f"Erreur capturée: {e}")

    try:
        parent = BinaryTreeNode(10)
        child = BinaryTreeNode(20)
        parent.add_child(child)
        # Essayer de créer une référence circulaire
        child.add_child(parent)
    except Exception as e:
        print(f"Erreur de référence circulaire: {e}")


if __name__ == "__main__":
    print("Librairie d'arbres - Exemple d'utilisation")
    print("=" * 50)

    demonstrate_tree_node()
    demonstrate_binary_tree_node()
    demonstrate_metadata()
    demonstrate_error_handling()

    print("\n" + "=" * 50)
    print("Démonstration terminée avec succès !")