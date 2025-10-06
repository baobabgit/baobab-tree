# Spécification détaillée - Treap

## Vue d'ensemble
Le Treap (Tree + Heap) est une structure de données hybride qui combine les propriétés d'un arbre binaire de recherche (BST) et d'un tas (heap). Chaque nœud a une clé (pour BST) et une priorité (pour heap).

## Objectifs
- Implémenter un BST avec propriétés de heap
- Maintenir l'équilibrage probabiliste
- Fournir des opérations de base efficaces
- Optimiser les performances moyennes

## Structure de données

### Treap
```cpp
template<typename T>
class Treap {
private:
    TreapNode<T>* root;
    size_t size;
    std::mt19937 rng;
    
public:
    // Constructeurs
    Treap();
    Treap(int seed);
    ~Treap();
    
    // Opérations de base
    bool insert(const T& value);
    bool insert(const T& value, int priority);
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
    void merge(Treap<T>& other);
    Treap<T> split(const T& value);
    
    // Opérations de debug
    void print() const;
    bool isValid() const;
    int getHeight() const;
    double getAverageHeight() const;
    
    // Opérations de priorité
    void updatePriority(const T& value, int newPriority);
    int getPriority(const T& value) const;
    std::vector<std::pair<T, int>> getPriorities() const;
};
```

## Algorithmes principaux

### 1. Insertion avec priorité
```cpp
bool insert(const T& value, int priority = -1) {
    if (priority == -1) {
        priority = rng();
    }
    
    if (!root) {
        root = new TreapNode<T>(value, priority);
        size = 1;
        return true;
    }
    
    // Recherche de la position d'insertion
    TreapNode<T>* current = root;
    TreapNode<T>* parent = nullptr;
    
    while (current) {
        if (current->data == value) {
            return false; // Élément déjà présent
        }
        
        parent = current;
        if (value < current->data) {
            current = current->left;
        } else {
            current = current->right;
        }
    }
    
    // Création du nouveau nœud
    TreapNode<T>* newNode = new TreapNode<T>(value, priority);
    newNode->parent = parent;
    
    if (value < parent->data) {
        parent->left = newNode;
    } else {
        parent->right = newNode;
    }
    
    // Restauration de la propriété heap
    heapifyUp(newNode);
    size++;
    return true;
}
```

### 2. Suppression
```cpp
bool remove(const T& value) {
    TreapNode<T>* node = findNode(value);
    if (!node) return false;
    
    // Suppression en faisant descendre le nœud vers une feuille
    while (node->left || node->right) {
        if (!node->left) {
            rotateLeft(node);
        } else if (!node->right) {
            rotateRight(node);
        } else if (node->left->priority > node->right->priority) {
            rotateRight(node);
        } else {
            rotateLeft(node);
        }
    }
    
    // Suppression du nœud feuille
    if (node->parent) {
        if (node->parent->left == node) {
            node->parent->left = nullptr;
        } else {
            node->parent->right = nullptr;
        }
    } else {
        root = nullptr;
    }
    
    delete node;
    size--;
    return true;
}
```

### 3. Restauration de la propriété heap
```cpp
void heapifyUp(TreapNode<T>* node) {
    while (node->parent && node->priority > node->parent->priority) {
        if (node == node->parent->left) {
            rotateRight(node->parent);
        } else {
            rotateLeft(node->parent);
        }
    }
}

void heapifyDown(TreapNode<T>* node) {
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

## Propriétés

### 1. Propriété BST
- Clé gauche < clé nœud < clé droite
- Parcours en ordre donne les clés triées
- Recherche efficace en O(log n) en moyenne

### 2. Propriété Heap
- Priorité parent ≥ priorité enfants
- Racine a la priorité maximale
- Équilibrage probabiliste

### 3. Équilibrage
- Probabiliste basé sur les priorités
- Hauteur moyenne O(log n)
- Pas d'équilibrage explicite

## Opérations spécialisées

### 1. Fusion de Treaps
```cpp
void merge(Treap<T>& other) {
    if (!other.root) return;
    
    // Trouver le maximum dans this
    TreapNode<T>* maxThis = root;
    while (maxThis && maxThis->right) {
        maxThis = maxThis->right;
    }
    
    if (maxThis) {
        // Splay du maximum vers la racine
        splay(maxThis);
        // Fusionner
        root->right = other.root;
        if (other.root) {
            other.root->parent = root;
        }
    } else {
        root = other.root;
    }
    
    size += other.size;
    other.root = nullptr;
    other.size = 0;
}
```

### 2. Division de Treap
```cpp
Treap<T> split(const T& value) {
    Treap<T> rightTreap;
    
    if (!root) return rightTreap;
    
    // Recherche et splay de la valeur
    TreapNode<T>* node = findNode(value);
    if (node) {
        splay(node);
        
        if (node->right) {
            rightTreap.root = node->right;
            rightTreap.root->parent = nullptr;
            node->right = nullptr;
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
            splay(current);
            if (current->right) {
                rightTreap.root = current->right;
                rightTreap.root->parent = nullptr;
                current->right = nullptr;
            }
        }
    }
    
    return rightTreap;
}
```

## Complexités

| Opération | Complexité | Notes |
|-----------|------------|-------|
| Insertion | O(log n) en moyenne | O(n) dans le pire cas |
| Suppression | O(log n) en moyenne | O(n) dans le pire cas |
| Recherche | O(log n) en moyenne | O(n) dans le pire cas |
| Fusion | O(log n) en moyenne | O(n) dans le pire cas |
| Division | O(log n) en moyenne | O(n) dans le pire cas |
| Parcours | O(n) | Visite de tous les nœuds |

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
- Insertion, suppression, recherche
- Opérations de parcours
- Fusion et division
- Gestion des priorités

### 2. Tests de performance
- Temps d'accès pour différents patterns
- Comparaison avec BST standard
- Analyse de la hauteur moyenne

### 3. Tests de robustesse
- Gestion des doublons
- Opérations sur arbre vide
- Gestion mémoire

## Optimisations

### 1. Optimisations de rotation
- Rotation optimisée
- Réduction des comparaisons
- Cache des pointeurs fréquents

### 2. Gestion mémoire
- Pool d'allocateurs
- Réutilisation des nœuds
- Gestion des fuites mémoire

### 3. Optimisations de priorité
- Génération de priorités optimisée
- Cache des priorités fréquentes
- Réduction des comparaisons

## Exemples d'utilisation

```cpp
// Création et utilisation basique
Treap<int> treap;
treap.insert(5, 10);
treap.insert(3, 5);
treap.insert(7, 15);

// Recherche
bool found = treap.search(3);

// Suppression
treap.remove(5);

// Parcours
std::vector<int> elements = treap.inorder();

// Fusion
Treap<int> other;
other.insert(9, 20);
treap.merge(other);
```

## Notes d'implémentation

### 1. Gestion des priorités
- Génération aléatoire des priorités
- Gestion des priorités personnalisées
- Maintien de la propriété heap

### 2. Gestion des pointeurs
- Mise à jour correcte des pointeurs parent
- Gestion des cas de racine
- Éviter les cycles

### 3. Compatibilité
- Support des types génériques
- Comparateurs personnalisés
- Itérateurs STL

## Dépendances
- TreapNode (nœud spécialisé)
- TreapOperations (opérations spécialisées)
- Structures de base de la Phase 1

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