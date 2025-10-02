"""
Module contenant la factory pour créer des instances de stratégies d'équilibrage.

Ce module implémente la classe BalancingStrategyFactory qui permet de créer
des instances de stratégies d'équilibrage selon le type spécifié.
"""

from __future__ import annotations

from typing import Dict, Type, TypeVar

from ..core.exceptions import InvalidStrategyError
from .avl_balancing_strategy import AVLBalancingStrategy
from .balancing_strategy import BalancingStrategy
from .red_black_balancing_strategy import RedBlackBalancingStrategy
from .splay_balancing_strategy import SplayBalancingStrategy
from .treap_balancing_strategy import TreapBalancingStrategy

T = TypeVar('T')


class BalancingStrategyFactory:
    """
    Factory pour créer des instances de stratégies d'équilibrage.
    
    Cette classe fournit des méthodes statiques pour créer des instances
    de stratégies d'équilibrage selon le type spécifié, avec validation
    des types et gestion des erreurs.
    
    Attributes:
        _strategy_registry (Dict[str, Type[BalancingStrategy]]): Registre des stratégies disponibles
    """
    
    _strategy_registry: Dict[str, Type[BalancingStrategy]] = {
        'avl': AVLBalancingStrategy,
        'red_black': RedBlackBalancingStrategy,
        'redblack': RedBlackBalancingStrategy,
        'rb': RedBlackBalancingStrategy,
        'splay': SplayBalancingStrategy,
        'treap': TreapBalancingStrategy
    }
    
    @staticmethod
    def create_strategy(strategy_type: str) -> BalancingStrategy[T]:
        """
        Crée une stratégie selon le type spécifié.
        
        Cette méthode valide le type de stratégie, crée l'instance appropriée
        et retourne la stratégie configurée.
        
        Args:
            strategy_type: Le type de stratégie à créer
            
        Returns:
            Instance de la stratégie d'équilibrage créée
            
        Raises:
            InvalidStrategyError: Si le type de stratégie est invalide
            
        Examples:
            >>> avl_strategy = BalancingStrategyFactory.create_strategy("avl")
            >>> rb_strategy = BalancingStrategyFactory.create_strategy("red_black")
            >>> splay_strategy = BalancingStrategyFactory.create_strategy("splay")
        """
        # Normaliser le type de stratégie
        normalized_type = strategy_type.lower().strip()
        
        # Valider le type de stratégie
        if normalized_type not in BalancingStrategyFactory._strategy_registry:
            available_types = list(BalancingStrategyFactory._strategy_registry.keys())
            raise InvalidStrategyError(
                f"Type de stratégie invalide: {strategy_type}",
                strategy_type,
                f"Types disponibles: {available_types}"
            )
        
        # Créer l'instance de la stratégie
        strategy_class = BalancingStrategyFactory._strategy_registry[normalized_type]
        
        try:
            strategy = strategy_class()
            return strategy
        except Exception as e:
            raise InvalidStrategyError(
                f"Impossible de créer la stratégie {strategy_type}: {str(e)}",
                strategy_type,
                f"Erreur lors de l'instanciation: {str(e)}"
            )
    
    @staticmethod
    def get_available_strategies() -> list[str]:
        """
        Retourne la liste des stratégies disponibles.
        
        Returns:
            Liste des types de stratégies disponibles
            
        Examples:
            >>> strategies = BalancingStrategyFactory.get_available_strategies()
            >>> print(strategies)
            ['avl', 'red_black', 'redblack', 'rb', 'splay', 'treap']
        """
        return list(BalancingStrategyFactory._strategy_registry.keys())
    
    @staticmethod
    def is_strategy_available(strategy_type: str) -> bool:
        """
        Vérifie si une stratégie est disponible.
        
        Args:
            strategy_type: Le type de stratégie à vérifier
            
        Returns:
            True si la stratégie est disponible, False sinon
            
        Examples:
            >>> is_available = BalancingStrategyFactory.is_strategy_available("avl")
            >>> print(is_available)
            True
        """
        normalized_type = strategy_type.lower().strip()
        return normalized_type in BalancingStrategyFactory._strategy_registry
    
    @staticmethod
    def register_strategy(strategy_type: str, strategy_class: Type[BalancingStrategy]) -> None:
        """
        Enregistre une nouvelle stratégie dans le registre.
        
        Cette méthode permet d'ajouter des stratégies personnalisées au registre
        de la factory.
        
        Args:
            strategy_type: Le type de stratégie à enregistrer
            strategy_class: La classe de stratégie à enregistrer
            
        Raises:
            InvalidStrategyError: Si la classe de stratégie est invalide
            
        Examples:
            >>> class CustomStrategy(BalancingStrategy):
            ...     pass
            >>> BalancingStrategyFactory.register_strategy("custom", CustomStrategy)
        """
        # Valider la classe de stratégie
        if not issubclass(strategy_class, BalancingStrategy):
            raise InvalidStrategyError(
                f"Classe de stratégie invalide: {strategy_class.__name__}",
                strategy_type,
                "La classe doit hériter de BalancingStrategy"
            )
        
        # Enregistrer la stratégie
        normalized_type = strategy_type.lower().strip()
        BalancingStrategyFactory._strategy_registry[normalized_type] = strategy_class
    
    @staticmethod
    def unregister_strategy(strategy_type: str) -> None:
        """
        Désenregistre une stratégie du registre.
        
        Args:
            strategy_type: Le type de stratégie à désenregistrer
            
        Raises:
            InvalidStrategyError: Si la stratégie n'est pas enregistrée
            
        Examples:
            >>> BalancingStrategyFactory.unregister_strategy("custom")
        """
        normalized_type = strategy_type.lower().strip()
        
        if normalized_type not in BalancingStrategyFactory._strategy_registry:
            raise InvalidStrategyError(
                f"Stratégie non enregistrée: {strategy_type}",
                strategy_type,
                "La stratégie n'est pas dans le registre"
            )
        
        del BalancingStrategyFactory._strategy_registry[normalized_type]
    
    @staticmethod
    def get_strategy_info(strategy_type: str) -> Dict[str, str]:
        """
        Retourne les informations sur une stratégie.
        
        Args:
            strategy_type: Le type de stratégie dont obtenir les informations
            
        Returns:
            Dictionnaire contenant les informations sur la stratégie
            
        Raises:
            InvalidStrategyError: Si le type de stratégie est invalide
            
        Examples:
            >>> info = BalancingStrategyFactory.get_strategy_info("avl")
            >>> print(info['description'])
            Stratégie d'équilibrage AVL basée sur les facteurs d'équilibre
        """
        # Créer une instance temporaire pour obtenir les informations
        strategy = BalancingStrategyFactory.create_strategy(strategy_type)
        
        return {
            'type': strategy_type,
            'class_name': strategy.__class__.__name__,
            'description': strategy.get_description(),
            'complexity': strategy.get_complexity()
        }
    
    @staticmethod
    def create_all_strategies() -> Dict[str, BalancingStrategy[T]]:
        """
        Crée toutes les stratégies disponibles.
        
        Returns:
            Dictionnaire contenant toutes les stratégies créées
            
        Examples:
            >>> all_strategies = BalancingStrategyFactory.create_all_strategies()
            >>> print(list(all_strategies.keys()))
            ['avl', 'red_black', 'redblack', 'rb', 'splay', 'treap']
        """
        strategies = {}
        
        for strategy_type in BalancingStrategyFactory._strategy_registry.keys():
            try:
                strategies[strategy_type] = BalancingStrategyFactory.create_strategy(strategy_type)
            except Exception:
                # Ignorer les stratégies qui ne peuvent pas être créées
                continue
        
        return strategies