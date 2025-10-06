# Spécification détaillée - TrieOperations

## Vue d'ensemble
TrieOperations contient les algorithmes spécialisés pour les opérations de Trie, incluant les opérations de recherche, de préfixe et d'optimisation.

## Objectifs
- Implémenter les algorithmes de Trie optimisés
- Fournir les opérations de recherche spécialisées
- Optimiser les performances des opérations courantes
- Maintenir la cohérence de la structure d'arbre

## Structure de données

### TrieOperations
```cpp
template<typename T = char>
class TrieOperations {
public:
    // Opérations de recherche
    static bool search(TrieNode<T>* root, const std::string& word);
    static bool search(TrieNode<T>* root, const std::vector<T>& word);
    static TrieNode<T>* findNode(TrieNode<T>* root, const std::string& word);
    static TrieNode<T>* findNode(TrieNode<T>* root, const std::vector<T>& word);
    
    // Opérations de préfixe
    static bool startsWith(TrieNode<T>* root, const std::string& prefix);
    static bool startsWith(TrieNode<T>* root, const std::vector<T>& prefix);
    static std::vector<std::string> getWordsWithPrefix(TrieNode<T>* root, const std::string& prefix);
    static std::vector<std::vector<T>> getWordsWithPrefix(TrieNode<T>* root, const std::vector<T>& prefix);
    
    // Opérations de correspondance
    static std::vector<std::string> findWords(TrieNode<T>* root, const std::string& pattern);
    static std::vector<std::vector<T>> findWords(TrieNode<T>* root, const std::vector<T>& pattern);
    static std::vector<std::string> findWordsWithWildcards(TrieNode<T>* root, const std::string& pattern);
    
    // Opérations de parcours
    static std::vector<std::string> getAllWords(TrieNode<T>* root);
    static std::vector<std::vector<T>> getAllWordsAsVectors(TrieNode<T>* root);
    static void traverse(TrieNode<T>* root, std::function<void(const std::string&)> callback);
    static void traverse(TrieNode<T>* root, std::function<void(const std::vector<T>&)> callback);
    
    // Opérations d'optimisation
    static TrieNode<T>* compress(TrieNode<T>* root);
    static TrieNode<T>* optimize(TrieNode<T>* root);
    static void removeEmptyNodes(TrieNode<T>* root);
    static TrieNode<T>* rebuild(TrieNode<T>* root);
    
    // Opérations de maintenance
    static void updateHeights(TrieNode<T>* root);
    static int getHeight(TrieNode<T>* root);
    static bool isValid(TrieNode<T>* root);
    static void clear(TrieNode<T>* root);
    
    // Opérations de debug
    static void printTree(TrieNode<T>* root, int level = 0);
    static void printStatistics(TrieNode<T>* root);
    static bool validateTree(TrieNode<T>* root);
    static std::vector<std::string> getInorder(TrieNode<T>* root);
    
    // Opérations spécialisées
    static std::string getLongestCommonPrefix(TrieNode<T>* root);
    static std::string getShortestWord(TrieNode<T>* root);
    static std::string getLongestWord(TrieNode<T>* root);
    static int getWordCount(TrieNode<T>* root);
    static int getNodeCount(TrieNode<T>* root);
};
```

## Algorithmes principaux

### 1. Recherche de mots
```cpp
template<typename T>
bool TrieOperations<T>::search(TrieNode<T>* root, const std::string& word) {
    if (!root || word.empty()) return false;
    
    TrieNode<T>* current = root;
    
    for (char c : word) {
        if (!current->hasChild(c)) {
            return false;
        }
        current = current->getChild(c);
    }
    
    return current->isEndOfWord();
}

template<typename T>
TrieNode<T>* TrieOperations<T>::findNode(TrieNode<T>* root, const std::string& word) {
    if (!root || word.empty()) return nullptr;
    
    TrieNode<T>* current = root;
    
    for (char c : word) {
        if (!current->hasChild(c)) {
            return nullptr;
        }
        current = current->getChild(c);
    }
    
    return current;
}
```

### 2. Recherche de préfixes
```cpp
template<typename T>
std::vector<std::string> TrieOperations<T>::getWordsWithPrefix(TrieNode<T>* root, const std::string& prefix) {
    std::vector<std::string> result;
    
    if (!root || prefix.empty()) {
        return result;
    }
    
    TrieNode<T>* current = root;
    
    // Navigation vers le nœud de préfixe
    for (char c : prefix) {
        if (!current->hasChild(c)) {
            return result; // Préfixe non trouvé
        }
        current = current->getChild(c);
    }
    
    // Collecte des mots avec ce préfixe
    collectWords(current, prefix, result);
    
    return result;
}

private:
template<typename T>
void TrieOperations<T>::collectWords(TrieNode<T>* node, const std::string& prefix, std::vector<std::string>& result) {
    if (node->isEndOfWord()) {
        result.push_back(prefix);
    }
    
    for (auto& child : node->getChildren()) {
        std::string newPrefix = prefix + static_cast<char>(child.first);
        collectWords(child.second, newPrefix, result);
    }
}
```

### 3. Correspondance de motifs
```cpp
template<typename T>
std::vector<std::string> TrieOperations<T>::findWords(TrieNode<T>* root, const std::string& pattern) {
    std::vector<std::string> result;
    
    if (!root || pattern.empty()) {
        return result;
    }
    
    findWordsRecursive(root, "", pattern, 0, result);
    
    return result;
}

private:
template<typename T>
void TrieOperations<T>::findWordsRecursive(TrieNode<T>* node, const std::string& current, 
                                         const std::string& pattern, int index, 
                                         std::vector<std::string>& result) {
    if (index == pattern.length()) {
        if (node->isEndOfWord()) {
            result.push_back(current);
        }
        return;
    }
    
    char c = pattern[index];
    
    if (c == '.') {
        // Caractère joker
        for (auto& child : node->getChildren()) {
            std::string newCurrent = current + static_cast<char>(child.first);
            findWordsRecursive(child.second, newCurrent, pattern, index + 1, result);
        }
    } else {
        // Caractère spécifique
        if (node->hasChild(c)) {
            std::string newCurrent = current + c;
            findWordsRecursive(node->getChild(c), newCurrent, pattern, index + 1, result);
        }
    }
}
```

### 4. Compression de l'arbre
```cpp
template<typename T>
TrieNode<T>* TrieOperations<T>::compress(TrieNode<T>* root) {
    if (!root) return nullptr;
    
    compressRecursive(root);
    return root;
}

private:
template<typename T>
void TrieOperations<T>::compressRecursive(TrieNode<T>* node) {
    if (!node) return;
    
    // Compression récursive des enfants
    for (auto& child : node->getChildren()) {
        compressRecursive(child.second);
    }
    
    // Compression du nœud actuel
    if (node->getChildren().size() == 1 && !node->isEndOfWord()) {
        auto& child = *node->getChildren().begin();
        TrieNode<T>* childNode = child.second;
        
        // Fusion des nœuds
        node->mergeWith(childNode);
    }
}
```

## Opérations spécialisées

### 1. Recherche avec jokers
```cpp
template<typename T>
std::vector<std::string> TrieOperations<T>::findWordsWithWildcards(TrieNode<T>* root, const std::string& pattern) {
    std::vector<std::string> result;
    
    if (!root || pattern.empty()) {
        return result;
    }
    
    findWordsWithWildcardsRecursive(root, "", pattern, 0, result);
    
    return result;
}

private:
template<typename T>
void TrieOperations<T>::findWordsWithWildcardsRecursive(TrieNode<T>* node, const std::string& current, 
                                                       const std::string& pattern, int index, 
                                                       std::vector<std::string>& result) {
    if (index == pattern.length()) {
        if (node->isEndOfWord()) {
            result.push_back(current);
        }
        return;
    }
    
    char c = pattern[index];
    
    if (c == '*') {
        // Zéro ou plus de caractères
        if (node->isEndOfWord()) {
            result.push_back(current);
        }
        
        for (auto& child : node->getChildren()) {
            std::string newCurrent = current + static_cast<char>(child.first);
            findWordsWithWildcardsRecursive(child.second, newCurrent, pattern, index, result);
            findWordsWithWildcardsRecursive(child.second, newCurrent, pattern, index + 1, result);
        }
    } else if (c == '?') {
        // Un caractère quelconque
        for (auto& child : node->getChildren()) {
            std::string newCurrent = current + static_cast<char>(child.first);
            findWordsWithWildcardsRecursive(child.second, newCurrent, pattern, index + 1, result);
        }
    } else {
        // Caractère spécifique
        if (node->hasChild(c)) {
            std::string newCurrent = current + c;
            findWordsWithWildcardsRecursive(node->getChild(c), newCurrent, pattern, index + 1, result);
        }
    }
}
```

### 2. Calcul du préfixe commun le plus long
```cpp
template<typename T>
std::string TrieOperations<T>::getLongestCommonPrefix(TrieNode<T>* root) {
    if (!root) return "";
    
    std::string prefix = "";
    TrieNode<T>* current = root;
    
    while (current->getChildren().size() == 1 && !current->isEndOfWord()) {
        auto& child = *current->getChildren().begin();
        prefix += static_cast<char>(child.first);
        current = child.second;
    }
    
    return prefix;
}
```

### 3. Optimisation de l'arbre
```cpp
template<typename T>
TrieNode<T>* TrieOperations<T>::optimize(TrieNode<T>* root) {
    if (!root) return nullptr;
    
    // Compression
    compress(root);
    
    // Suppression des nœuds vides
    removeEmptyNodes(root);
    
    // Reconstruction si nécessaire
    if (getNodeCount(root) > getWordCount(root) * 2) {
        return rebuild(root);
    }
    
    return root;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Recherche | O(m) | m = longueur de la chaîne |
| Préfixe | O(m + k) | m = longueur préfixe, k = nombre de mots |
| Correspondance | O(m + k) | m = longueur motif, k = nombre de matches |
| Compression | O(n) | n = nombre de nœuds |
| Optimisation | O(n) | n = nombre de nœuds |
| Parcours | O(n) | n = nombre de nœuds |

## Propriétés

### 1. Efficacité
- Recherche en O(m) où m est la longueur
- Insertion en O(m)
- Suppression en O(m)

### 2. Optimisation
- Compression des nœuds
- Réduction de la mémoire
- Amélioration des performances

### 3. Robustesse
- Gestion des cas limites
- Validation des opérations
- Gestion des erreurs

## Cas d'usage

### 1. Dictionnaire
- Stockage de mots
- Recherche rapide
- Suggestions de mots

### 2. Autocomplétion
- Suggestions de préfixes
- Recherche en temps réel
- Interface utilisateur

### 3. Recherche de motifs
- Correspondance de patterns
- Recherche avec jokers
- Filtrage de texte

## Tests

### 1. Tests unitaires
- Opérations de recherche
- Opérations de préfixe
- Opérations de correspondance
- Opérations d'optimisation

### 2. Tests d'intégration
- Interaction avec Trie
- Gestion des pointeurs parent
- Maintien des propriétés

### 3. Tests de performance
- Temps d'exécution des opérations
- Utilisation mémoire
- Optimisations

## Optimisations

### 1. Optimisations de recherche
- Cache des résultats
- Indexation des préfixes
- Optimisation des parcours

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des nœuds
- Gestion des fuites mémoire

### 3. Optimisations de compression
- Compression automatique
- Détection des redondances
- Optimisation de la structure

## Exemples d'utilisation

```cpp
// Opérations de base
TrieNode<char>* root = new TrieNode<char>();
bool found = TrieOperations<char>::search(root, "hello");

// Recherche de préfixes
std::vector<std::string> words = TrieOperations<char>::getWordsWithPrefix(root, "hel");

// Correspondance de motifs
std::vector<std::string> matches = TrieOperations<char>::findWords(root, "h.llo");

// Optimisation
root = TrieOperations<char>::optimize(root);
```

## Notes d'implémentation

### 1. Gestion des caractères
- Support des types génériques
- Gestion des caractères spéciaux
- Encodage approprié

### 2. Gestion mémoire
- Allocation dynamique
- Gestion des fuites
- Optimisation de l'espace

### 3. Compatibilité
- Support des chaînes et vecteurs
- Itérateurs STL
- Fonctions de callback

## Dépendances
- TrieNode (nœud spécialisé)
- Structures de base de la Phase 1
- Algorithmes de recherche

## Risques et mitigations

### 1. Utilisation mémoire
- **Risque** : Consommation excessive
- **Mitigation** : Compression, optimisation

### 2. Performance
- **Risque** : Dégradation avec la profondeur
- **Mitigation** : Optimisations, tests de performance

### 3. Gestion des caractères
- **Risque** : Problèmes d'encodage
- **Mitigation** : Support robuste, tests

## Métriques de qualité

### 1. Performance
- Temps d'accès O(m) garanti
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