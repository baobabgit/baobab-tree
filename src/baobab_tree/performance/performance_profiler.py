"""
Profiler de performance pour les arbres et leurs opérations.

Ce module implémente la classe principale PerformanceProfiler qui permet
de profiler les performances des opérations sur les différents types d'arbres.
"""

import time
import threading
from typing import Any, Callable, Dict, List, Optional, Generic, TypeVar
from contextlib import contextmanager

from .performance_metrics import PerformanceMetrics
from .performance_analyzer import PerformanceAnalyzer
from .performance_reporter import PerformanceReporter
from .performance_monitor import PerformanceMonitor
from .performance_visualizer import PerformanceVisualizer

T = TypeVar("T")


class PerformanceProfilerError(Exception):
    """Exception de base pour le profiler de performance."""

    pass


class ProfilingError(PerformanceProfilerError):
    """Erreur lors du profiling d'une opération."""

    pass


class AnalysisError(PerformanceProfilerError):
    """Erreur lors de l'analyse des performances."""

    pass


class ReportingError(PerformanceProfilerError):
    """Erreur lors de la génération de rapports."""

    pass


class PerformanceProfiler(Generic[T]):
    """
    Profiler de performance pour les arbres et leurs opérations.

    Cette classe fournit des outils complets pour analyser et mesurer
    les performances des différentes structures d'arbres.

    Examples:
        >>> profiler = PerformanceProfiler[int]()
        >>> profiler.configure_profiling({'memory_tracking': True})
        >>> profile = profiler.profile_operation(tree.insert, 42)
        >>> comparison = profiler.compare_performance([avl_tree, rb_tree], ['insert'])
    """

    def __init__(self):
        """Initialise le profiler de performance."""
        self._metrics = PerformanceMetrics()
        self._analyzer = PerformanceAnalyzer()
        self._reporter = PerformanceReporter()
        self._monitor = PerformanceMonitor()
        self._visualizer = PerformanceVisualizer()

        self._config: Dict[str, Any] = {
            "memory_tracking": True,
            "time_tracking": True,
            "operation_tracking": True,
            "continuous_profiling": False,
            "real_time_monitoring": False,
        }

        self._profiles: List[Dict[str, Any]] = []
        self._continuous_profiling = False
        self._profiling_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def configure_profiling(self, config: Dict[str, Any]) -> None:
        """
        Configure les paramètres de profiling.

        Args:
            config: Configuration du profiling.

        Raises:
            ValueError: Si la configuration est invalide.
        """
        # Valider la configuration
        valid_keys = {
            "memory_tracking",
            "time_tracking",
            "operation_tracking",
            "continuous_profiling",
            "real_time_monitoring",
            "sampling_rate",
            "thresholds",
            "filters",
        }

        for key in config:
            if key not in valid_keys:
                raise ValueError(f"Configuration key '{key}' is not valid")

        # Appliquer la configuration
        self._config.update(config)

        # Initialiser les métriques
        self._metrics.reset()

        # Configurer le monitoring
        if self._config.get("real_time_monitoring", False):
            self._monitor.configure(config)

    def profile_operation(self, operation: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile une opération spécifique.

        Args:
            operation: Fonction à profiler.
            *args: Arguments positionnels pour l'opération.
            **kwargs: Arguments nommés pour l'opération.

        Returns:
            Dict contenant le profil de l'opération.

        Raises:
            ProfilingError: Si le profiling échoue.
        """
        try:
            # Enregistrer l'état initial
            initial_memory = (
                self._get_memory_usage() if self._config["memory_tracking"] else 0
            )
            initial_time = time.perf_counter() if self._config["time_tracking"] else 0

            # Exécuter l'opération
            try:
                result = operation(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)

            # Enregistrer l'état final
            final_time = time.perf_counter() if self._config["time_tracking"] else 0
            final_memory = (
                self._get_memory_usage() if self._config["memory_tracking"] else 0
            )

            # Calculer les métriques
            execution_time = (
                final_time - initial_time if self._config["time_tracking"] else 0
            )
            memory_delta = (
                final_memory - initial_memory if self._config["memory_tracking"] else 0
            )

            # Créer le profil
            profile = {
                "operation": operation.__name__,
                "execution_time": execution_time,
                "memory_delta": memory_delta,
                "memory_usage": final_memory,
                "success": success,
                "result": result,
                "timestamp": time.time(),
                "args": args,
                "kwargs": kwargs,
            }

            if not success:
                profile["error"] = error

            # Enregistrer le profil
            self._record_profile(profile)

            return profile

        except Exception as e:
            raise ProfilingError(f"Failed to profile operation: {e}") from e

    def profile_sequence(
        self, operations: List[Callable], *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Profile une séquence d'opérations.

        Args:
            operations: Liste des opérations à profiler.
            *args: Arguments positionnels pour les opérations.
            **kwargs: Arguments nommés pour les opérations.

        Returns:
            Dict contenant le profil de la séquence.

        Raises:
            ProfilingError: Si le profiling échoue.
        """
        try:
            sequence_profile = {
                "sequence_start": time.time(),
                "operations": [],
                "total_execution_time": 0,
                "total_memory_delta": 0,
                "success_count": 0,
                "error_count": 0,
            }

            for operation in operations:
                # Profiler chaque opération
                operation_profile = self.profile_operation(operation, *args, **kwargs)
                sequence_profile["operations"].append(operation_profile)

                # Accumuler les métriques
                sequence_profile["total_execution_time"] += operation_profile[
                    "execution_time"
                ]
                sequence_profile["total_memory_delta"] += operation_profile[
                    "memory_delta"
                ]

                if operation_profile["success"]:
                    sequence_profile["success_count"] += 1
                else:
                    sequence_profile["error_count"] += 1

            sequence_profile["sequence_end"] = time.time()
            sequence_profile["sequence_duration"] = (
                sequence_profile["sequence_end"] - sequence_profile["sequence_start"]
            )

            # Analyser les tendances
            sequence_profile["trends"] = self._analyzer.analyze_trends(
                sequence_profile["operations"]
            )

            return sequence_profile

        except Exception as e:
            raise ProfilingError(f"Failed to profile sequence: {e}") from e

    def start_continuous_profiling(self) -> None:
        """
        Démarre le profiling continu.

        Raises:
            ProfilingError: Si le profiling continu ne peut pas démarrer.
        """
        if self._continuous_profiling:
            raise ProfilingError("Continuous profiling is already running")

        try:
            self._continuous_profiling = True
            self._stop_event.clear()

            # Démarrer le thread de profiling
            self._profiling_thread = threading.Thread(
                target=self._continuous_profiling_loop, daemon=True
            )
            self._profiling_thread.start()

        except Exception as e:
            self._continuous_profiling = False
            raise ProfilingError(f"Failed to start continuous profiling: {e}") from e

    def stop_continuous_profiling(self) -> Dict[str, Any]:
        """
        Arrête le profiling continu et retourne les résultats.

        Returns:
            Dict contenant les résultats du profiling continu.

        Raises:
            ProfilingError: Si le profiling continu n'est pas en cours.
        """
        if not self._continuous_profiling:
            raise ProfilingError("Continuous profiling is not running")

        try:
            # Arrêter le profiling
            self._continuous_profiling = False
            self._stop_event.set()

            # Attendre que le thread se termine
            if self._profiling_thread and self._profiling_thread.is_alive():
                self._profiling_thread.join(timeout=5.0)

            # Collecter les métriques finales
            final_metrics = self._metrics.get_all_metrics()

            # Analyser les données
            analysis = self._analyzer.analyze_continuous_data(self._profiles)

            # Créer le rapport
            report = {
                "profiling_duration": (
                    time.time() - self._profiles[0]["timestamp"]
                    if self._profiles
                    else 0
                ),
                "total_profiles": len(self._profiles),
                "metrics": final_metrics,
                "analysis": analysis,
                "summary": self._generate_summary(analysis),
            }

            return report

        except Exception as e:
            raise ProfilingError(f"Failed to stop continuous profiling: {e}") from e

    def compare_performance(
        self, trees: List[Any], operations: List[str]
    ) -> Dict[str, Any]:
        """
        Compare les performances de différents arbres.

        Args:
            trees: Liste des arbres à comparer.
            operations: Liste des opérations à tester.

        Returns:
            Dict contenant la comparaison des performances.

        Raises:
            AnalysisError: Si l'analyse comparative échoue.
        """
        try:
            results = {}

            for tree in trees:
                tree_name = tree.__class__.__name__
                results[tree_name] = {}

                for operation in operations:
                    if hasattr(tree, operation):
                        # Profiler l'opération sur cet arbre
                        profile = self.profile_operation(
                            getattr(tree, operation), self._get_test_data(operation)
                        )
                        results[tree_name][operation] = profile
                    else:
                        results[tree_name][operation] = {
                            "error": f"Operation '{operation}' not found",
                            "success": False,
                        }

            # Analyser les comparaisons
            comparison = self._analyzer.compare_results(results)

            return {
                "results": results,
                "comparison": comparison,
                "summary": self._generate_comparison_summary(comparison),
            }

        except Exception as e:
            raise AnalysisError(f"Failed to compare performance: {e}") from e

    def analyze_complexity(
        self, tree: Any, operation: str, sizes: List[int]
    ) -> Dict[str, Any]:
        """
        Analyse la complexité d'une opération selon la taille.

        Args:
            tree: Arbre à analyser.
            operation: Opération à analyser.
            sizes: Liste des tailles à tester.

        Returns:
            Dict contenant l'analyse de complexité.

        Raises:
            AnalysisError: Si l'analyse de complexité échoue.
        """
        try:
            complexity_data = {}

            for size in sizes:
                # Préparer les données de test
                test_data = self._generate_test_data(size)

                # Profiler l'opération avec cette taille
                profiles = []
                for data_point in test_data:
                    profile = self.profile_operation(
                        getattr(tree, operation), data_point
                    )
                    profiles.append(profile)

                # Calculer les statistiques pour cette taille
                execution_times = [
                    p["execution_time"] for p in profiles if p["success"]
                ]
                complexity_data[size] = {
                    "size": size,
                    "profiles": profiles,
                    "avg_execution_time": (
                        sum(execution_times) / len(execution_times)
                        if execution_times
                        else 0
                    ),
                    "min_execution_time": (
                        min(execution_times) if execution_times else 0
                    ),
                    "max_execution_time": (
                        max(execution_times) if execution_times else 0
                    ),
                    "success_rate": (
                        len(execution_times) / len(profiles) if profiles else 0
                    ),
                }

            # Analyser la complexité
            complexity_analysis = self._analyzer.analyze_complexity_trends(
                complexity_data
            )

            return {
                "complexity_data": complexity_data,
                "analysis": complexity_analysis,
                "summary": self._generate_complexity_summary(complexity_analysis),
            }

        except Exception as e:
            raise AnalysisError(f"Failed to analyze complexity: {e}") from e

    def identify_bottlenecks(self, tree: Any) -> List[Dict[str, Any]]:
        """
        Identifie les goulots d'étranglement de performance.

        Args:
            tree: Arbre à analyser.

        Returns:
            Liste des goulots d'étranglement identifiés.

        Raises:
            AnalysisError: Si l'identification des goulots échoue.
        """
        try:
            # Profiler toutes les opérations disponibles
            operations = ["insert", "delete", "search", "find_min", "find_max"]
            available_operations = [op for op in operations if hasattr(tree, op)]

            bottlenecks = []

            for operation in available_operations:
                # Profiler l'opération plusieurs fois
                profiles = []
                for _ in range(10):  # 10 exécutions pour avoir des statistiques
                    profile = self.profile_operation(
                        getattr(tree, operation), self._get_test_data(operation)
                    )
                    profiles.append(profile)

                # Analyser les performances
                execution_times = [
                    p["execution_time"] for p in profiles if p["success"]
                ]
                if execution_times:
                    avg_time = sum(execution_times) / len(execution_times)
                    max_time = max(execution_times)

                    # Identifier les goulots d'étranglement
                    if avg_time > 0.1:  # Seuil arbitraire de 100ms
                        bottlenecks.append(
                            {
                                "operation": operation,
                                "avg_execution_time": avg_time,
                                "max_execution_time": max_time,
                                "severity": "high" if avg_time > 1.0 else "medium",
                                "profiles": profiles,
                            }
                        )

            return bottlenecks

        except Exception as e:
            raise AnalysisError(f"Failed to identify bottlenecks: {e}") from e

    def generate_report(self, format_type: str = "text") -> str:
        """
        Génère un rapport de performance.

        Args:
            format_type: Format du rapport ('text', 'json', 'html').

        Returns:
            Rapport de performance formaté.

        Raises:
            ReportingError: Si la génération du rapport échoue.
        """
        try:
            return self._reporter.generate_report(
                self._profiles, self._metrics.get_all_metrics(), format_type
            )
        except Exception as e:
            raise ReportingError(f"Failed to generate report: {e}") from e

    def export_data(self, format_type: str = "json") -> str:
        """
        Exporte les données de performance.

        Args:
            format_type: Format d'export ('json', 'csv', 'xml').

        Returns:
            Données exportées.

        Raises:
            ReportingError: Si l'export échoue.
        """
        try:
            return self._reporter.export_data(
                self._profiles, self._metrics.get_all_metrics(), format_type
            )
        except Exception as e:
            raise ReportingError(f"Failed to export data: {e}") from e

    def create_visualization(self, metric: str, output_file: str) -> None:
        """
        Crée une visualisation des métriques.

        Args:
            metric: Métrique à visualiser.
            output_file: Fichier de sortie pour la visualisation.

        Raises:
            ReportingError: Si la création de visualisation échoue.
        """
        try:
            self._visualizer.create_visualization(self._profiles, metric, output_file)
        except Exception as e:
            raise ReportingError(f"Failed to create visualization: {e}") from e

    def set_metric_filters(self, filters: List[str]) -> None:
        """
        Définit les filtres pour les métriques.

        Args:
            filters: Liste des filtres à appliquer.
        """
        self._config["filters"] = filters

    def set_performance_thresholds(self, thresholds: Dict[str, float]) -> None:
        """
        Définit les seuils de performance.

        Args:
            thresholds: Dict des seuils de performance.
        """
        self._config["thresholds"] = thresholds

    def start_real_time_monitoring(self) -> None:
        """Démarre le monitoring en temps réel."""
        self._monitor.start_monitoring()

    def set_performance_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """
        Configure les alertes de performance.

        Args:
            alerts: Liste des alertes à configurer.
        """
        self._monitor.set_alerts(alerts)

    def enable_adaptive_monitoring(self) -> None:
        """Active le monitoring adaptatif."""
        self._monitor.enable_adaptive_monitoring()

    def _record_profile(self, profile: Dict[str, Any]) -> None:
        """
        Enregistre un profil dans la liste des profils.

        Args:
            profile: Profil à enregistrer.
        """
        self._profiles.append(profile)

        # Appliquer les filtres si configurés
        if "filters" in self._config:
            # Logique de filtrage à implémenter
            pass

    def _continuous_profiling_loop(self) -> None:
        """Boucle de profiling continu."""
        while not self._stop_event.is_set():
            # Collecter les métriques système
            system_metrics = self._get_system_metrics()

            # Enregistrer les métriques
            profile = {
                "timestamp": time.time(),
                "system_metrics": system_metrics,
                "type": "system_monitoring",
            }
            self._record_profile(profile)

            # Attendre avant la prochaine collecte
            self._stop_event.wait(timeout=1.0)  # Collecte toutes les secondes

    def _get_memory_usage(self) -> int:
        """
        Obtient l'utilisation mémoire actuelle.

        Returns:
            Utilisation mémoire en octets.
        """
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss
        except (ImportError, psutil.NoSuchProcess, psutil.AccessDenied):
            return 0

    def _get_system_metrics(self) -> Dict[str, Any]:
        """
        Obtient les métriques système.

        Returns:
            Dict contenant les métriques système.
        """
        try:
            import psutil

            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage("/").percent,
            }
        except ImportError:
            return {}

    def _get_test_data(self, operation: str) -> Any:
        """
        Génère des données de test pour une opération.

        Args:
            operation: Nom de l'opération.

        Returns:
            Données de test appropriées.
        """
        # Générer des données de test basiques
        if operation in ["insert", "search", "delete"]:
            return 42  # Valeur de test simple
        elif operation in ["find_min", "find_max"]:
            return None  # Pas d'arguments nécessaires
        else:
            return None

    def _generate_test_data(self, size: int) -> List[Any]:
        """
        Génère des données de test pour une taille donnée.

        Args:
            size: Taille des données à générer.

        Returns:
            Liste des données de test.
        """
        import random

        return [random.randint(1, 1000) for _ in range(size)]

    def _generate_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un résumé de l'analyse.

        Args:
            analysis: Analyse à résumer.

        Returns:
            Résumé de l'analyse.
        """
        # Filtrer les profils qui ont des temps d'exécution
        operation_profiles = [p for p in self._profiles if "execution_time" in p]

        return {
            "total_operations": len(operation_profiles),
            "success_rate": (
                len([p for p in operation_profiles if p.get("success", False)])
                / len(operation_profiles)
                if operation_profiles
                else 0
            ),
            "avg_execution_time": (
                sum(p["execution_time"] for p in operation_profiles)
                / len(operation_profiles)
                if operation_profiles
                else 0
            ),
            "analysis_summary": analysis.get("summary", {}),
        }

    def _generate_comparison_summary(
        self, comparison: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Génère un résumé de la comparaison.

        Args:
            comparison: Comparaison à résumer.

        Returns:
            Résumé de la comparaison.
        """
        return {
            "best_performer": comparison.get("best_performer", "unknown"),
            "worst_performer": comparison.get("worst_performer", "unknown"),
            "performance_difference": comparison.get("performance_difference", 0),
            "recommendations": comparison.get("recommendations", []),
        }

    def _generate_complexity_summary(
        self, complexity_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Génère un résumé de l'analyse de complexité.

        Args:
            complexity_analysis: Analyse de complexité à résumer.

        Returns:
            Résumé de l'analyse de complexité.
        """
        return {
            "complexity_class": complexity_analysis.get("complexity_class", "unknown"),
            "scalability": complexity_analysis.get("scalability", "unknown"),
            "recommendations": complexity_analysis.get("recommendations", []),
        }
