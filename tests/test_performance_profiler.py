"""
Tests unitaires pour PerformanceProfiler.

Ce module teste toutes les fonctionnalités du PerformanceProfiler
selon les spécifications détaillées.
"""

import pytest
import time
import threading
from unittest.mock import Mock, patch, MagicMock

from baobab_tree.performance import (
    PerformanceProfiler,
    PerformanceMetrics,
    PerformanceAnalyzer,
    PerformanceReporter,
    PerformanceMonitor,
    PerformanceVisualizer,
    PerformanceProfilerError,
    ProfilingError,
    AnalysisError,
    ReportingError,
)


class TestPerformanceProfiler:
    """Tests pour la classe PerformanceProfiler."""
    
    def test_profiler_creation(self):
        """Test de création du profiler."""
        profiler = PerformanceProfiler[int]()
        assert profiler is not None
        assert profiler._config is not None
        assert profiler._profiles == []
        
    def test_configure_profiling(self):
        """Test de configuration du profiler."""
        profiler = PerformanceProfiler[int]()
        
        config = {
            'memory_tracking': True,
            'time_tracking': True,
            'operation_tracking': True,
            'continuous_profiling': False
        }
        
        profiler.configure_profiling(config)
        
        assert profiler._config['memory_tracking'] is True
        assert profiler._config['time_tracking'] is True
        assert profiler._config['operation_tracking'] is True
        
    def test_configure_profiling_invalid_key(self):
        """Test de configuration avec clé invalide."""
        profiler = PerformanceProfiler[int]()
        
        config = {'invalid_key': True}
        
        with pytest.raises(ValueError, match="Configuration key 'invalid_key' is not valid"):
            profiler.configure_profiling(config)
            
    def test_profile_operation_success(self):
        """Test de profiling d'opération réussie."""
        profiler = PerformanceProfiler[int]()
        
        def test_operation(x):
            time.sleep(0.001)  # Simuler une opération
            return x * 2
            
        profile = profiler.profile_operation(test_operation, 42)
        
        assert profile['operation'] == 'test_operation'
        assert profile['success'] is True
        assert profile['result'] == 84
        assert profile['execution_time'] > 0
        assert 'timestamp' in profile
        
    def test_profile_operation_failure(self):
        """Test de profiling d'opération échouée."""
        profiler = PerformanceProfiler[int]()
        
        def failing_operation(x):
            raise ValueError("Test error")
            
        profile = profiler.profile_operation(failing_operation, 42)
        
        assert profile['operation'] == 'failing_operation'
        assert profile['success'] is False
        assert profile['result'] is None
        assert profile['error'] == "Test error"
        assert profile['execution_time'] > 0
        
    def test_profile_sequence(self):
        """Test de profiling de séquence d'opérations."""
        profiler = PerformanceProfiler[int]()
        
        def op1(x):
            return x + 1
            
        def op2(x):
            return x * 2
            
        operations = [op1, op2]
        sequence_profile = profiler.profile_sequence(operations, 10)
        
        assert len(sequence_profile['operations']) == 2
        assert sequence_profile['success_count'] == 2
        assert sequence_profile['error_count'] == 0
        assert sequence_profile['total_execution_time'] > 0
        assert 'trends' in sequence_profile
        
    def test_continuous_profiling(self):
        """Test de profiling continu."""
        profiler = PerformanceProfiler[int]()
        
        # Démarrer le profiling continu
        profiler.start_continuous_profiling()
        assert profiler._continuous_profiling is True
        
        # Attendre un peu
        time.sleep(0.1)
        
        # Arrêter le profiling continu
        results = profiler.stop_continuous_profiling()
        
        assert 'profiling_duration' in results
        assert 'total_profiles' in results
        assert 'metrics' in results
        assert 'analysis' in results
        
    def test_continuous_profiling_already_running(self):
        """Test d'erreur si profiling continu déjà en cours."""
        profiler = PerformanceProfiler[int]()
        
        profiler.start_continuous_profiling()
        
        with pytest.raises(ProfilingError, match="Continuous profiling is already running"):
            profiler.start_continuous_profiling()
            
        profiler.stop_continuous_profiling()
        
    def test_continuous_profiling_not_running(self):
        """Test d'erreur si profiling continu pas en cours."""
        profiler = PerformanceProfiler[int]()
        
        with pytest.raises(ProfilingError, match="Continuous profiling is not running"):
            profiler.stop_continuous_profiling()
            
    def test_compare_performance(self):
        """Test de comparaison de performances."""
        profiler = PerformanceProfiler[int]()
        
        # Créer des arbres mock
        tree1 = Mock()
        tree1.__class__.__name__ = "AVLTree"
        tree1.insert = Mock(return_value=True)
        tree1.insert.__name__ = "insert"
        
        tree2 = Mock()
        tree2.__class__.__name__ = "RedBlackTree"
        tree2.insert = Mock(return_value=True)
        tree2.insert.__name__ = "insert"
        
        trees = [tree1, tree2]
        operations = ['insert']
        
        comparison = profiler.compare_performance(trees, operations)
        
        assert 'results' in comparison
        assert 'comparison' in comparison
        assert 'summary' in comparison
        assert 'AVLTree' in comparison['results']
        assert 'RedBlackTree' in comparison['results']
        
    def test_analyze_complexity(self):
        """Test d'analyse de complexité."""
        profiler = PerformanceProfiler[int]()
        
        # Créer un arbre mock
        tree = Mock()
        tree.insert = Mock(return_value=True)
        tree.insert.__name__ = "insert"
        
        sizes = [10, 100, 1000]
        complexity = profiler.analyze_complexity(tree, 'insert', sizes)
        
        assert 'complexity_data' in complexity
        assert 'analysis' in complexity
        assert 'summary' in complexity
        assert len(complexity['complexity_data']) == 3
        
    def test_identify_bottlenecks(self):
        """Test d'identification de goulots d'étranglement."""
        profiler = PerformanceProfiler[int]()
        
        # Créer un arbre mock avec opérations lentes
        tree = Mock()
        tree.insert = Mock(side_effect=lambda x: time.sleep(0.1))
        tree.insert.__name__ = "insert"
        tree.delete = Mock(side_effect=lambda x: time.sleep(0.05))
        tree.delete.__name__ = "delete"
        tree.search = Mock(side_effect=lambda x: time.sleep(0.01))
        tree.search.__name__ = "search"
        tree.find_min = Mock(side_effect=lambda: time.sleep(0.02))
        tree.find_min.__name__ = "find_min"
        tree.find_max = Mock(side_effect=lambda: time.sleep(0.02))
        tree.find_max.__name__ = "find_max"
        
        bottlenecks = profiler.identify_bottlenecks(tree)
        
        assert isinstance(bottlenecks, list)
        # Vérifier que les opérations lentes sont identifiées
        bottleneck_operations = [b['operation'] for b in bottlenecks]
        assert 'insert' in bottleneck_operations
        
    def test_generate_report(self):
        """Test de génération de rapport."""
        profiler = PerformanceProfiler[int]()
        
        # Ajouter quelques profils
        profiler._profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'success': True, 'timestamp': time.time()},
            {'operation': 'test', 'execution_time': 0.2, 'success': True, 'timestamp': time.time()}
        ]
        
        report = profiler.generate_report("text")
        
        assert isinstance(report, str)
        assert "PERFORMANCE REPORT" in report
        assert "Total Profiles: 2" in report
        
    def test_export_data(self):
        """Test d'export de données."""
        profiler = PerformanceProfiler[int]()
        
        # Ajouter quelques profils
        profiler._profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'success': True, 'timestamp': time.time()}
        ]
        
        data = profiler.export_data("json")
        
        assert isinstance(data, str)
        import json
        parsed_data = json.loads(data)
        assert 'profiles' in parsed_data
        
    def test_create_visualization(self):
        """Test de création de visualisation."""
        profiler = PerformanceProfiler[int]()
        
        # Ajouter quelques profils
        profiler._profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'success': True, 'timestamp': time.time()}
        ]
        
        # Mock la sauvegarde de fichier
        with patch('builtins.open', mock_open()) as mock_file:
            profiler.create_visualization("execution_time", "test.png")
            mock_file.assert_called_once_with("test.png", 'w', encoding='utf-8')
            
    def test_set_metric_filters(self):
        """Test de définition des filtres de métriques."""
        profiler = PerformanceProfiler[int]()
        
        filters = ['execution_time', 'memory_delta']
        profiler.set_metric_filters(filters)
        
        assert profiler._config['filters'] == filters
        
    def test_set_performance_thresholds(self):
        """Test de définition des seuils de performance."""
        profiler = PerformanceProfiler[int]()
        
        thresholds = {'execution_time': 1.0, 'memory_delta': 1000}
        profiler.set_performance_thresholds(thresholds)
        
        assert profiler._config['thresholds'] == thresholds
        
    def test_start_real_time_monitoring(self):
        """Test de démarrage du monitoring temps réel."""
        profiler = PerformanceProfiler[int]()
        
        profiler.start_real_time_monitoring()
        
        # Vérifier que le monitoring a été démarré
        assert profiler._monitor is not None
        
    def test_set_performance_alerts(self):
        """Test de configuration des alertes de performance."""
        profiler = PerformanceProfiler[int]()
        
        alerts = [
            {'metric': 'execution_time', 'threshold': 1.0, 'condition': 'greater_than', 'action': 'log'}
        ]
        
        profiler.set_performance_alerts(alerts)
        
        # Vérifier que les alertes ont été configurées
        assert profiler._monitor is not None
        
    def test_enable_adaptive_monitoring(self):
        """Test d'activation du monitoring adaptatif."""
        profiler = PerformanceProfiler[int]()
        
        profiler.enable_adaptive_monitoring()
        
        # Vérifier que le monitoring adaptatif a été activé
        assert profiler._monitor is not None


class TestPerformanceMetrics:
    """Tests pour la classe PerformanceMetrics."""
    
    def test_metrics_creation(self):
        """Test de création des métriques."""
        metrics = PerformanceMetrics()
        assert metrics is not None
        
    def test_start_end_measurement(self):
        """Test de mesure start/end."""
        metrics = PerformanceMetrics()
        
        metrics.start_measurement()
        time.sleep(0.001)
        measurement = metrics.end_measurement()
        
        assert 'execution_time' in measurement
        assert 'memory_delta' in measurement
        assert 'memory_usage' in measurement
        assert 'timestamp' in measurement
        assert measurement['execution_time'] > 0
        
    def test_end_measurement_without_start(self):
        """Test d'erreur si end_measurement sans start_measurement."""
        metrics = PerformanceMetrics()
        
        with pytest.raises(ValueError, match="start_measurement\\(\\) must be called first"):
            metrics.end_measurement()
            
    def test_record_operation(self):
        """Test d'enregistrement d'opération."""
        metrics = PerformanceMetrics()
        
        metrics.record_operation('insert')
        metrics.record_operation('delete')
        metrics.record_operation('search')
        
        operational = metrics.get_operational_metrics()
        assert operational.insert_count == 1
        assert operational.delete_count == 1
        assert operational.search_count == 1
        
    def test_get_all_metrics(self):
        """Test d'obtention de toutes les métriques."""
        metrics = PerformanceMetrics()
        
        metrics.start_measurement()
        time.sleep(0.001)
        metrics.end_measurement()
        metrics.record_operation('insert')
        
        all_metrics = metrics.get_all_metrics()
        
        assert 'temporal' in all_metrics
        assert 'spatial' in all_metrics
        assert 'operational' in all_metrics
        assert 'measurements' in all_metrics
        
    def test_reset(self):
        """Test de remise à zéro des métriques."""
        metrics = PerformanceMetrics()
        
        metrics.start_measurement()
        time.sleep(0.001)
        metrics.end_measurement()
        metrics.record_operation('insert')
        
        metrics.reset()
        
        temporal = metrics.get_temporal_metrics()
        spatial = metrics.get_spatial_metrics()
        operational = metrics.get_operational_metrics()
        
        assert temporal.total_time == 0
        assert spatial.memory_usage == 0
        assert operational.insert_count == 0
        
    def test_get_statistics(self):
        """Test d'obtention des statistiques."""
        metrics = PerformanceMetrics()
        
        # Ajouter plusieurs mesures
        for _ in range(5):
            metrics.start_measurement()
            time.sleep(0.001)
            metrics.end_measurement()
            
        stats = metrics.get_statistics()
        
        assert 'execution_time' in stats
        assert 'memory_delta' in stats
        assert 'total_operations' in stats
        assert 'total_time' in stats
        assert stats['total_operations'] == 5


class TestPerformanceAnalyzer:
    """Tests pour la classe PerformanceAnalyzer."""
    
    def test_analyzer_creation(self):
        """Test de création de l'analyseur."""
        analyzer = PerformanceAnalyzer()
        assert analyzer is not None
        
    def test_analyze_trends(self):
        """Test d'analyse des tendances."""
        analyzer = PerformanceAnalyzer()
        
        profiles = [
            {'execution_time': 0.1, 'memory_delta': 100},
            {'execution_time': 0.2, 'memory_delta': 200},
            {'execution_time': 0.3, 'memory_delta': 300}
        ]
        
        trends = analyzer.analyze_trends(profiles)
        
        assert 'execution_time' in trends
        assert 'memory_delta' in trends
        assert 'performance_trend' in trends
        assert 'memory_trend' in trends
        assert 'stability' in trends
        
    def test_analyze_trends_empty(self):
        """Test d'analyse des tendances avec données vides."""
        analyzer = PerformanceAnalyzer()
        
        trends = analyzer.analyze_trends([])
        assert trends == {}
        
    def test_compare_results(self):
        """Test de comparaison des résultats."""
        analyzer = PerformanceAnalyzer()
        
        results = {
            'AVLTree': {
                'insert': {'execution_time': 0.1, 'success': True},
                'search': {'execution_time': 0.05, 'success': True}
            },
            'RedBlackTree': {
                'insert': {'execution_time': 0.15, 'success': True},
                'search': {'execution_time': 0.08, 'success': True}
            }
        }
        
        comparison = analyzer.compare_results(results)
        
        assert 'tree_rankings' in comparison
        assert 'operation_rankings' in comparison
        assert 'best_performer' in comparison
        assert 'worst_performer' in comparison
        assert 'recommendations' in comparison
        
    def test_analyze_complexity_trends(self):
        """Test d'analyse des tendances de complexité."""
        analyzer = PerformanceAnalyzer()
        
        complexity_data = {
            10: {'avg_execution_time': 0.01},
            100: {'avg_execution_time': 0.1},
            1000: {'avg_execution_time': 1.0}
        }
        
        analysis = analyzer.analyze_complexity_trends(complexity_data)
        
        assert 'sizes' in analysis
        assert 'avg_execution_times' in analysis
        assert 'growth_rate' in analysis
        assert 'complexity_class' in analysis
        assert 'scalability' in analysis
        
    def test_analyze_continuous_data(self):
        """Test d'analyse des données continues."""
        analyzer = PerformanceAnalyzer()
        
        profiles = [
            {'type': 'operation', 'execution_time': 0.1, 'operation': 'insert'},
            {'type': 'system_monitoring', 'cpu_percent': 50, 'memory_percent': 60}
        ]
        
        analysis = analyzer.analyze_continuous_data(profiles)
        
        assert 'operation_analysis' in analysis
        assert 'system_analysis' in analysis
        assert 'correlation_analysis' in analysis
        assert 'summary' in analysis


class TestPerformanceReporter:
    """Tests pour la classe PerformanceReporter."""
    
    def test_reporter_creation(self):
        """Test de création du reporter."""
        reporter = PerformanceReporter()
        assert reporter is not None
        
    def test_generate_text_report(self):
        """Test de génération de rapport texte."""
        reporter = PerformanceReporter()
        
        profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'success': True, 'timestamp': time.time()}
        ]
        
        metrics = {
            'temporal': Mock(total_time=0.1, average_time=0.1, min_time=0.1, max_time=0.1),
            'spatial': Mock(memory_usage=1000, peak_memory=1000, memory_growth=0, node_count=1),
            'operational': Mock(insert_count=1, delete_count=0, search_count=0, rotation_count=0, rebalance_count=0)
        }
        
        report = reporter.generate_report(profiles, metrics, "text")
        
        assert isinstance(report, str)
        assert "PERFORMANCE REPORT" in report
        
    def test_generate_json_report(self):
        """Test de génération de rapport JSON."""
        reporter = PerformanceReporter()
        
        profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'success': True, 'timestamp': time.time()}
        ]
        
        metrics = {}
        
        report = reporter.generate_report(profiles, metrics, "json")
        
        assert isinstance(report, str)
        import json
        parsed_report = json.loads(report)
        assert 'report_info' in parsed_report
        assert 'profiles' in parsed_report
        
    def test_generate_html_report(self):
        """Test de génération de rapport HTML."""
        reporter = PerformanceReporter()
        
        profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'success': True, 'timestamp': time.time()}
        ]
        
        metrics = {}
        
        report = reporter.generate_report(profiles, metrics, "html")
        
        assert isinstance(report, str)
        assert "<!DOCTYPE html>" in report
        assert "<html>" in report
        
    def test_export_csv_data(self):
        """Test d'export CSV."""
        reporter = PerformanceReporter()
        
        profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'memory_delta': 100, 'success': True, 'timestamp': time.time()}
        ]
        
        metrics = {}
        
        data = reporter.export_data(profiles, metrics, "csv")
        
        assert isinstance(data, str)
        assert "operation,execution_time" in data
        
    def test_export_xml_data(self):
        """Test d'export XML."""
        reporter = PerformanceReporter()
        
        profiles = [
            {'operation': 'test', 'execution_time': 0.1, 'success': True, 'timestamp': time.time()}
        ]
        
        metrics = {}
        
        data = reporter.export_data(profiles, metrics, "xml")
        
        assert isinstance(data, str)
        assert "<performance_report>" in data
        
    def test_unsupported_format(self):
        """Test d'erreur pour format non supporté."""
        reporter = PerformanceReporter()
        
        profiles = []
        metrics = {}
        
        with pytest.raises(ValueError, match="Unsupported format"):
            reporter.generate_report(profiles, metrics, "unsupported")


class TestPerformanceMonitor:
    """Tests pour la classe PerformanceMonitor."""
    
    def test_monitor_creation(self):
        """Test de création du moniteur."""
        monitor = PerformanceMonitor()
        assert monitor is not None
        
    def test_configure(self):
        """Test de configuration du moniteur."""
        monitor = PerformanceMonitor()
        
        config = {
            'sampling_interval': 2.0,
            'buffer_size': 500,
            'adaptive_monitoring': True
        }
        
        monitor.configure(config)
        
        assert monitor._config['sampling_interval'] == 2.0
        assert monitor._config['buffer_size'] == 500
        assert monitor._config['adaptive_monitoring'] is True
        
    def test_start_stop_monitoring(self):
        """Test de démarrage/arrêt du monitoring."""
        monitor = PerformanceMonitor()
        
        monitor.start_monitoring()
        assert monitor._monitoring is True
        
        time.sleep(0.1)
        
        monitor.stop_monitoring()
        assert monitor._monitoring is False
        
    def test_start_monitoring_already_running(self):
        """Test d'erreur si monitoring déjà en cours."""
        monitor = PerformanceMonitor()
        
        monitor.start_monitoring()
        
        with pytest.raises(RuntimeError, match="Monitoring is already running"):
            monitor.start_monitoring()
            
        monitor.stop_monitoring()
        
    def test_stop_monitoring_not_running(self):
        """Test d'erreur si monitoring pas en cours."""
        monitor = PerformanceMonitor()
        
        with pytest.raises(RuntimeError, match="Monitoring is not running"):
            monitor.stop_monitoring()
            
    def test_set_alerts(self):
        """Test de configuration des alertes."""
        monitor = PerformanceMonitor()
        
        alerts = [
            {
                'metric': 'cpu_percent',
                'threshold': 80.0,
                'condition': 'greater_than',
                'action': 'log',
                'enabled': True
            }
        ]
        
        monitor.set_alerts(alerts)
        
        assert len(monitor._alerts) == 1
        assert monitor._alerts[0].metric == 'cpu_percent'
        assert monitor._alerts[0].threshold == 80.0
        
    def test_add_remove_alert(self):
        """Test d'ajout/suppression d'alerte."""
        monitor = PerformanceMonitor()
        
        alert = Mock()
        alert.metric = 'test_metric'
        alert.threshold = 50.0
        
        monitor.add_alert(alert)
        assert len(monitor._alerts) == 1
        
        removed = monitor.remove_alert('test_metric', 50.0)
        assert removed is True
        assert len(monitor._alerts) == 0
        
    def test_get_current_metrics(self):
        """Test d'obtention des métriques actuelles."""
        monitor = PerformanceMonitor()
        
        metrics = monitor.get_current_metrics()
        
        assert 'timestamp' in metrics
        assert 'cpu_percent' in metrics
        assert 'memory_percent' in metrics
        
    def test_get_performance_summary(self):
        """Test d'obtention du résumé de performance."""
        monitor = PerformanceMonitor()
        
        # Ajouter quelques métriques au buffer
        monitor._metrics_buffer.append({
            'timestamp': time.time(),
            'cpu_percent': 50,
            'memory_percent': 60
        })
        
        summary = monitor.get_performance_summary()
        
        assert 'monitoring_duration' in summary
        assert 'total_samples' in summary
        assert 'cpu_stats' in summary
        assert 'memory_stats' in summary
        assert 'monitoring_status' in summary


class TestPerformanceVisualizer:
    """Tests pour la classe PerformanceVisualizer."""
    
    def test_visualizer_creation(self):
        """Test de création du visualiseur."""
        visualizer = PerformanceVisualizer()
        assert visualizer is not None
        
    def test_create_visualization_line_chart(self):
        """Test de création de graphique en ligne."""
        visualizer = PerformanceVisualizer()
        
        profiles = [
            {'execution_time': 0.1, 'operation': 'test', 'timestamp': time.time()},
            {'execution_time': 0.2, 'operation': 'test', 'timestamp': time.time()}
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            visualizer.create_visualization(profiles, "execution_time", "test.html", "line")
            mock_file.assert_called_once_with("test.html", 'w', encoding='utf-8')
            
    def test_create_visualization_bar_chart(self):
        """Test de création de graphique en barres."""
        visualizer = PerformanceVisualizer()
        
        profiles = [
            {'execution_time': 0.1, 'operation': 'insert'},
            {'execution_time': 0.2, 'operation': 'delete'},
            {'execution_time': 0.15, 'operation': 'search'}
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            visualizer.create_visualization(profiles, "execution_time", "test.html", "bar")
            mock_file.assert_called_once_with("test.html", 'w', encoding='utf-8')
            
    def test_create_visualization_scatter_chart(self):
        """Test de création de graphique en nuage de points."""
        visualizer = PerformanceVisualizer()
        
        profiles = [
            {'execution_time': 0.1, 'operation': 'test', 'timestamp': time.time()},
            {'execution_time': 0.2, 'operation': 'test', 'timestamp': time.time()}
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            visualizer.create_visualization(profiles, "execution_time", "test.html", "scatter")
            mock_file.assert_called_once_with("test.html", 'w', encoding='utf-8')
            
    def test_create_visualization_histogram(self):
        """Test de création d'histogramme."""
        visualizer = PerformanceVisualizer()
        
        profiles = [
            {'execution_time': 0.1, 'operation': 'test'},
            {'execution_time': 0.2, 'operation': 'test'},
            {'execution_time': 0.15, 'operation': 'test'}
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            visualizer.create_visualization(profiles, "execution_time", "test.html", "histogram")
            mock_file.assert_called_once_with("test.html", 'w', encoding='utf-8')
            
    def test_create_visualization_unsupported_type(self):
        """Test d'erreur pour type de graphique non supporté."""
        visualizer = PerformanceVisualizer()
        
        profiles = [{'execution_time': 0.1}]
        
        with pytest.raises(ValueError, match="Unsupported chart type"):
            visualizer.create_visualization(profiles, "execution_time", "test.html", "unsupported")
            
    def test_create_summary_chart(self):
        """Test de création de graphique de résumé."""
        visualizer = PerformanceVisualizer()
        
        profiles = [
            {'operation': 'insert', 'execution_time': 0.1, 'success': True},
            {'operation': 'delete', 'execution_time': 0.2, 'success': True}
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            visualizer.create_summary_chart(profiles, "summary.html")
            mock_file.assert_called_once_with("summary.html", 'w', encoding='utf-8')
            
    def test_export_chart_data_csv(self):
        """Test d'export de données CSV."""
        visualizer = PerformanceVisualizer()
        
        profiles = [
            {'execution_time': 0.1, 'operation': 'test', 'timestamp': time.time()}
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            visualizer.export_chart_data(profiles, "execution_time", "data.csv", "csv")
            mock_file.assert_called_once_with("data.csv", 'w', newline='', encoding='utf-8')
            
    def test_export_chart_data_json(self):
        """Test d'export de données JSON."""
        visualizer = PerformanceVisualizer()
        
        profiles = [
            {'execution_time': 0.1, 'operation': 'test', 'timestamp': time.time()}
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            visualizer.export_chart_data(profiles, "execution_time", "data.json", "json")
            mock_file.assert_called_once_with("data.json", 'w', encoding='utf-8')
            
    def test_export_chart_data_unsupported_format(self):
        """Test d'erreur pour format d'export non supporté."""
        visualizer = PerformanceVisualizer()
        
        profiles = [{'execution_time': 0.1}]
        
        with pytest.raises(ValueError, match="Unsupported export format"):
            visualizer.export_chart_data(profiles, "execution_time", "data.txt", "txt")


def mock_open():
    """Mock pour la fonction open."""
    return MagicMock()


if __name__ == "__main__":
    pytest.main([__file__])