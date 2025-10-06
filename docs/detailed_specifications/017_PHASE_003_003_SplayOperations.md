# Spécification détaillée - SplayOperations

## Vue d'ensemble
SplayOperations contient les algorithmes spécialisés pour les opérations de splay, incluant les rotations, les opérations de splay et les optimisations de performance.

## Objectifs
- Implémenter les algorithmes de splay optimisés
- Fournir les opérations de rotation spécialisées
- Optimiser les performances des opérations courantes
- Maintenir la cohérence de la structure d'arbre

## Structure de données

### SplayOperations
```cpp
template<typename T>
class SplayOperations {
public:
    // Opérations de splay
    static SplayNode<T>* splay(SplayNode<T>* root, const T& value);
    static SplayNode<T>* splayToRoot(SplayNode<T>* node);
    static SplayNode<T>* splayToParent(SplayNode<T>* node);
    
    // Opérations de rotation
    static SplayNode<T>* zig(SplayNode<T>* node);
    static SplayNode<T>* zigZig(SplayNode<T>* node);
    static SplayNode<T>* zigZag(SplayNode<T>* node);
    static SplayNode<T>* rotateLeft(SplayNode<T>* node);
    static SplayNode<T>* rotateRight(SplayNode<T>* node);
    
    // Opérations de recherche avec splay
    static SplayNode<T>* findAndSplay(SplayNode<T>* root, const T& value);
    static SplayNode<T>* findMinAndSplay(SplayNode<T>* root);
    static SplayNode<T>* findMaxAndSplay(SplayNode<T>* root);
    
    // Opérations de fusion et division
    static SplayNode<T>* merge(SplayNode<T>* left, SplayNode<T>* right);
    static std::pair<SplayNode<T>*, SplayNode<T>*> split(SplayNode<T>* root, const T& value);
    static SplayNode<T>* join(SplayNode<T>* left, SplayNode<T>* right);
    
    // Opérations d'optimisation
    static SplayNode<T>* optimizeAccess(SplayNode<T>* root, const T& value);
    static SplayNode<T>* rebalance(SplayNode<T>* root);
    static SplayNode<T>* compress(SplayNode<T>* root);
    
    // Opérations de maintenance
    static void updateHeights(SplayNode<T>* root);
    static int getHeight(SplayNode<T>* node);
    static bool isBalanced(SplayNode<T>* root);
    
    // Opérations de debug
    static void printTree(SplayNode<T>* root, int level = 0);
    static bool validateTree(SplayNode<T>* root);
    static std::vector<T> getInorder(SplayNode<T>* root);
};
```

## Algorithmes principaux

### 1. Opération Splay principale
```cpp
template<typename T>
SplayNode<T>* SplayOperations<T>::splay(SplayNode<T>* root, const T& value) {
    if (!root) return nullptr;
    
    SplayNode<T>* current = root;
    SplayNode<T>* parent = nullptr;
    SplayNode<T>* grandparent = nullptr;
    
    while (current) {
        if (current->data == value) {
            break;
        }
        
        parent = current;
        if (value < current->data) {
            current = current->left;
        } else {
            current = current->right;
        }
    }
    
    if (!current) {
        // Élément non trouvé, splay du dernier nœud visité
        current = parent;
    }
    
    // Splay jusqu'à la racine
    while (current->parent) {
        SplayNode<T>* p = current->parent;
        SplayNode<T>* g = p->parent;
        
        if (!g) {
            // Cas zig
            if (current == p->left) {
                rotateRight(p);
            } else {
                rotateLeft(p);
            }
        } else if (current == p->left && p == g->left) {
            // Cas zig-zig
            rotateRight(g);
            rotateRight(p);
        } else if (current == p->right && p == g->right) {
            // Cas zig-zig
            rotateLeft(g);
            rotateLeft(p);
        } else if (current == p->left && p == g->right) {
            // Cas zig-zag
            rotateRight(p);
            rotateLeft(g);
        } else {
            // Cas zig-zag
            rotateLeft(p);
            rotateRight(g);
        }
    }
    
    return current;
}
```

### 2. Opérations de rotation
```cpp
template<typename T>
SplayNode<T>* SplayOperations<T>::rotateLeft(SplayNode<T>* node) {
    if (!node || !node->right) return node;
    
    SplayNode<T>* newRoot = node->right;
    SplayNode<T>* parent = node->parent;
    
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
SplayNode<T>* SplayOperations<T>::rotateRight(SplayNode<T>* node) {
    if (!node || !node->left) return node;
    
    SplayNode<T>* newRoot = node->left;
    SplayNode<T>* parent = node->parent;
    
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

### 3. Opérations de fusion
```cpp
template<typename T>
SplayNode<T>* SplayOperations<T>::merge(SplayNode<T>* left, SplayNode<T>* right) {
    if (!left) return right;
    if (!right) return left;
    
    // Trouver le maximum dans l'arbre gauche
    SplayNode<T>* maxLeft = left;
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
std::pair<SplayNode<T>*, SplayNode<T>*> SplayOperations<T>::split(SplayNode<T>* root, const T& value) {
    if (!root) {
        return {nullptr, nullptr};
    }
    
    // Splay de la valeur vers la racine
    root = splay(root, value);
    
    if (root->data <= value) {
        // La racine et son sous-arbre gauche vont à gauche
        SplayNode<T>* right = root->right;
        if (right) {
            right->parent = nullptr;
        }
        root->right = nullptr;
        return {root, right};
    } else {
        // Le sous-arbre gauche va à gauche, la racine et son sous-arbre droit vont à droite
        SplayNode<T>* left = root->left;
        if (left) {
            left->parent = nullptr;
        }
        root->left = nullptr;
        return {left, root};
    }
}
```

## Opérations spécialisées

### 1. Recherche avec splay
```cpp
template<typename T>
SplayNode<T>* SplayOperations<T>::findAndSplay(SplayNode<T>* root, const T& value) {
    if (!root) return nullptr;
    
    SplayNode<T>* current = root;
    while (current) {
        if (current->data == value) {
            return splayToRoot(current);
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

### 2. Optimisation d'accès
```cpp
template<typename T>
SplayNode<T>* SplayOperations<T>::optimizeAccess(SplayNode<T>* root, const T& value) {
    if (!root) return nullptr;
    
    // Splay de la valeur
    root = splay(root, value);
    
    // Si la valeur n'existe pas, splay du nœud le plus proche
    if (root->data != value) {
        // Splay du nœud le plus proche
        if (value < root->data && root->left) {
            SplayNode<T>* closest = root->left;
            while (closest->right) {
                closest = closest->right;
            }
            root = splay(root, closest->data);
        } else if (value > root->data && root->right) {
            SplayNode<T>* closest = root->right;
            while (closest->left) {
                closest = closest->left;
            }
            root = splay(root, closest->data);
        }
    }
    
    return root;
}
```

### 3. Reéquilibrage
```cpp
template<typename T>
SplayNode<T>* SplayOperations<T>::rebalance(SplayNode<T>* root) {
    if (!root) return nullptr;
    
    // Parcours en ordre et reconstruction
    std::vector<T> elements = getInorder(root);
    
    // Reconstruction équilibrée
    return buildBalancedTree(elements, 0, elements.size() - 1);
}

private:
template<typename T>
SplayNode<T>* buildBalancedTree(const std::vector<T>& elements, int start, int end) {
    if (start > end) return nullptr;
    
    int mid = (start + end) / 2;
    SplayNode<T>* node = new SplayNode<T>(elements[mid]);
    
    node->left = buildBalancedTree(elements, start, mid - 1);
    node->right = buildBalancedTree(elements, mid + 1, end);
    
    if (node->left) node->left->parent = node;
    if (node->right) node->right->parent = node;
    
    return node;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Splay | O(log n) amorti | O(n) dans le pire cas |
| Rotation | O(1) | Opération locale |
| Fusion | O(log n) amorti | O(n) dans le pire cas |
| Division | O(log n) amorti | O(n) dans le pire cas |
| Recherche | O(log n) amorti | O(n) dans le pire cas |
| Reéquilibrage | O(n) | Reconstruction complète |

## Propriétés

### 1. Auto-ajustement
- Chaque accès déplace l'élément vers la racine
- Amélioration des performances pour les accès répétés
- Maintien de la propriété BST

### 2. Optimisations
- Réduction des comparaisons
- Cache des pointeurs fréquents
- Optimisation des rotations

### 3. Robustesse
- Gestion des cas limites
- Validation des opérations
- Gestion des erreurs

## Cas d'usage

### 1. Cache LRU
- Éléments récemment accédés en haut
- Suppression des éléments les moins utilisés
- Performance optimale

### 2. Index de base de données
- Requêtes fréquentes optimisées
- Auto-ajustement basé sur l'usage
- Performance amortie excellente

### 3. Système de fichiers
- Fichiers récemment accédés en cache
- Optimisation des accès répétés
- Gestion automatique de la hiérarchie

## Tests

### 1. Tests unitaires
- Opérations de splay
- Opérations de rotation
- Opérations de fusion et division
- Opérations d'optimisation

### 2. Tests d'intégration
- Interaction avec SplayTree
- Gestion des pointeurs parent
- Maintien des propriétés

### 3. Tests de performance
- Temps d'exécution des opérations
- Analyse de la complexité amortie
- Comparaison avec BST standard

## Optimisations

### 1. Optimisations de splay
- Rotation optimisée
- Réduction des comparaisons
- Cache des pointeurs fréquents

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des nœuds
- Gestion des fuites mémoire

### 3. Optimisations de parcours
- Itérateurs optimisés
- Parcours en place
- Réduction des allocations

## Exemples d'utilisation

```cpp
// Opérations de base
SplayNode<int>* root = new SplayNode<int>(5);
root = SplayOperations<int>::splay(root, 3);

// Fusion et division
SplayNode<int>* left = new SplayNode<int>(2);
SplayNode<int>* right = new SplayNode<int>(8);
SplayNode<int>* merged = SplayOperations<int>::merge(left, right);

auto [leftSplit, rightSplit] = SplayOperations<int>::split(root, 4);

// Optimisation
root = SplayOperations<int>::optimizeAccess(root, 7);
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
- SplayNode (nœud spécialisé)
- Structures de base de la Phase 1
- Algorithmes de rotation

## Risques et mitigations

### 1. Performance dégradée
- **Risque** : O(n) dans le pire cas
- **Mitigation** : Analyse amortie, tests de performance

### 2. Complexité d'implémentation
- **Risque** : Algorithmes de splay complexes
- **Mitigation** : Tests exhaustifs, documentation détaillée

### 3. Gestion mémoire
- **Risque** : Fuites mémoire, fragmentation
- **Mitigation** : RAII, tests de mémoire, profilage

## Métriques de qualité

### 1. Performance
- Temps d'accès moyen < 2x BST standard
- Complexité amortie O(log n)
- Pas de dégradation significative

### 2. Robustesse
- 100% de couverture de tests
- Gestion de tous les cas limites
- Pas de fuites mémoire

### 3. Maintenabilité
- Code lisible et documenté
- Tests compréhensibles
- Documentation complète