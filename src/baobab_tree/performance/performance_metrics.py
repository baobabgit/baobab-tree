"""
Métriques de performance pour le profiling des arbres.

Ce module définit les métriques de base utilisées pour mesurer
les performances des opérations sur les arbres.
"""

import time
import psutil
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class MetricType(Enum):
    """Types de métriques disponibles."""

    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    OPERATIONAL = "operational"


@dataclass
class TemporalMetrics:
    """Métriques temporelles."""

    operation_time: float = 0.0
    total_time: float = 0.0
    average_time: float = 0.0
    min_time: float = float("inf")
    max_time: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class SpatialMetrics:
    """Métriques spatiales."""

    memory_usage: int = 0
    peak_memory: int = 0
    memory_growth: int = 0
    node_count: int = 0


@dataclass
class OperationalMetrics:
    """Métriques d'opérations."""

    insert_count: int = 0
    delete_count: int = 0
    search_count: int = 0
    rotation_count: int = 0
    rebalance_count: int = 0


class PerformanceMetrics:
    """
    Collecteur de métriques de performance.

    Cette classe collecte et calcule les métriques de performance
    pour les opérations sur les arbres.

    Examples:
        >>> metrics = PerformanceMetrics()
        >>> metrics.start_measurement()
        >>> # ... exécuter une opération ...
        >>> metrics.end_measurement()
        >>> temporal = metrics.get_temporal_metrics()
    """

    def __init__(self):
        """Initialise le collecteur de métriques."""
        self._temporal = TemporalMetrics()
        self._spatial = SpatialMetrics()
        self._operational = OperationalMetrics()
        self._measurements: List[Dict[str, Any]] = []
        self._start_time: Optional[float] = None
        self._start_memory: Optional[int] = None

    def start_measurement(self) -> None:
        """
        Démarre la mesure des métriques.

        Enregistre l'état initial pour le calcul des deltas.
        """
        self._start_time = time.perf_counter()
        self._start_memory = self._get_memory_usage()

    def end_measurement(self) -> Dict[str, Any]:
        """
        Termine la mesure et calcule les métriques.

        Returns:
            Dict contenant toutes les métriques calculées.
        """
        if self._start_time is None:
            raise ValueError("start_measurement() must be called first")

        end_time = time.perf_counter()
        end_memory = self._get_memory_usage()

        # Calculer les métriques temporelles
        execution_time = end_time - self._start_time
        self._temporal.operation_time = execution_time
        self._temporal.total_time += execution_time
        self._temporal.min_time = min(self._temporal.min_time, execution_time)
        self._temporal.max_time = max(self._temporal.max_time, execution_time)

        # Calculer les métriques spatiales
        memory_delta = end_memory - (self._start_memory or 0)
        self._spatial.memory_usage = end_memory
        self._spatial.memory_growth += memory_delta
        self._spatial.peak_memory = max(self._spatial.peak_memory, end_memory)

        # Créer la mesure
        measurement = {
            "execution_time": execution_time,
            "memory_delta": memory_delta,
            "memory_usage": end_memory,
            "timestamp": time.time(),
        }

        self._measurements.append(measurement)

        # Réinitialiser pour la prochaine mesure
        self._start_time = None
        self._start_memory = None

        return measurement

    def record_operation(self, operation_type: str) -> None:
        """
        Enregistre une opération spécifique.

        Args:
            operation_type: Type d'opération ('insert', 'delete', 'search', etc.)
        """
        if operation_type == "insert":
            self._operational.insert_count += 1
        elif operation_type == "delete":
            self._operational.delete_count += 1
        elif operation_type == "search":
            self._operational.search_count += 1
        elif operation_type == "rotation":
            self._operational.rotation_count += 1
        elif operation_type == "rebalance":
            self._operational.rebalance_count += 1

    def get_temporal_metrics(self) -> TemporalMetrics:
        """
        Retourne les métriques temporelles.

        Returns:
            Objet TemporalMetrics contenant les métriques temporelles.
        """
        # Calculer la moyenne
        if self._measurements:
            total_time = sum(m["execution_time"] for m in self._measurements)
            self._temporal.average_time = total_time / len(self._measurements)

        return self._temporal

    def get_spatial_metrics(self) -> SpatialMetrics:
        """
        Retourne les métriques spatiales.

        Returns:
            Objet SpatialMetrics contenant les métriques spatiales.
        """
        return self._spatial

    def get_operational_metrics(self) -> OperationalMetrics:
        """
        Retourne les métriques d'opérations.

        Returns:
            Objet OperationalMetrics contenant les métriques d'opérations.
        """
        return self._operational

    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Retourne toutes les métriques.

        Returns:
            Dict contenant toutes les métriques organisées par type.
        """
        return {
            "temporal": self.get_temporal_metrics(),
            "spatial": self.get_spatial_metrics(),
            "operational": self.get_operational_metrics(),
            "measurements": self._measurements.copy(),
        }

    def reset(self) -> None:
        """Remet à zéro toutes les métriques."""
        self._temporal = TemporalMetrics()
        self._spatial = SpatialMetrics()
        self._operational = OperationalMetrics()
        self._measurements.clear()
        self._start_time = None
        self._start_memory = None

    def _get_memory_usage(self) -> int:
        """
        Obtient l'utilisation mémoire actuelle.

        Returns:
            Utilisation mémoire en octets.
        """
        try:
            process = psutil.Process()
            return process.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """
        Calcule les statistiques des métriques.

        Returns:
            Dict contenant les statistiques calculées.
        """
        if not self._measurements:
            return {}

        execution_times = [m["execution_time"] for m in self._measurements]
        memory_deltas = [m["memory_delta"] for m in self._measurements]

        return {
            "execution_time": {
                "mean": sum(execution_times) / len(execution_times),
                "median": sorted(execution_times)[len(execution_times) // 2],
                "std": self._calculate_std(execution_times),
                "min": min(execution_times),
                "max": max(execution_times),
            },
            "memory_delta": {
                "mean": sum(memory_deltas) / len(memory_deltas),
                "median": sorted(memory_deltas)[len(memory_deltas) // 2],
                "std": self._calculate_std(memory_deltas),
                "min": min(memory_deltas),
                "max": max(memory_deltas),
            },
            "total_operations": len(self._measurements),
            "total_time": sum(execution_times),
        }

    def _calculate_std(self, values: List[float]) -> float:
        """
        Calcule l'écart-type d'une liste de valeurs.

        Args:
            values: Liste de valeurs numériques.

        Returns:
            Écart-type calculé.
        """
        if len(values) < 2:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance**0.5
