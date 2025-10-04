"""
Générateur de rapports de performance.

Ce module implémente la classe PerformanceReporter qui génère
des rapports de performance dans différents formats.
"""

import json
import csv
import xml.etree.ElementTree as ET
from typing import Any, Dict, List
from datetime import datetime


class PerformanceReporter:
    """
    Générateur de rapports de performance.

    Cette classe génère des rapports de performance dans différents
    formats (texte, JSON, HTML, CSV, XML).

    Examples:
        >>> reporter = PerformanceReporter()
        >>> report = reporter.generate_report(profiles, metrics, "text")
        >>> data = reporter.export_data(profiles, metrics, "json")
    """

    def __init__(self):
        """Initialise le générateur de rapports."""
        self._report_templates = {
            "text": self._generate_text_report,
            "json": self._generate_json_report,
            "html": self._generate_html_report,
            "csv": self._generate_csv_report,
            "xml": self._generate_xml_report,
        }

    def generate_report(
        self,
        profiles: List[Dict[str, Any]],
        metrics: Dict[str, Any],
        format_type: str = "text",
    ) -> str:
        """
        Génère un rapport de performance.

        Args:
            profiles: Liste des profils de performance.
            metrics: Métriques de performance.
            format_type: Format du rapport ('text', 'json', 'html', 'csv', 'xml').

        Returns:
            Rapport de performance formaté.

        Raises:
            ValueError: Si le format n'est pas supporté.
        """
        if format_type not in self._report_templates:
            raise ValueError(f"Unsupported format: {format_type}")

        return self._report_templates[format_type](profiles, metrics)

    def export_data(
        self,
        profiles: List[Dict[str, Any]],
        metrics: Dict[str, Any],
        format_type: str = "json",
    ) -> str:
        """
        Exporte les données de performance.

        Args:
            profiles: Liste des profils de performance.
            metrics: Métriques de performance.
            format_type: Format d'export ('json', 'csv', 'xml').

        Returns:
            Données exportées.

        Raises:
            ValueError: Si le format n'est pas supporté.
        """
        if format_type not in ["json", "csv", "xml"]:
            raise ValueError(f"Unsupported export format: {format_type}")

        return self._report_templates[format_type](profiles, metrics)

    def _generate_text_report(
        self, profiles: List[Dict[str, Any]], metrics: Dict[str, Any]
    ) -> str:
        """
        Génère un rapport en format texte.

        Args:
            profiles: Liste des profils de performance.
            metrics: Métriques de performance.

        Returns:
            Rapport en format texte.
        """
        report_lines = []

        # En-tête
        report_lines.append("=" * 80)
        report_lines.append("PERFORMANCE REPORT")
        report_lines.append("=" * 80)
        report_lines.append(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append(f"Total Profiles: {len(profiles)}")
        report_lines.append("")

        # Résumé des métriques
        if metrics:
            report_lines.append("METRICS SUMMARY")
            report_lines.append("-" * 40)

            # Métriques temporelles
            if "temporal" in metrics:
                temporal = metrics["temporal"]
                report_lines.append("Temporal Metrics:")
                report_lines.append(f"  Total Time: {temporal.total_time:.6f} seconds")
                report_lines.append(
                    f"  Average Time: {temporal.average_time:.6f} seconds"
                )
                report_lines.append(f"  Min Time: {temporal.min_time:.6f} seconds")
                report_lines.append(f"  Max Time: {temporal.max_time:.6f} seconds")
                report_lines.append("")

            # Métriques spatiales
            if "spatial" in metrics:
                spatial = metrics["spatial"]
                report_lines.append("Spatial Metrics:")
                report_lines.append(f"  Memory Usage: {spatial.memory_usage:,} bytes")
                report_lines.append(f"  Peak Memory: {spatial.peak_memory:,} bytes")
                report_lines.append(f"  Memory Growth: {spatial.memory_growth:,} bytes")
                report_lines.append(f"  Node Count: {spatial.node_count:,}")
                report_lines.append("")

            # Métriques opérationnelles
            if "operational" in metrics:
                operational = metrics["operational"]
                report_lines.append("Operational Metrics:")
                report_lines.append(f"  Insertions: {operational.insert_count:,}")
                report_lines.append(f"  Deletions: {operational.delete_count:,}")
                report_lines.append(f"  Searches: {operational.search_count:,}")
                report_lines.append(f"  Rotations: {operational.rotation_count:,}")
                report_lines.append(f"  Rebalances: {operational.rebalance_count:,}")
                report_lines.append("")

        # Détails des profils
        if profiles:
            report_lines.append("PROFILE DETAILS")
            report_lines.append("-" * 40)

            for i, profile in enumerate(profiles[:10]):  # Limiter à 10 profils
                report_lines.append(f"Profile {i + 1}:")
                report_lines.append(
                    f"  Operation: {profile.get('operation', 'unknown')}"
                )
                report_lines.append(
                    f"  Execution Time: {profile.get('execution_time', 0):.6f} seconds"
                )
                report_lines.append(
                    f"  Memory Delta: {profile.get('memory_delta', 0):,} bytes"
                )
                report_lines.append(f"  Success: {profile.get('success', False)}")
                report_lines.append(
                    f"  Timestamp: {datetime.fromtimestamp(profile.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}"
                )

                if "error" in profile:
                    report_lines.append(f"  Error: {profile['error']}")

                report_lines.append("")

            if len(profiles) > 10:
                report_lines.append(f"... and {len(profiles) - 10} more profiles")
                report_lines.append("")

        # Statistiques
        if profiles:
            report_lines.append("STATISTICS")
            report_lines.append("-" * 40)

            execution_times = [
                p.get("execution_time", 0) for p in profiles if "execution_time" in p
            ]
            if execution_times:
                report_lines.append(f"Execution Time Statistics:")
                report_lines.append(
                    f"  Mean: {sum(execution_times) / len(execution_times):.6f} seconds"
                )
                report_lines.append(f"  Min: {min(execution_times):.6f} seconds")
                report_lines.append(f"  Max: {max(execution_times):.6f} seconds")
                report_lines.append("")

            success_count = sum(1 for p in profiles if p.get("success", False))
            report_lines.append(
                f"Success Rate: {success_count / len(profiles) * 100:.1f}%"
            )
            report_lines.append("")

        report_lines.append("=" * 80)

        return "\n".join(report_lines)

    def _generate_json_report(
        self, profiles: List[Dict[str, Any]], metrics: Dict[str, Any]
    ) -> str:
        """
        Génère un rapport en format JSON.

        Args:
            profiles: Liste des profils de performance.
            metrics: Métriques de performance.

        Returns:
            Rapport en format JSON.
        """
        report_data = {
            "report_info": {
                "generated": datetime.now().isoformat(),
                "total_profiles": len(profiles),
                "format": "json",
            },
            "metrics": metrics,
            "profiles": profiles,
            "statistics": self._calculate_statistics(profiles),
        }

        return json.dumps(report_data, indent=2, default=str)

    def _generate_html_report(
        self, profiles: List[Dict[str, Any]], metrics: Dict[str, Any]
    ) -> str:
        """
        Génère un rapport en format HTML.

        Args:
            profiles: Liste des profils de performance.
            metrics: Métriques de performance.

        Returns:
            Rapport en format HTML.
        """
        html_lines = []

        # En-tête HTML
        html_lines.append("<!DOCTYPE html>")
        html_lines.append("<html>")
        html_lines.append("<head>")
        html_lines.append("    <title>Performance Report</title>")
        html_lines.append("    <style>")
        html_lines.append(
            "        body { font-family: Arial, sans-serif; margin: 20px; }"
        )
        html_lines.append("        h1, h2 { color: #333; }")
        html_lines.append("        table { border-collapse: collapse; width: 100%; }")
        html_lines.append(
            "        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }"
        )
        html_lines.append("        th { background-color: #f2f2f2; }")
        html_lines.append(
            "        .metric { background-color: #f9f9f9; padding: 10px; margin: 10px 0; }"
        )
        html_lines.append("    </style>")
        html_lines.append("</head>")
        html_lines.append("<body>")

        # Titre
        html_lines.append("    <h1>Performance Report</h1>")
        html_lines.append(
            f"    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        )
        html_lines.append(f"    <p>Total Profiles: {len(profiles)}</p>")

        # Métriques
        if metrics:
            html_lines.append("    <h2>Metrics Summary</h2>")

            if "temporal" in metrics:
                temporal = metrics["temporal"]
                html_lines.append("    <div class='metric'>")
                html_lines.append("        <h3>Temporal Metrics</h3>")
                html_lines.append(
                    f"        <p>Total Time: {temporal.total_time:.6f} seconds</p>"
                )
                html_lines.append(
                    f"        <p>Average Time: {temporal.average_time:.6f} seconds</p>"
                )
                html_lines.append(
                    f"        <p>Min Time: {temporal.min_time:.6f} seconds</p>"
                )
                html_lines.append(
                    f"        <p>Max Time: {temporal.max_time:.6f} seconds</p>"
                )
                html_lines.append("    </div>")

            if "spatial" in metrics:
                spatial = metrics["spatial"]
                html_lines.append("    <div class='metric'>")
                html_lines.append("        <h3>Spatial Metrics</h3>")
                html_lines.append(
                    f"        <p>Memory Usage: {spatial.memory_usage:,} bytes</p>"
                )
                html_lines.append(
                    f"        <p>Peak Memory: {spatial.peak_memory:,} bytes</p>"
                )
                html_lines.append(
                    f"        <p>Memory Growth: {spatial.memory_growth:,} bytes</p>"
                )
                html_lines.append(f"        <p>Node Count: {spatial.node_count:,}</p>")
                html_lines.append("    </div>")

        # Tableau des profils
        if profiles:
            html_lines.append("    <h2>Profile Details</h2>")
            html_lines.append("    <table>")
            html_lines.append("        <tr>")
            html_lines.append("            <th>Operation</th>")
            html_lines.append("            <th>Execution Time</th>")
            html_lines.append("            <th>Memory Delta</th>")
            html_lines.append("            <th>Success</th>")
            html_lines.append("            <th>Timestamp</th>")
            html_lines.append("        </tr>")

            for profile in profiles[:20]:  # Limiter à 20 profils
                html_lines.append("        <tr>")
                html_lines.append(
                    f"            <td>{profile.get('operation', 'unknown')}</td>"
                )
                html_lines.append(
                    f"            <td>{profile.get('execution_time', 0):.6f}</td>"
                )
                html_lines.append(
                    f"            <td>{profile.get('memory_delta', 0):,}</td>"
                )
                html_lines.append(
                    f"            <td>{profile.get('success', False)}</td>"
                )
                html_lines.append(
                    f"            <td>{datetime.fromtimestamp(profile.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}</td>"
                )
                html_lines.append("        </tr>")

            html_lines.append("    </table>")

        html_lines.append("</body>")
        html_lines.append("</html>")

        return "\n".join(html_lines)

    def _generate_csv_report(
        self, profiles: List[Dict[str, Any]], metrics: Dict[str, Any]
    ) -> str:
        """
        Génère un rapport en format CSV.

        Args:
            profiles: Liste des profils de performance.
            metrics: Métriques de performance.

        Returns:
            Rapport en format CSV.
        """
        if not profiles:
            return "No data available"

        # Préparer les données CSV
        csv_lines = []

        # En-tête
        headers = [
            "operation",
            "execution_time",
            "memory_delta",
            "memory_usage",
            "success",
            "timestamp",
            "error",
        ]
        csv_lines.append(",".join(headers))

        # Données
        for profile in profiles:
            row = [
                profile.get("operation", ""),
                str(profile.get("execution_time", 0)),
                str(profile.get("memory_delta", 0)),
                str(profile.get("memory_usage", 0)),
                str(profile.get("success", False)),
                str(profile.get("timestamp", 0)),
                profile.get("error", ""),
            ]
            csv_lines.append(",".join(row))

        return "\n".join(csv_lines)

    def _generate_xml_report(
        self, profiles: List[Dict[str, Any]], metrics: Dict[str, Any]
    ) -> str:
        """
        Génère un rapport en format XML.

        Args:
            profiles: Liste des profils de performance.
            metrics: Métriques de performance.

        Returns:
            Rapport en format XML.
        """
        # Créer l'élément racine
        root = ET.Element("performance_report")

        # Informations du rapport
        report_info = ET.SubElement(root, "report_info")
        ET.SubElement(report_info, "generated").text = datetime.now().isoformat()
        ET.SubElement(report_info, "total_profiles").text = str(len(profiles))
        ET.SubElement(report_info, "format").text = "xml"

        # Métriques
        if metrics:
            metrics_elem = ET.SubElement(root, "metrics")

            if "temporal" in metrics:
                temporal_elem = ET.SubElement(metrics_elem, "temporal")
                temporal = metrics["temporal"]
                ET.SubElement(temporal_elem, "total_time").text = str(
                    temporal.total_time
                )
                ET.SubElement(temporal_elem, "average_time").text = str(
                    temporal.average_time
                )
                ET.SubElement(temporal_elem, "min_time").text = str(temporal.min_time)
                ET.SubElement(temporal_elem, "max_time").text = str(temporal.max_time)

            if "spatial" in metrics:
                spatial_elem = ET.SubElement(metrics_elem, "spatial")
                spatial = metrics["spatial"]
                ET.SubElement(spatial_elem, "memory_usage").text = str(
                    spatial.memory_usage
                )
                ET.SubElement(spatial_elem, "peak_memory").text = str(
                    spatial.peak_memory
                )
                ET.SubElement(spatial_elem, "memory_growth").text = str(
                    spatial.memory_growth
                )
                ET.SubElement(spatial_elem, "node_count").text = str(spatial.node_count)

        # Profils
        if profiles:
            profiles_elem = ET.SubElement(root, "profiles")

            for profile in profiles:
                profile_elem = ET.SubElement(profiles_elem, "profile")
                ET.SubElement(profile_elem, "operation").text = str(
                    profile.get("operation", "")
                )
                ET.SubElement(profile_elem, "execution_time").text = str(
                    profile.get("execution_time", 0)
                )
                ET.SubElement(profile_elem, "memory_delta").text = str(
                    profile.get("memory_delta", 0)
                )
                ET.SubElement(profile_elem, "success").text = str(
                    profile.get("success", False)
                )
                ET.SubElement(profile_elem, "timestamp").text = str(
                    profile.get("timestamp", 0)
                )

                if "error" in profile:
                    ET.SubElement(profile_elem, "error").text = str(profile["error"])

        # Convertir en string
        ET.indent(root, space="  ", level=0)
        return ET.tostring(root, encoding="unicode")

    def _calculate_statistics(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcule les statistiques des profils.

        Args:
            profiles: Liste des profils de performance.

        Returns:
            Dict contenant les statistiques.
        """
        if not profiles:
            return {}

        execution_times = [
            p.get("execution_time", 0) for p in profiles if "execution_time" in p
        ]
        memory_deltas = [
            p.get("memory_delta", 0) for p in profiles if "memory_delta" in p
        ]
        success_count = sum(1 for p in profiles if p.get("success", False))

        stats = {
            "total_profiles": len(profiles),
            "success_rate": success_count / len(profiles) if profiles else 0,
            "error_rate": (
                (len(profiles) - success_count) / len(profiles) if profiles else 0
            ),
        }

        if execution_times:
            stats["execution_time"] = {
                "mean": sum(execution_times) / len(execution_times),
                "min": min(execution_times),
                "max": max(execution_times),
                "total": sum(execution_times),
            }

        if memory_deltas:
            stats["memory_delta"] = {
                "mean": sum(memory_deltas) / len(memory_deltas),
                "min": min(memory_deltas),
                "max": max(memory_deltas),
                "total": sum(memory_deltas),
            }

        return stats
