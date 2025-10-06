# Spécification détaillée - TreapOperations

## Vue d'ensemble
TreapOperations contient les algorithmes spécialisés pour les opérations de Treap, incluant les rotations, les opérations de heap et les optimisations de performance.

## Objectifs
- Implémenter les algorithmes de Treap optimisés
- Fournir les opérations de rotation spécialisées
- Optimiser les performances des opérations courantes
- Maintenir la cohérence des propriétés BST et heap

## Structure de données

### TreapOperations
```cpp
template<typename T>
class TreapOperations {
public:
    // Opérations de rotation
    static TreapNode<T>* rotateLeft(TreapNode<T>* node);
    static TreapNode<T>* rotateRight(TreapNode<T>* node);
    static TreapNode<T>* rotateLeftRight(TreapNode<T>* node);
    static TreapNode<T>* rotateRightLeft(TreapNode<T>* node);
    
    // Opérations de heap
    static void heapifyUp(TreapNode<T>* node);
    static void heapifyDown(TreapNode<T>* node);
    static bool isHeapProperty(TreapNode<T>* root);
    static void restoreHeapProperty(TreapNode<T>* root);
    
    // Opérations de recherche
    static TreapNode<T>* findNode(TreapNode<T>* root, const T& value);
    static TreapNode<T>* findMin(TreapNode<T>* root);
    static TreapNode<T>* findMax(TreapNode<T>* root);
    static TreapNode<T>* findSuccessor(TreapNode<T>* node);
    static TreapNode<T>* findPredecessor(TreapNode<T>* node);
    
    // Opérations de fusion et division
    static TreapNode<T>* merge(TreapNode<T>* left, TreapNode<T>* right);
    static std::pair<TreapNode<T>*, TreapNode<T>*> split(TreapNode<T>* root, const T& value);
    static TreapNode<T>* join(TreapNode<T>* left, TreapNode<T>* right);
    
    // Opérations d'optimisation
    static TreapNode<T>* optimizeStructure(TreapNode<T>* root);
    static TreapNode<T>* rebalance(TreapNode<T>* root);
    static TreapNode<T>* compress(TreapNode<T>* root);
    
    // Opérations de maintenance
    static void updateHeights(TreapNode<T>* root);
    static int getHeight(TreapNode<T>* node);
    static bool isBalanced(TreapNode<T>* root);
    static void updatePriorities(TreapNode<T>* root);
    
    // Opérations de debug
    static void printTree(TreapNode<T>* root, int level = 0);
    static bool validateTree(TreapNode<T>* root);
    static std::vector<T> getInorder(TreapNode<T>* root);
    static std::vector<std::pair<T, int>> getPriorities(TreapNode<T>* root);
};
```

## Algorithmes principaux

### 1. Opérations de rotation
```cpp
template<typename T>
TreapNode<T>* TreapOperations<T>::rotateLeft(TreapNode<T>* node) {
    if (!node || !node->right) return node;
    
    TreapNode<T>* newRoot = node->right;
    TreapNode<T>* parent = node->parent;
    
    // Mise à jour des pointeurs
    node->right = newRoot->left;
    if (node->right) {
        node->right->parent = node;
    }
    
    newRoot->left = node;
    node->parent = newRoot;
    
    newRoot->parent = parent;
    if (parent) {
        if (parent->left == node) {
            parent->left = newRoot;
        } else {
            parent->right = newRoot;
        }
    }
    
    return newRoot;
}

template<typename T>
TreapNode<T>* TreapOperations<T>::rotateRight(TreapNode<T>* node) {
    if (!node || !node->left) return node;
    
    TreapNode<T>* newRoot = node->left;
    TreapNode<T>* parent = node->parent;
    
    // Mise à jour des pointeurs
    node->left = newRoot->right;
    if (node->left) {
        node->left->parent = node;
    }
    
    newRoot->right = node;
    node->parent = newRoot;
    
    newRoot->parent = parent;
    if (parent) {
        if (parent->left == node) {
            parent->left = newRoot;
        } else {
            parent->right = newRoot;
        }
    }
    
    return newRoot;
}
```

### 2. Opérations de heap
```cpp
template<typename T>
void TreapOperations<T>::heapifyUp(TreapNode<T>* node) {
    while (node->parent && node->priority > node->parent->priority) {
        if (node == node->parent->left) {
            rotateRight(node->parent);
        } else {
            rotateLeft(node->parent);
        }
    }
}

template<typename T>
void TreapOperations<T>::heapifyDown(TreapNode<T>* node) {
    while (node->left || node->right) {
        TreapNode<T>* maxChild = nullptr;
        
        if (node->left && node->right) {
            maxChild = (node->left->priority > node->right->priority) 
                      ? node->left : node->right;
        } else if (node->left) {
            maxChild = node->left;
        } else {
            maxChild = node->right;
        }
        
        if (maxChild->priority > node->priority) {
            if (maxChild == node->left) {
                rotateRight(node);
            } else {
                rotateLeft(node);
            }
        } else {
            break;
        }
    }
}
```

### 3. Opérations de fusion
```cpp
template<typename T>
TreapNode<T>* TreapOperations<T>::merge(TreapNode<T>* left, TreapNode<T>* right) {
    if (!left) return right;
    if (!right) return left;
    
    // Trouver le maximum dans l'arbre gauche
    TreapNode<T>* maxLeft = left;
    while (maxLeft->right) {
        maxLeft = maxLeft->right;
    }
    
    // Splay du maximum vers la racine
    left = splay(left, maxLeft->data);
    
    // Fusionner
    left->right = right;
    right->parent = left;
    
    return left;
}
```

### 4. Opérations de division
```cpp
template<typename T>
std::pair<TreapNode<T>*, TreapNode<T>*> TreapOperations<T>::split(TreapNode<T>* root, const T& value) {
    if (!root) {
        return {nullptr, nullptr};
    }
    
    // Recherche de la valeur
    TreapNode<T>* node = findNode(root, value);
    if (node) {
        // Splay de la valeur vers la racine
        root = splay(root, value);
        
        if (root->data <= value) {
            // La racine et son sous-arbre gauche vont à gauche
            TreapNode<T>* right = root->right;
            if (right) {
                right->parent = nullptr;
            }
            root->right = nullptr;
            return {root, right};
        } else {
            // Le sous-arbre gauche va à gauche, la racine et son sous-arbre droit vont à droite
            TreapNode<T>* left = root->left;
            if (left) {
                left->parent = nullptr;
            }
            root->left = nullptr;
            return {left, root};
        }
    } else {
        // Valeur non trouvée, division basée sur la position
        TreapNode<T>* current = root;
        while (current) {
            if (value < current->data) {
                current = current->left;
            } else {
                current = current->right;
            }
        }
        
        if (current && current->data > value) {
            root = splay(root, current->data);
            if (root->right) {
                TreapNode<T>* right = root->right;
                right->parent = nullptr;
                root->right = nullptr;
                return {root, right};
            }
        }
        
        return {root, nullptr};
    }
}
```

## Opérations spécialisées

### 1. Recherche avec splay
```cpp
template<typename T>
TreapNode<T>* TreapOperations<T>::findNode(TreapNode<T>* root, const T& value) {
    if (!root) return nullptr;
    
    TreapNode<T>* current = root;
    while (current) {
        if (current->data == value) {
            return current;
        }
        
        if (value < current->data) {
            current = current->left;
        } else {
            current = current->right;
        }
    }
    
    return nullptr;
}
```

### 2. Optimisation de structure
```cpp
template<typename T>
TreapNode<T>* TreapOperations<T>::optimizeStructure(TreapNode<T>* root) {
    if (!root) return nullptr;
    
    // Parcours en ordre et reconstruction
    std::vector<T> elements = getInorder(root);
    
    // Reconstruction équilibrée
    return buildBalancedTree(elements, 0, elements.size() - 1);
}

private:
template<typename T>
TreapNode<T>* buildBalancedTree(const std::vector<T>& elements, int start, int end) {
    if (start > end) return nullptr;
    
    int mid = (start + end) / 2;
    TreapNode<T>* node = new TreapNode<T>(elements[mid], 0);
    
    node->left = buildBalancedTree(elements, start, mid - 1);
    node->right = buildBalancedTree(elements, mid + 1, end);
    
    if (node->left) node->left->parent = node;
    if (node->right) node->right->parent = node;
    
    return node;
}
```

### 3. Restauration de la propriété heap
```cpp
template<typename T>
void TreapOperations<T>::restoreHeapProperty(TreapNode<T>* root) {
    if (!root) return;
    
    // Parcours post-ordre pour restaurer la propriété heap
    std::stack<TreapNode<T>*> stack;
    TreapNode<T>* current = root;
    TreapNode<T>* lastVisited = nullptr;
    
    while (!stack.empty() || current) {
        if (current) {
            stack.push(current);
            current = current->left;
        } else {
            TreapNode<T>* peekNode = stack.top();
            if (peekNode->right && lastVisited != peekNode->right) {
                current = peekNode->right;
            } else {
                heapifyDown(peekNode);
                lastVisited = stack.top();
                stack.pop();
            }
        }
    }
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Rotation | O(1) | Opération locale |
| HeapifyUp | O(log n) | Hauteur de l'arbre |
| HeapifyDown | O(log n) | Hauteur de l'arbre |
| Fusion | O(log n) en moyenne | O(n) dans le pire cas |
| Division | O(log n) en moyenne | O(n) dans le pire cas |
| Recherche | O(log n) en moyenne | O(n) dans le pire cas |
| Optimisation | O(n) | Reconstruction complète |

## Propriétés

### 1. Propriété BST
- Clé gauche < clé nœud < clé droite
- Parcours en ordre donne les clés triées
- Recherche efficace en O(log n) en moyenne

### 2. Propriété Heap
- Priorité parent ≥ priorité enfants
- Racine a la priorité maximale
- Équilibrage probabiliste

### 3. Optimisations
- Réduction des comparaisons
- Cache des pointeurs fréquents
- Optimisation des rotations

## Cas d'usage

### 1. Index de base de données
- Clés triées avec priorités
- Recherche et insertion efficaces
- Équilibrage automatique

### 2. Cache avec priorités
- Éléments avec priorités de cache
- Suppression des éléments de faible priorité
- Performance optimale

### 3. Planificateur de tâches
- Tâches avec priorités
- Insertion et suppression dynamiques
- Accès au plus prioritaire

## Tests

### 1. Tests unitaires
- Opérations de rotation
- Opérations de heap
- Opérations de fusion et division
- Opérations d'optimisation

### 2. Tests d'intégration
- Interaction avec Treap
- Gestion des pointeurs parent
- Maintien des propriétés

### 3. Tests de performance
- Temps d'exécution des opérations
- Analyse de la complexité amortie
- Comparaison avec BST standard

## Optimisations

### 1. Optimisations de rotation
- Rotation optimisée
- Réduction des comparaisons
- Cache des pointeurs fréquents

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des nœuds
- Gestion des fuites mémoire

### 3. Optimisations de heap
- Cache des priorités fréquentes
- Réduction des comparaisons
- Optimisation des rotations

## Exemples d'utilisation

```cpp
// Opérations de base
TreapNode<int>* root = new TreapNode<int>(5, 10);
root = TreapOperations<int>::rotateLeft(root);

// Opérations de heap
TreapOperations<int>::heapifyUp(root);
TreapOperations<int>::heapifyDown(root);

// Fusion et division
TreapNode<int>* left = new TreapNode<int>(2, 5);
TreapNode<int>* right = new TreapNode<int>(8, 15);
TreapNode<int>* merged = TreapOperations<int>::merge(left, right);

auto [leftSplit, rightSplit] = TreapOperations<int>::split(root, 4);

// Optimisation
root = TreapOperations<int>::optimizeStructure(root);
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
- TreapNode (nœud spécialisé)
- Structures de base de la Phase 1
- Algorithmes de rotation

## Risques et mitigations

### 1. Performance dégradée
- **Risque** : O(n) dans le pire cas
- **Mitigation** : Analyse probabiliste, tests de performance

### 2. Complexité d'implémentation
- **Risque** : Algorithmes de rotation complexes
- **Mitigation** : Tests exhaustifs, documentation détaillée

### 3. Gestion mémoire
- **Risque** : Fuites mémoire, fragmentation
- **Mitigation** : RAII, tests de mémoire, profilage

## Métriques de qualité

### 1. Performance
- Temps d'accès moyen O(log n)
- Hauteur moyenne O(log n)
- Pas de dégradation significative

### 2. Robustesse
- 100% de couverture de tests
- Gestion de tous les cas limites
- Pas de fuites mémoire

### 3. Maintenabilité
- Code lisible et documenté
- Tests compréhensibles
- Documentation complète