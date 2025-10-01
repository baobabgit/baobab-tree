# Spécification Détaillée - AVLTree (PRIORITÉ ABSOLUE)

## Vue d'ensemble
Cette spécification définit l'implémentation de la classe `AVLTree`, arbre auto-équilibré critique pour le projet d'interpréteur. L'AVL garantit une hauteur logarithmique et des performances optimales.

## Contexte
- **Phase** : Phase 2 - Arbres Équilibrés
- **Priorité** : ABSOLUE (critique pour l'interpréteur)
- **Dépendances** : BinarySearchTree, BinaryTreeNode
- **Agent cible** : Agent de développement des arbres équilibrés

## Spécifications techniques

### 1. Classe AVLTree

#### 1.1 Signature de classe
```python
class AVLTree(Generic[T]):
    """Arbre AVL auto-équilibré."""
```

#### 1.2 Héritage
```python
class AVLTree(BinarySearchTree[T]):
    """Hérite de BinarySearchTree et ajoute l'équilibrage AVL."""
```

#### 1.3 Attributs supplémentaires
- `_balance_threshold`: Seuil de déséquilibre (constante = 1)
- `_rotation_count`: Compteur de rotations (pour debugging)

### 2. Classe AVLNode

#### 2.1 Signature de classe
```python
class AVLNode(BinaryTreeNode[T]):
    """Nœud spécialisé pour l'arbre AVL avec facteur d'équilibre."""
```

#### 2.2 Attributs supplémentaires
- `balance_factor`: Facteur d'équilibre (int, -1, 0, ou 1)
- `height`: Hauteur du sous-arbre (int, mis à jour automatiquement)

#### 2.3 Méthodes spécialisées
- `update_balance_factor() -> None`: Met à jour le facteur d'équilibre
- `update_height() -> None`: Met à jour la hauteur
- `is_left_heavy() -> bool`: Vérifie si le nœud penche à gauche
- `is_right_heavy() -> bool`: Vérifie si le nœud penche à droite
- `is_balanced() -> bool`: Vérifie si le nœud est équilibré

### 3. Méthodes d'équilibrage

#### 3.1 Rotations simples
- `_rotate_left(node: AVLNode[T]) -> AVLNode[T]`: Rotation gauche
- `_rotate_right(node: AVLNode[T]) -> AVLNode[T]`: Rotation droite

#### 3.2 Rotations doubles
- `_rotate_left_right(node: AVLNode[T]) -> AVLNode[T]`: Rotation gauche-droite
- `_rotate_right_left(node: AVLNode[T]) -> AVLNode[T]`: Rotation droite-gauche

#### 3.3 Équilibrage
- `_balance_node(node: AVLNode[T]) -> None`: Équilibre un nœud
- `_rebalance_path(node: AVLNode[T]) -> None`: Rééquilibre le chemin vers la racine

### 4. Surcharge des méthodes de base

#### 4.1 Insertion AVL
```python
def insert(self, value: T) -> bool:
    """Insère une valeur avec équilibrage automatique."""
    # 1. Insérer comme dans un BST normal
    # 2. Mettre à jour les hauteurs et facteurs d'équilibre
    # 3. Vérifier et corriger les déséquilibres
    # 4. Effectuer les rotations nécessaires
```

#### 4.2 Suppression AVL
```python
def delete(self, value: T) -> bool:
    """Supprime une valeur avec équilibrage automatique."""
    # 1. Supprimer comme dans un BST normal
    # 2. Mettre à jour les hauteurs et facteurs d'équilibre
    # 3. Vérifier et corriger les déséquilibres
    # 4. Effectuer les rotations nécessaires
```

### 5. Méthodes de validation AVL

#### 5.1 Validation des propriétés
- `is_avl_valid() -> bool`: Valide les propriétés AVL
- `check_balance_factors() -> bool`: Vérifie tous les facteurs d'équilibre
- `validate_heights() -> bool`: Valide le calcul des hauteurs

#### 5.2 Méthodes de diagnostic
- `get_balance_statistics() -> Dict[str, int]`: Statistiques d'équilibre
- `get_rotation_count() -> int`: Nombre de rotations effectuées
- `get_height_analysis() -> Dict[str, int]`: Analyse des hauteurs

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── avl_tree.py           # Classe principale AVLTree
├── avl_node.py           # Classe AVLNode
├── avl_rotations.py      # Algorithmes de rotation
└── avl_balancing.py      # Algorithmes d'équilibrage
```

### 2. Algorithme d'insertion AVL
```python
def _insert_avl(self, value: T) -> bool:
    """Insertion avec équilibrage automatique."""
    # 1. Insérer le nœud comme dans un BST
    # 2. Remonter vers la racine en mettant à jour les hauteurs
    # 3. Pour chaque nœud sur le chemin:
    #    a. Calculer le nouveau facteur d'équilibre
    #    b. Si déséquilibre détecté:
    #       - Identifier le type de déséquilibre
    #       - Effectuer la rotation appropriée
    #       - Mettre à jour les hauteurs
    # 4. Retourner True si insertion réussie
```

### 3. Algorithme de suppression AVL
```python
def _delete_avl(self, value: T) -> bool:
    """Suppression avec équilibrage automatique."""
    # 1. Supprimer le nœud comme dans un BST
    # 2. Remonter vers la racine en mettant à jour les hauteurs
    # 3. Pour chaque nœud sur le chemin:
    #    a. Calculer le nouveau facteur d'équilibre
    #    b. Si déséquilibre détecté:
    #       - Identifier le type de déséquilibre
    #       - Effectuer la rotation appropriée
    #       - Mettre à jour les hauteurs
    # 4. Retourner True si suppression réussie
```

### 4. Algorithmes de rotation

#### 4.1 Rotation gauche
```python
def _rotate_left(self, node: AVLNode[T]) -> AVLNode[T]:
    """Rotation gauche pour équilibrer l'arbre."""
    # 1. Sauvegarder le nœud droit
    # 2. Remplacer le nœud droit par son enfant gauche
    # 3. Définir le nœud comme enfant gauche du nœud droit
    # 4. Mettre à jour les références parent
    # 5. Mettre à jour les hauteurs et facteurs d'équilibre
    # 6. Retourner la nouvelle racine du sous-arbre
```

#### 4.2 Rotation droite
```python
def _rotate_right(self, node: AVLNode[T]) -> AVLNode[T]:
    """Rotation droite pour équilibrer l'arbre."""
    # 1. Sauvegarder le nœud gauche
    # 2. Remplacer le nœud gauche par son enfant droit
    # 3. Définir le nœud comme enfant droit du nœud gauche
    # 4. Mettre à jour les références parent
    # 5. Mettre à jour les hauteurs et facteurs d'équilibre
    # 6. Retourner la nouvelle racine du sous-arbre
```

### 5. Gestion des erreurs
- `AVLError`: Exception de base pour AVL
- `InvalidBalanceFactorError`: Facteur d'équilibre invalide
- `RotationError`: Erreur lors d'une rotation
- `HeightMismatchError`: Incohérence de hauteur

## Tests unitaires

### 1. Tests de base
- Test de création et initialisation
- Test d'insertion avec équilibrage
- Test de suppression avec équilibrage
- Test de recherche (héritée de BST)

### 2. Tests d'équilibrage
- Test d'insertion séquentielle (1,2,3,4,5)
- Test d'insertion en ordre décroissant (5,4,3,2,1)
- Test d'insertion aléatoire
- Test de suppression avec rééquilibrage

### 3. Tests de rotation
- Test de rotation gauche simple
- Test de rotation droite simple
- Test de rotation gauche-droite
- Test de rotation droite-gauche
- Test de séquences de rotations

### 4. Tests de validation
- Test des propriétés AVL après chaque opération
- Test des facteurs d'équilibre
- Test des hauteurs calculées
- Test de la hauteur maximale (log n)

### 5. Tests de performance
- Test d'insertion de 10^6 éléments
- Test de suppression aléatoire
- Test de recherche sur gros arbre
- Test de stabilité à long terme

### 6. Tests de stress
- Test d'insertion/suppression alternées
- Test de déséquilibre intentionnel
- Test de récupération après erreur
- Test de cohérence des métadonnées

## Documentation

### 1. Docstrings
- Documentation complète en reStructuredText
- Exemples d'utilisation détaillés
- Description des algorithmes d'équilibrage
- Documentation des complexités

### 2. Exemples d'utilisation
```python
# Création d'un AVL
avl = AVLTree[int]()

# Insertion avec équilibrage automatique
avl.insert(50)
avl.insert(30)
avl.insert(70)
avl.insert(20)
avl.insert(40)
avl.insert(60)
avl.insert(80)

# Vérification de l'équilibre
assert avl.is_avl_valid()
assert avl.get_height() <= 2 * math.log2(avl.get_size() + 1)

# Recherche optimisée
result = avl.search(40)
assert result is not None

# Suppression avec rééquilibrage
avl.delete(30)
assert avl.is_avl_valid()
```

## Complexités temporelles

### 1. Opérations de base
- `insert()`: O(log n) garanti
- `delete()`: O(log n) garanti
- `search()`: O(log n) garanti
- `contains()`: O(log n) garanti

### 2. Opérations d'équilibrage
- `_rotate_left()`: O(1)
- `_rotate_right()`: O(1)
- `_balance_node()`: O(1)
- `_rebalance_path()`: O(log n)

### 3. Validation
- `is_avl_valid()`: O(n)
- `check_balance_factors()`: O(n)
- `validate_heights()`: O(n)

## Critères d'acceptation
- [ ] Classe AVLTree implémentée et fonctionnelle
- [ ] Classe AVLNode implémentée et fonctionnelle
- [ ] Toutes les rotations implémentées
- [ ] Équilibrage automatique validé
- [ ] Complexité O(log n) garantie
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Tests de stress passés
- [ ] Documentation complète
- [ ] Score Pylint >= 8.5/10

## Notes pour l'agent de développement
- Cette classe est CRITIQUE pour l'interpréteur
- L'équilibrage doit être parfait
- Les performances doivent être optimales
- Les tests doivent être exhaustifs
- La documentation doit être professionnelle
- Privilégier la robustesse sur la performance