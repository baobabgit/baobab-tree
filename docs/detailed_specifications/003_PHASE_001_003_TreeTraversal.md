# Spécification Détaillée - TreeTraversal (PRIORITÉ HAUTE)

## Vue d'ensemble
Cette spécification définit l'implémentation des classes de parcours d'arbres, essentielles pour la navigation et l'itération sur tous les types d'arbres de la librairie.

## Contexte
- **Phase** : Phase 1 - Fondations
- **Priorité** : HAUTE (nécessaire pour tous les arbres)
- **Dépendances** : TreeNode, BinaryTreeNode
- **Agent cible** : Agent de développement des algorithmes de parcours

## Spécifications techniques

### 1. Classe TreeTraversal (abstraite)

#### 1.1 Signature de classe
```python
class TreeTraversal(ABC, Generic[T]):
    """Classe abstraite pour tous les parcours d'arbres."""
```

#### 1.2 Méthodes abstraites
- `traverse(root: Optional[TreeNode[T]]) -> List[T]`: Parcours complet
- `traverse_iter(root: Optional[TreeNode[T]]) -> Iterator[T]`: Parcours itératif

#### 1.3 Méthodes concrètes
- `get_traversal_name() -> str`: Nom du parcours
- `is_empty() -> bool`: Vérifie si l'arbre est vide
- `validate_tree(root: Optional[TreeNode[T]]) -> bool`: Valide la structure

### 2. Classes de parcours spécialisées

#### 2.1 PreorderTraversal
```python
class PreorderTraversal(TreeTraversal[T]):
    """Parcours préfixe (NLR: Nœud, Gauche, Droite)."""
```

#### 2.2 InorderTraversal
```python
class InorderTraversal(TreeTraversal[T]):
    """Parcours infixe (LNR: Gauche, Nœud, Droite)."""
```

#### 2.3 PostorderTraversal
```python
class PostorderTraversal(TreeTraversal[T]):
    """Parcours postfixe (LRN: Gauche, Droite, Nœud)."""
```

#### 2.4 LevelOrderTraversal
```python
class LevelOrderTraversal(TreeTraversal[T]):
    """Parcours par niveaux (BFS: Breadth-First Search)."""
```

### 3. Itérateurs spécialisés

#### 3.1 Classe TreeIterator (abstraite)
```python
class TreeIterator(ABC, Generic[T]):
    """Classe abstraite pour les itérateurs d'arbres."""
```

#### 3.2 Itérateurs concrets
- `PreorderIterator`: Itérateur préfixe
- `InorderIterator`: Itérateur infixe
- `PostorderIterator`: Itérateur postfixe
- `LevelOrderIterator`: Itérateur par niveaux

### 4. Méthodes utilitaires

#### 4.1 Parcours avec callback
- `traverse_with_callback(root: TreeNode[T], callback: Callable[[T], None]) -> None`
- `traverse_with_condition(root: TreeNode[T], condition: Callable[[T], bool]) -> List[T]`

#### 4.2 Parcours limité
- `traverse_depth_limited(root: TreeNode[T], max_depth: int) -> List[T]`
- `traverse_count_limited(root: TreeNode[T], max_count: int) -> List[T]`

#### 4.3 Parcours inversé
- `traverse_reverse(root: TreeNode[T]) -> List[T]`
- `traverse_right_to_left(root: TreeNode[T]) -> List[T]`

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── tree_traversal.py      # Classe abstraite TreeTraversal
├── preorder_traversal.py  # Parcours préfixe
├── inorder_traversal.py   # Parcours infixe
├── postorder_traversal.py # Parcours postfixe
├── level_order_traversal.py # Parcours par niveaux
├── tree_iterator.py       # Itérateurs abstraits
└── traversal_iterators.py # Itérateurs concrets
```

### 2. Algorithme de parcours préfixe
```python
def traverse(self, root: Optional[TreeNode[T]]) -> List[T]:
    """Parcours préfixe récursif."""
    if root is None:
        return []
    
    result = [root.value]
    result.extend(self.traverse(root.get_left()))
    result.extend(self.traverse(root.get_right()))
    return result
```

### 3. Algorithme de parcours infixe
```python
def traverse(self, root: Optional[TreeNode[T]]) -> List[T]:
    """Parcours infixe récursif."""
    if root is None:
        return []
    
    result = []
    result.extend(self.traverse(root.get_left()))
    result.append(root.value)
    result.extend(self.traverse(root.get_right()))
    return result
```

### 4. Algorithme de parcours postfixe
```python
def traverse(self, root: Optional[TreeNode[T]]) -> List[T]:
    """Parcours postfixe récursif."""
    if root is None:
        return []
    
    result = []
    result.extend(self.traverse(root.get_left()))
    result.extend(self.traverse(root.get_right()))
    result.append(root.value)
    return result
```

### 5. Algorithme de parcours par niveaux
```python
def traverse(self, root: Optional[TreeNode[T]]) -> List[T]:
    """Parcours par niveaux avec queue."""
    if root is None:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        result.append(node.value)
        
        if node.get_left():
            queue.append(node.get_left())
        if node.get_right():
            queue.append(node.get_right())
    
    return result
```

### 6. Implémentation des itérateurs
```python
class PreorderIterator(TreeIterator[T]):
    """Itérateur préfixe avec pile."""
    
    def __init__(self, root: Optional[TreeNode[T]]):
        self._stack = []
        if root:
            self._stack.append(root)
    
    def __iter__(self) -> 'PreorderIterator[T]':
        return self
    
    def __next__(self) -> T:
        if not self._stack:
            raise StopIteration
        
        node = self._stack.pop()
        
        if node.get_right():
            self._stack.append(node.get_right())
        if node.get_left():
            self._stack.append(node.get_left())
        
        return node.value
```

## Tests unitaires

### 1. Tests de base
- Test de création des parcours
- Test de parcours sur arbre vide
- Test de parcours sur arbre à un nœud
- Test de parcours sur arbre simple

### 2. Tests de parcours
- Test du parcours préfixe
- Test du parcours infixe
- Test du parcours postfixe
- Test du parcours par niveaux

### 3. Tests d'itérateurs
- Test des itérateurs préfixe
- Test des itérateurs infixe
- Test des itérateurs postfixe
- Test des itérateurs par niveaux

### 4. Tests de performance
- Test de parcours sur gros arbre
- Test de parcours avec callback
- Test de parcours limité
- Test de parcours inversé

### 5. Tests d'intégration
- Test avec différents types d'arbres
- Test de cohérence entre parcours
- Test de gestion des erreurs
- Test de validation des arbres

## Documentation

### 1. Docstrings
- Documentation complète en reStructuredText
- Exemples d'utilisation pour chaque parcours
- Description des algorithmes
- Documentation des complexités

### 2. Exemples d'utilisation
```python
# Création d'un arbre
tree = BinarySearchTree[int]()
tree.insert(50)
tree.insert(30)
tree.insert(70)
tree.insert(20)
tree.insert(40)

# Parcours préfixe
preorder = PreorderTraversal[int]()
result = preorder.traverse(tree.get_root())
assert result == [50, 30, 20, 40, 70]

# Parcours infixe
inorder = InorderTraversal[int]()
result = inorder.traverse(tree.get_root())
assert result == [20, 30, 40, 50, 70]

# Parcours postfixe
postorder = PostorderTraversal[int]()
result = postorder.traverse(tree.get_root())
assert result == [20, 40, 30, 70, 50]

# Parcours par niveaux
level_order = LevelOrderTraversal[int]()
result = level_order.traverse(tree.get_root())
assert result == [50, 30, 70, 20, 40]

# Itération
for value in PreorderIterator(tree.get_root()):
    print(value)
```

## Complexités temporelles

### 1. Parcours récursifs
- `traverse()`: O(n) temps, O(h) espace (h = hauteur)
- `traverse_with_callback()`: O(n) temps, O(h) espace
- `traverse_with_condition()`: O(n) temps, O(h) espace

### 2. Parcours itératifs
- `traverse_iter()`: O(n) temps, O(h) espace
- `traverse_depth_limited()`: O(min(n, 2^d)) temps, O(d) espace
- `traverse_count_limited()`: O(k) temps, O(h) espace

### 3. Parcours par niveaux
- `traverse()`: O(n) temps, O(w) espace (w = largeur maximale)

## Critères d'acceptation
- [x] Classe TreeTraversal implémentée
- [x] Tous les parcours implémentés (PreorderTraversal, InorderTraversal, PostorderTraversal, LevelOrderTraversal)
- [x] Tous les itérateurs implémentés (PreorderIterator, InorderIterator, PostorderIterator, LevelOrderIterator, LevelOrderWithLevelIterator)
- [x] Tests unitaires avec couverture complète (192 tests au total)
- [x] Documentation complète en reStructuredText
- [x] Score Pylint >= 8.5/10 (9.84/10)
- [x] Performance validée (complexités temporelles respectées)
- [x] Algorithmes récursifs et itératifs fonctionnels
- [x] Méthodes utilitaires implémentées (callback, condition, limitation, inversion)
- [x] Validation des arbres avec détection des références circulaires
- [x] Support des types génériques avec Generic[T]
- [x] API complète avec toutes les méthodes requises

## Notes pour l'agent de développement
- Les parcours sont fondamentaux pour tous les arbres
- Privilégier la simplicité et la lisibilité
- Les itérateurs doivent être efficaces
- Les tests doivent couvrir tous les cas
- La documentation doit être claire et complète
