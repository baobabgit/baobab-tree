# Spécification Détaillée - TreeNode (PRIORITÉ CRITIQUE)

## Vue d'ensemble
Cette spécification définit l'implémentation de la classe `TreeNode`, classe abstraite de base pour tous les nœuds d'arbres dans la librairie. Cette classe est critique car elle sert de fondation à tous les autres types d'arbres, notamment l'AVL.

## Contexte
- **Phase** : Phase 1 - Fondations
- **Priorité** : CRITIQUE (nécessaire pour AVL)
- **Dépendances** : Aucune
- **Agent cible** : Agent de développement des structures de base

## Spécifications techniques

### 1. Classe TreeNode

#### 1.1 Signature de classe
```python
class TreeNode(ABC):
    """Classe abstraite de base pour tous les nœuds d'arbres."""
```

#### 1.2 Attributs
- `value`: Valeur stockée dans le nœud (générique)
- `parent`: Référence vers le nœud parent (optionnel)
- `children`: Liste des nœuds enfants (optionnel)
- `metadata`: Dictionnaire pour métadonnées supplémentaires

#### 1.3 Méthodes abstraites
- `is_leaf() -> bool`: Vérifie si le nœud est une feuille
- `is_root() -> bool`: Vérifie si le nœud est la racine
- `get_height() -> int`: Calcule la hauteur du nœud
- `get_depth() -> int`: Calcule la profondeur du nœud
- `validate() -> bool`: Valide les propriétés du nœud

#### 1.4 Méthodes concrètes
- `add_child(child: 'TreeNode') -> None`: Ajoute un enfant
- `remove_child(child: 'TreeNode') -> bool`: Supprime un enfant
- `get_children() -> List['TreeNode']`: Retourne les enfants
- `get_parent() -> Optional['TreeNode']`: Retourne le parent
- `set_parent(parent: Optional['TreeNode']) -> None`: Définit le parent
- `clear_metadata() -> None`: Efface les métadonnées
- `set_metadata(key: str, value: Any) -> None`: Définit une métadonnée
- `get_metadata(key: str, default: Any = None) -> Any`: Récupère une métadonnée

### 2. Classe BinaryTreeNode

#### 2.1 Signature de classe
```python
class BinaryTreeNode(TreeNode):
    """Nœud spécialisé pour les arbres binaires."""
```

#### 2.2 Attributs supplémentaires
- `left`: Nœud enfant gauche (optionnel)
- `right`: Nœud enfant droit (optionnel)

#### 2.3 Méthodes spécialisées
- `set_left(node: Optional['BinaryTreeNode']) -> None`: Définit l'enfant gauche
- `set_right(node: Optional['BinaryTreeNode']) -> None`: Définit l'enfant droit
- `get_left() -> Optional['BinaryTreeNode']`: Retourne l'enfant gauche
- `get_right() -> Optional['BinaryTreeNode']`: Retourne l'enfant droit
- `has_left() -> bool`: Vérifie la présence d'un enfant gauche
- `has_right() -> bool`: Vérifie la présence d'un enfant droit
- `is_leaf() -> bool`: Vérifie si c'est une feuille (surcharge)
- `get_children() -> List['BinaryTreeNode']`: Retourne les enfants (surcharge)

### 3. Interfaces et types

#### 3.1 Type générique
```python
T = TypeVar('T', bound=Comparable)
```

#### 3.2 Interface Comparable
```python
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
```

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── tree_node.py          # Classe TreeNode
├── binary_tree_node.py   # Classe BinaryTreeNode
└── interfaces.py         # Interfaces et types
```

### 2. Gestion des erreurs
- `TreeNodeError`: Exception de base pour les erreurs de nœud
- `InvalidNodeOperationError`: Opération invalide sur un nœud
- `CircularReferenceError`: Référence circulaire détectée

### 3. Validation
- Validation des références parent-enfant
- Détection des références circulaires
- Validation des métadonnées

### 4. Performance
- Accès O(1) aux enfants directs
- Calcul de hauteur en O(h) où h est la hauteur
- Gestion mémoire optimisée

## Tests unitaires

### 1. Tests TreeNode
- Test de création et initialisation
- Test des méthodes abstraites (avec implémentation de test)
- Test de gestion des métadonnées
- Test de validation des nœuds
- Test de gestion des erreurs

### 2. Tests BinaryTreeNode
- Test de création et initialisation
- Test des opérations gauche/droite
- Test de la validation des propriétés binaires
- Test des méthodes héritées
- Test des cas limites

### 3. Tests d'intégration
- Test de création d'arbres simples
- Test de navigation parent-enfant
- Test de validation d'arbres complets

## Documentation

### 1. Docstrings
- Documentation complète en reStructuredText
- Exemples d'utilisation pour chaque méthode
- Description des paramètres et valeurs de retour
- Documentation des exceptions

### 2. Exemples d'utilisation
```python
# Création d'un nœud binaire
node = BinaryTreeNode(value=42)
node.set_left(BinaryTreeNode(value=21))
node.set_right(BinaryTreeNode(value=84))

# Vérification des propriétés
assert not node.is_leaf()
assert node.get_height() == 1
assert node.get_depth() == 0
```

## Critères d'acceptation
- [ ] Classe TreeNode implémentée et testée
- [ ] Classe BinaryTreeNode implémentée et testée
- [ ] Toutes les méthodes abstraites définies
- [ ] Gestion d'erreurs complète
- [ ] Tests unitaires avec couverture >= 95%
- [ ] Documentation complète
- [ ] Score Pylint >= 8.5/10

## Notes pour l'agent de développement
- Cette classe est la fondation de toute la librairie
- La robustesse est plus importante que la performance
- Les interfaces doivent être claires et extensibles
- Privilégier la simplicité et la lisibilité du code
- Les tests doivent couvrir tous les cas limites