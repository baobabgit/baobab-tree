"""
Analyseur de performance pour les données de profiling.

Ce module implémente la classe PerformanceAnalyzer qui analyse
les données collectées par le PerformanceProfiler.
"""

import statistics
from typing import Any, Dict, List, Optional
from collections import defaultdict


class PerformanceAnalyzer:
    """
    Analyseur de performance pour les données de profiling.

    Cette classe analyse les données collectées par le PerformanceProfiler
    et fournit des insights sur les performances.

    Examples:
        >>> analyzer = PerformanceAnalyzer()
        >>> trends = analyzer.analyze_trends(profiles)
        >>> comparison = analyzer.compare_results(results)
    """

    def __init__(self):
        """Initialise l'analyseur de performance."""
        self._analysis_cache: Dict[str, Any] = {}

    def analyze_trends(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyse les tendances dans une liste de profils.

        Args:
            profiles: Liste des profils à analyser.

        Returns:
            Dict contenant l'analyse des tendances.
        """
        if not profiles:
            return {}

        # Extraire les métriques temporelles
        execution_times = [
            p["execution_time"] for p in profiles if "execution_time" in p
        ]
        memory_deltas = [p["memory_delta"] for p in profiles if "memory_delta" in p]

        # Calculer les statistiques
        trends = {
            "execution_time": self._calculate_statistics(execution_times),
            "memory_delta": self._calculate_statistics(memory_deltas),
            "performance_trend": self._detect_performance_trend(execution_times),
            "memory_trend": self._detect_memory_trend(memory_deltas),
            "stability": self._calculate_stability(execution_times),
            "outliers": self._detect_outliers(execution_times),
        }

        return trends

    def compare_results(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare les résultats de différents arbres.

        Args:
            results: Dict des résultats par arbre.

        Returns:
            Dict contenant la comparaison.
        """
        comparison = {
            "tree_rankings": {},
            "operation_rankings": {},
            "best_performer": None,
            "worst_performer": None,
            "performance_difference": 0,
            "recommendations": [],
        }

        # Analyser chaque arbre
        tree_stats = {}
        for tree_name, operations in results.items():
            tree_stats[tree_name] = self._analyze_tree_performance(operations)

        # Classer les arbres
        tree_rankings = sorted(
            tree_stats.items(), key=lambda x: x[1]["avg_execution_time"]
        )

        comparison["tree_rankings"] = {
            tree: rank + 1 for rank, (tree, _) in enumerate(tree_rankings)
        }

        if tree_rankings:
            comparison["best_performer"] = tree_rankings[0][0]
            comparison["worst_performer"] = tree_rankings[-1][0]
            comparison["performance_difference"] = (
                tree_rankings[-1][1]["avg_execution_time"]
                - tree_rankings[0][1]["avg_execution_time"]
            )

        # Analyser les opérations
        operation_stats = defaultdict(list)
        for tree_name, operations in results.items():
            for operation_name, profile in operations.items():
                if isinstance(profile, dict) and "execution_time" in profile:
                    operation_stats[operation_name].append(
                        {"tree": tree_name, "execution_time": profile["execution_time"]}
                    )

        # Classer les opérations
        for operation_name, stats in operation_stats.items():
            sorted_stats = sorted(stats, key=lambda x: x["execution_time"])
            comparison["operation_rankings"][operation_name] = [
                stat["tree"] for stat in sorted_stats
            ]

        # Générer des recommandations
        comparison["recommendations"] = self._generate_recommendations(tree_stats)

        return comparison

    def analyze_complexity_trends(
        self, complexity_data: Dict[int, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyse les tendances de complexité.

        Args:
            complexity_data: Données de complexité par taille.

        Returns:
            Dict contenant l'analyse de complexité.
        """
        if not complexity_data:
            return {}

        # Extraire les données
        sizes = sorted(complexity_data.keys())
        avg_times = [complexity_data[size]["avg_execution_time"] for size in sizes]

        # Analyser la croissance
        complexity_analysis = {
            "sizes": sizes,
            "avg_execution_times": avg_times,
            "growth_rate": self._calculate_growth_rate(sizes, avg_times),
            "complexity_class": self._determine_complexity_class(sizes, avg_times),
            "scalability": self._assess_scalability(sizes, avg_times),
            "recommendations": [],
        }

        # Générer des recommandations
        complexity_analysis["recommendations"] = (
            self._generate_complexity_recommendations(complexity_analysis)
        )

        return complexity_analysis

    def analyze_continuous_data(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyse les données de profiling continu.

        Args:
            profiles: Liste des profils de profiling continu.

        Returns:
            Dict contenant l'analyse des données continues.
        """
        if not profiles:
            return {}

        # Séparer les profils par type
        operation_profiles = [
            p for p in profiles if p.get("type") != "system_monitoring"
        ]
        system_profiles = [p for p in profiles if p.get("type") == "system_monitoring"]

        analysis = {
            "operation_analysis": self._analyze_operation_patterns(operation_profiles),
            "system_analysis": self._analyze_system_patterns(system_profiles),
            "correlation_analysis": self._analyze_correlations(
                operation_profiles, system_profiles
            ),
            "summary": {},
        }

        # Générer un résumé
        analysis["summary"] = self._generate_continuous_summary(analysis)

        return analysis

    def _calculate_statistics(self, values: List[float]) -> Dict[str, float]:
        """
        Calcule les statistiques d'une liste de valeurs.

        Args:
            values: Liste de valeurs numériques.

        Returns:
            Dict contenant les statistiques.
        """
        if not values:
            return {}

        return {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "mode": statistics.mode(values) if len(set(values)) < len(values) else None,
            "std": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values),
            "count": len(values),
        }

    def _detect_performance_trend(self, execution_times: List[float]) -> str:
        """
        Détecte la tendance de performance.

        Args:
            execution_times: Liste des temps d'exécution.

        Returns:
            Description de la tendance.
        """
        if len(execution_times) < 2:
            return "insufficient_data"

        # Calculer la corrélation avec l'index
        n = len(execution_times)
        x = list(range(n))

        # Calculer la corrélation de Pearson simplifiée
        mean_x = sum(x) / n
        mean_y = sum(execution_times) / n

        numerator = sum(
            (x[i] - mean_x) * (execution_times[i] - mean_y) for i in range(n)
        )
        denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        denominator_y = sum((execution_times[i] - mean_y) ** 2 for i in range(n))

        if denominator_x == 0 or denominator_y == 0:
            return "stable"

        correlation = numerator / (denominator_x * denominator_y) ** 0.5

        if correlation > 0.3:
            return "degrading"
        elif correlation < -0.3:
            return "improving"
        else:
            return "stable"

    def _detect_memory_trend(self, memory_deltas: List[int]) -> str:
        """
        Détecte la tendance d'utilisation mémoire.

        Args:
            memory_deltas: Liste des deltas mémoire.

        Returns:
            Description de la tendance mémoire.
        """
        if not memory_deltas:
            return "no_data"

        positive_deltas = sum(1 for delta in memory_deltas if delta > 0)
        negative_deltas = sum(1 for delta in memory_deltas if delta < 0)

        if positive_deltas > negative_deltas * 2:
            return "increasing"
        elif negative_deltas > positive_deltas * 2:
            return "decreasing"
        else:
            return "stable"

    def _calculate_stability(self, execution_times: List[float]) -> float:
        """
        Calcule la stabilité des performances.

        Args:
            execution_times: Liste des temps d'exécution.

        Returns:
            Score de stabilité (0-1, 1 étant le plus stable).
        """
        if len(execution_times) < 2:
            return 1.0

        mean_time = statistics.mean(execution_times)
        if mean_time == 0:
            return 1.0

        cv = statistics.stdev(execution_times) / mean_time
        stability = max(0, 1 - cv)

        return stability

    def _detect_outliers(self, execution_times: List[float]) -> List[int]:
        """
        Détecte les valeurs aberrantes.

        Args:
            execution_times: Liste des temps d'exécution.

        Returns:
            Liste des indices des valeurs aberrantes.
        """
        if len(execution_times) < 3:
            return []

        mean_time = statistics.mean(execution_times)
        std_time = statistics.stdev(execution_times)

        outliers = []
        for i, time_val in enumerate(execution_times):
            if abs(time_val - mean_time) > 2 * std_time:
                outliers.append(i)

        return outliers

    def _analyze_tree_performance(self, operations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse les performances d'un arbre.

        Args:
            operations: Dict des opérations et leurs profils.

        Returns:
            Dict contenant l'analyse des performances de l'arbre.
        """
        execution_times = []
        success_count = 0
        total_count = 0

        for operation_name, profile in operations.items():
            if isinstance(profile, dict) and "execution_time" in profile:
                execution_times.append(profile["execution_time"])
                total_count += 1
                if profile.get("success", False):
                    success_count += 1

        return {
            "avg_execution_time": (
                statistics.mean(execution_times) if execution_times else 0
            ),
            "total_operations": total_count,
            "success_rate": success_count / total_count if total_count > 0 else 0,
            "operation_count": len(operations),
        }

    def _calculate_growth_rate(self, sizes: List[int], avg_times: List[float]) -> float:
        """
        Calcule le taux de croissance des performances.

        Args:
            sizes: Liste des tailles.
            avg_times: Liste des temps moyens.

        Returns:
            Taux de croissance.
        """
        if len(sizes) < 2:
            return 0.0

        # Calculer la régression linéaire simple
        n = len(sizes)
        sum_x = sum(sizes)
        sum_y = sum(avg_times)
        sum_xy = sum(sizes[i] * avg_times[i] for i in range(n))
        sum_x2 = sum(size**2 for size in sizes)

        denominator = n * sum_x2 - sum_x**2
        if denominator == 0:
            return 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope

    def _determine_complexity_class(
        self, sizes: List[int], avg_times: List[float]
    ) -> str:
        """
        Détermine la classe de complexité.

        Args:
            sizes: Liste des tailles.
            avg_times: Liste des temps moyens.

        Returns:
            Classe de complexité estimée.
        """
        if len(sizes) < 2:
            return "unknown"

        # Analyser la croissance
        growth_rate = self._calculate_growth_rate(sizes, avg_times)

        # Comparer avec les tailles pour estimer la complexité
        if growth_rate < 0.001:
            return "O(1)"
        elif growth_rate < 0.01:
            return "O(log n)"
        elif growth_rate < 0.1:
            return "O(n)"
        elif growth_rate < 1.0:
            return "O(n log n)"
        else:
            return "O(n²) or higher"

    def _assess_scalability(self, sizes: List[int], avg_times: List[float]) -> str:
        """
        Évalue la scalabilité.

        Args:
            sizes: Liste des tailles.
            avg_times: Liste des temps moyens.

        Returns:
            Évaluation de la scalabilité.
        """
        if len(sizes) < 2:
            return "unknown"

        # Calculer le ratio de croissance
        min_size = min(sizes)
        max_size = max(sizes)
        min_time = min(avg_times)
        max_time = max(avg_times)

        size_ratio = max_size / min_size
        time_ratio = max_time / min_time if min_time > 0 else float("inf")

        if time_ratio < size_ratio * 1.1:
            return "excellent"
        elif time_ratio < size_ratio * 2:
            return "good"
        elif time_ratio < size_ratio * 5:
            return "fair"
        else:
            return "poor"

    def _analyze_operation_patterns(
        self, profiles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyse les patterns d'opérations.

        Args:
            profiles: Liste des profils d'opérations.

        Returns:
            Dict contenant l'analyse des patterns.
        """
        if not profiles:
            return {}

        # Grouper par opération
        operation_groups = defaultdict(list)
        for profile in profiles:
            if "operation" in profile:
                operation_groups[profile["operation"]].append(profile)

        patterns = {}
        for operation, op_profiles in operation_groups.items():
            execution_times = [p["execution_time"] for p in op_profiles]
            patterns[operation] = {
                "count": len(op_profiles),
                "avg_time": statistics.mean(execution_times),
                "trend": self._detect_performance_trend(execution_times),
                "stability": self._calculate_stability(execution_times),
            }

        return patterns

    def _analyze_system_patterns(
        self, profiles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyse les patterns système.

        Args:
            profiles: Liste des profils système.

        Returns:
            Dict contenant l'analyse des patterns système.
        """
        if not profiles:
            return {}

        # Extraire les métriques système
        cpu_values = []
        memory_values = []

        for profile in profiles:
            if "system_metrics" in profile:
                metrics = profile["system_metrics"]
                if "cpu_percent" in metrics:
                    cpu_values.append(metrics["cpu_percent"])
                if "memory_percent" in metrics:
                    memory_values.append(metrics["memory_percent"])

        return {
            "cpu": self._calculate_statistics(cpu_values),
            "memory": self._calculate_statistics(memory_values),
            "system_load": (
                "high" if cpu_values and statistics.mean(cpu_values) > 80 else "normal"
            ),
        }

    def _analyze_correlations(
        self,
        operation_profiles: List[Dict[str, Any]],
        system_profiles: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyse les corrélations entre opérations et système.

        Args:
            operation_profiles: Profils d'opérations.
            system_profiles: Profils système.

        Returns:
            Dict contenant l'analyse des corrélations.
        """
        # Cette analyse nécessiterait une implémentation plus sophistiquée
        # pour corréler les timestamps et analyser les relations
        return {
            "correlation_analysis": "not_implemented",
            "note": "Correlation analysis requires more sophisticated timestamp matching",
        }

    def _generate_recommendations(
        self, tree_stats: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Génère des recommandations basées sur l'analyse.

        Args:
            tree_stats: Statistiques des arbres.

        Returns:
            Liste des recommandations.
        """
        recommendations = []

        # Analyser les performances
        avg_times = [stats["avg_execution_time"] for stats in tree_stats.values()]
        if avg_times:
            best_time = min(avg_times)
            worst_time = max(avg_times)

            if worst_time > best_time * 2:
                recommendations.append(
                    "Consider using the fastest tree implementation for critical operations"
                )

        # Analyser les taux de succès
        success_rates = [stats["success_rate"] for stats in tree_stats.values()]
        if success_rates and min(success_rates) < 0.95:
            recommendations.append(
                "Some implementations have low success rates - investigate error handling"
            )

        return recommendations

    def _generate_complexity_recommendations(
        self, complexity_analysis: Dict[str, Any]
    ) -> List[str]:
        """
        Génère des recommandations basées sur l'analyse de complexité.

        Args:
            complexity_analysis: Analyse de complexité.

        Returns:
            Liste des recommandations.
        """
        recommendations = []

        complexity_class = complexity_analysis.get("complexity_class", "unknown")
        scalability = complexity_analysis.get("scalability", "unknown")

        if complexity_class in ["O(n²) or higher"]:
            recommendations.append(
                "Consider optimizing the algorithm - complexity is higher than expected"
            )

        if scalability == "poor":
            recommendations.append(
                "Scalability is poor - consider alternative data structures for large datasets"
            )

        if complexity_class == "O(1)" and scalability == "excellent":
            recommendations.append(
                "Excellent performance - this implementation is optimal for the use case"
            )

        return recommendations

    def _generate_continuous_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un résumé de l'analyse continue.

        Args:
            analysis: Analyse continue.

        Returns:
            Résumé de l'analyse.
        """
        operation_analysis = analysis.get("operation_analysis", {})
        system_analysis = analysis.get("system_analysis", {})

        summary = {
            "total_operations": sum(op["count"] for op in operation_analysis.values()),
            "avg_operation_time": (
                statistics.mean([op["avg_time"] for op in operation_analysis.values()])
                if operation_analysis
                else 0
            ),
            "system_load": system_analysis.get("system_load", "unknown"),
            "performance_trend": "stable",  # À calculer basé sur les données
        }

        return summary
