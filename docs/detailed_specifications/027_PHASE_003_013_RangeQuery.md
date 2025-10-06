# Spécification détaillée - RangeQuery

## Vue d'ensemble
RangeQuery contient les algorithmes spécialisés pour les requêtes de plage, incluant les opérations de somme, minimum, maximum et autres agrégations sur des intervalles.

## Objectifs
- Implémenter les algorithmes de requêtes de plage optimisés
- Fournir des opérations d'agrégation efficaces
- Optimiser les performances des opérations courantes
- Maintenir la cohérence des résultats

## Structure de données

### RangeQuery
```cpp
template<typename T>
class RangeQuery {
public:
    // Algorithmes de base
    static T rangeSum(const std::vector<T>& arr, int left, int right);
    static T rangeMin(const std::vector<T>& arr, int left, int right);
    static T rangeMax(const std::vector<T>& arr, int left, int right);
    static T rangeProduct(const std::vector<T>& arr, int left, int right);
    static T rangeGCD(const std::vector<T>& arr, int left, int right);
    static T rangeLCM(const std::vector<T>& arr, int left, int right);
    
    // Algorithmes avec précalcul
    static void precomputePrefixSums(const std::vector<T>& arr, std::vector<T>& prefixSums);
    static void precomputeSparseTable(const std::vector<T>& arr, std::vector<std::vector<T>>& sparseTable);
    static void precomputeSegmentTree(const std::vector<T>& arr, std::vector<T>& segmentTree);
    
    // Algorithmes de requêtes optimisées
    static T querySum(const std::vector<T>& prefixSums, int left, int right);
    static T queryMin(const std::vector<std::vector<T>>& sparseTable, const std::vector<T>& arr, int left, int right);
    static T queryMax(const std::vector<std::vector<T>>& sparseTable, const std::vector<T>& arr, int left, int right);
    static T queryGCD(const std::vector<T>& arr, int left, int right);
    static T queryLCM(const std::vector<T>& arr, int left, int right);
    
    // Algorithmes de requêtes multiples
    static std::vector<T> batchQuerySum(const std::vector<T>& arr, const std::vector<std::pair<int, int>>& queries);
    static std::vector<T> batchQueryMin(const std::vector<T>& arr, const std::vector<std::pair<int, int>>& queries);
    static std::vector<T> batchQueryMax(const std::vector<T>& arr, const std::vector<std::pair<int, int>>& queries);
    
    // Algorithmes de requêtes dynamiques
    static void updateValue(std::vector<T>& arr, int index, T value);
    static void updateRange(std::vector<T>& arr, int left, int right, T value);
    static T querySumDynamic(const std::vector<T>& arr, int left, int right);
    static T queryMinDynamic(const std::vector<T>& arr, int left, int right);
    static T queryMaxDynamic(const std::vector<T>& arr, int left, int right);
    
    // Algorithmes de requêtes spécialisées
    static int countInRange(const std::vector<T>& arr, int left, int right, T value);
    static int countInRange(const std::vector<T>& arr, int left, int right, std::function<bool(T)> predicate);
    static std::vector<T> getRangeValues(const std::vector<T>& arr, int left, int right);
    static void setRangeValues(std::vector<T>& arr, int left, int right, T value);
    
    // Algorithmes de requêtes avec conditions
    static bool allInRange(const std::vector<T>& arr, int left, int right, std::function<bool(T)> predicate);
    static bool anyInRange(const std::vector<T>& arr, int left, int right, std::function<bool(T)> predicate);
    static T findFirstInRange(const std::vector<T>& arr, int left, int right, std::function<bool(T)> predicate);
    static T findLastInRange(const std::vector<T>& arr, int left, int right, std::function<bool(T)> predicate);
    
    // Algorithmes de requêtes statistiques
    static T getMedian(const std::vector<T>& arr, int left, int right);
    static T getMode(const std::vector<T>& arr, int left, int right);
    static double getMean(const std::vector<T>& arr, int left, int right);
    static T getVariance(const std::vector<T>& arr, int left, int right);
    
    // Algorithmes de debug
    static void printQueryResults(const std::vector<T>& results);
    static void printArrayAnalysis(const std::vector<T>& arr);
    static void printQueryStatistics(const std::vector<T>& arr, const std::vector<std::pair<int, int>>& queries);
};
```

## Algorithmes principaux

### 1. Requêtes de somme avec précalcul
```cpp
static void precomputePrefixSums(const std::vector<T>& arr, std::vector<T>& prefixSums) {
    prefixSums.resize(arr.size() + 1);
    prefixSums[0] = T{};
    
    for (size_t i = 0; i < arr.size(); ++i) {
        prefixSums[i + 1] = prefixSums[i] + arr[i];
    }
}

static T querySum(const std::vector<T>& prefixSums, int left, int right) {
    if (left < 0 || right >= prefixSums.size() - 1 || left > right) {
        return T{};
    }
    
    return prefixSums[right + 1] - prefixSums[left];
}
```

### 2. Requêtes de minimum/maximum avec table clairsemée
```cpp
static void precomputeSparseTable(const std::vector<T>& arr, std::vector<std::vector<T>>& sparseTable) {
    int n = arr.size();
    int logn = 32 - __builtin_clz(n);
    
    sparseTable.resize(n, std::vector<T>(logn));
    
    // Initialisation
    for (int i = 0; i < n; ++i) {
        sparseTable[i][0] = arr[i];
    }
    
    // Construction de la table
    for (int j = 1; j < logn; ++j) {
        for (int i = 0; i + (1 << j) <= n; ++i) {
            sparseTable[i][j] = std::min(sparseTable[i][j - 1], sparseTable[i + (1 << (j - 1))][j - 1]);
        }
    }
}

static T queryMin(const std::vector<std::vector<T>>& sparseTable, const std::vector<T>& arr, int left, int right) {
    if (left < 0 || right >= arr.size() || left > right) {
        return std::numeric_limits<T>::max();
    }
    
    int length = right - left + 1;
    int k = 32 - __builtin_clz(length) - 1;
    
    return std::min(sparseTable[left][k], sparseTable[right - (1 << k) + 1][k]);
}
```

### 3. Requêtes de GCD/LCM
```cpp
static T queryGCD(const std::vector<T>& arr, int left, int right) {
    if (left < 0 || right >= arr.size() || left > right) {
        return T{};
    }
    
    T result = arr[left];
    for (int i = left + 1; i <= right; ++i) {
        result = std::gcd(result, arr[i]);
    }
    
    return result;
}

static T queryLCM(const std::vector<T>& arr, int left, int right) {
    if (left < 0 || right >= arr.size() || left > right) {
        return T{};
    }
    
    T result = arr[left];
    for (int i = left + 1; i <= right; ++i) {
        result = (result * arr[i]) / std::gcd(result, arr[i]);
    }
    
    return result;
}
```

## Opérations spécialisées

### 1. Requêtes par lots
```cpp
static std::vector<T> batchQuerySum(const std::vector<T>& arr, const std::vector<std::pair<int, int>>& queries) {
    std::vector<T> results;
    results.reserve(queries.size());
    
    // Précalcul des sommes de préfixes
    std::vector<T> prefixSums;
    precomputePrefixSums(arr, prefixSums);
    
    // Exécution des requêtes
    for (const auto& query : queries) {
        results.push_back(querySum(prefixSums, query.first, query.second));
    }
    
    return results;
}
```

### 2. Requêtes avec conditions
```cpp
static bool allInRange(const std::vector<T>& arr, int left, int right, std::function<bool(T)> predicate) {
    if (left < 0 || right >= arr.size() || left > right) {
        return false;
    }
    
    for (int i = left; i <= right; ++i) {
        if (!predicate(arr[i])) {
            return false;
        }
    }
    
    return true;
}

static T findFirstInRange(const std::vector<T>& arr, int left, int right, std::function<bool(T)> predicate) {
    if (left < 0 || right >= arr.size() || left > right) {
        return T{};
    }
    
    for (int i = left; i <= right; ++i) {
        if (predicate(arr[i])) {
            return arr[i];
        }
    }
    
    return T{};
}
```

### 3. Requêtes statistiques
```cpp
static T getMedian(const std::vector<T>& arr, int left, int right) {
    if (left < 0 || right >= arr.size() || left > right) {
        return T{};
    }
    
    std::vector<T> range(arr.begin() + left, arr.begin() + right + 1);
    std::sort(range.begin(), range.end());
    
    int n = range.size();
    if (n % 2 == 0) {
        return (range[n / 2 - 1] + range[n / 2]) / 2;
    } else {
        return range[n / 2];
    }
}

static double getMean(const std::vector<T>& arr, int left, int right) {
    if (left < 0 || right >= arr.size() || left > right) {
        return 0.0;
    }
    
    T sum = T{};
    int count = 0;
    
    for (int i = left; i <= right; ++i) {
        sum += arr[i];
        count++;
    }
    
    return static_cast<double>(sum) / count;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Précalcul somme | O(n) | n = taille du tableau |
| Requête somme | O(1) | Avec précalcul |
| Précalcul min/max | O(n log n) | Table clairsemée |
| Requête min/max | O(1) | Avec précalcul |
| Requête GCD/LCM | O(n) | n = taille de la plage |
| Requête par lots | O(n + q) | n = taille, q = nombre de requêtes |
| Requête statistique | O(n log n) | n = taille de la plage |

## Cas d'usage

### 1. Requêtes de plage
- Calculs de sommes
- Recherche de min/max
- Agrégations de données

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
- Algorithmes de base
- Algorithmes avec précalcul
- Gestion des cas limites

### 2. Tests de performance
- Temps d'exécution des algorithmes
- Utilisation mémoire
- Comparaison des performances

### 3. Tests de robustesse
- Gestion des plages invalides
- Gestion des valeurs extrêmes
- Gestion mémoire

## Optimisations

### 1. Optimisations d'algorithmes
- Précalcul des structures
- Optimisation des boucles
- Réduction des calculs

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des structures
- Gestion des fuites mémoire

### 3. Optimisations de requêtes
- Cache des résultats
- Indexation des données
- Optimisation des parcours

## Exemples d'utilisation

```cpp
// Requêtes basiques
std::vector<int> arr = {1, 3, 5, 7, 9, 11};
int sum = RangeQuery<int>::rangeSum(arr, 1, 4);
int min = RangeQuery<int>::rangeMin(arr, 0, 5);

// Requêtes avec précalcul
std::vector<int> prefixSums;
RangeQuery<int>::precomputePrefixSums(arr, prefixSums);
int sumFast = RangeQuery<int>::querySum(prefixSums, 1, 4);

// Requêtes par lots
std::vector<std::pair<int, int>> queries = {{0, 2}, {1, 4}, {2, 5}};
std::vector<int> results = RangeQuery<int>::batchQuerySum(arr, queries);

// Requêtes avec conditions
bool allPositive = RangeQuery<int>::allInRange(arr, 0, 5, [](int x) { return x > 0; });
```

## Notes d'implémentation

### 1. Gestion des types
- Support des types génériques
- Gestion des opérations arithmétiques
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
- Structures de base de la Phase 1
- Algorithmes de plage
- Gestion mémoire appropriée

## Risques et mitigations

### 1. Performance
- **Risque** : Dégradation avec la taille
- **Mitigation** : Optimisations, tests de performance

### 2. Gestion des plages
- **Risque** : Plages invalides
- **Mitigation** : Validation, gestion d'erreurs

### 3. Gestion mémoire
- **Risque** : Fuites mémoire, fragmentation
- **Mitigation** : RAII, tests de mémoire, profilage

## Métriques de qualité

### 1. Performance
- Temps d'exécution optimisé
- Utilisation mémoire minimale
- Pas de dégradation significative

### 2. Robustesse
- 100% de couverture de tests
- Gestion de tous les cas limites
- Pas de fuites mémoire

### 3. Maintenabilité
- Code lisible et documenté
- Tests compréhensibles
- Documentation complète