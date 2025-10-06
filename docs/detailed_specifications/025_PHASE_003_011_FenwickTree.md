# Spécification détaillée - FenwickTree

## Vue d'ensemble
L'arbre de Fenwick (Binary Indexed Tree, BIT) est une structure de données spécialisée pour effectuer des requêtes de somme de préfixes et des mises à jour sur un tableau de manière efficace. Il permet des opérations en O(log n) pour les requêtes et mises à jour.

## Objectifs
- Implémenter un arbre de Fenwick optimisé
- Fournir des requêtes de somme de préfixes efficaces
- Supporter les mises à jour en temps réel
- Optimiser l'utilisation mémoire

## Structure de données

### FenwickTree
```cpp
template<typename T>
class FenwickTree {
private:
    std::vector<T> tree;
    size_t size;
    
public:
    // Constructeurs
    FenwickTree(size_t size);
    FenwickTree(const std::vector<T>& arr);
    ~FenwickTree();
    
    // Opérations de base
    void update(int index, T value);
    void add(int index, T value);
    T query(int index);
    T query(int left, int right);
    
    // Opérations de requête
    T getSum(int index);
    T getSum(int left, int right);
    T getPrefixSum(int index);
    T getRangeSum(int left, int right);
    
    // Opérations de mise à jour
    void set(int index, T value);
    void addRange(int left, int right, T value);
    void multiply(int index, T value);
    void multiplyRange(int left, int right, T value);
    
    // Opérations de maintenance
    void rebuild();
    void clear();
    bool empty() const;
    size_t getSize() const;
    
    // Opérations spécialisées
    int findKth(int k);
    int findFirst(int left, int right, std::function<bool(T)> predicate);
    int findLast(int left, int right, std::function<bool(T)> predicate);
    std::vector<T> getArray();
    void setArray(const std::vector<T>& arr);
    
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
FenwickTree(const std::vector<T>& arr) : size(arr.size()) {
    if (size == 0) return;
    
    tree.resize(size + 1, T{});
    
    // Construction de l'arbre
    for (size_t i = 0; i < size; ++i) {
        update(i, arr[i]);
    }
}
```

### 2. Mise à jour
```cpp
void update(int index, T value) {
    if (index < 0 || index >= size) return;
    
    index++; // Conversion en 1-indexé
    
    while (index <= size) {
        tree[index] += value;
        index += index & (-index); // Ajout du bit le moins significatif
    }
}

void add(int index, T value) {
    update(index, value);
}
```

### 3. Requête de somme
```cpp
T query(int index) {
    if (index < 0 || index >= size) return T{};
    
    index++; // Conversion en 1-indexé
    T result = T{};
    
    while (index > 0) {
        result += tree[index];
        index -= index & (-index); // Suppression du bit le moins significatif
    }
    
    return result;
}

T query(int left, int right) {
    if (left < 0 || right >= size || left > right) return T{};
    
    if (left == 0) {
        return query(right);
    }
    
    return query(right) - query(left - 1);
}
```

## Propriétés

### 1. Structure d'arbre
- Arbre binaire indexé
- Chaque nœud stocke la somme d'un intervalle
- Indexation basée sur les bits

### 2. Efficacité
- Requêtes en O(log n)
- Mises à jour en O(log n)
- Construction en O(n log n)

### 3. Optimisation mémoire
- Utilisation minimale de la mémoire
- Pas de lazy propagation nécessaire
- Structure compacte

## Opérations spécialisées

### 1. Recherche du k-ième élément
```cpp
int findKth(int k) {
    if (k < 1 || k > query(size - 1)) {
        return -1;
    }
    
    int index = 0;
    int bit = 1;
    
    // Trouver la puissance de 2 la plus grande
    while (bit < size) {
        bit <<= 1;
    }
    
    while (bit > 0) {
        int nextIndex = index + bit;
        if (nextIndex <= size && tree[nextIndex] < k) {
            k -= tree[nextIndex];
            index = nextIndex;
        }
        bit >>= 1;
    }
    
    return index;
}
```

### 2. Mise à jour de plage
```cpp
void addRange(int left, int right, T value) {
    if (left < 0 || right >= size || left > right) return;
    
    // Mise à jour du début de la plage
    update(left, value);
    
    // Mise à jour de la fin de la plage
    if (right + 1 < size) {
        update(right + 1, -value);
    }
}
```

### 3. Recherche du premier élément
```cpp
int findFirst(int left, int right, std::function<bool(T)> predicate) {
    if (left < 0 || right >= size || left > right) return -1;
    
    T prefixSum = (left == 0) ? T{} : query(left - 1);
    
    for (int i = left; i <= right; ++i) {
        prefixSum += getValue(i);
        if (predicate(prefixSum)) {
            return i;
        }
    }
    
    return -1;
}

private:
T getValue(int index) {
    if (index < 0 || index >= size) return T{};
    
    T result = tree[index + 1];
    int parent = index + 1;
    
    while (parent > 0) {
        int prevParent = parent - (parent & (-parent));
        if (prevParent > 0) {
            result -= tree[prevParent];
        }
        parent = prevParent;
    }
    
    return result;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Construction | O(n log n) | n = taille du tableau |
| Requête | O(log n) | n = taille du tableau |
| Mise à jour | O(log n) | n = taille du tableau |
| Mise à jour de plage | O(log n) | n = taille du tableau |
| Recherche | O(log n) | n = taille du tableau |

## Cas d'usage

### 1. Requêtes de somme de préfixes
- Calculs de sommes cumulatives
- Requêtes fréquentes
- Mises à jour en temps réel

### 2. Algorithmes de géométrie
- Calculs de plage
- Optimisation spatiale
- Requêtes de rectangle

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
- Gestion des indices invalides
- Gestion des valeurs extrêmes
- Gestion mémoire

## Optimisations

### 1. Optimisations de requête
- Cache des résultats
- Optimisation des parcours
- Réduction des allocations

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des nœuds
- Gestion des fuites mémoire

### 3. Optimisations de mise à jour
- Mise à jour en lot
- Optimisation des opérations
- Réduction des calculs

## Exemples d'utilisation

```cpp
// Création et utilisation basique
std::vector<int> arr = {1, 3, 5, 7, 9, 11};
FenwickTree<int> ft(arr);

// Requêtes
int sum = ft.getSum(4); // Somme des éléments de l'index 0 à 4
int rangeSum = ft.getRangeSum(1, 4); // Somme des éléments de l'index 1 à 4

// Mises à jour
ft.add(2, 10); // Ajout de 10 à l'élément à l'index 2
ft.addRange(1, 3, 5); // Ajout de 5 aux éléments de l'index 1 à 3

// Recherche
int kth = ft.findKth(5); // Trouver le 5-ième élément
```

## Notes d'implémentation

### 1. Gestion des types
- Support des types génériques
- Gestion des valeurs numériques
- Gestion des opérations arithmétiques

### 2. Gestion mémoire
- Allocation dynamique
- Gestion des fuites
- Optimisation de l'espace

### 3. Compatibilité
- Support des types numériques
- Itérateurs STL
- Fonctions de callback

## Dépendances
- Structures de base de la Phase 1
- Algorithmes de plage
- Gestion mémoire appropriée

## Risques et mitigations

### 1. Utilisation mémoire
- **Risque** : Consommation excessive
- **Mitigation** : Optimisation, compression

### 2. Performance
- **Risque** : Dégradation avec la taille
- **Mitigation** : Optimisations, tests de performance

### 3. Gestion des indices
- **Risque** : Indices invalides
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