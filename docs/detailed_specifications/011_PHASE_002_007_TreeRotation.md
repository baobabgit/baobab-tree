# Spécification Détaillée - TreeRotation

## Vue d'ensemble
Cette spécification définit l'implémentation de la classe abstraite `TreeRotation` et ses implémentations concrètes pour les rotations d'arbres équilibrés.

## Contexte
- **Phase** : Phase 2 - Arbres Équilibrés
- **Priorité** : MOYENNE (utilitaire pour les arbres équilibrés)
- **Dépendances** : BinaryTreeNode
- **Agent cible** : Agent de développement des rotations d'arbres

## Spécifications techniques

### 1. Classe abstraite TreeRotation

#### 1.1 Signature de classe
```python
class TreeRotation(ABC, Generic[T]):
    """Classe abstraite pour les rotations d'arbres équilibrés."""
```

#### 1.2 Caractéristiques
- Classe abstraite avec méthodes abstraites
- Support générique pour différents types de nœuds
- Interface commune pour toutes les rotations
- Gestion des références parent/enfant

### 2. Méthodes abstraites

#### 2.1 Méthode de rotation principale
```python
@abstractmethod
def rotate(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
    """Effectue la rotation sur le nœud donné."""
    pass
```

#### 2.2 Méthode de validation
```python
@abstractmethod
def can_rotate(self, node: BinaryTreeNode[T]) -> bool:
    """Vérifie si la rotation peut être effectuée."""
    pass
```

#### 2.3 Méthode de description
```python
@abstractmethod
def get_description(self) -> str:
    """Retourne une description de la rotation."""
    pass
```

### 3. Méthodes concrètes communes

#### 3.1 Validation pré-rotation
```python
def validate_before_rotation(self, node: BinaryTreeNode[T]) -> bool:
    """Valide qu'une rotation peut être effectuée."""
    # 1. Vérifier que le nœud existe
    # 2. Vérifier que les enfants nécessaires existent
    # 3. Appeler can_rotate pour validation spécifique
    # 4. Retourner True si valide
```

#### 3.2 Validation post-rotation
```python
def validate_after_rotation(self, node: BinaryTreeNode[T]) -> bool:
    """Valide qu'une rotation a été effectuée correctement."""
    # 1. Vérifier la cohérence des références
    # 2. Vérifier les propriétés de l'arbre
    # 3. Vérifier la structure résultante
    # 4. Retourner True si valide
```

#### 3.3 Gestion des références parent
```python
def update_parent_references(self, old_root: BinaryTreeNode[T], new_root: BinaryTreeNode[T]) -> None:
    """Met à jour les références parent après une rotation."""
    # 1. Obtenir le parent de l'ancienne racine
    # 2. Mettre à jour la référence parent vers la nouvelle racine
    # 3. Mettre à jour la référence parent de la nouvelle racine
    # 4. Valider les références
```

### 4. Implémentations concrètes

#### 4.1 Classe LeftRotation
```python
class LeftRotation(TreeRotation[T]):
    """Rotation gauche pour équilibrer les arbres."""
    
    def rotate(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """Effectue une rotation gauche."""
        # 1. Sauvegarder l'enfant droit
        # 2. Remplacer l'enfant droit par l'enfant gauche de l'enfant droit
        # 3. Définir le nœud comme enfant gauche de l'enfant droit
        # 4. Mettre à jour les références parent
        # 5. Retourner la nouvelle racine
```

#### 4.2 Classe RightRotation
```python
class RightRotation(TreeRotation[T]):
    """Rotation droite pour équilibrer les arbres."""
    
    def rotate(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """Effectue une rotation droite."""
        # 1. Sauvegarder l'enfant gauche
        # 2. Remplacer l'enfant gauche par l'enfant droit de l'enfant gauche
        # 3. Définir le nœud comme enfant droit de l'enfant gauche
        # 4. Mettre à jour les références parent
        # 5. Retourner la nouvelle racine
```

#### 4.3 Classe LeftRightRotation
```python
class LeftRightRotation(TreeRotation[T]):
    """Rotation gauche-droite (double rotation)."""
    
    def rotate(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """Effectue une rotation gauche-droite."""
        # 1. Effectuer une rotation gauche sur l'enfant gauche
        # 2. Effectuer une rotation droite sur le nœud
        # 3. Mettre à jour toutes les références
        # 4. Retourner la nouvelle racine
```

#### 4.4 Classe RightLeftRotation
```python
class RightLeftRotation(TreeRotation[T]):
    """Rotation droite-gauche (double rotation)."""
    
    def rotate(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """Effectue une rotation droite-gauche."""
        # 1. Effectuer une rotation droite sur l'enfant droit
        # 2. Effectuer une rotation gauche sur le nœud
        # 3. Mettre à jour toutes les références
        # 4. Retourner la nouvelle racine
```

### 5. Méthodes utilitaires

#### 5.1 Factory de rotations
```python
class RotationFactory:
    """Factory pour créer des instances de rotations."""
    
    @staticmethod
    def create_rotation(rotation_type: str) -> TreeRotation[T]:
        """Crée une rotation selon le type spécifié."""
        # 1. Valider le type de rotation
        # 2. Créer l'instance appropriée
        # 3. Retourner la rotation
```

#### 5.2 Sélecteur de rotation
```python
class RotationSelector:
    """Sélecteur automatique de rotation selon le contexte."""
    
    @staticmethod
    def select_rotation(node: BinaryTreeNode[T], context: Dict[str, Any]) -> TreeRotation[T]:
        """Sélectionne la rotation appropriée selon le contexte."""
        # 1. Analyser le contexte
        # 2. Identifier le type de déséquilibre
        # 3. Sélectionner la rotation appropriée
        # 4. Retourner la rotation
```

### 6. Méthodes de diagnostic

#### 6.1 Analyse de rotation
```python
def analyze_rotation(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
    """Analyse l'effet d'une rotation avant de l'effectuer."""
    # 1. Analyser l'état actuel du nœud
    # 2. Prédire l'effet de la rotation
    # 3. Calculer les métriques de performance
    # 4. Retourner un rapport d'analyse
```

#### 6.2 Statistiques de rotation
```python
def get_rotation_stats(self, node: BinaryTreeNode[T]) -> Dict[str, Any]:
    """Retourne les statistiques de rotation du sous-arbre."""
    # 1. Compter les rotations effectuées
    # 2. Analyser les types de rotations
    # 3. Calculer les métriques de performance
    # 4. Retourner les statistiques
```

### 7. Méthodes de validation

#### 7.1 Validation de cohérence
```python
def validate_consistency(self, node: BinaryTreeNode[T]) -> bool:
    """Valide la cohérence de l'arbre après rotation."""
    # 1. Vérifier la cohérence des références
    # 2. Vérifier les propriétés de l'arbre
    # 3. Vérifier la structure résultante
    # 4. Retourner True si cohérent
```

#### 7.2 Validation des propriétés
```python
def validate_properties(self, node: BinaryTreeNode[T]) -> Dict[str, bool]:
    """Valide les propriétés spécifiques de l'arbre après rotation."""
    # 1. Vérifier les propriétés de base
    # 2. Vérifier les propriétés d'équilibre
    # 3. Vérifier les propriétés spécifiques
    # 4. Retourner un rapport de validation
```

## Implémentation détaillée

### 1. Structure des fichiers
```
src/
├── tree_rotation.py       # Classe abstraite TreeRotation
├── left_rotation.py       # Implémentation LeftRotation
├── right_rotation.py      # Implémentation RightRotation
├── left_right_rotation.py # Implémentation LeftRightRotation
├── right_left_rotation.py # Implémentation RightLeftRotation
├── rotation_factory.py   # Factory pour les rotations
└── rotation_selector.py   # Sélecteur de rotations
```

### 2. Algorithme de rotation gauche détaillé
```python
class LeftRotation(TreeRotation[T]):
    def rotate(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """Rotation gauche détaillée."""
        # Validation pré-rotation
        if not self.validate_before_rotation(node):
            raise RotationError("Rotation gauche invalide")
        
        # Sauvegarde des références
        right_child = node.right_child
        if right_child is None:
            raise RotationError("Pas d'enfant droit pour rotation gauche")
        
        # Effectuer la rotation
        node.set_right_child(right_child.left_child)
        right_child.set_left_child(node)
        
        # Mise à jour des références parent
        self.update_parent_references(node, right_child)
        
        # Validation post-rotation
        if not self.validate_after_rotation(right_child):
            raise RotationError("Rotation gauche échouée")
        
        return right_child
    
    def can_rotate(self, node: BinaryTreeNode[T]) -> bool:
        """Vérifie si une rotation gauche peut être effectuée."""
        return node is not None and node.right_child is not None
    
    def get_description(self) -> str:
        """Retourne la description de la rotation gauche."""
        return "Rotation gauche: l'enfant droit devient la racine"
```

### 3. Algorithme de rotation droite détaillé
```python
class RightRotation(TreeRotation[T]):
    def rotate(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        """Rotation droite détaillée."""
        # Validation pré-rotation
        if not self.validate_before_rotation(node):
            raise RotationError("Rotation droite invalide")
        
        # Sauvegarde des références
        left_child = node.left_child
        if left_child is None:
            raise RotationError("Pas d'enfant gauche pour rotation droite")
        
        # Effectuer la rotation
        node.set_left_child(left_child.right_child)
        left_child.set_right_child(node)
        
        # Mise à jour des références parent
        self.update_parent_references(node, left_child)
        
        # Validation post-rotation
        if not self.validate_after_rotation(left_child):
            raise RotationError("Rotation droite échouée")
        
        return left_child
    
    def can_rotate(self, node: BinaryTreeNode[T]) -> bool:
        """Vérifie si une rotation droite peut être effectuée."""
        return node is not None and node.left_child is not None
    
    def get_description(self) -> str:
        """Retourne la description de la rotation droite."""
        return "Rotation droite: l'enfant gauche devient la racine"
```

### 4. Gestion des erreurs
- `RotationError`: Exception de base pour les rotations
- `InvalidRotationError`: Rotation invalide
- `MissingChildError`: Enfant manquant pour la rotation
- `RotationValidationError`: Échec de validation

### 5. Optimisations

#### 5.1 Cache des références
- Mise en cache des références parent
- Invalidation intelligente du cache
- Recalcul optimisé

#### 5.2 Propagation optimisée
- Propagation des changements uniquement si nécessaire
- Mise à jour en lot
- Arrêt anticipé si aucun changement

## Tests unitaires

### 1. Tests de base
- Test de création des rotations
- Test de validation pré-rotation
- Test de validation post-rotation
- Test de gestion des références parent

### 2. Tests de rotation gauche
- Test de rotation gauche simple
- Test de rotation gauche avec validation
- Test de rotation gauche avec erreurs
- Test de rotation gauche avec gros arbres

### 3. Tests de rotation droite
- Test de rotation droite simple
- Test de rotation droite avec validation
- Test de rotation droite avec erreurs
- Test de rotation droite avec gros arbres

### 4. Tests de rotations doubles
- Test de rotation gauche-droite
- Test de rotation droite-gauche
- Test de validation des rotations doubles
- Test de performance des rotations doubles

### 5. Tests de factory et sélecteur
- Test de création par factory
- Test de sélection automatique
- Test de validation des types
- Test de gestion des erreurs

### 6. Tests de diagnostic
- Test d'analyse de rotation
- Test de statistiques de rotation
- Test de validation de cohérence
- Test de validation des propriétés

### 7. Tests d'intégration
- Test avec différents types d'arbres
- Test avec différents types de nœuds
- Test de séquences de rotations
- Test de récupération après erreur

## Documentation

### 1. Docstrings
- Documentation complète en reStructuredText
- Exemples d'utilisation détaillés
- Description des algorithmes de rotation
- Documentation des complexités

### 2. Exemples d'utilisation
```python
# Création de rotations
left_rotation = LeftRotation[int]()
right_rotation = RightRotation[int]()
left_right_rotation = LeftRightRotation[int]()
right_left_rotation = RightLeftRotation[int]()

# Effectuer des rotations
new_root = left_rotation.rotate(node)
new_root = right_rotation.rotate(node)
new_root = left_right_rotation.rotate(node)
new_root = right_left_rotation.rotate(node)

# Validation
can_rotate = left_rotation.can_rotate(node)
is_valid = left_rotation.validate_before_rotation(node)
is_correct = left_rotation.validate_after_rotation(new_root)

# Factory et sélecteur
rotation = RotationFactory.create_rotation("left")
rotation = RotationSelector.select_rotation(node, context)

# Diagnostic
analysis = left_rotation.analyze_rotation(node)
stats = left_rotation.get_rotation_stats(node)
is_consistent = left_rotation.validate_consistency(node)
properties = left_rotation.validate_properties(node)
```

## Complexités temporelles

### 1. Rotations simples
- `rotate()`: O(1)
- `can_rotate()`: O(1)
- `validate_before_rotation()`: O(1)
- `validate_after_rotation()`: O(1)

### 2. Rotations doubles
- `rotate()`: O(1)
- `can_rotate()`: O(1)
- `validate_before_rotation()`: O(1)
- `validate_after_rotation()`: O(1)

### 3. Méthodes utilitaires
- `update_parent_references()`: O(1)
- `analyze_rotation()`: O(1)
- `get_rotation_stats()`: O(n) où n est la taille du sous-arbre
- `validate_consistency()`: O(1)

### 4. Factory et sélecteur
- `create_rotation()`: O(1)
- `select_rotation()`: O(1)

## Critères d'acceptation
- [x] Classe abstraite TreeRotation implémentée
- [x] Toutes les rotations concrètes implémentées
- [x] Factory et sélecteur fonctionnels
- [x] Validation complète des rotations
- [x] Tests unitaires avec couverture >= 95%
- [x] Documentation complète
- [x] Score Pylint >= 8.5/10
- [x] Performance optimisée (O(1) pour rotations)
- [x] Gestion d'erreurs robuste
- [x] Méthodes de diagnostic fonctionnelles

## Notes pour l'agent de développement
- Cette classe est utilitaire pour tous les arbres équilibrés
- Les rotations doivent être parfaitement implémentées
- La validation doit être exhaustive
- Les tests doivent couvrir tous les cas limites
- La documentation doit être professionnelle
- Privilégier la robustesse et la cohérence