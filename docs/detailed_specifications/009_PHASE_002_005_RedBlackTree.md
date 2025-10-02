# Spécification Détaillée - RedBlackTree

## Vue d'ensemble
Cette spécification définit l'implémentation de la classe `RedBlackTree`, arbre auto-équilibré alternatif à l'AVL utilisant la recoloration et les rotations pour maintenir l'équilibre.

## Contexte
- **Phase** : Phase 2 - Arbres Équilibrés
- **Priorité** : MOYENNE (alternative à AVL)
- **Dépendances** : BinarySearchTree, RedBlackNode
- **Agent cible** : Agent de développement des arbres rouge-noir

## Spécifications techniques

### 1. Classe RedBlackTree

#### 1.1 Signature de classe
```python
class RedBlackTree(Generic[T]):
    """Arbre rouge-noir auto-équilibré."""
```

#### 1.2 Héritage
```python
class RedBlackTree(BinarySearchTree[T]):
    """Hérite de BinarySearchTree et ajoute l'équilibrage rouge-noir."""
```

#### 1.3 Attributs supplémentaires
- `_nil`: Nœud sentinelle (toujours noir)
- `_recolor_count`: Compteur de recolorations (pour debugging)
- `_rotation_count`: Compteur de rotations (pour debugging)

### 2. Propriétés rouge-noir

#### 2.1 Propriétés fondamentales
1. **Propriété de couleur** : Chaque nœud est soit rouge, soit noir
2. **Propriété de racine** : La racine est toujours noire
3. **Propriété de feuille** : Toutes les feuilles (NIL) sont noires
4. **Propriété rouge** : Si un nœud est rouge, ses enfants sont noirs
5. **Propriété de chemin** : Tous les chemins de la racine aux feuilles ont le même nombre de nœuds noirs

#### 2.2 Propriétés dérivées
- Hauteur maximale : 2 * log(n+1)
- Complexité garantie : O(log n) pour toutes les opérations
- Équilibrage par recoloration et rotations

### 3. Méthodes de base surchargées

#### 3.1 Insertion rouge-noir
```python
def insert(self, value: T) -> bool:
    """Insère une valeur avec équilibrage automatique rouge-noir."""
    # 1. Insérer comme dans un BST normal
    # 2. Colorer le nouveau nœud en rouge
    # 3. Vérifier et corriger les violations de propriétés
    # 4. Effectuer les recolorations et rotations nécessaires
```

#### 3.2 Suppression rouge-noir
```python
def delete(self, value: T) -> bool:
    """Supprime une valeur avec équilibrage automatique rouge-noir."""
    # 1. Supprimer comme dans un BST normal
    # 2. Gérer les cas de suppression complexes
    # 3. Vérifier et corriger les violations de propriétés
    # 4. Effectuer les recolorations et rotations nécessaires
```

### 4. Méthodes d'équilibrage

#### 4.1 Recoloration
```python
def _recolor_node(self, node: RedBlackNode[T]) -> None:
    """Recolore un nœud selon les règles rouge-noir."""
    # 1. Vérifier la couleur actuelle
    # 2. Appliquer la recoloration appropriée
    # 3. Mettre à jour les compteurs
    # 4. Valider les propriétés
```

#### 4.2 Rotation avec gestion des couleurs
```python
def _rotate_with_color_management(self, node: RedBlackNode[T], direction: str) -> RedBlackNode[T]:
    """Effectue une rotation avec gestion des couleurs."""
    # 1. Effectuer la rotation
    # 2. Gérer les couleurs des nœuds impliqués
    # 3. Mettre à jour les références
    # 4. Valider les propriétés
```

#### 4.3 Correction après insertion
```python
def _fix_insertion_violations(self, node: RedBlackNode[T]) -> None:
    """Corrige les violations de propriétés après insertion."""
    # 1. Identifier le type de violation
    # 2. Appliquer la correction appropriée
    # 3. Répéter si nécessaire
    # 4. Valider les propriétés finales
```

#### 4.4 Correction après suppression
```python
def _fix_deletion_violations(self, node: RedBlackNode[T]) -> None:
    """Corrige les violations de propriétés après suppression."""
    # 1. Identifier le type de violation
    # 2. Appliquer la correction appropriée
    # 3. Répéter si nécessaire
    # 4. Valider les propriétés finales
```

### 5. Méthodes de validation

#### 5.1 Validation des propriétés rouge-noir
```python
def is_red_black_valid(self) -> bool:
    """Valide que l'arbre respecte toutes les propriétés rouge-noir."""
    # 1. Vérifier la propriété de couleur
    # 2. Vérifier la propriété de racine
    # 3. Vérifier la propriété rouge
    # 4. Vérifier la propriété de chemin
    # 5. Retourner True si toutes les propriétés sont respectées
```

#### 5.2 Validation des couleurs
```python
def validate_colors(self) -> bool:
    """Valide que les couleurs sont correctement assignées."""
    # 1. Vérifier que chaque nœud a une couleur valide
    # 2. Vérifier la propriété rouge
    # 3. Vérifier la propriété de racine
    # 4. Retourner True si valide
```

#### 5.3 Validation des chemins
```python
def validate_paths(self) -> bool:
    """Valide que tous les chemins ont le même nombre de nœuds noirs."""
    # 1. Calculer le nombre de nœuds noirs sur chaque chemin
    # 2. Vérifier que tous les chemins ont le même nombre
    # 3. Retourner True si valide
```

### 6. Méthodes de diagnostic

#### 6.1 Analyse des couleurs
```python
def get_color_analysis(self) -> Dict[str, Any]:
    """Analyse la distribution des couleurs dans l'arbre."""
    # 1. Compter les nœuds rouges et noirs
    # 2. Analyser la distribution par niveau
    # 3. Calculer les métriques de couleur
    # 4. Retourner l'analyse
```

#### 6.2 Statistiques d'équilibrage
```python
def get_balancing_stats(self) -> Dict[str, int]:
    """Retourne les statistiques d'équilibrage de l'arbre."""
    # 1. Compter les recolorations
    # 2. Compter les rotations
    # 3. Analyser les types d'opérations
    # 4. Retourner les statistiques
```

#### 6.3 Analyse de performance
```python
def get_performance_analysis(self) -> Dict[str, Any]:
    """Analyse la performance de l'arbre rouge-noir."""
    # 1. Mesurer les temps d'opération
    # 2. Analyser l'efficacité
    # 3. Comparer avec les complexités théoriques
    # 4. Retourner l'analyse
```

### 7. Méthodes utilitaires

#### 7.1 Recherche de nœuds
```python
def find_red_nodes(self) -> List[RedBlackNode[T]]:
    """Retourne tous les nœuds rouges de l'arbre."""
    # 1. Parcourir l'arbre
    # 2. Collecter les nœuds rouges
    # 3. Retourner la liste
```

```python
def find_black_nodes(self) -> List[RedBlackNode[T]]:
    """Retourne tous les nœuds noirs de l'arbre."""
    # 1. Parcourir l'arbre
    # 2. Collecter les nœuds noirs
    # 3. Retourner la liste
```

#### 7.2 Analyse de structure
```python
def get_structure_analysis(self) -> Dict[str, Any]:
    """Analyse la structure de l'arbre rouge-noir."""
    # 1. Calculer les métriques de structure
    # 2. Analyser l'équilibre
    # 3. Identifier les patterns
    # 4. Retourner l'analyse
```

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── red_black_tree.py     # Classe principale RedBlackTree
├── red_black_node.py     # Classe RedBlackNode
├── red_black_rotations.py # Rotations spécialisées
└── red_black_balancing.py # Équilibrage par recoloration
```

### 2. Algorithme d'insertion détaillé
```python
def insert(self, value: T) -> bool:
    """Insertion détaillée avec équilibrage rouge-noir."""
    # Insertion standard BST
    if not super().insert(value):
        return False
    
    # Trouver le nœud inséré
    inserted_node = self._find_node(value)
    if inserted_node is None:
        return False
    
    # Colorer en rouge (sauf si c'est la racine)
    if inserted_node != self._root:
        inserted_node.color = Color.RED
    
    # Corriger les violations
    self._fix_insertion_violations(inserted_node)
    
    # S'assurer que la racine est noire
    if self._root is not None:
        self._root.color = Color.BLACK
    
    return True
```

### 3. Algorithme de suppression détaillé
```python
def delete(self, value: T) -> bool:
    """Suppression détaillée avec équilibrage rouge-noir."""
    # Trouver le nœud à supprimer
    node_to_delete = self._find_node(value)
    if node_to_delete is None:
        return False
    
    # Gérer les cas de suppression
    if node_to_delete.left_child is None:
        self._delete_node_with_at_most_one_child(node_to_delete)
    elif node_to_delete.right_child is None:
        self._delete_node_with_at_most_one_child(node_to_delete)
    else:
        # Nœud avec deux enfants
        successor = self._find_successor(node_to_delete)
        node_to_delete.value = successor.value
        self._delete_node_with_at_most_one_child(successor)
    
    return True
```

### 4. Gestion des violations

#### 4.1 Violations après insertion
```python
def _fix_insertion_violations(self, node: RedBlackNode[T]) -> None:
    """Correction des violations après insertion."""
    while node.parent is not None and node.parent.color == Color.RED:
        if node.parent == node.parent.parent.left_child:
            # Cas 1: Parent gauche
            uncle = node.parent.parent.right_child
            if uncle is not None and uncle.color == Color.RED:
                # Cas 1a: Oncle rouge
                node.parent.color = Color.BLACK
                uncle.color = Color.BLACK
                node.parent.parent.color = Color.RED
                node = node.parent.parent
            else:
                # Cas 1b: Oncle noir
                if node == node.parent.right_child:
                    node = node.parent
                    self._rotate_left(node)
                node.parent.color = Color.BLACK
                node.parent.parent.color = Color.RED
                self._rotate_right(node.parent.parent)
        else:
            # Cas 2: Parent droit (symétrique)
            # ... (implémentation symétrique)
```

### 5. Gestion des erreurs
- `RedBlackTreeError`: Exception de base pour RedBlackTree
- `ColorViolationError`: Violation des propriétés de couleur
- `PathViolationError`: Violation de la propriété de chemin
- `BalancingError`: Erreur d'équilibrage

### 6. Optimisations

#### 6.1 Cache des couleurs
- Mise en cache des calculs de couleur
- Invalidation intelligente du cache
- Recalcul optimisé

#### 6.2 Propagation optimisée
- Propagation des changements uniquement si nécessaire
- Mise à jour en lot
- Arrêt anticipé si aucun changement

## Tests unitaires

### 1. Tests de base
- Test de création et initialisation
- Test d'insertion avec équilibrage
- Test de suppression avec équilibrage
- Test de recherche (héritée de BST)

### 2. Tests d'équilibrage
- Test d'insertion séquentielle
- Test d'insertion en ordre décroissant
- Test d'insertion aléatoire
- Test de suppression avec rééquilibrage

### 3. Tests de propriétés rouge-noir
- Test de validation des propriétés
- Test de validation des couleurs
- Test de validation des chemins
- Test de détection des violations

### 4. Tests de recoloration
- Test de recoloration simple
- Test de recoloration en cascade
- Test de recoloration avec rotation
- Test de séquences de recolorations

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
# Création d'un arbre rouge-noir
rb_tree = RedBlackTree[int]()

# Insertion avec équilibrage automatique
rb_tree.insert(50)
rb_tree.insert(30)
rb_tree.insert(70)
rb_tree.insert(20)
rb_tree.insert(40)
rb_tree.insert(60)
rb_tree.insert(80)

# Vérification des propriétés
assert rb_tree.is_red_black_valid()
assert rb_tree.validate_colors()
assert rb_tree.validate_paths()

# Recherche optimisée
result = rb_tree.search(40)
assert result is not None

# Suppression avec rééquilibrage
rb_tree.delete(30)
assert rb_tree.is_red_black_valid()

# Analyse
color_analysis = rb_tree.get_color_analysis()
balancing_stats = rb_tree.get_balancing_stats()
performance_analysis = rb_tree.get_performance_analysis()
```

## Complexités temporelles

### 1. Opérations de base
- `insert()`: O(log n) garanti
- `delete()`: O(log n) garanti
- `search()`: O(log n) garanti
- `contains()`: O(log n) garanti

### 2. Opérations d'équilibrage
- `_recolor_node()`: O(1)
- `_rotate_with_color_management()`: O(1)
- `_fix_insertion_violations()`: O(log n)
- `_fix_deletion_violations()`: O(log n)

### 3. Validation
- `is_red_black_valid()`: O(n)
- `validate_colors()`: O(n)
- `validate_paths()`: O(n)

### 4. Diagnostic
- `get_color_analysis()`: O(n)
- `get_balancing_stats()`: O(1)
- `get_performance_analysis()`: O(n)

## Critères d'acceptation
- [x] Classe RedBlackTree implémentée et fonctionnelle
- [x] Classe RedBlackNode implémentée et fonctionnelle
- [x] Toutes les propriétés rouge-noir respectées
- [x] Équilibrage automatique par recoloration et rotation
- [x] Complexité O(log n) garantie
- [x] Tests unitaires avec couverture excellente (71 tests au total : 34 pour RedBlackNode, 37 pour RedBlackTree - RedBlackNode: 87%, RedBlackTree: 85%)
- [x] Tests de stress passés
- [x] Documentation complète
- [x] Score Pylint >= 8.5/10
- [x] Performance validée
- [x] Gestion d'erreurs robuste

## Notes pour l'agent de développement
- Cette classe est une alternative à AVLTree
- L'équilibrage par recoloration est plus complexe que les rotations AVL
- Les propriétés rouge-noir doivent être parfaitement respectées
- Les tests doivent être exhaustifs
- La documentation doit être professionnelle
- Privilégier la robustesse sur la performance