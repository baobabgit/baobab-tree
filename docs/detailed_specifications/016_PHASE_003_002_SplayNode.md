# Spécification détaillée - SplayNode

## Vue d'ensemble
SplayNode est le nœud spécialisé pour l'arbre Splay, conçu pour supporter les opérations d'auto-ajustement et maintenir les propriétés de l'arbre binaire de recherche.

## Objectifs
- Fournir une structure de nœud optimisée pour Splay
- Supporter les opérations de rotation et splay
- Maintenir les pointeurs parent pour les opérations efficaces
- Optimiser la gestion mémoire

## Structure de données

### SplayNode
```cpp
template<typename T>
class SplayNode {
public:
    T data;
    SplayNode<T>* left;
    SplayNode<T>* right;
    SplayNode<T>* parent;
    
    // Constructeurs
    SplayNode(const T& value);
    SplayNode(const T& value, SplayNode<T>* parent);
    ~SplayNode();
    
    // Opérations de base
    bool isLeaf() const;
    bool hasLeftChild() const;
    bool hasRightChild() const;
    bool hasParent() const;
    bool isLeftChild() const;
    bool isRightChild() const;
    bool isRoot() const;
    
    // Opérations de navigation
    SplayNode<T>* getLeftmost();
    SplayNode<T>* getRightmost();
    SplayNode<T>* getSuccessor();
    SplayNode<T>* getPredecessor();
    
    // Opérations de rotation
    SplayNode<T>* rotateLeft();
    SplayNode<T>* rotateRight();
    
    // Opérations de splay
    SplayNode<T>* splay();
    SplayNode<T>* zig();
    SplayNode<T>* zigZig();
    SplayNode<T>* zigZag();
    
    // Opérations de maintenance
    void updateParent(SplayNode<T>* newParent);
    void detachFromParent();
    void swapWith(SplayNode<T>* other);
    
    // Opérations de debug
    void print() const;
    int getHeight() const;
    int getBalance() const;
    bool isValid() const;
    
    // Opérations de comparaison
    bool operator<(const SplayNode<T>& other) const;
    bool operator>(const SplayNode<T>& other) const;
    bool operator==(const SplayNode<T>& other) const;
};
```

## Algorithmes principaux

### 1. Constructeurs
```cpp
template<typename T>
SplayNode<T>::SplayNode(const T& value) 
    : data(value), left(nullptr), right(nullptr), parent(nullptr) {}

template<typename T>
SplayNode<T>::SplayNode(const T& value, SplayNode<T>* parent) 
    : data(value), left(nullptr), right(nullptr), parent(parent) {}
```

### 2. Opérations de navigation
```cpp
template<typename T>
SplayNode<T>* SplayNode<T>::getLeftmost() {
    SplayNode<T>* current = this;
    while (current->left) {
        current = current->left;
    }
    return current;
}

template<typename T>
SplayNode<T>* SplayNode<T>::getRightmost() {
    SplayNode<T>* current = this;
    while (current->right) {
        current = current->right;
    }
    return current;
}

template<typename T>
SplayNode<T>* SplayNode<T>::getSuccessor() {
    if (right) {
        return right->getLeftmost();
    }
    
    SplayNode<T>* current = this;
    SplayNode<T>* parent = this->parent;
    
    while (parent && current == parent->right) {
        current = parent;
        parent = parent->parent;
    }
    
    return parent;
}
```

### 3. Opérations de rotation
```cpp
template<typename T>
SplayNode<T>* SplayNode<T>::rotateLeft() {
    if (!right) return this;
    
    SplayNode<T>* newRoot = right;
    SplayNode<T>* parent = this->parent;
    
    // Mise à jour des pointeurs
    right = newRoot->left;
    if (right) right->parent = this;
    
    newRoot->left = this;
    this->parent = newRoot;
    
    newRoot->parent = parent;
    if (parent) {
        if (parent->left == this) {
            parent->left = newRoot;
        } else {
            parent->right = newRoot;
        }
    }
    
    return newRoot;
}

template<typename T>
SplayNode<T>* SplayNode<T>::rotateRight() {
    if (!left) return this;
    
    SplayNode<T>* newRoot = left;
    SplayNode<T>* parent = this->parent;
    
    // Mise à jour des pointeurs
    left = newRoot->right;
    if (left) left->parent = this;
    
    newRoot->right = this;
    this->parent = newRoot;
    
    newRoot->parent = parent;
    if (parent) {
        if (parent->left == this) {
            parent->left = newRoot;
        } else {
            parent->right = newRoot;
        }
    }
    
    return newRoot;
}
```

### 4. Opérations de splay
```cpp
template<typename T>
SplayNode<T>* SplayNode<T>::splay() {
    SplayNode<T>* current = this;
    
    while (current->parent) {
        SplayNode<T>* parent = current->parent;
        SplayNode<T>* grandparent = parent->parent;
        
        if (!grandparent) {
            // Cas zig
            if (current == parent->left) {
                parent->rotateRight();
            } else {
                parent->rotateLeft();
            }
        } else if (current == parent->left && parent == grandparent->left) {
            // Cas zig-zig
            grandparent->rotateRight();
            parent->rotateRight();
        } else if (current == parent->right && parent == grandparent->right) {
            // Cas zig-zig
            grandparent->rotateLeft();
            parent->rotateLeft();
        } else if (current == parent->left && parent == grandparent->right) {
            // Cas zig-zag
            parent->rotateRight();
            grandparent->rotateLeft();
        } else {
            // Cas zig-zag
            parent->rotateLeft();
            grandparent->rotateRight();
        }
    }
    
    return current;
}
```

## Propriétés

### 1. Structure de nœud
- **data** : Valeur stockée dans le nœud
- **left** : Pointeur vers le fils gauche
- **right** : Pointeur vers le fils droit
- **parent** : Pointeur vers le parent (essentiel pour splay)

### 2. Navigation efficace
- Accès direct aux enfants et parent
- Méthodes de navigation optimisées
- Support des opérations de rotation

### 3. Gestion mémoire
- Constructeurs et destructeurs appropriés
- Gestion des pointeurs parent
- Éviter les cycles et fuites

## Opérations spécialisées

### 1. Détection de position
```cpp
template<typename T>
bool SplayNode<T>::isLeftChild() const {
    return parent && parent->left == this;
}

template<typename T>
bool SplayNode<T>::isRightChild() const {
    return parent && parent->right == this;
}

template<typename T>
bool SplayNode<T>::isRoot() const {
    return parent == nullptr;
}
```

### 2. Mise à jour des pointeurs
```cpp
template<typename T>
void SplayNode<T>::updateParent(SplayNode<T>* newParent) {
    if (parent) {
        if (parent->left == this) {
            parent->left = nullptr;
        } else {
            parent->right = nullptr;
        }
    }
    
    parent = newParent;
    
    if (parent) {
        if (data < parent->data) {
            parent->left = this;
        } else {
            parent->right = this;
        }
    }
}
```

### 3. Échange de nœuds
```cpp
template<typename T>
void SplayNode<T>::swapWith(SplayNode<T>* other) {
    if (!other) return;
    
    // Échanger les données
    std::swap(data, other->data);
    
    // Échanger les pointeurs enfants
    std::swap(left, other->left);
    std::swap(right, other->right);
    
    // Mise à jour des pointeurs parent des enfants
    if (left) left->parent = this;
    if (right) right->parent = this;
    if (other->left) other->left->parent = other;
    if (other->right) other->right->parent = other;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Constructeur | O(1) | Initialisation simple |
| Destructeur | O(1) | Pas de récursion |
| Navigation | O(log n) | Hauteur de l'arbre |
| Rotation | O(1) | Opération locale |
| Splay | O(log n) amorti | O(n) dans le pire cas |
| Mise à jour parent | O(1) | Opération locale |

## Cas d'usage

### 1. Opérations de splay
- Déplacement vers la racine
- Optimisation des accès futurs
- Maintien de la structure BST

### 2. Navigation dans l'arbre
- Parcours ordonné
- Recherche de successeur/prédécesseur
- Accès aux extrema

### 3. Opérations de rotation
- Rééquilibrage local
- Maintien des propriétés
- Optimisation de la structure

## Tests

### 1. Tests unitaires
- Constructeurs et destructeurs
- Opérations de navigation
- Opérations de rotation
- Opérations de splay

### 2. Tests d'intégration
- Interaction avec SplayTree
- Gestion des pointeurs parent
- Maintien des propriétés

### 3. Tests de performance
- Temps d'exécution des opérations
- Gestion mémoire
- Optimisations

## Optimisations

### 1. Optimisations de rotation
- Réduction des comparaisons
- Mise à jour optimisée des pointeurs
- Éviter les opérations redondantes

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des nœuds
- Gestion des fuites

### 3. Optimisations de navigation
- Cache des pointeurs fréquents
- Réduction des accès mémoire
- Optimisation des branches

## Exemples d'utilisation

```cpp
// Création de nœuds
SplayNode<int>* node1 = new SplayNode<int>(5);
SplayNode<int>* node2 = new SplayNode<int>(3, node1);

// Navigation
SplayNode<int>* leftmost = node1->getLeftmost();
SplayNode<int>* successor = node1->getSuccessor();

// Rotation
SplayNode<int>* newRoot = node1->rotateLeft();

// Splay
SplayNode<int>* splayed = node2->splay();
```

## Notes d'implémentation

### 1. Gestion des pointeurs
- Mise à jour cohérente des pointeurs parent
- Éviter les cycles
- Gestion des cas de racine

### 2. Gestion des erreurs
- Validation des paramètres
- Gestion des cas limites
- Messages d'erreur informatifs

### 3. Compatibilité
- Support des types génériques
- Comparateurs personnalisés
- Itérateurs STL

## Dépendances
- Types de base de la Phase 1
- Structures de données génériques
- Gestion mémoire appropriée

## Risques et mitigations

### 1. Gestion des pointeurs
- **Risque** : Cycles, pointeurs invalides
- **Mitigation** : Tests exhaustifs, validation

### 2. Performance
- **Risque** : Opérations coûteuses
- **Mitigation** : Optimisations, profilage

### 3. Gestion mémoire
- **Risque** : Fuites, fragmentation
- **Mitigation** : RAII, tests de mémoire

## Métriques de qualité

### 1. Performance
- Opérations O(1) pour les opérations locales
- Navigation O(log n) optimisée
- Pas de dégradation significative

### 2. Robustesse
- 100% de couverture de tests
- Gestion de tous les cas limites
- Pas de fuites mémoire

### 3. Maintenabilité
- Code lisible et documenté
- Tests compréhensibles
- Documentation complète