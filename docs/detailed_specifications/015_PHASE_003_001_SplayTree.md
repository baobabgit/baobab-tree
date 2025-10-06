# Spécification détaillée - SplayTree

## Vue d'ensemble
L'arbre Splay est une structure de données auto-ajustable qui déplace automatiquement les éléments accédés vers la racine. Cette propriété améliore les performances pour les accès répétés aux mêmes éléments.

## Objectifs
- Implémenter un arbre binaire de recherche auto-ajustable
- Optimiser les performances pour les accès répétés
- Maintenir la propriété BST après chaque opération
- Fournir des opérations de base avec auto-ajustement

## Structure de données

### SplayTree
```cpp
template<typename T>
class SplayTree {
private:
    SplayNode<T>* root;
    size_t size;
    
public:
    // Constructeurs
    SplayTree();
    ~SplayTree();
    
    // Opérations de base
    bool insert(const T& value);
    bool remove(const T& value);
    bool search(const T& value);
    bool contains(const T& value);
    
    // Opérations d'accès
    T& find(const T& value);
    const T& find(const T& value) const;
    
    // Opérations de parcours
    std::vector<T> inorder() const;
    std::vector<T> preorder() const;
    std::vector<T> postorder() const;
    
    // Opérations de maintenance
    void clear();
    bool empty() const;
    size_t getSize() const;
    
    // Opérations spécialisées
    T& getMin();
    T& getMax();
    T removeMin();
    T removeMax();
    
    // Opérations de fusion et division
    void merge(SplayTree<T>& other);
    SplayTree<T> split(const T& value);
    
    // Opérations de debug
    void print() const;
    bool isValid() const;
    int getHeight() const;
};
```

## Algorithmes principaux

### 1. Opération Splay
```cpp
private:
    SplayNode<T>* splay(SplayNode<T>* node, const T& value);
    SplayNode<T>* zig(SplayNode<T>* node);
    SplayNode<T>* zigZig(SplayNode<T>* node);
    SplayNode<T>* zigZag(SplayNode<T>* node);
```

### 2. Insertion avec Splay
```cpp
bool insert(const T& value) {
    if (!root) {
        root = new SplayNode<T>(value);
        size = 1;
        return true;
    }
    
    root = splay(root, value);
    
    if (root->data == value) {
        return false; // Élément déjà présent
    }
    
    SplayNode<T>* newNode = new SplayNode<T>(value);
    
    if (value < root->data) {
        newNode->right = root;
        newNode->left = root->left;
        root->left = nullptr;
        if (newNode->left) newNode->left->parent = newNode;
    } else {
        newNode->left = root;
        newNode->right = root->right;
        root->right = nullptr;
        if (newNode->right) newNode->right->parent = newNode;
    }
    
    root->parent = newNode;
    root = newNode;
    size++;
    return true;
}
```

### 3. Suppression avec Splay
```cpp
bool remove(const T& value) {
    if (!root) return false;
    
    root = splay(root, value);
    
    if (root->data != value) {
        return false; // Élément non trouvé
    }
    
    SplayNode<T>* leftTree = root->left;
    SplayNode<T>* rightTree = root->right;
    
    delete root;
    
    if (!leftTree) {
        root = rightTree;
    } else if (!rightTree) {
        root = leftTree;
    } else {
        leftTree->parent = nullptr;
        rightTree->parent = nullptr;
        
        // Trouver le maximum dans le sous-arbre gauche
        SplayNode<T>* maxLeft = leftTree;
        while (maxLeft->right) {
            maxLeft = maxLeft->right;
        }
        
        leftTree = splay(leftTree, maxLeft->data);
        leftTree->right = rightTree;
        rightTree->parent = leftTree;
        root = leftTree;
    }
    
    if (root) root->parent = nullptr;
    size--;
    return true;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Insertion | O(log n) amorti | O(n) dans le pire cas |
| Suppression | O(log n) amorti | O(n) dans le pire cas |
| Recherche | O(log n) amorti | O(n) dans le pire cas |
| Splay | O(log n) amorti | O(n) dans le pire cas |
| Parcours | O(n) | Visite de tous les nœuds |
| Fusion | O(log n) amorti | O(n) dans le pire cas |
| Division | O(log n) amorti | O(n) dans le pire cas |

## Propriétés

### 1. Auto-ajustement
- Chaque accès déplace l'élément vers la racine
- Les éléments fréquemment accédés restent près de la racine
- Amélioration des performances pour les accès répétés

### 2. Propriété BST
- Maintenue après chaque opération
- Ordre des éléments préservé
- Structure de recherche binaire valide

### 3. Équilibrage
- Pas d'équilibrage explicite
- Auto-ajustement basé sur l'usage
- Performance amortie O(log n)

## Cas d'usage

### 1. Cache LRU
- Éléments récemment accédés en haut
- Suppression des éléments les moins utilisés
- Performance optimale pour les accès répétés

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
- Insertion, suppression, recherche
- Opérations de parcours
- Fusion et division
- Gestion des cas limites

### 2. Tests de performance
- Temps d'accès pour différents patterns
- Comparaison avec BST standard
- Analyse de la complexité amortie

### 3. Tests de robustesse
- Gestion des doublons
- Opérations sur arbre vide
- Gestion mémoire

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
// Création et utilisation basique
SplayTree<int> tree;
tree.insert(5);
tree.insert(3);
tree.insert(7);

// Recherche avec auto-ajustement
bool found = tree.search(3); // 3 devient la racine

// Suppression
tree.remove(5);

// Parcours
std::vector<int> elements = tree.inorder();
```

## Notes d'implémentation

### 1. Gestion des pointeurs
- Mise à jour correcte des pointeurs parent
- Gestion des cas de racine
- Éviter les cycles

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
- SplayOperations (opérations de splay)
- Structures de base de la Phase 1

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

## Livrables

### Classes principales
- [x] **SplayTree** - Classe principale de l'arbre auto-ajustable
- [x] **SplayNode** - Nœud spécialisé avec métadonnées de performance

### Exceptions spécialisées
- [x] **SplayTreeError** - Exception de base pour les erreurs SplayTree
- [x] **SplayOperationError** - Exception pour les erreurs d'opérations de splay
- [x] **SplayNodeError** - Exception pour les erreurs de nœuds Splay
- [x] **SplayValidationError** - Exception pour les erreurs de validation

### Opérations de base
- [x] **insert(value)** - Insertion avec splay automatique
- [x] **search(value)** - Recherche avec splay automatique
- [x] **delete(value)** - Suppression avec splay automatique
- [x] **find(value)** - Recherche et retour de valeur avec splay

### Opérations d'accès
- [x] **get_min()** - Récupération du minimum avec splay
- [x] **get_max()** - Récupération du maximum avec splay
- [x] **remove_min()** - Suppression et retour du minimum
- [x] **remove_max()** - Suppression et retour du maximum

### Opérations de parcours
- [x] **inorder()** - Parcours infixe (hérité de BinarySearchTree)
- [x] **preorder()** - Parcours préfixe (hérité de BinarySearchTree)
- [x] **postorder()** - Parcours postfixe (hérité de BinarySearchTree)
- [x] **level_order()** - Parcours par niveaux (hérité de BinarySearchTree)

### Opérations de maintenance
- [x] **clear()** - Vidage de l'arbre (hérité de BinarySearchTree)
- [x] **empty()** - Vérification si l'arbre est vide (hérité de BinarySearchTree)
- [x] **get_size()** - Taille de l'arbre (hérité de BinarySearchTree)
- [x] **is_valid()** - Validation de l'arbre Splay

### Opérations spécialisées
- [x] **merge(other)** - Fusion de deux arbres Splay
- [x] **split(value)** - Division de l'arbre selon une valeur

### Algorithmes de splay
- [x] **_splay(node)** - Opération de splay principale
- [x] **_zig(node)** - Rotation simple (zig)
- [x] **_zig_zig(node)** - Rotation double zig-zig
- [x] **_zig_zag(node)** - Rotation double zig-zag
- [x] **_is_zig_zig(node)** - Détection du cas zig-zig

### Méthodes de diagnostic et performance
- [x] **get_splay_count()** - Nombre total d'opérations de splay
- [x] **get_total_accesses()** - Nombre total d'accès
- [x] **get_performance_metrics()** - Métriques de performance complètes

### Méthodes de debug
- [x] **print()** - Affichage de l'arbre
- [x] **get_height()** - Hauteur de l'arbre (hérité de BinarySearchTree)

### Tests unitaires
- [x] **TestSplayTree** - 42 tests pour la classe SplayTree
- [x] **TestSplayNode** - 17 tests pour la classe SplayNode
- [x] **Tests de fonctionnalité de base** - Insertion, recherche, suppression
- [x] **Tests d'opérations avancées** - Min, max, merge, split
- [x] **Tests de performance** - Compteurs et métriques
- [x] **Tests de comportement splay** - Vérification de l'auto-ajustement

### Documentation
- [x] **Documentation complète** - Docstrings reStructuredText pour toutes les méthodes
- [x] **Exemples d'utilisation** - Exemples dans les docstrings
- [x] **Types et annotations** - Annotations de type complètes
- [x] **Gestion d'erreurs** - Messages d'erreur informatifs

### Intégration
- [x] **Exports dans __init__.py** - Classes exportées dans le module principal
- [x] **Héritage de BinarySearchTree** - Réutilisation des fonctionnalités de base
- [x] **Compatibilité avec les interfaces** - Respect des interfaces existantes

### Métadonnées de performance (SplayNode)
- [x] **access_count** - Compteur d'accès au nœud
- [x] **splay_count** - Compteur de splay du nœud
- [x] **last_accessed** - Timestamp du dernier accès
- [x] **Méthodes de gestion** - increment_access, increment_splay, reset_metrics
- [x] **Méthodes de diagnostic** - get_metrics, get_rotation_type, get_splay_path

### Fonctionnalités avancées (SplayNode)
- [x] **Détection de cas de rotation** - is_zig_case, is_zig_zig_case, is_zig_zag_case
- [x] **Analyse de structure** - get_splay_depth, get_splay_path
- [x] **Représentation** - to_string, __str__, __repr__