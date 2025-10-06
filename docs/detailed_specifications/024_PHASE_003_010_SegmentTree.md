# Spécification détaillée - SegmentTree

## Vue d'ensemble
L'arbre de segments (Segment Tree) est une structure de données spécialisée pour effectuer des requêtes de plage et des mises à jour sur un tableau de manière efficace. Il permet des opérations en O(log n) pour les requêtes et mises à jour.

## Objectifs
- Implémenter un arbre de segments optimisé
- Fournir des requêtes de plage efficaces
- Supporter les mises à jour en temps réel
- Optimiser l'utilisation mémoire

## Structure de données

### SegmentTree
```cpp
template<typename T, typename Func = std::plus<T>>
class SegmentTree {
private:
    std::vector<T> tree;
    std::vector<T> lazy;
    std::vector<T> data;
    size_t size;
    Func operation;
    T identity;
    
public:
    // Constructeurs
    SegmentTree(const std::vector<T>& arr);
    SegmentTree(const std::vector<T>& arr, Func op, T identity);
    ~SegmentTree();
    
    // Opérations de base
    void update(int index, T value);
    void updateRange(int left, int right, T value);
    T query(int left, int right);
    T query(int index);
    
    // Opérations de requête
    T getSum(int left, int right);
    T getMin(int left, int right);
    T getMax(int left, int right);
    T getProduct(int left, int right);
    
    // Opérations de mise à jour
    void add(int left, int right, T value);
    void multiply(int left, int right, T value);
    void set(int left, int right, T value);
    
    // Opérations de maintenance
    void rebuild();
    void clear();
    bool empty() const;
    size_t getSize() const;
    
    // Opérations spécialisées
    int findFirst(int left, int right, std::function<bool(T)> predicate);
    int findLast(int left, int right, std::function<bool(T)> predicate);
    std::vector<T> getRange(int left, int right);
    void setRange(int left, int right, const std::vector<T>& values);
    
    // Opérations de debug
    void print() const;
    bool isValid() const;
    void printStatistics() const;
    
    // Opérations de compression
    void compress();
    void optimize();
    void removeUnusedNodes();
};
```

## Algorithmes principaux

### 1. Construction
```cpp
SegmentTree(const std::vector<T>& arr) : data(arr), size(arr.size()) {
    if (size == 0) return;
    
    // Calcul de la taille de l'arbre
    size_t treeSize = 1;
    while (treeSize < size) {
        treeSize <<= 1;
    }
    treeSize <<= 1;
    
    tree.resize(treeSize);
    lazy.resize(treeSize);
    
    // Construction de l'arbre
    build(1, 0, size - 1);
}

private:
void build(int node, int start, int end) {
    if (start == end) {
        tree[node] = data[start];
    } else {
        int mid = (start + end) / 2;
        build(2 * node, start, mid);
        build(2 * node + 1, mid + 1, end);
        tree[node] = operation(tree[2 * node], tree[2 * node + 1]);
    }
}
```

### 2. Requête de plage
```cpp
T query(int left, int right) {
    if (left < 0 || right >= size || left > right) {
        return identity;
    }
    
    return queryRange(1, 0, size - 1, left, right);
}

private:
T queryRange(int node, int start, int end, int left, int right) {
    // Propagation de la lazy update
    if (lazy[node] != identity) {
        tree[node] = operation(tree[node], lazy[node] * (end - start + 1));
        if (start != end) {
            lazy[2 * node] = operation(lazy[2 * node], lazy[node]);
            lazy[2 * node + 1] = operation(lazy[2 * node + 1], lazy[node]);
        }
        lazy[node] = identity;
    }
    
    if (right < start || left > end) {
        return identity;
    }
    
    if (left <= start && end <= right) {
        return tree[node];
    }
    
    int mid = (start + end) / 2;
    T leftResult = queryRange(2 * node, start, mid, left, right);
    T rightResult = queryRange(2 * node + 1, mid + 1, end, left, right);
    
    return operation(leftResult, rightResult);
}
```

### 3. Mise à jour de plage
```cpp
void updateRange(int left, int right, T value) {
    if (left < 0 || right >= size || left > right) {
        return;
    }
    
    updateRangeRecursive(1, 0, size - 1, left, right, value);
}

private:
void updateRangeRecursive(int node, int start, int end, int left, int right, T value) {
    // Propagation de la lazy update
    if (lazy[node] != identity) {
        tree[node] = operation(tree[node], lazy[node] * (end - start + 1));
        if (start != end) {
            lazy[2 * node] = operation(lazy[2 * node], lazy[node]);
            lazy[2 * node + 1] = operation(lazy[2 * node + 1], lazy[node]);
        }
        lazy[node] = identity;
    }
    
    if (right < start || left > end) {
        return;
    }
    
    if (left <= start && end <= right) {
        tree[node] = operation(tree[node], value * (end - start + 1));
        if (start != end) {
            lazy[2 * node] = operation(lazy[2 * node], value);
            lazy[2 * node + 1] = operation(lazy[2 * node + 1], value);
        }
        return;
    }
    
    int mid = (start + end) / 2;
    updateRangeRecursive(2 * node, start, mid, left, right, value);
    updateRangeRecursive(2 * node + 1, mid + 1, end, left, right, value);
    
    tree[node] = operation(tree[2 * node], tree[2 * node + 1]);
}
```

## Propriétés

### 1. Structure d'arbre
- Arbre binaire complet
- Chaque nœud représente un intervalle
- Feuilles représentent les éléments individuels

### 2. Efficacité
- Requêtes en O(log n)
- Mises à jour en O(log n)
- Construction en O(n)

### 3. Lazy Propagation
- Mise à jour différée
- Optimisation des mises à jour en lot
- Réduction de la complexité

## Opérations spécialisées

### 1. Recherche du premier élément
```cpp
int findFirst(int left, int right, std::function<bool(T)> predicate) {
    if (left < 0 || right >= size || left > right) {
        return -1;
    }
    
    return findFirstRecursive(1, 0, size - 1, left, right, predicate);
}

private:
int findFirstRecursive(int node, int start, int end, int left, int right, std::function<bool(T)> predicate) {
    // Propagation de la lazy update
    if (lazy[node] != identity) {
        tree[node] = operation(tree[node], lazy[node] * (end - start + 1));
        if (start != end) {
            lazy[2 * node] = operation(lazy[2 * node], lazy[node]);
            lazy[2 * node + 1] = operation(lazy[2 * node + 1], lazy[node]);
        }
        lazy[node] = identity;
    }
    
    if (right < start || left > end) {
        return -1;
    }
    
    if (left <= start && end <= right) {
        if (start == end) {
            return predicate(tree[node]) ? start : -1;
        }
        
        int mid = (start + end) / 2;
        int leftResult = findFirstRecursive(2 * node, start, mid, left, right, predicate);
        if (leftResult != -1) {
            return leftResult;
        }
        return findFirstRecursive(2 * node + 1, mid + 1, end, left, right, predicate);
    }
    
    int mid = (start + end) / 2;
    int leftResult = findFirstRecursive(2 * node, start, mid, left, right, predicate);
    if (leftResult != -1) {
        return leftResult;
    }
    return findFirstRecursive(2 * node + 1, mid + 1, end, left, right, predicate);
}
```

### 2. Opérations de plage spécialisées
```cpp
T getSum(int left, int right) {
    return query(left, right);
}

T getMin(int left, int right) {
    if (left < 0 || right >= size || left > right) {
        return std::numeric_limits<T>::max();
    }
    
    return getMinRecursive(1, 0, size - 1, left, right);
}

private:
T getMinRecursive(int node, int start, int end, int left, int right) {
    // Propagation de la lazy update
    if (lazy[node] != identity) {
        tree[node] = operation(tree[node], lazy[node] * (end - start + 1));
        if (start != end) {
            lazy[2 * node] = operation(lazy[2 * node], lazy[node]);
            lazy[2 * node + 1] = operation(lazy[2 * node + 1], lazy[node]);
        }
        lazy[node] = identity;
    }
    
    if (right < start || left > end) {
        return std::numeric_limits<T>::max();
    }
    
    if (left <= start && end <= right) {
        return tree[node];
    }
    
    int mid = (start + end) / 2;
    T leftResult = getMinRecursive(2 * node, start, mid, left, right);
    T rightResult = getMinRecursive(2 * node + 1, mid + 1, end, left, right);
    
    return std::min(leftResult, rightResult);
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Construction | O(n) | n = taille du tableau |
| Requête | O(log n) | n = taille du tableau |
| Mise à jour | O(log n) | n = taille du tableau |
| Mise à jour de plage | O(log n) | n = taille du tableau |
| Recherche | O(log n) | n = taille du tableau |

## Cas d'usage

### 1. Requêtes de plage
- Somme, minimum, maximum
- Requêtes fréquentes
- Mises à jour en temps réel

### 2. Algorithmes de géométrie
- Intersection de segments
- Calculs de plage
- Optimisation spatiale

### 3. Traitement de données
- Agrégation de données
- Calculs statistiques
- Mises à jour en lot

## Tests

### 1. Tests unitaires
- Construction, requêtes, mises à jour
- Opérations de plage
- Gestion des cas limites

### 2. Tests de performance
- Temps d'exécution des opérations
- Utilisation mémoire
- Comparaison avec autres structures

### 3. Tests de robustesse
- Gestion des plages invalides
- Gestion des valeurs extrêmes
- Gestion mémoire

## Optimisations

### 1. Optimisations de lazy propagation
- Propagation optimisée
- Réduction des opérations
- Cache des valeurs

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des nœuds
- Gestion des fuites mémoire

### 3. Optimisations de requête
- Cache des résultats
- Optimisation des parcours
- Réduction des allocations

## Exemples d'utilisation

```cpp
// Création et utilisation basique
std::vector<int> arr = {1, 3, 5, 7, 9, 11};
SegmentTree<int> st(arr);

// Requêtes
int sum = st.getSum(1, 4); // Somme des éléments de l'index 1 à 4
int min = st.getMin(0, 5); // Minimum de tous les éléments

// Mises à jour
st.update(2, 10); // Mise à jour de l'élément à l'index 2
st.updateRange(1, 3, 5); // Ajout de 5 aux éléments de l'index 1 à 3

// Recherche
int first = st.findFirst(0, 5, [](int x) { return x > 5; });
```

## Notes d'implémentation

### 1. Gestion des types
- Support des types génériques
- Fonctions d'opération personnalisées
- Gestion des valeurs d'identité

### 2. Gestion mémoire
- Allocation dynamique
- Gestion des fuites
- Optimisation de l'espace

### 3. Compatibilité
- Support des types numériques
- Itérateurs STL
- Fonctions de callback

## Dépendances
- SegmentNode (nœud spécialisé)
- Structures de base de la Phase 1
- Algorithmes de plage

## Risques et mitigations

### 1. Utilisation mémoire
- **Risque** : Consommation excessive
- **Mitigation** : Optimisation, compression

### 2. Performance
- **Risque** : Dégradation avec la taille
- **Mitigation** : Optimisations, tests de performance

### 3. Gestion des plages
- **Risque** : Plages invalides
- **Mitigation** : Validation, gestion d'erreurs

## Métriques de qualité

### 1. Performance
- Temps d'accès O(log n) garanti
- Utilisation mémoire optimisée
- Pas de dégradation significative

### 2. Robustesse
- 100% de couverture de tests
- Gestion de tous les cas limites
- Pas de fuites mémoire

### 3. Maintenabilité
- Code lisible et documenté
- Tests compréhensibles
- Documentation complète