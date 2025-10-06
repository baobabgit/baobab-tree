# Spécification détaillée - TreapNode

## Vue d'ensemble
TreapNode est le nœud spécialisé pour le Treap, conçu pour supporter les propriétés de BST et de heap avec une priorité associée à chaque nœud.

## Objectifs
- Fournir une structure de nœud optimisée pour Treap
- Supporter les opérations de rotation et heapify
- Maintenir les pointeurs parent pour les opérations efficaces
- Gérer les priorités et les clés

## Structure de données

### TreapNode
```cpp
template<typename T>
class TreapNode {
public:
    T data;
    int priority;
    TreapNode<T>* left;
    TreapNode<T>* right;
    TreapNode<T>* parent;
    
    // Constructeurs
    TreapNode(const T& value, int priority);
    TreapNode(const T& value, int priority, TreapNode<T>* parent);
    ~TreapNode();
    
    // Opérations de base
    bool isLeaf() const;
    bool hasLeftChild() const;
    bool hasRightChild() const;
    bool hasParent() const;
    bool isLeftChild() const;
    bool isRightChild() const;
    bool isRoot() const;
    
    // Opérations de navigation
    TreapNode<T>* getLeftmost();
    TreapNode<T>* getRightmost();
    TreapNode<T>* getSuccessor();
    TreapNode<T>* getPredecessor();
    
    // Opérations de rotation
    TreapNode<T>* rotateLeft();
    TreapNode<T>* rotateRight();
    
    // Opérations de heap
    bool isHeapProperty() const;
    void heapifyUp();
    void heapifyDown();
    void updatePriority(int newPriority);
    
    // Opérations de maintenance
    void updateParent(TreapNode<T>* newParent);
    void detachFromParent();
    void swapWith(TreapNode<T>* other);
    
    // Opérations de debug
    void print() const;
    int getHeight() const;
    int getBalance() const;
    bool isValid() const;
    
    // Opérations de comparaison
    bool operator<(const TreapNode<T>& other) const;
    bool operator>(const TreapNode<T>& other) const;
    bool operator==(const TreapNode<T>& other) const;
    
    // Opérations de priorité
    bool hasHigherPriority(const TreapNode<T>& other) const;
    bool hasLowerPriority(const TreapNode<T>& other) const;
    int getPriority() const;
    void setPriority(int newPriority);
};
```

## Algorithmes principaux

### 1. Constructeurs
```cpp
template<typename T>
TreapNode<T>::TreapNode(const T& value, int priority) 
    : data(value), priority(priority), left(nullptr), right(nullptr), parent(nullptr) {}

template<typename T>
TreapNode<T>::TreapNode(const T& value, int priority, TreapNode<T>* parent) 
    : data(value), priority(priority), left(nullptr), right(nullptr), parent(parent) {}
```

### 2. Opérations de rotation
```cpp
template<typename T>
TreapNode<T>* TreapNode<T>::rotateLeft() {
    if (!right) return this;
    
    TreapNode<T>* newRoot = right;
    TreapNode<T>* parent = this->parent;
    
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
TreapNode<T>* TreapNode<T>::rotateRight() {
    if (!left) return this;
    
    TreapNode<T>* newRoot = left;
    TreapNode<T>* parent = this->parent;
    
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

### 3. Opérations de heap
```cpp
template<typename T>
void TreapNode<T>::heapifyUp() {
    TreapNode<T>* current = this;
    
    while (current->parent && current->priority > current->parent->priority) {
        if (current == current->parent->left) {
            current->parent->rotateRight();
        } else {
            current->parent->rotateLeft();
        }
    }
}

template<typename T>
void TreapNode<T>::heapifyDown() {
    TreapNode<T>* current = this;
    
    while (current->left || current->right) {
        TreapNode<T>* maxChild = nullptr;
        
        if (current->left && current->right) {
            maxChild = (current->left->priority > current->right->priority) 
                      ? current->left : current->right;
        } else if (current->left) {
            maxChild = current->left;
        } else {
            maxChild = current->right;
        }
        
        if (maxChild->priority > current->priority) {
            if (maxChild == current->left) {
                current->rotateRight();
            } else {
                current->rotateLeft();
            }
        } else {
            break;
        }
    }
}
```

## Propriétés

### 1. Structure de nœud
- **data** : Valeur stockée dans le nœud (clé BST)
- **priority** : Priorité du nœud (propriété heap)
- **left** : Pointeur vers le fils gauche
- **right** : Pointeur vers le fils droit
- **parent** : Pointeur vers le parent

### 2. Propriété BST
- Clé gauche < clé nœud < clé droite
- Ordre des éléments préservé
- Structure de recherche binaire valide

### 3. Propriété Heap
- Priorité parent ≥ priorité enfants
- Racine a la priorité maximale
- Équilibrage probabiliste

## Opérations spécialisées

### 1. Vérification de la propriété heap
```cpp
template<typename T>
bool TreapNode<T>::isHeapProperty() const {
    bool leftValid = !left || (left->priority <= priority && left->isHeapProperty());
    bool rightValid = !right || (right->priority <= priority && right->isHeapProperty());
    return leftValid && rightValid;
}
```

### 2. Mise à jour de priorité
```cpp
template<typename T>
void TreapNode<T>::updatePriority(int newPriority) {
    priority = newPriority;
    
    // Restaurer la propriété heap
    if (parent && priority > parent->priority) {
        heapifyUp();
    } else if (left || right) {
        heapifyDown();
    }
}
```

### 3. Détection de position
```cpp
template<typename T>
bool TreapNode<T>::isLeftChild() const {
    return parent && parent->left == this;
}

template<typename T>
bool TreapNode<T>::isRightChild() const {
    return parent && parent->right == this;
}

template<typename T>
bool TreapNode<T>::isRoot() const {
    return parent == nullptr;
}
```

### 4. Navigation dans l'arbre
```cpp
template<typename T>
TreapNode<T>* TreapNode<T>::getLeftmost() {
    TreapNode<T>* current = this;
    while (current->left) {
        current = current->left;
    }
    return current;
}

template<typename T>
TreapNode<T>* TreapNode<T>::getRightmost() {
    TreapNode<T>* current = this;
    while (current->right) {
        current = current->right;
    }
    return current;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Constructeur | O(1) | Initialisation simple |
| Destructeur | O(1) | Pas de récursion |
| Navigation | O(log n) | Hauteur de l'arbre |
| Rotation | O(1) | Opération locale |
| HeapifyUp | O(log n) | Hauteur de l'arbre |
| HeapifyDown | O(log n) | Hauteur de l'arbre |
| Mise à jour priorité | O(log n) | Restauration heap |

## Cas d'usage

### 1. Opérations de Treap
- Insertion avec priorité
- Suppression avec restauration heap
- Recherche avec propriété BST

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
- Opérations de heap

### 2. Tests d'intégration
- Interaction avec Treap
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

### 3. Optimisations de heap
- Cache des priorités fréquentes
- Réduction des comparaisons
- Optimisation des rotations

## Exemples d'utilisation

```cpp
// Création de nœuds
TreapNode<int>* node1 = new TreapNode<int>(5, 10);
TreapNode<int>* node2 = new TreapNode<int>(3, 5, node1);

// Navigation
TreapNode<int>* leftmost = node1->getLeftmost();
TreapNode<int>* successor = node1->getSuccessor();

// Rotation
TreapNode<int>* newRoot = node1->rotateLeft();

// Opérations de heap
node1->heapifyUp();
node1->updatePriority(15);
```

## Notes d'implémentation

### 1. Gestion des priorités
- Mise à jour cohérente des priorités
- Restauration de la propriété heap
- Gestion des cas limites

### 2. Gestion des pointeurs
- Mise à jour cohérente des pointeurs parent
- Éviter les cycles
- Gestion des cas de racine

### 3. Compatibilité
- Support des types génériques
- Comparateurs personnalisés
- Itérateurs STL

## Dépendances
- Types de base de la Phase 1
- Structures de données génériques
- Gestion mémoire appropriée

## Risques et mitigations

### 1. Gestion des priorités
- **Risque** : Violation de la propriété heap
- **Mitigation** : Tests exhaustifs, validation

### 2. Gestion des pointeurs
- **Risque** : Cycles, pointeurs invalides
- **Mitigation** : Tests exhaustifs, validation

### 3. Performance
- **Risque** : Opérations coûteuses
- **Mitigation** : Optimisations, profilage

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