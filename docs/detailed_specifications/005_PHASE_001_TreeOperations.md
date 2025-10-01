# Spécification Détaillée - TreeOperations (PRIORITÉ HAUTE)

## Vue d'ensemble
Cette spécification définit l'implémentation des classes d'opérations de base sur les arbres, incluant la recherche, l'insertion, la suppression et les opérations utilitaires.

## Contexte
- **Phase** : Phase 1 - Fondations
- **Priorité** : HAUTE (nécessaire pour tous les arbres)
- **Dépendances** : TreeNode, BinaryTreeNode, TreeTraversal
- **Agent cible** : Agent de développement des opérations de base

## Spécifications techniques

### 1. Classe TreeOperations (abstraite)

#### 1.1 Signature de classe
```python
class TreeOperations(ABC, Generic[T]):
    """Classe abstraite pour les opérations de base sur les arbres."""
```

#### 1.2 Méthodes abstraites
- `search(root: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]`
- `insert(root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]`
- `delete(root: Optional[TreeNode[T]], value: T) -> Tuple[Optional[TreeNode[T]], bool]`

#### 1.3 Méthodes concrètes
- `contains(root: Optional[TreeNode[T]], value: T) -> bool`
- `get_min(root: Optional[TreeNode[T]]) -> Optional[T]`
- `get_max(root: Optional[TreeNode[T]]) -> Optional[T]`
- `get_height(root: Optional[TreeNode[T]]) -> int`
- `get_size(root: Optional[TreeNode[T]]) -> int`

### 2. Classes d'opérations spécialisées

#### 2.1 BinaryTreeOperations
```python
class BinaryTreeOperations(TreeOperations[T]):
    """Opérations spécialisées pour les arbres binaires."""
```

#### 2.2 BSTOperations
```python
class BSTOperations(BinaryTreeOperations[T]):
    """Opérations spécialisées pour les arbres binaires de recherche."""
```

#### 2.3 AVLOperations
```python
class AVLOperations(BSTOperations[T]):
    """Opérations spécialisées pour les arbres AVL."""
```

### 3. Opérations de recherche

#### 3.1 Recherche simple
- `search(root: TreeNode[T], value: T) -> Optional[TreeNode[T]]`
- `search_recursive(root: TreeNode[T], value: T) -> Optional[TreeNode[T]]`
- `search_iterative(root: TreeNode[T], value: T) -> Optional[TreeNode[T]]`

#### 3.2 Recherche avancée
- `find_successor(node: TreeNode[T]) -> Optional[TreeNode[T]]`
- `find_predecessor(node: TreeNode[T]) -> Optional[TreeNode[T]]`
- `find_floor(root: TreeNode[T], value: T) -> Optional[T]`
- `find_ceiling(root: TreeNode[T], value: T) -> Optional[T]`

#### 3.3 Recherche par plage
- `range_search(root: TreeNode[T], min_val: T, max_val: T) -> List[T]`
- `count_range(root: TreeNode[T], min_val: T, max_val: T) -> int`

### 4. Opérations d'insertion

#### 4.1 Insertion simple
- `insert(root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]`
- `insert_recursive(root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]`
- `insert_iterative(root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]`

#### 4.2 Insertion avec validation
- `insert_with_validation(root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]`
- `insert_with_duplicates(root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]`

### 5. Opérations de suppression

#### 5.1 Suppression simple
- `delete(root: Optional[TreeNode[T]], value: T) -> Tuple[Optional[TreeNode[T]], bool]`
- `delete_recursive(root: Optional[TreeNode[T]], value: T) -> Tuple[Optional[TreeNode[T]], bool]`
- `delete_iterative(root: Optional[TreeNode[T]], value: T) -> Tuple[Optional[TreeNode[T]], bool]`

#### 5.2 Suppression avec gestion des cas
- `delete_leaf(node: TreeNode[T]) -> None`
- `delete_single_child(node: TreeNode[T]) -> TreeNode[T]`
- `delete_two_children(node: TreeNode[T]) -> TreeNode[T]`

### 6. Opérations utilitaires

#### 6.1 Calculs de propriétés
- `get_height(root: Optional[TreeNode[T]]) -> int`
- `get_depth(node: TreeNode[T]) -> int`
- `get_size(root: Optional[TreeNode[T]]) -> int`
- `get_balance_factor(node: TreeNode[T]) -> int`

#### 6.2 Validation
- `is_valid_bst(root: Optional[TreeNode[T]]) -> bool`
- `is_balanced(root: Optional[TreeNode[T]]) -> bool`
- `is_complete(root: Optional[TreeNode[T]]) -> bool`
- `is_full(root: Optional[TreeNode[T]]) -> bool`

#### 6.3 Opérations sur les nœuds
- `get_min_node(root: TreeNode[T]) -> TreeNode[T]`
- `get_max_node(root: TreeNode[T]) -> TreeNode[T]`
- `get_leaf_nodes(root: Optional[TreeNode[T]]) -> List[TreeNode[T]]`
- `get_internal_nodes(root: Optional[TreeNode[T]]) -> List[TreeNode[T]]`

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── tree_operations.py     # Classe abstraite TreeOperations
├── binary_tree_operations.py # Opérations binaires
├── bst_operations.py      # Opérations BST
├── avl_operations.py      # Opérations AVL
├── search_operations.py   # Opérations de recherche
├── insertion_operations.py # Opérations d'insertion
├── deletion_operations.py # Opérations de suppression
└── utility_operations.py  # Opérations utilitaires
```

### 2. Algorithme de recherche BST
```python
def search(self, root: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
    """Recherche une valeur dans un BST."""
    current = root
    
    while current is not None:
        if value == current.value:
            return current
        elif value < current.value:
            current = current.get_left()
        else:
            current = current.get_right()
    
    return None
```

### 3. Algorithme d'insertion BST
```python
def insert(self, root: Optional[TreeNode[T]], value: T) -> Tuple[TreeNode[T], bool]:
    """Insère une valeur dans un BST."""
    if root is None:
        return BinaryTreeNode(value), True
    
    if value < root.value:
        new_left, inserted = self.insert(root.get_left(), value)
        root.set_left(new_left)
        new_left.set_parent(root)
    elif value > root.value:
        new_right, inserted = self.insert(root.get_right(), value)
        root.set_right(new_right)
        new_right.set_parent(root)
    else:
        return root, False  # Valeur déjà présente
    
    return root, inserted
```

### 4. Algorithme de suppression BST
```python
def delete(self, root: Optional[TreeNode[T]], value: T) -> Tuple[Optional[TreeNode[T]], bool]:
    """Supprime une valeur d'un BST."""
    if root is None:
        return None, False
    
    if value < root.value:
        new_left, deleted = self.delete(root.get_left(), value)
        root.set_left(new_left)
        if new_left:
            new_left.set_parent(root)
        return root, deleted
    elif value > root.value:
        new_right, deleted = self.delete(root.get_right(), value)
        root.set_right(new_right)
        if new_right:
            new_right.set_parent(root)
        return root, deleted
    else:
        # Nœud à supprimer trouvé
        if root.get_left() is None:
            return root.get_right(), True
        elif root.get_right() is None:
            return root.get_left(), True
        else:
            # Nœud avec deux enfants
            successor = self.get_min_node(root.get_right())
            root.value = successor.value
            new_right, _ = self.delete(root.get_right(), successor.value)
            root.set_right(new_right)
            if new_right:
                new_right.set_parent(root)
            return root, True
```

### 5. Algorithme de recherche de successeur
```python
def find_successor(self, node: TreeNode[T]) -> Optional[TreeNode[T]]:
    """Trouve le successeur d'un nœud."""
    if node.get_right() is not None:
        return self.get_min_node(node.get_right())
    
    parent = node.get_parent()
    while parent is not None and node == parent.get_right():
        node = parent
        parent = parent.get_parent()
    
    return parent
```

### 6. Algorithme de validation BST
```python
def is_valid_bst(self, root: Optional[TreeNode[T]]) -> bool:
    """Valide les propriétés d'un BST."""
    def validate(node: Optional[TreeNode[T]], min_val: Optional[T], max_val: Optional[T]) -> bool:
        if node is None:
            return True
        
        if min_val is not None and node.value <= min_val:
            return False
        if max_val is not None and node.value >= max_val:
            return False
        
        return (validate(node.get_left(), min_val, node.value) and
                validate(node.get_right(), node.value, max_val))
    
    return validate(root, None, None)
```

## Tests unitaires

### 1. Tests de recherche
- Test de recherche sur arbre vide
- Test de recherche sur arbre à un nœud
- Test de recherche de valeur existante
- Test de recherche de valeur inexistante
- Test de recherche sur gros arbre

### 2. Tests d'insertion
- Test d'insertion sur arbre vide
- Test d'insertion sur arbre existant
- Test d'insertion de valeur dupliquée
- Test d'insertion en séquence
- Test d'insertion aléatoire

### 3. Tests de suppression
- Test de suppression sur arbre vide
- Test de suppression de feuille
- Test de suppression de nœud avec un enfant
- Test de suppression de nœud avec deux enfants
- Test de suppression de valeur inexistante

### 4. Tests d'opérations avancées
- Test de recherche de successeur
- Test de recherche de prédécesseur
- Test de recherche par plage
- Test de calcul de propriétés
- Test de validation d'arbres

### 5. Tests de performance
- Test de recherche sur gros arbre
- Test d'insertion en masse
- Test de suppression aléatoire
- Test de validation sur gros arbre

## Documentation

### 1. Docstrings
- Documentation complète en reStructuredText
- Exemples d'utilisation pour chaque opération
- Description des algorithmes
- Documentation des complexités

### 2. Exemples d'utilisation
```python
# Création d'un BST
tree = BinarySearchTree[int]()
tree.insert(50)
tree.insert(30)
tree.insert(70)
tree.insert(20)
tree.insert(40)

# Opérations de recherche
operations = BSTOperations[int]()
result = operations.search(tree.get_root(), 30)
assert result is not None

# Recherche de successeur
successor = operations.find_successor(result)
assert successor.value == 40

# Validation de l'arbre
assert operations.is_valid_bst(tree.get_root())

# Calcul de propriétés
height = operations.get_height(tree.get_root())
size = operations.get_size(tree.get_root())
assert height >= 0
assert size == 5
```

## Complexités temporelles

### 1. Opérations de base
- `search()`: O(h) où h est la hauteur
- `insert()`: O(h) où h est la hauteur
- `delete()`: O(h) où h est la hauteur
- `contains()`: O(h) où h est la hauteur

### 2. Opérations avancées
- `find_successor()`: O(h)
- `find_predecessor()`: O(h)
- `range_search()`: O(h + k) où k est le nombre de résultats
- `get_min()`: O(h)
- `get_max()`: O(h)

### 3. Opérations utilitaires
- `get_height()`: O(n)
- `get_size()`: O(n)
- `is_valid_bst()`: O(n)
- `is_balanced()`: O(n)

## Critères d'acceptation
- [ ] Classe TreeOperations implémentée
- [ ] Toutes les opérations de base implémentées
- [ ] Opérations spécialisées par type d'arbre
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Documentation complète
- [ ] Score Pylint >= 8.5/10
- [ ] Performance validée

## Notes pour l'agent de développement
- Les opérations sont fondamentales pour tous les arbres
- Privilégier la robustesse et la performance
- Les algorithmes doivent être optimisés
- Les tests doivent couvrir tous les cas
- La documentation doit être claire et complète