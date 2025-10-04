"""
Visualiseur de performance pour les données de profiling.

Ce module implémente la classe PerformanceVisualizer qui crée
des visualisations des métriques de performance.
"""

import json
import csv
from typing import Any, Dict, List, Optional
from datetime import datetime


class PerformanceVisualizer:
    """
    Visualiseur de performance pour les données de profiling.

    Cette classe crée des visualisations des métriques de performance
    dans différents formats (graphiques, tableaux, etc.).

    Examples:
        >>> visualizer = PerformanceVisualizer()
        >>> visualizer.create_visualization(profiles, "execution_time", "chart.png")
        >>> visualizer.create_summary_chart(profiles, "summary.html")
    """

    def __init__(self):
        """Initialise le visualiseur de performance."""
        self._chart_templates = {
            "line": self._create_line_chart,
            "bar": self._create_bar_chart,
            "scatter": self._create_scatter_chart,
            "histogram": self._create_histogram_chart,
        }

    def create_visualization(
        self,
        profiles: List[Dict[str, Any]],
        metric: str,
        output_file: str,
        chart_type: str = "line",
    ) -> None:
        """
        Crée une visualisation des métriques.

        Args:
            profiles: Liste des profils de performance.
            metric: Métrique à visualiser.
            output_file: Fichier de sortie pour la visualisation.
            chart_type: Type de graphique ('line', 'bar', 'scatter', 'histogram').

        Raises:
            ValueError: Si le type de graphique n'est pas supporté.
        """
        if chart_type not in self._chart_templates:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        # Extraire les données pour la métrique
        data = self._extract_metric_data(profiles, metric)

        if not data:
            raise ValueError(f"No data available for metric: {metric}")

        # Créer le graphique
        chart_content = self._chart_templates[chart_type](data, metric)

        # Sauvegarder le fichier
        self._save_visualization(chart_content, output_file)

    def create_summary_chart(
        self, profiles: List[Dict[str, Any]], output_file: str
    ) -> None:
        """
        Crée un graphique de résumé des performances.

        Args:
            profiles: Liste des profils de performance.
            output_file: Fichier de sortie pour le graphique.
        """
        # Analyser les données
        summary_data = self._analyze_profiles_for_summary(profiles)

        # Créer le contenu HTML
        html_content = self._create_summary_html(summary_data)

        # Sauvegarder le fichier
        self._save_visualization(html_content, output_file)

    def create_comparison_chart(
        self, comparison_data: Dict[str, Any], output_file: str
    ) -> None:
        """
        Crée un graphique de comparaison des performances.

        Args:
            comparison_data: Données de comparaison.
            output_file: Fichier de sortie pour le graphique.
        """
        # Créer le contenu HTML pour la comparaison
        html_content = self._create_comparison_html(comparison_data)

        # Sauvegarder le fichier
        self._save_visualization(html_content, output_file)

    def create_timeline_chart(
        self, profiles: List[Dict[str, Any]], output_file: str
    ) -> None:
        """
        Crée un graphique de timeline des performances.

        Args:
            profiles: Liste des profils de performance.
            output_file: Fichier de sortie pour le graphique.
        """
        # Extraire les données temporelles
        timeline_data = self._extract_timeline_data(profiles)

        # Créer le contenu HTML
        html_content = self._create_timeline_html(timeline_data)

        # Sauvegarder le fichier
        self._save_visualization(html_content, output_file)

    def export_chart_data(
        self,
        profiles: List[Dict[str, Any]],
        metric: str,
        output_file: str,
        format_type: str = "csv",
    ) -> None:
        """
        Exporte les données de graphique.

        Args:
            profiles: Liste des profils de performance.
            metric: Métrique à exporter.
            output_file: Fichier de sortie.
            format_type: Format d'export ('csv', 'json').
        """
        # Extraire les données
        data = self._extract_metric_data(profiles, metric)

        if format_type == "csv":
            self._export_csv_data(data, output_file)
        elif format_type == "json":
            self._export_json_data(data, output_file)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def _extract_metric_data(
        self, profiles: List[Dict[str, Any]], metric: str
    ) -> List[Dict[str, Any]]:
        """
        Extrait les données pour une métrique spécifique.

        Args:
            profiles: Liste des profils de performance.
            metric: Métrique à extraire.

        Returns:
            Liste des données extraites.
        """
        data = []

        for i, profile in enumerate(profiles):
            if metric in profile:
                data.append(
                    {
                        "index": i,
                        "value": profile[metric],
                        "timestamp": profile.get("timestamp", 0),
                        "operation": profile.get("operation", "unknown"),
                        "success": profile.get("success", False),
                    }
                )

        return data

    def _extract_timeline_data(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extrait les données pour un graphique de timeline.

        Args:
            profiles: Liste des profils de performance.

        Returns:
            Dict contenant les données de timeline.
        """
        timeline_data = {
            "execution_times": [],
            "memory_deltas": [],
            "timestamps": [],
            "operations": [],
            "success_rates": [],
        }

        for profile in profiles:
            timeline_data["execution_times"].append(profile.get("execution_time", 0))
            timeline_data["memory_deltas"].append(profile.get("memory_delta", 0))
            timeline_data["timestamps"].append(profile.get("timestamp", 0))
            timeline_data["operations"].append(profile.get("operation", "unknown"))
            timeline_data["success_rates"].append(
                1 if profile.get("success", False) else 0
            )

        return timeline_data

    def _analyze_profiles_for_summary(
        self, profiles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyse les profils pour créer un résumé.

        Args:
            profiles: Liste des profils de performance.

        Returns:
            Dict contenant les données de résumé.
        """
        if not profiles:
            return {}

        # Grouper par opération
        operation_stats = {}
        for profile in profiles:
            operation = profile.get("operation", "unknown")
            if operation not in operation_stats:
                operation_stats[operation] = {
                    "count": 0,
                    "total_time": 0,
                    "success_count": 0,
                    "times": [],
                }

            operation_stats[operation]["count"] += 1
            operation_stats[operation]["total_time"] += profile.get("execution_time", 0)
            operation_stats[operation]["times"].append(profile.get("execution_time", 0))

            if profile.get("success", False):
                operation_stats[operation]["success_count"] += 1

        # Calculer les moyennes
        for operation, stats in operation_stats.items():
            stats["avg_time"] = stats["total_time"] / stats["count"]
            stats["success_rate"] = stats["success_count"] / stats["count"]
            stats["min_time"] = min(stats["times"])
            stats["max_time"] = max(stats["times"])

        return {
            "total_profiles": len(profiles),
            "operation_stats": operation_stats,
            "overall_stats": self._calculate_overall_stats(profiles),
        }

    def _calculate_overall_stats(
        self, profiles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calcule les statistiques globales.

        Args:
            profiles: Liste des profils de performance.

        Returns:
            Dict contenant les statistiques globales.
        """
        execution_times = [p.get("execution_time", 0) for p in profiles]
        memory_deltas = [p.get("memory_delta", 0) for p in profiles]
        success_count = sum(1 for p in profiles if p.get("success", False))

        return {
            "total_operations": len(profiles),
            "success_rate": success_count / len(profiles) if profiles else 0,
            "avg_execution_time": (
                sum(execution_times) / len(execution_times) if execution_times else 0
            ),
            "total_execution_time": sum(execution_times),
            "avg_memory_delta": (
                sum(memory_deltas) / len(memory_deltas) if memory_deltas else 0
            ),
            "total_memory_delta": sum(memory_deltas),
        }

    def _create_line_chart(self, data: List[Dict[str, Any]], metric: str) -> str:
        """
        Crée un graphique en ligne.

        Args:
            data: Données à visualiser.
            metric: Nom de la métrique.

        Returns:
            Contenu HTML du graphique.
        """
        # Créer les données JavaScript
        js_data = json.dumps(data)

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Chart - {metric}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .chart-container {{ width: 800px; height: 400px; }}
    </style>
</head>
<body>
    <h1>Performance Chart - {metric}</h1>
    <div class="chart-container">
        <canvas id="performanceChart"></canvas>
    </div>
    
    <script>
        const data = {js_data};
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: data.map(d => d.index),
                datasets: [{{
                    label: '{metric}',
                    data: data.map(d => d.value),
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        return html_content

    def _create_bar_chart(self, data: List[Dict[str, Any]], metric: str) -> str:
        """
        Crée un graphique en barres.

        Args:
            data: Données à visualiser.
            metric: Nom de la métrique.

        Returns:
            Contenu HTML du graphique.
        """
        # Grouper par opération
        operation_data = {}
        for item in data:
            operation = item["operation"]
            if operation not in operation_data:
                operation_data[operation] = []
            operation_data[operation].append(item["value"])

        # Calculer les moyennes
        chart_data = {}
        for operation, values in operation_data.items():
            chart_data[operation] = sum(values) / len(values)

        js_data = json.dumps(chart_data)

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Chart - {metric}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .chart-container {{ width: 800px; height: 400px; }}
    </style>
</head>
<body>
    <h1>Performance Chart - {metric}</h1>
    <div class="chart-container">
        <canvas id="performanceChart"></canvas>
    </div>
    
    <script>
        const data = {js_data};
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: Object.keys(data),
                datasets: [{{
                    label: '{metric}',
                    data: Object.values(data),
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        return html_content

    def _create_scatter_chart(self, data: List[Dict[str, Any]], metric: str) -> str:
        """
        Crée un graphique en nuage de points.

        Args:
            data: Données à visualiser.
            metric: Nom de la métrique.

        Returns:
            Contenu HTML du graphique.
        """
        js_data = json.dumps(data)

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Chart - {metric}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .chart-container {{ width: 800px; height: 400px; }}
    </style>
</head>
<body>
    <h1>Performance Chart - {metric}</h1>
    <div class="chart-container">
        <canvas id="performanceChart"></canvas>
    </div>
    
    <script>
        const data = {js_data};
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        new Chart(ctx, {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: '{metric}',
                    data: data.map(d => ({{x: d.index, y: d.value}})),
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    x: {{
                        type: 'linear',
                        position: 'bottom'
                    }},
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        return html_content

    def _create_histogram_chart(self, data: List[Dict[str, Any]], metric: str) -> str:
        """
        Crée un graphique en histogramme.

        Args:
            data: Données à visualiser.
            metric: Nom de la métrique.

        Returns:
            Contenu HTML du graphique.
        """
        # Créer des bins pour l'histogramme
        values = [item["value"] for item in data]
        if not values:
            return "<html><body><h1>No data available</h1></body></html>"

        min_val = min(values)
        max_val = max(values)
        bin_count = min(20, len(values) // 2)  # Maximum 20 bins

        if max_val == min_val:
            bins = [min_val]
            counts = [len(values)]
        else:
            bin_size = (max_val - min_val) / bin_count
            bins = [min_val + i * bin_size for i in range(bin_count + 1)]
            counts = [0] * bin_count

            for value in values:
                bin_index = min(int((value - min_val) / bin_size), bin_count - 1)
                counts[bin_index] += 1

        js_data = json.dumps({"bins": bins[:-1], "counts": counts})

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Chart - {metric}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .chart-container {{ width: 800px; height: 400px; }}
    </style>
</head>
<body>
    <h1>Performance Chart - {metric}</h1>
    <div class="chart-container">
        <canvas id="performanceChart"></canvas>
    </div>
    
    <script>
        const data = {js_data};
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: data.bins.map(b => b.toFixed(2)),
                datasets: [{{
                    label: '{metric} Distribution',
                    data: data.counts,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        return html_content

    def _create_summary_html(self, summary_data: Dict[str, Any]) -> str:
        """
        Crée le HTML pour le résumé.

        Args:
            summary_data: Données de résumé.

        Returns:
            Contenu HTML du résumé.
        """
        html_lines = []

        html_lines.append("<!DOCTYPE html>")
        html_lines.append("<html>")
        html_lines.append("<head>")
        html_lines.append("    <title>Performance Summary</title>")
        html_lines.append("    <style>")
        html_lines.append(
            "        body { font-family: Arial, sans-serif; margin: 20px; }"
        )
        html_lines.append(
            "        .summary { background-color: #f9f9f9; padding: 20px; margin: 20px 0; }"
        )
        html_lines.append("        .operation-stats { margin: 10px 0; }")
        html_lines.append("        table { border-collapse: collapse; width: 100%; }")
        html_lines.append(
            "        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }"
        )
        html_lines.append("        th { background-color: #f2f2f2; }")
        html_lines.append("    </style>")
        html_lines.append("</head>")
        html_lines.append("<body>")

        html_lines.append("    <h1>Performance Summary</h1>")
        html_lines.append(
            f"    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        )

        # Statistiques globales
        if "overall_stats" in summary_data:
            overall = summary_data["overall_stats"]
            html_lines.append("    <div class='summary'>")
            html_lines.append("        <h2>Overall Statistics</h2>")
            html_lines.append(
                f"        <p>Total Operations: {overall['total_operations']:,}</p>"
            )
            html_lines.append(
                f"        <p>Success Rate: {overall['success_rate']:.1%}</p>"
            )
            html_lines.append(
                f"        <p>Average Execution Time: {overall['avg_execution_time']:.6f} seconds</p>"
            )
            html_lines.append(
                f"        <p>Total Execution Time: {overall['total_execution_time']:.6f} seconds</p>"
            )
            html_lines.append("    </div>")

        # Statistiques par opération
        if "operation_stats" in summary_data:
            html_lines.append("    <h2>Operation Statistics</h2>")
            html_lines.append("    <table>")
            html_lines.append("        <tr>")
            html_lines.append("            <th>Operation</th>")
            html_lines.append("            <th>Count</th>")
            html_lines.append("            <th>Avg Time</th>")
            html_lines.append("            <th>Min Time</th>")
            html_lines.append("            <th>Max Time</th>")
            html_lines.append("            <th>Success Rate</th>")
            html_lines.append("        </tr>")

            for operation, stats in summary_data["operation_stats"].items():
                html_lines.append("        <tr>")
                html_lines.append(f"            <td>{operation}</td>")
                html_lines.append(f"            <td>{stats['count']:,}</td>")
                html_lines.append(f"            <td>{stats['avg_time']:.6f}</td>")
                html_lines.append(f"            <td>{stats['min_time']:.6f}</td>")
                html_lines.append(f"            <td>{stats['max_time']:.6f}</td>")
                html_lines.append(f"            <td>{stats['success_rate']:.1%}</td>")
                html_lines.append("        </tr>")

            html_lines.append("    </table>")

        html_lines.append("</body>")
        html_lines.append("</html>")

        return "\n".join(html_lines)

    def _create_comparison_html(self, comparison_data: Dict[str, Any]) -> str:
        """
        Crée le HTML pour la comparaison.

        Args:
            comparison_data: Données de comparaison.

        Returns:
            Contenu HTML de la comparaison.
        """
        # Implémentation simplifiée - à étendre selon les besoins
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Comparison</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .comparison {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Performance Comparison</h1>
    <div class="comparison">
        <pre>{json.dumps(comparison_data, indent=2)}</pre>
    </div>
</body>
</html>
"""
        return html_content

    def _create_timeline_html(self, timeline_data: Dict[str, Any]) -> str:
        """
        Crée le HTML pour la timeline.

        Args:
            timeline_data: Données de timeline.

        Returns:
            Contenu HTML de la timeline.
        """
        js_data = json.dumps(timeline_data)

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Timeline</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .chart-container {{ width: 1000px; height: 500px; }}
    </style>
</head>
<body>
    <h1>Performance Timeline</h1>
    <div class="chart-container">
        <canvas id="timelineChart"></canvas>
    </div>
    
    <script>
        const data = {js_data};
        const ctx = document.getElementById('timelineChart').getContext('2d');
        
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: data.timestamps.map(t => new Date(t * 1000).toLocaleTimeString()),
                datasets: [
                    {{
                        label: 'Execution Time',
                        data: data.execution_times,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        yAxisID: 'y'
                    }},
                    {{
                        label: 'Memory Delta',
                        data: data.memory_deltas,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        type: 'linear',
                        display: true,
                        position: 'left',
                    }},
                    y1: {{
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {{
                            drawOnChartArea: false,
                        }},
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        return html_content

    def _save_visualization(self, content: str, output_file: str) -> None:
        """
        Sauvegarde la visualisation dans un fichier.

        Args:
            content: Contenu à sauvegarder.
            output_file: Fichier de sortie.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _export_csv_data(self, data: List[Dict[str, Any]], output_file: str) -> None:
        """
        Exporte les données en CSV.

        Args:
            data: Données à exporter.
            output_file: Fichier de sortie.
        """
        if not data:
            return

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def _export_json_data(self, data: List[Dict[str, Any]], output_file: str) -> None:
        """
        Exporte les données en JSON.

        Args:
            data: Données à exporter.
            output_file: Fichier de sortie.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
