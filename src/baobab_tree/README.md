# Baobab Tree - Librairie d'arbres Python

## Structure du projet

La librairie Baobab Tree est organisée de manière modulaire pour faciliter la maintenance et l'utilisation :

```
src/baobab_tree/
├── core/           # Structures de base
│   ├── interfaces.py      # Interfaces et types génériques
│   ├── exceptions.py      # Exceptions personnalisées
│   ├── tree_node.py       # Classe abstraite TreeNode
│   ├── tree_operations.py # Opérations de base sur les arbres
│   └── utility_operations.py # Opérations utilitaires
├── binary/         # Arbres binaires
│   ├── binary_tree_node.py    # Nœud d'arbre binaire
│   ├── binary_search_tree.py  # Arbre binaire de recherche
│   ├── bst_iterators.py       # Itérateurs pour BST
│   ├── bst_operations.py      # Opérations spécifiques aux BST
│   ├── search_operations.py   # Opérations de recherche
│   └── binary_tree_operations.py # Opérations sur arbres binaires
├── balanced/       # Arbres équilibrés
│   ├── avl_tree.py        # Arbre AVL
│   ├── avl_node.py        # Nœud AVL
│   ├── avl_operations.py  # Opérations AVL
│   ├── avl_rotations.py    # Rotations AVL
│   └── avl_balancing.py   # Équilibrage AVL
├── nary/           # Arbres n-aires
│   ├── btree.py      # Arbre B
│   └── btree_node.py # Nœud B-tree
├── spatial/        # Arbres spatiaux et parcours
│   ├── tree_traversal.py        # Parcours d'arbres
│   ├── inorder_traversal.py      # Parcours infixe
│   ├── preorder_traversal.py     # Parcours préfixe
│   ├── postorder_traversal.py    # Parcours postfixe
│   └── level_order_traversal.py  # Parcours par niveaux
├── search/         # Arbres de recherche et itérateurs
│   ├── tree_iterator.py       # Itérateur générique
│   └── traversal_iterators.py  # Itérateurs de parcours
└── specialized/    # Arbres spécialisés
    └── (vide pour l'instant)
```

## Utilisation

### Import de base

```python
from src.baobab_tree import BinarySearchTree, AVLTree, BTree
```

### Exemples d'utilisation

#### Arbre binaire de recherche (BST)

```python
from src.baobab_tree import BinarySearchTree

# Créer un BST
bst = BinarySearchTree()

# Insérer des valeurs
bst.insert(5)
bst.insert(3)
bst.insert(7)
bst.insert(1)
bst.insert(9)

# Parcours
print("Inorder:", bst.inorder_traversal())  # [1, 3, 5, 7, 9]
print("Preorder:", bst.preorder_traversal())  # [5, 3, 1, 7, 9]

# Recherche
print("Contient 5:", bst.contains(5))  # True
print("Contient 4:", bst.contains(4))  # False

# Suppression
bst.delete(3)
print("Après suppression:", bst.inorder_traversal())  # [1, 5, 7, 9]
```

#### Arbre AVL (auto-équilibré)

```python
from src.baobab_tree import AVLTree

# Créer un AVL
avl = AVLTree()

# Insérer des valeurs (équilibrage automatique)
avl.insert(5)
avl.insert(3)
avl.insert(7)
avl.insert(1)
avl.insert(9)

# Vérifier l'équilibre
print("Est équilibré:", avl.is_avl_valid())  # True
print("Hauteur:", avl.get_height())  # 3
print("Nombre de rotations:", avl.get_rotation_count())
```

#### Arbre B

```python
from src.baobab_tree import BTree

# Créer un B-tree d'ordre 3
btree = BTree(order=3)

# Insérer des clés
btree.insert(5)
btree.insert(3)
btree.insert(7)
btree.insert(1)
btree.insert(9)

# Statistiques
print("Taille:", btree.get_size())
print("Hauteur:", btree.get_height())
print("Est valide:", btree.is_valid())
```

## Fonctionnalités

### Arbres binaires de recherche (BST)
- Insertion, suppression, recherche en O(log n) dans le meilleur cas
- Parcours infixe, préfixe, postfixe et par niveaux
- Recherche de successeur/prédécesseur
- Requêtes de plage
- Validation des propriétés BST

### Arbres AVL
- Auto-équilibrage après chaque insertion/suppression
- Hauteur garantie O(log n)
- Rotations simples et doubles
- Statistiques d'équilibrage
- Validation des propriétés AVL

### Arbres B
- Optimisés pour les accès disque
- Ordre configurable
- Opérations de fusion et division
- Requêtes de plage efficaces
- Validation des propriétés B-tree

### Parcours et itérateurs
- Parcours préfixe, infixe, postfixe
- Parcours par niveaux (BFS)
- Itérateurs paresseux
- Parcours avec conditions et limitations

## Tests

Les tests sont organisés dans le dossier `tests/` et couvrent :
- Tests unitaires pour chaque classe
- Tests d'intégration
- Tests de performance
- Tests de cas d'erreur

Pour exécuter les tests :

```bash
PYTHONPATH=/workspace python3 -m unittest discover tests
```

## Développement

### Structure des modules

Chaque module suit une structure cohérente :
- Documentation complète avec docstrings
- Types hints pour la sécurité des types
- Gestion d'erreurs robuste
- Tests unitaires complets

### Ajout de nouveaux types d'arbres

Pour ajouter un nouveau type d'arbre :
1. Créer le fichier dans le dossier approprié
2. Hériter des interfaces de base (`TreeInterface`, `TreeNode`)
3. Implémenter les méthodes abstraites
4. Ajouter les tests correspondants
5. Mettre à jour les imports dans `__init__.py`

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.