# Spécification détaillée - StringMatching

## Vue d'ensemble
StringMatching contient les algorithmes spécialisés pour la correspondance de chaînes de caractères, incluant les algorithmes de recherche de motifs et d'optimisation de performance.

## Objectifs
- Implémenter les algorithmes de correspondance de chaînes optimisés
- Fournir des opérations de recherche de motifs efficaces
- Optimiser les performances des opérations courantes
- Maintenir la cohérence des résultats

## Structure de données

### StringMatching
```cpp
class StringMatching {
public:
    // Algorithmes de base
    static int naiveSearch(const std::string& text, const std::string& pattern);
    static int kmpSearch(const std::string& text, const std::string& pattern);
    static int boyerMooreSearch(const std::string& text, const std::string& pattern);
    static int rabinKarpSearch(const std::string& text, const std::string& pattern);
    
    // Algorithmes avancés
    static std::vector<int> findAllOccurrences(const std::string& text, const std::string& pattern);
    static std::vector<int> findAllOccurrencesKMP(const std::string& text, const std::string& pattern);
    static std::vector<int> findAllOccurrencesBoyerMoore(const std::string& text, const std::string& pattern);
    static std::vector<int> findAllOccurrencesRabinKarp(const std::string& text, const std::string& pattern);
    
    // Algorithmes de préfixe
    static std::vector<int> computePrefixFunction(const std::string& pattern);
    static std::vector<int> computeZFunction(const std::string& text);
    static std::vector<int> computeFailureFunction(const std::string& pattern);
    
    // Algorithmes de correspondance multiple
    static std::vector<std::pair<int, std::string>> findMultiplePatterns(const std::string& text, const std::vector<std::string>& patterns);
    static std::vector<std::pair<int, std::string>> findMultiplePatternsAhoCorasick(const std::string& text, const std::vector<std::string>& patterns);
    
    // Algorithmes de correspondance approximative
    static int levenshteinDistance(const std::string& s1, const std::string& s2);
    static int editDistance(const std::string& s1, const std::string& s2);
    static bool fuzzyMatch(const std::string& text, const std::string& pattern, int maxDistance);
    
    // Algorithmes de correspondance avec jokers
    static bool wildcardMatch(const std::string& text, const std::string& pattern);
    static bool regexMatch(const std::string& text, const std::string& pattern);
    static std::vector<int> findWildcardOccurrences(const std::string& text, const std::string& pattern);
    
    // Algorithmes d'optimisation
    static void preprocessPattern(const std::string& pattern);
    static void preprocessText(const std::string& text);
    static void optimizeSearch(const std::string& pattern);
    
    // Algorithmes de debug
    static void printSearchResults(const std::vector<int>& results);
    static void printPatternAnalysis(const std::string& pattern);
    static void printTextAnalysis(const std::string& text);
};
```

## Algorithmes principaux

### 1. Algorithme de Knuth-Morris-Pratt (KMP)
```cpp
static int kmpSearch(const std::string& text, const std::string& pattern) {
    if (pattern.empty()) return 0;
    if (text.empty()) return -1;
    
    std::vector<int> prefix = computePrefixFunction(pattern);
    int textIndex = 0;
    int patternIndex = 0;
    
    while (textIndex < text.length()) {
        if (text[textIndex] == pattern[patternIndex]) {
            textIndex++;
            patternIndex++;
            
            if (patternIndex == pattern.length()) {
                return textIndex - patternIndex;
            }
        } else {
            if (patternIndex != 0) {
                patternIndex = prefix[patternIndex - 1];
            } else {
                textIndex++;
            }
        }
    }
    
    return -1;
}

static std::vector<int> computePrefixFunction(const std::string& pattern) {
    std::vector<int> prefix(pattern.length(), 0);
    int length = 0;
    
    for (int i = 1; i < pattern.length(); ++i) {
        while (length > 0 && pattern[i] != pattern[length]) {
            length = prefix[length - 1];
        }
        
        if (pattern[i] == pattern[length]) {
            length++;
        }
        
        prefix[i] = length;
    }
    
    return prefix;
}
```

### 2. Algorithme de Boyer-Moore
```cpp
static int boyerMooreSearch(const std::string& text, const std::string& pattern) {
    if (pattern.empty()) return 0;
    if (text.empty()) return -1;
    
    std::vector<int> badChar = computeBadCharacterTable(pattern);
    std::vector<int> goodSuffix = computeGoodSuffixTable(pattern);
    
    int textIndex = 0;
    
    while (textIndex <= text.length() - pattern.length()) {
        int patternIndex = pattern.length() - 1;
        
        while (patternIndex >= 0 && text[textIndex + patternIndex] == pattern[patternIndex]) {
            patternIndex--;
        }
        
        if (patternIndex < 0) {
            return textIndex;
        }
        
        int badCharShift = badChar[text[textIndex + patternIndex]];
        int goodSuffixShift = goodSuffix[patternIndex];
        
        textIndex += std::max(1, std::max(badCharShift, goodSuffixShift));
    }
    
    return -1;
}

private:
static std::vector<int> computeBadCharacterTable(const std::string& pattern) {
    std::vector<int> table(256, -1);
    
    for (int i = 0; i < pattern.length(); ++i) {
        table[pattern[i]] = i;
    }
    
    return table;
}

static std::vector<int> computeGoodSuffixTable(const std::string& pattern) {
    std::vector<int> table(pattern.length(), 0);
    std::vector<int> suffix(pattern.length(), 0);
    
    // Calcul des suffixes
    for (int i = pattern.length() - 1; i >= 0; --i) {
        if (i == pattern.length() - 1) {
            suffix[i] = pattern.length();
        } else {
            int j = i + 1;
            while (j < pattern.length() && pattern[i] != pattern[j]) {
                j = suffix[j];
            }
            suffix[i] = j;
        }
    }
    
    // Calcul de la table de bon suffixe
    for (int i = 0; i < pattern.length(); ++i) {
        if (suffix[i] == pattern.length()) {
            table[i] = pattern.length() - 1 - i;
        } else {
            table[i] = pattern.length() - 1 - suffix[i];
        }
    }
    
    return table;
}
```

### 3. Algorithme de Rabin-Karp
```cpp
static int rabinKarpSearch(const std::string& text, const std::string& pattern) {
    if (pattern.empty()) return 0;
    if (text.empty()) return -1;
    
    const int base = 256;
    const int mod = 1000000007;
    
    int patternHash = 0;
    int textHash = 0;
    int power = 1;
    
    // Calcul du hash du pattern et de la première fenêtre de texte
    for (int i = 0; i < pattern.length(); ++i) {
        patternHash = (patternHash * base + pattern[i]) % mod;
        textHash = (textHash * base + text[i]) % mod;
        if (i < pattern.length() - 1) {
            power = (power * base) % mod;
        }
    }
    
    // Recherche
    for (int i = 0; i <= text.length() - pattern.length(); ++i) {
        if (patternHash == textHash) {
            // Vérification caractère par caractère
            bool match = true;
            for (int j = 0; j < pattern.length(); ++j) {
                if (text[i + j] != pattern[j]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                return i;
            }
        }
        
        // Mise à jour du hash pour la fenêtre suivante
        if (i < text.length() - pattern.length()) {
            textHash = (base * (textHash - text[i] * power) + text[i + pattern.length()]) % mod;
            if (textHash < 0) {
                textHash += mod;
            }
        }
    }
    
    return -1;
}
```

## Opérations spécialisées

### 1. Correspondance multiple avec Aho-Corasick
```cpp
static std::vector<std::pair<int, std::string>> findMultiplePatternsAhoCorasick(const std::string& text, const std::vector<std::string>& patterns) {
    std::vector<std::pair<int, std::string>> results;
    
    // Construction de l'automate Aho-Corasick
    AhoCorasickAutomaton automaton;
    for (const auto& pattern : patterns) {
        automaton.addPattern(pattern);
    }
    automaton.build();
    
    // Recherche dans le texte
    int state = 0;
    for (int i = 0; i < text.length(); ++i) {
        state = automaton.getNextState(state, text[i]);
        std::vector<std::string> matches = automaton.getMatches(state);
        
        for (const auto& match : matches) {
            results.push_back({i - match.length() + 1, match});
        }
    }
    
    return results;
}
```

### 2. Correspondance approximative
```cpp
static int levenshteinDistance(const std::string& s1, const std::string& s2) {
    int m = s1.length();
    int n = s2.length();
    
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
    
    // Initialisation
    for (int i = 0; i <= m; ++i) {
        dp[i][0] = i;
    }
    for (int j = 0; j <= n; ++j) {
        dp[0][j] = j;
    }
    
    // Calcul de la distance
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + std::min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
            }
        }
    }
    
    return dp[m][n];
}

static bool fuzzyMatch(const std::string& text, const std::string& pattern, int maxDistance) {
    return levenshteinDistance(text, pattern) <= maxDistance;
}
```

### 3. Correspondance avec jokers
```cpp
static bool wildcardMatch(const std::string& text, const std::string& pattern) {
    int m = text.length();
    int n = pattern.length();
    
    std::vector<std::vector<bool>> dp(m + 1, std::vector<bool>(n + 1, false));
    dp[0][0] = true;
    
    // Gestion des jokers '*' au début
    for (int j = 1; j <= n; ++j) {
        if (pattern[j - 1] == '*') {
            dp[0][j] = dp[0][j - 1];
        }
    }
    
    // Calcul de la correspondance
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (pattern[j - 1] == '*') {
                dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
            } else if (pattern[j - 1] == '?' || text[i - 1] == pattern[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            }
        }
    }
    
    return dp[m][n];
}
```

## Complexités

| Algorithme | Complexité | Notes |
|------------|------------|-------|
| Naive | O(mn) | m = longueur texte, n = longueur pattern |
| KMP | O(m + n) | m = longueur texte, n = longueur pattern |
| Boyer-Moore | O(m + n) | m = longueur texte, n = longueur pattern |
| Rabin-Karp | O(m + n) | m = longueur texte, n = longueur pattern |
| Aho-Corasick | O(m + k) | m = longueur texte, k = nombre de patterns |
| Levenshtein | O(mn) | m = longueur s1, n = longueur s2 |
| Wildcard | O(mn) | m = longueur texte, n = longueur pattern |

## Cas d'usage

### 1. Recherche de texte
- Moteurs de recherche
- Éditeurs de texte
- Traitement de documents

### 2. Correspondance de motifs
- Détection de patterns
- Analyse de séquences
- Traitement de données

### 3. Correspondance approximative
- Correction d'erreurs
- Recherche floue
- Traitement de langage naturel

## Tests

### 1. Tests unitaires
- Algorithmes de base
- Algorithmes avancés
- Gestion des cas limites

### 2. Tests de performance
- Temps d'exécution des algorithmes
- Utilisation mémoire
- Comparaison des performances

### 3. Tests de robustesse
- Gestion des chaînes vides
- Gestion des caractères spéciaux
- Gestion des cas limites

## Optimisations

### 1. Optimisations d'algorithmes
- Précalcul des tables
- Optimisation des boucles
- Réduction des comparaisons

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des structures
- Gestion des fuites mémoire

### 3. Optimisations de recherche
- Cache des résultats
- Indexation des patterns
- Optimisation des parcours

## Exemples d'utilisation

```cpp
// Recherche basique
std::string text = "hello world";
std::string pattern = "world";
int position = StringMatching::kmpSearch(text, pattern);

// Recherche de toutes les occurrences
std::vector<int> positions = StringMatching::findAllOccurrences(text, pattern);

// Correspondance approximative
int distance = StringMatching::levenshteinDistance("hello", "hallo");
bool fuzzy = StringMatching::fuzzyMatch("hello", "hallo", 1);

// Correspondance avec jokers
bool wildcard = StringMatching::wildcardMatch("hello", "h*lo");
```

## Notes d'implémentation

### 1. Gestion des caractères
- Support des encodages
- Gestion des caractères spéciaux
- Optimisation des comparaisons

### 2. Gestion mémoire
- Allocation dynamique
- Gestion des fuites
- Optimisation de l'espace

### 3. Compatibilité
- Support des chaînes Unicode
- Itérateurs STL
- Fonctions de callback

## Dépendances
- Structures de base de la Phase 1
- Algorithmes de recherche
- Gestion mémoire appropriée

## Risques et mitigations

### 1. Performance
- **Risque** : Dégradation avec la taille
- **Mitigation** : Optimisations, tests de performance

### 2. Gestion des caractères
- **Risque** : Problèmes d'encodage
- **Mitigation** : Support robuste, tests

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