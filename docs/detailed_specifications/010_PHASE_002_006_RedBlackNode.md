# Spécification Détaillée - RedBlackNode

## Vue d'ensemble
Cette spécification définit l'implémentation de la classe `RedBlackNode`, nœud spécialisé pour les arbres rouge-noir avec gestion automatique de la couleur et des propriétés rouge-noir.

## Contexte
- **Phase** : Phase 2 - Arbres Équilibrés
- **Priorité** : MOYENNE (nécessaire pour RedBlackTree)
- **Dépendances** : BinaryTreeNode
- **Agent cible** : Agent de développement des nœuds rouge-noir

## Spécifications techniques

### 1. Classe RedBlackNode

#### 1.1 Signature de classe
```python
class RedBlackNode(BinaryTreeNode[T]):
    """Nœud spécialisé pour l'arbre rouge-noir avec gestion de couleur."""
```

#### 1.2 Héritage
```python
class RedBlackNode(BinaryTreeNode[T]):
    """Hérite de BinaryTreeNode et ajoute les propriétés rouge-noir."""
```

#### 1.3 Attributs supplémentaires
- `color`: Couleur du nœud (Color.RED ou Color.BLACK)
- `_black_height`: Hauteur noire du sous-arbre (int, cache)
- `_is_nil`: Indicateur si le nœud est une sentinelle (bool)

### 2. Énumération des couleurs

#### 2.1 Classe Color
```python
class Color(Enum):
    """Énumération des couleurs pour les nœuds rouge-noir."""
    RED = "red"
    BLACK = "black"
```

#### 2.2 Propriétés des couleurs
- `RED`: Couleur rouge pour les nœuds internes
- `BLACK`: Couleur noire pour la racine et les sentinelles

### 3. Constructeur et initialisation

#### 3.1 Constructeur principal
```python
def __init__(self, value: T, parent: Optional['RedBlackNode[T]'] = None, color: Color = Color.RED) -> None:
    """Initialise un nœud rouge-noir avec une valeur, un parent et une couleur."""
    # 1. Appeler le constructeur parent
    # 2. Initialiser la couleur
    # 3. Initialiser la hauteur noire à 0
    # 4. Initialiser l'indicateur de sentinelle à False
```

#### 3.2 Constructeur de sentinelle
```python
@classmethod
def create_nil_node(cls) -> 'RedBlackNode[T]':
    """Crée un nœud sentinelle (NIL) noir."""
    # 1. Créer un nœud avec valeur None
    # 2. Définir la couleur comme BLACK
    # 3. Marquer comme sentinelle
    # 4. Retourner le nœud sentinelle
```

#### 3.3 Constructeur de copie
```python
def __init__(self, other: 'RedBlackNode[T]') -> None:
    """Crée une copie profonde d'un nœud rouge-noir."""
    # 1. Copier la valeur
    # 2. Copier la couleur
    # 3. Copier les propriétés rouge-noir
    # 4. Récursivement copier les enfants
```

### 4. Propriétés et accesseurs

#### 4.1 Propriétés de base
- `color` (property): Couleur du nœud en lecture seule
- `is_red` (property): Vérifie si le nœud est rouge
- `is_black` (property): Vérifie si le nœud est noir
- `is_nil` (property): Vérifie si le nœud est une sentinelle
- `black_height` (property): Hauteur noire du sous-arbre

#### 4.2 Méthodes d'accès
- `get_color() -> Color`: Retourne la couleur du nœud
- `get_black_height() -> int`: Retourne la hauteur noire
- `is_red_node() -> bool`: Vérifie si le nœud est rouge
- `is_black_node() -> bool`: Vérifie si le nœud est noir

### 5. Méthodes de gestion des couleurs

#### 5.1 Changement de couleur
```python
def set_color(self, color: Color) -> None:
    """Définit la couleur du nœud."""
    # 1. Valider la couleur
    # 2. Mettre à jour la couleur
    # 3. Mettre à jour la hauteur noire
    # 4. Propager les changements si nécessaire
```

#### 5.2 Inversion de couleur
```python
def flip_color(self) -> None:
    """Inverse la couleur du nœud."""
    # 1. Vérifier que le nœud n'est pas une sentinelle
    # 2. Inverser la couleur
    # 3. Mettre à jour la hauteur noire
    # 4. Valider les propriétés
```

#### 5.3 Mise à jour de la hauteur noire
```python
def update_black_height(self) -> None:
    """Met à jour la hauteur noire du nœud."""
    # 1. Calculer la hauteur noire des enfants
    # 2. Ajouter 1 si le nœud est noir
    # 3. Mettre à jour la hauteur noire
    # 4. Propager vers le parent
```

### 6. Méthodes de validation

#### 6.1 Validation des propriétés rouge-noir
```python
def is_red_black_valid(self) -> bool:
    """Valide que le nœud respecte les propriétés rouge-noir."""
    # 1. Vérifier que la couleur est valide
    # 2. Vérifier la propriété rouge (si rouge, enfants noirs)
    # 3. Vérifier la hauteur noire
    # 4. Vérifier récursivement les enfants
```

#### 6.2 Validation de la couleur
```python
def validate_color(self) -> bool:
    """Valide que la couleur est correctement assignée."""
    # 1. Vérifier que la couleur est valide
    # 2. Vérifier les contraintes de couleur
    # 3. Vérifier la cohérence avec les enfants
    # 4. Retourner True si valide
```

#### 6.3 Validation de la hauteur noire
```python
def validate_black_height(self) -> bool:
    """Valide que la hauteur noire est correctement calculée."""
    # 1. Calculer la hauteur noire réelle
    # 2. Comparer avec la hauteur stockée
    # 3. Vérifier la cohérence
    # 4. Retourner True si valide
```

### 7. Méthodes utilitaires

#### 7.1 Analyse du nœud
```python
def get_node_info(self) -> Dict[str, Any]:
    """Retourne les informations complètes du nœud."""
    # 1. Collecter toutes les propriétés
    # 2. Calculer les statistiques de couleur
    # 3. Retourner un dictionnaire structuré
```

#### 7.2 Comparaison de nœuds
```python
def compare_with(self, other: 'RedBlackNode[T]') -> Dict[str, Any]:
    """Compare ce nœud avec un autre nœud rouge-noir."""
    # 1. Comparer les valeurs
    # 2. Comparer les couleurs
    # 3. Comparer les propriétés rouge-noir
    # 4. Retourner un rapport de comparaison
```

#### 7.3 Diagnostic du nœud
```python
def diagnose(self) -> Dict[str, Any]:
    """Effectue un diagnostic complet du nœud."""
    # 1. Valider toutes les propriétés
    # 2. Détecter les problèmes potentiels
    # 3. Analyser la couleur et la hauteur noire
    # 4. Retourner un rapport de diagnostic
```

### 8. Méthodes de sérialisation

#### 8.1 Sérialisation en dictionnaire
```python
def to_dict(self) -> Dict[str, Any]:
    """Sérialise le nœud en dictionnaire."""
    # 1. Inclure la valeur
    # 2. Inclure la couleur
    # 3. Inclure les propriétés rouge-noir
    # 4. Récursivement sérialiser les enfants
```

#### 8.2 Désérialisation depuis dictionnaire
```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'RedBlackNode[T]':
    """Désérialise un nœud depuis un dictionnaire."""
    # 1. Créer le nœud avec la valeur
    # 2. Restaurer la couleur
    # 3. Restaurer les propriétés rouge-noir
    # 4. Récursivement désérialiser les enfants
```

### 9. Méthodes de visualisation

#### 9.1 Représentation textuelle
```python
def to_string(self, indent: int = 0) -> str:
    """Retourne une représentation textuelle du nœud."""
    # 1. Formater la valeur et la couleur
    # 2. Indenter selon le niveau
    # 3. Inclure les enfants récursivement
```

#### 9.2 Représentation compacte
```python
def to_compact_string(self) -> str:
    """Retourne une représentation compacte du nœud."""
    # 1. Format: "value(color)"
    # 2. color = R pour rouge, B pour noir
```

#### 9.3 Représentation colorée
```python
def to_colored_string(self) -> str:
    """Retourne une représentation colorée du nœud."""
    # 1. Utiliser des codes couleur ANSI
    # 2. Rouge pour les nœuds rouges
    # 3. Noir pour les nœuds noirs
```

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── red_black_node.py     # Classe principale RedBlackNode
├── color.py              # Énumération Color
└── red_black_node_utils.py # Utilitaires pour RedBlackNode
```

### 2. Gestion des références

#### 2.1 Surcharge des setters
```python
def set_left_child(self, child: Optional['RedBlackNode[T]']) -> None:
    """Définit l'enfant gauche avec mise à jour automatique."""
    # 1. Appeler la méthode parent
    # 2. Mettre à jour les propriétés rouge-noir
    # 3. Propager les changements vers le parent
```

```python
def set_right_child(self, child: Optional['RedBlackNode[T]']) -> None:
    """Définit l'enfant droit avec mise à jour automatique."""
    # 1. Appeler la méthode parent
    # 2. Mettre à jour les propriétés rouge-noir
    # 3. Propager les changements vers le parent
```

### 3. Calcul de la hauteur noire

#### 3.1 Algorithme de calcul
```python
def calculate_black_height(self) -> int:
    """Calcule la hauteur noire du nœud."""
    if self.is_nil:
        return 0
    
    # Calculer la hauteur noire des enfants
    left_height = self.left_child.black_height if self.left_child else 0
    right_height = self.right_child.black_height if self.right_child else 0
    
    # Vérifier la cohérence
    if left_height != right_height:
        raise BlackHeightMismatchError("Hauteurs noires incohérentes")
    
    # Ajouter 1 si le nœud est noir
    return left_height + (1 if self.is_black else 0)
```

### 4. Gestion des erreurs
- `RedBlackNodeError`: Exception de base pour RedBlackNode
- `InvalidColorError`: Couleur invalide
- `BlackHeightMismatchError`: Incohérence de hauteur noire
- `NodeValidationError`: Erreur de validation du nœud

### 5. Optimisations

#### 5.1 Cache de la hauteur noire
- Mise en cache de la hauteur noire
- Invalidation du cache lors des modifications
- Recalcul automatique si nécessaire

#### 5.2 Propagation optimisée
- Propagation des changements uniquement si nécessaire
- Mise à jour en lot pour les opérations multiples
- Arrêt anticipé si aucun changement

## Tests unitaires

### 1. Tests de base
- Test de création et initialisation
- Test des propriétés de base
- Test des accesseurs
- Test des méthodes de gestion des couleurs

### 2. Tests de validation
- Test de validation des propriétés rouge-noir
- Test de validation de la couleur
- Test de validation de la hauteur noire
- Test de détection des erreurs

### 3. Tests de gestion des couleurs
- Test de changement de couleur
- Test d'inversion de couleur
- Test de mise à jour de la hauteur noire
- Test de cohérence après changement

### 4. Tests de sérialisation
- Test de sérialisation en dictionnaire
- Test de désérialisation depuis dictionnaire
- Test de cohérence après sérialisation/désérialisation
- Test avec nœuds complexes

### 5. Tests de visualisation
- Test de représentation textuelle
- Test de représentation compacte
- Test de représentation colorée
- Test avec différents niveaux d'indentation

### 6. Tests de performance
- Test de mise à jour rapide
- Test de propagation efficace
- Test avec de gros sous-arbres
- Test de cache de la hauteur noire

### 7. Tests de sentinelle
- Test de création de nœud sentinelle
- Test des propriétés de sentinelle
- Test de validation de sentinelle
- Test d'utilisation dans l'arbre

## Documentation

### 1. Docstrings
- Documentation complète en reStructuredText
- Exemples d'utilisation détaillés
- Description des propriétés rouge-noir
- Documentation des complexités

### 2. Exemples d'utilisation
```python
# Création d'un nœud rouge-noir
node = RedBlackNode[int](42, color=Color.RED)

# Gestion des couleurs
node.set_color(Color.BLACK)
node.flip_color()

# Accès aux propriétés
color = node.color
is_red = node.is_red
is_black = node.is_black
black_height = node.black_height

# Validation
assert node.is_red_black_valid()
assert node.validate_color()
assert node.validate_black_height()

# Diagnostic
info = node.get_node_info()
diagnosis = node.diagnose()

# Sérialisation
data = node.to_dict()
restored = RedBlackNode.from_dict(data)

# Visualisation
text_repr = node.to_string()
compact_repr = node.to_compact_string()
colored_repr = node.to_colored_string()

# Création de sentinelle
nil_node = RedBlackNode.create_nil_node()
assert nil_node.is_nil
assert nil_node.is_black
```

## Complexités temporelles

### 1. Opérations de base
- `__init__()`: O(1)
- `set_color()`: O(1)
- `flip_color()`: O(1)
- `update_black_height()`: O(h) où h est la hauteur

### 2. Validation
- `is_red_black_valid()`: O(n) où n est la taille du sous-arbre
- `validate_color()`: O(1)
- `validate_black_height()`: O(1)

### 3. Utilitaires
- `get_node_info()`: O(n)
- `diagnose()`: O(n)
- `to_dict()`: O(n)
- `from_dict()`: O(n)

### 4. Visualisation
- `to_string()`: O(n)
- `to_compact_string()`: O(1)
- `to_colored_string()`: O(1)

## Critères d'acceptation
- [ ] Classe RedBlackNode implémentée et fonctionnelle
- [ ] Toutes les propriétés rouge-noir gérées automatiquement
- [ ] Gestion automatique des couleurs et hauteurs noires
- [ ] Validation complète des propriétés rouge-noir
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Documentation complète
- [ ] Score Pylint >= 8.5/10
- [ ] Performance optimisée
- [ ] Sérialisation/désérialisation fonctionnelle
- [ ] Gestion d'erreurs robuste
- [ ] Support des nœuds sentinelles

## Notes pour l'agent de développement
- Cette classe est fondamentale pour RedBlackTree
- Les propriétés rouge-noir doivent être maintenues automatiquement
- La gestion des couleurs est critique
- Les tests doivent couvrir tous les cas limites
- La documentation doit être exhaustive
- Privilégier la robustesse et la cohérence