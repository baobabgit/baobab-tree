"""
Moniteur de performance en temps réel.

Ce module implémente la classe PerformanceMonitor qui surveille
les performances en temps réel et gère les alertes.
"""

import time
import threading
from typing import Any, Dict, List, Optional, Callable
from collections import deque
from dataclasses import dataclass


@dataclass
class Alert:
    """Configuration d'une alerte de performance."""

    metric: str
    threshold: float
    condition: str  # 'greater_than', 'less_than', 'equals'
    action: str  # 'log', 'callback', 'email'
    callback: Optional[Callable] = None
    enabled: bool = True


class PerformanceMonitor:
    """
    Moniteur de performance en temps réel.

    Cette classe surveille les performances en temps réel et peut
    déclencher des alertes basées sur des seuils configurés.

    Examples:
        >>> monitor = PerformanceMonitor()
        >>> monitor.set_alerts([Alert('execution_time', 1.0, 'greater_than', 'log')])
        >>> monitor.start_monitoring()
    """

    def __init__(self):
        """Initialise le moniteur de performance."""
        self._alerts: List[Alert] = []
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Buffer circulaire pour les métriques récentes
        self._metrics_buffer = deque(maxlen=1000)
        self._alert_history: List[Dict[str, Any]] = []

        # Configuration du monitoring
        self._config = {
            "sampling_interval": 1.0,  # secondes
            "buffer_size": 1000,
            "adaptive_monitoring": False,
            "alert_cooldown": 60.0,  # secondes entre alertes similaires
        }

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure le moniteur.

        Args:
            config: Configuration du moniteur.
        """
        self._config.update(config)

        # Ajuster la taille du buffer si nécessaire
        if "buffer_size" in config:
            self._metrics_buffer = deque(maxlen=config["buffer_size"])

    def start_monitoring(self) -> None:
        """
        Démarre le monitoring en temps réel.

        Raises:
            RuntimeError: Si le monitoring est déjà en cours.
        """
        if self._monitoring:
            raise RuntimeError("Monitoring is already running")

        self._monitoring = True
        self._stop_event.clear()

        # Démarrer le thread de monitoring
        self._monitor_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self._monitor_thread.start()

    def stop_monitoring(self) -> None:
        """
        Arrête le monitoring en temps réel.

        Raises:
            RuntimeError: Si le monitoring n'est pas en cours.
        """
        if not self._monitoring:
            raise RuntimeError("Monitoring is not running")

        self._monitoring = False
        self._stop_event.set()

        # Attendre que le thread se termine
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5.0)

    def set_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """
        Configure les alertes de performance.

        Args:
            alerts: Liste des alertes à configurer.
        """
        self._alerts.clear()

        for alert_config in alerts:
            alert = Alert(
                metric=alert_config.get("metric", ""),
                threshold=alert_config.get("threshold", 0.0),
                condition=alert_config.get("condition", "greater_than"),
                action=alert_config.get("action", "log"),
                callback=alert_config.get("callback"),
                enabled=alert_config.get("enabled", True),
            )
            self._alerts.append(alert)

    def add_alert(self, alert: Alert) -> None:
        """
        Ajoute une alerte.

        Args:
            alert: Alerte à ajouter.
        """
        self._alerts.append(alert)

    def remove_alert(self, metric: str, threshold: float) -> bool:
        """
        Supprime une alerte.

        Args:
            metric: Métrique de l'alerte.
            threshold: Seuil de l'alerte.

        Returns:
            True si l'alerte a été supprimée, False sinon.
        """
        for i, alert in enumerate(self._alerts):
            if alert.metric == metric and alert.threshold == threshold:
                del self._alerts[i]
                return True
        return False

    def enable_adaptive_monitoring(self) -> None:
        """Active le monitoring adaptatif."""
        self._config["adaptive_monitoring"] = True

    def disable_adaptive_monitoring(self) -> None:
        """Désactive le monitoring adaptatif."""
        self._config["adaptive_monitoring"] = False

    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Obtient les métriques actuelles.

        Returns:
            Dict contenant les métriques actuelles.
        """
        try:
            import psutil

            return {
                "timestamp": time.time(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": psutil.disk_usage("/").percent,
                "load_average": (
                    psutil.getloadavg() if hasattr(psutil, "getloadavg") else None
                ),
            }
        except ImportError:
            return {
                "timestamp": time.time(),
                "cpu_percent": 0,
                "memory_percent": 0,
                "memory_available": 0,
                "disk_usage": 0,
                "load_average": None,
            }

    def get_metrics_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtient l'historique des métriques.

        Args:
            limit: Nombre maximum de métriques à retourner.

        Returns:
            Liste des métriques historiques.
        """
        return list(self._metrics_buffer)[-limit:]

    def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Obtient l'historique des alertes.

        Args:
            limit: Nombre maximum d'alertes à retourner.

        Returns:
            Liste des alertes historiques.
        """
        return self._alert_history[-limit:]

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Obtient un résumé des performances.

        Returns:
            Dict contenant le résumé des performances.
        """
        if not self._metrics_buffer:
            return {}

        # Calculer les statistiques sur les métriques récentes
        cpu_values = [m.get("cpu_percent", 0) for m in self._metrics_buffer]
        memory_values = [m.get("memory_percent", 0) for m in self._metrics_buffer]

        summary = {
            "monitoring_duration": (
                time.time() - self._metrics_buffer[0]["timestamp"]
                if self._metrics_buffer
                else 0
            ),
            "total_samples": len(self._metrics_buffer),
            "cpu_stats": self._calculate_stats(cpu_values),
            "memory_stats": self._calculate_stats(memory_values),
            "alert_count": len(self._alert_history),
            "monitoring_status": "active" if self._monitoring else "inactive",
        }

        return summary

    def _monitoring_loop(self) -> None:
        """Boucle principale du monitoring."""
        while not self._stop_event.is_set():
            try:
                # Collecter les métriques actuelles
                current_metrics = self.get_current_metrics()

                # Ajouter au buffer
                self._metrics_buffer.append(current_metrics)

                # Vérifier les alertes
                self._check_alerts(current_metrics)

                # Monitoring adaptatif
                if self._config["adaptive_monitoring"]:
                    self._adaptive_monitoring_adjustment()

                # Attendre avant la prochaine collecte
                self._stop_event.wait(timeout=self._config["sampling_interval"])

            except Exception as e:
                # Logger l'erreur et continuer
                self._log_error(f"Error in monitoring loop: {e}")
                self._stop_event.wait(timeout=1.0)

    def _check_alerts(self, metrics: Dict[str, Any]) -> None:
        """
        Vérifie les alertes basées sur les métriques.

        Args:
            metrics: Métriques actuelles.
        """
        current_time = time.time()

        for alert in self._alerts:
            if not alert.enabled:
                continue

            # Vérifier le cooldown
            if self._is_alert_in_cooldown(alert, current_time):
                continue

            # Obtenir la valeur de la métrique
            metric_value = metrics.get(alert.metric, 0)

            # Vérifier la condition
            if self._check_alert_condition(metric_value, alert):
                # Déclencher l'alerte
                self._trigger_alert(alert, metric_value, current_time)

    def _check_alert_condition(self, value: float, alert: Alert) -> bool:
        """
        Vérifie si une condition d'alerte est remplie.

        Args:
            value: Valeur de la métrique.
            alert: Configuration de l'alerte.

        Returns:
            True si la condition est remplie.
        """
        if alert.condition == "greater_than":
            return value > alert.threshold
        elif alert.condition == "less_than":
            return value < alert.threshold
        elif alert.condition == "equals":
            return abs(value - alert.threshold) < 0.001
        else:
            return False

    def _trigger_alert(self, alert: Alert, value: float, timestamp: float) -> None:
        """
        Déclenche une alerte.

        Args:
            alert: Configuration de l'alerte.
            value: Valeur qui a déclenché l'alerte.
            timestamp: Timestamp du déclenchement.
        """
        alert_data = {
            "timestamp": timestamp,
            "metric": alert.metric,
            "value": value,
            "threshold": alert.threshold,
            "condition": alert.condition,
            "action": alert.action,
        }

        # Ajouter à l'historique
        self._alert_history.append(alert_data)

        # Exécuter l'action
        if alert.action == "log":
            self._log_alert(alert_data)
        elif alert.action == "callback" and alert.callback:
            try:
                alert.callback(alert_data)
            except Exception as e:
                self._log_error(f"Error in alert callback: {e}")

    def _is_alert_in_cooldown(self, alert: Alert, current_time: float) -> bool:
        """
        Vérifie si une alerte est en période de cooldown.

        Args:
            alert: Configuration de l'alerte.
            current_time: Temps actuel.

        Returns:
            True si l'alerte est en cooldown.
        """
        cooldown = self._config["alert_cooldown"]

        # Chercher la dernière alerte pour cette métrique
        for alert_data in reversed(self._alert_history):
            if (
                alert_data["metric"] == alert.metric
                and current_time - alert_data["timestamp"] < cooldown
            ):
                return True

        return False

    def _adaptive_monitoring_adjustment(self) -> None:
        """Ajuste le monitoring de manière adaptative."""
        if len(self._metrics_buffer) < 10:
            return

        # Analyser les tendances récentes
        recent_metrics = list(self._metrics_buffer)[-10:]
        cpu_trend = self._calculate_trend(
            [m.get("cpu_percent", 0) for m in recent_metrics]
        )
        memory_trend = self._calculate_trend(
            [m.get("memory_percent", 0) for m in recent_metrics]
        )

        # Ajuster l'intervalle de sampling
        if cpu_trend > 0.1 or memory_trend > 0.1:  # Tendances croissantes
            # Réduire l'intervalle pour un monitoring plus fréquent
            self._config["sampling_interval"] = max(
                0.1, self._config["sampling_interval"] * 0.8
            )
        elif cpu_trend < -0.1 and memory_trend < -0.1:  # Tendances décroissantes
            # Augmenter l'intervalle pour un monitoring moins fréquent
            self._config["sampling_interval"] = min(
                5.0, self._config["sampling_interval"] * 1.2
            )

    def _calculate_trend(self, values: List[float]) -> float:
        """
        Calcule la tendance d'une série de valeurs.

        Args:
            values: Liste de valeurs.

        Returns:
            Coefficient de tendance (positif = croissant, négatif = décroissant).
        """
        if len(values) < 2:
            return 0.0

        n = len(values)
        x = list(range(n))

        # Calculer la régression linéaire simple
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(xi**2 for xi in x)

        denominator = n * sum_x2 - sum_x**2
        if denominator == 0:
            return 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope

    def _calculate_stats(self, values: List[float]) -> Dict[str, float]:
        """
        Calcule les statistiques d'une liste de valeurs.

        Args:
            values: Liste de valeurs.

        Returns:
            Dict contenant les statistiques.
        """
        if not values:
            return {}

        return {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1] if values else 0,
        }

    def _log_alert(self, alert_data: Dict[str, Any]) -> None:
        """
        Log une alerte.

        Args:
            alert_data: Données de l'alerte.
        """
        message = (
            f"PERFORMANCE ALERT: {alert_data['metric']} = {alert_data['value']} "
            f"{alert_data['condition']} {alert_data['threshold']} "
            f"at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(alert_data['timestamp']))}"
        )
        print(message)  # En production, utiliser un logger approprié

    def _log_error(self, message: str) -> None:
        """
        Log une erreur.

        Args:
            message: Message d'erreur.
        """
        print(
            f"PERFORMANCE MONITOR ERROR: {message}"
        )  # En production, utiliser un logger approprié
