# Spécification Détaillée - BinarySearchTree (PRIORITÉ CRITIQUE)

## Vue d'ensemble
Cette spécification définit l'implémentation de la classe `BinarySearchTree` (BST), structure fondamentale nécessaire au développement de l'arbre AVL. Le BST sert de base pour tous les arbres équilibrés.

## Contexte
- **Phase** : Phase 1 - Fondations
- **Priorité** : CRITIQUE (base pour AVL)
- **Dépendances** : TreeNode, BinaryTreeNode
- **Agent cible** : Agent de développement des arbres binaires

## Spécifications techniques

### 1. Classe BinarySearchTree

#### 1.1 Signature de classe
```python
class BinarySearchTree(Generic[T]):
    """Arbre binaire de recherche générique."""
```

#### 1.2 Attributs
- `root`: Racine de l'arbre (BinaryTreeNode[T])
- `size`: Nombre d'éléments dans l'arbre (int)
- `comparator`: Fonction de comparaison (Callable[[T, T], int])

#### 1.3 Constructeur
```python
def __init__(self, comparator: Optional[Callable[[T, T], int]] = None) -> None
```

#### 1.4 Méthodes principales
- `insert(value: T) -> bool`: Insère une valeur
- `delete(value: T) -> bool`: Supprime une valeur
- `search(value: T) -> Optional[BinaryTreeNode[T]]`: Recherche une valeur
- `contains(value: T) -> bool`: Vérifie l'existence d'une valeur
- `clear() -> None`: Vide l'arbre
- `is_empty() -> bool`: Vérifie si l'arbre est vide

#### 1.5 Méthodes d'accès
- `get_root() -> Optional[BinaryTreeNode[T]]`: Retourne la racine
- `get_size() -> int`: Retourne la taille
- `get_height() -> int`: Calcule la hauteur
- `get_min() -> Optional[T]`: Trouve la valeur minimale
- `get_max() -> Optional[T]`: Trouve la valeur maximale

#### 1.6 Méthodes de validation
- `is_valid() -> bool`: Valide les propriétés BST
- `is_balanced() -> bool`: Vérifie l'équilibre (optionnel)
- `get_balance_factor() -> int`: Calcule le facteur d'équilibre

### 2. Méthodes de parcours

#### 2.1 Parcours récursifs
- `preorder_traversal() -> List[T]`: Parcours préfixe
- `inorder_traversal() -> List[T]`: Parcours infixe
- `postorder_traversal() -> List[T]`: Parcours postfixe

#### 2.2 Parcours itératifs
- `preorder_iter() -> Iterator[T]`: Itérateur préfixe
- `inorder_iter() -> Iterator[T]`: Itérateur infixe
- `postorder_iter() -> Iterator[T]`: Itérateur postfixe
- `level_order_iter() -> Iterator[T]`: Itérateur par niveaux

### 3. Méthodes utilitaires

#### 3.1 Recherche avancée
- `find_successor(value: T) -> Optional[T]`: Trouve le successeur
- `find_predecessor(value: T) -> Optional[T]`: Trouve le prédécesseur
- `find_floor(value: T) -> Optional[T]`: Trouve le plus grand <= value
- `find_ceiling(value: T) -> Optional[T]`: Trouve le plus petit >= value

#### 3.2 Opérations sur les plages
- `range_query(min_val: T, max_val: T) -> List[T]`: Requête de plage
- `count_range(min_val: T, max_val: T) -> int`: Compte dans une plage

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── binary_search_tree.py    # Classe principale
├── bst_operations.py        # Opérations spécialisées
└── bst_iterators.py         # Itérateurs
```

### 2. Algorithmes d'insertion
```python
def insert(self, value: T) -> bool:
    """Insère une valeur dans l'arbre BST."""
    # 1. Si l'arbre est vide, créer la racine
    # 2. Sinon, naviguer selon la propriété BST
    # 3. Insérer à la position appropriée
    # 4. Mettre à jour la taille
    # 5. Retourner True si insertion réussie
```

### 3. Algorithmes de suppression
```python
def delete(self, value: T) -> bool:
    """Supprime une valeur de l'arbre BST."""
    # 1. Rechercher le nœud à supprimer
    # 2. Cas 1: Nœud feuille -> suppression directe
    # 3. Cas 2: Un enfant -> remplacer par l'enfant
    # 4. Cas 3: Deux enfants -> remplacer par le successeur
    # 5. Mettre à jour la taille
    # 6. Retourner True si suppression réussie
```

### 4. Gestion des erreurs
- `BSTError`: Exception de base
- `DuplicateValueError`: Valeur dupliquée
- `ValueNotFoundError`: Valeur non trouvée
- `InvalidOperationError`: Opération invalide

### 5. Optimisations
- Cache de la taille pour O(1)
- Calcul paresseux de la hauteur
- Réutilisation des nœuds lors de la suppression

## Tests unitaires

### 1. Tests de base
- Test de création et initialisation
- Test d'insertion de valeurs
- Test de suppression de valeurs
- Test de recherche de valeurs
- Test de parcours

### 2. Tests de propriétés BST
- Test de la propriété BST après insertion
- Test de la propriété BST après suppression
- Test de validation de l'arbre
- Test des cas limites

### 3. Tests de performance
- Test d'insertion en séquence
- Test de suppression aléatoire
- Test de recherche sur gros arbre
- Test de parcours sur gros arbre

### 4. Tests d'intégration
- Test avec différents types de données
- Test avec comparateur personnalisé
- Test de gestion des erreurs
- Test de cohérence des métadonnées

## Documentation

### 1. Docstrings
- Documentation complète en reStructuredText
- Exemples d'utilisation détaillés
- Description des algorithmes
- Documentation des complexités

### 2. Exemples d'utilisation
```python
# Création d'un BST
bst = BinarySearchTree[int]()

# Insertion de valeurs
bst.insert(50)
bst.insert(30)
bst.insert(70)
bst.insert(20)
bst.insert(40)

# Recherche
result = bst.search(30)
assert result is not None

# Parcours
inorder = bst.inorder_traversal()
assert inorder == [20, 30, 40, 50, 70]

# Suppression
bst.delete(30)
assert not bst.contains(30)
```

## Complexités temporelles

### 1. Opérations de base
- `insert()`: O(h) où h est la hauteur
- `delete()`: O(h) où h est la hauteur
- `search()`: O(h) où h est la hauteur
- `contains()`: O(h) où h est la hauteur

### 2. Parcours
- `preorder_traversal()`: O(n)
- `inorder_traversal()`: O(n)
- `postorder_traversal()`: O(n)
- `level_order_traversal()`: O(n)

### 3. Opérations avancées
- `find_successor()`: O(h)
- `find_predecessor()`: O(h)
- `range_query()`: O(h + k) où k est le nombre de résultats

## Critères d'acceptation
- [ ] Classe BinarySearchTree implémentée
- [ ] Toutes les méthodes principales fonctionnelles
- [ ] Propriétés BST respectées
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Documentation complète
- [ ] Score Pylint >= 8.5/10
- [ ] Performance validée

## Notes pour l'agent de développement
- Cette classe est critique pour l'AVL
- Privilégier la robustesse et la simplicité
- Les algorithmes doivent être optimisés
- Les tests doivent couvrir tous les cas
- La documentation doit être exhaustive
