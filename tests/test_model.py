"""
Unit tests for the bioluminescent detection AI model.

This module contains comprehensive tests for all model components including
prediction, calibration, validation, and deployment functionality.
"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch

# Import the model components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bioluminescence_model import BioluminescenceModel, ModelParameters
from validation import ModelValidator, TestCondition
from deployment_controller import DeploymentController, EnvironmentalConditions

class TestModelParameters(unittest.TestCase):
    """Test ModelParameters dataclass."""
    
    def test_default_parameters(self):
        """Test that default parameters are set correctly."""
        params = ModelParameters()
        
        self.assertEqual(params.I0, 10.0)
        self.assertEqual(params.A, 0.015)
        self.assertEqual(params.Ea, 50000)
        self.assertEqual(params.alpha0, 0.002)
        self.assertEqual(params.gamma, 1.5)
        
        # Test sensor constants
        expected_sensors = {'human': 0.001, 'drone': 0.005, 'nvg': 0.0005}
        self.assertEqual(params.k_sensor, expected_sensors)
    
    def test_custom_parameters(self):
        """Test custom parameter initialization."""
        custom_sensors = {'custom': 0.003}
        params = ModelParameters(I0=12.0, A=0.02, k_sensor=custom_sensors)
        
        self.assertEqual(params.I0, 12.0)
        self.assertEqual(params.A, 0.02)
        self.assertEqual(params.k_sensor, custom_sensors)

class TestBioluminescenceModel(unittest.TestCase):
    """Test the main bioluminescence model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = BioluminescenceModel()
    
    def test_light_decay(self):
        """Test light decay calculation."""
        # Test at different times and temperatures
        intensity_1 = self.model.light_decay(t=0, T=10)
        intensity_2 = self.model.light_decay(t=60, T=10)
        intensity_3 = self.model.light_decay(t=60, T=20)
        
        # Initial intensity should be I0
        self.assertAlmostEqual(intensity_1, 10.0, places=1)
        
        # Intensity should decrease with time
        self.assertLess(intensity_2, intensity_1)
        
        # Higher temperature should cause faster decay
        self.assertLess(intensity_3, intensity_2)
        
        # Intensity should never be negative
        self.assertGreaterEqual(intensity_1, 0)
        self.assertGreaterEqual(intensity_2, 0)
        self.assertGreaterEqual(intensity_3, 0)
    
    def test_environmental_attenuation(self):
        """Test environmental attenuation calculation."""
        # Test calm conditions
        c_calm = self.model.environmental_attenuation(Uw=1.0, P=0.0, Hs=0.1)
        
        # Test stormy conditions
        c_storm = self.model.environmental_attenuation(Uw=15.0, P=20.0, Hs=3.0)
        
        # Stormy conditions should have higher attenuation
        self.assertGreater(c_storm, c_calm)
        
        # Attenuation should never be below minimum
        self.assertGreaterEqual(c_calm, 0.001)
        self.assertGreaterEqual(c_storm, 0.001)
    
    def test_detection_threshold(self):
        """Test detection threshold calculation."""
        # Test different sensor types
        threshold_human = self.model.detection_threshold(I_ambient=0.001, sensor_type='human')
        threshold_drone = self.model.detection_threshold(I_ambient=0.001, sensor_type='drone')
        threshold_nvg = self.model.detection_threshold(I_ambient=0.001, sensor_type='nvg')
        
        # NVG should be most sensitive (lowest threshold)
        self.assertLess(threshold_nvg, threshold_human)
        self.assertLess(threshold_human, threshold_drone)
        
        # Threshold should increase with ambient light
        threshold_bright = self.model.detection_threshold(I_ambient=0.1, sensor_type='drone')
        self.assertGreater(threshold_bright, threshold_drone)
        
        # Threshold should never be below minimum
        self.assertGreaterEqual(threshold_human, 0.0001)
        self.assertGreaterEqual(threshold_drone, 0.0001)
        self.assertGreaterEqual(threshold_nvg, 0.0001)
    
    def test_max_distance(self):
        """Test maximum distance calculation."""
        # Test case where detection is possible
        distance = self.model.max_distance(I_current=1.0, I_threshold=0.1, c=0.01)
        self.assertGreater(distance, 0)
        
        # Test case where detection is impossible
        distance_zero = self.model.max_distance(I_current=0.05, I_threshold=0.1, c=0.01)
        self.assertEqual(distance_zero, 0.0)
        
        # Test physical limits
        distance_limit = self.model.max_distance(I_current=1000.0, I_threshold=0.1, c=0.0001)
        self.assertLessEqual(distance_limit, 10000.0)
    
    def test_predict(self):
        """Test complete prediction functionality."""
        result = self.model.predict(
            activation_time=45,
            water_temp=8.5,
            wind_speed=5.2,
            precipitation=2.4,
            wave_height=1.2,
            ambient_light=0.002,
            sensor_type='drone'
        )
        
        # Check result structure
        required_keys = ['distance', 'confidence_interval', 'performance_score', 
                        'system_conditions', 'failure_flags', 'validation_status']
        for key in required_keys:
            self.assertIn(key, result)
        
        # Check data types
        self.assertIsInstance(result['distance'], (int, float))
        self.assertIsInstance(result['confidence_interval'], list)
        self.assertEqual(len(result['confidence_interval']), 3)
        self.assertIsInstance(result['performance_score'], (int, float))
        self.assertIsInstance(result['system_conditions'], list)
        self.assertIsInstance(result['failure_flags'], list)
        
        # Check value ranges
        self.assertGreaterEqual(result['distance'], 0)
        self.assertLessEqual(result['performance_score'], 100)
        self.assertGreaterEqual(result['performance_score'], 0)
        
        # Check confidence interval ordering
        ci = result['confidence_interval']
        self.assertLessEqual(ci[0], ci[1])
        self.assertLessEqual(ci[1], ci[2])
    
    def test_calibrate_parameters(self):
        """Test parameter calibration."""
        # Create synthetic field data
        field_data = pd.DataFrame({
            'actual_distance': [100, 200, 150, 300, 250],
            'activation_time': [30, 60, 45, 90, 75],
            'water_temp': [10, 15, 12, 8, 20],
            'wind_speed': [2, 5, 3, 8, 1],
            'precipitation': [0, 2, 1, 5, 0],
            'wave_height': [0.2, 0.8, 0.5, 1.5, 0.1],
            'ambient_light': [0.001, 0.005, 0.003, 0.002, 0.004],
            'sensor_type': ['drone', 'drone', 'drone', 'drone', 'drone']
        })
        
        # Perform calibration
        optimized_params = self.model.calibrate_parameters(field_data)
        
        # Check that parameters were optimized
        self.assertIsInstance(optimized_params, dict)
        self.assertIn('I0', optimized_params)
        self.assertIn('A', optimized_params)
        self.assertIn('Ea', optimized_params)
        
        # Check that calibration history was updated
        self.assertGreater(len(self.model.calibration_history), 0)
        
        # Check that model parameters were updated
        self.assertEqual(self.model.params.I0, optimized_params['I0'])
        self.assertEqual(self.model.params.A, optimized_params['A'])
    
    def test_add_validation_data(self):
        """Test adding validation data for continuous learning."""
        initial_count = len(self.model.validation_data)
        
        # Add validation data
        validation_data = {
            'actual_distance': 150.0,
            'activation_time': 60.0,
            'water_temp': 12.0,
            'wind_speed': 4.0,
            'precipitation': 1.0,
            'wave_height': 0.5,
            'ambient_light': 0.003,
            'sensor_type': 'drone'
        }
        
        self.model.add_validation_data(validation_data)
        
        # Check that data was added
        self.assertEqual(len(self.model.validation_data), initial_count + 1)
        self.assertEqual(self.model.validation_data[-1], validation_data)
    
    def test_get_model_info(self):
        """Test model information retrieval."""
        info = self.model.get_model_info()
        
        # Check structure
        required_keys = ['parameters', 'calibration_history', 'validation_data_count', 'model_version']
        for key in required_keys:
            self.assertIn(key, info)
        
        # Check parameter structure
        params = info['parameters']
        self.assertIn('I0', params)
        self.assertIn('A', params)
        self.assertIn('Ea', params)
        self.assertIn('k_sensor', params)
        
        # Check data types
        self.assertIsInstance(info['calibration_history'], list)
        self.assertIsInstance(info['validation_data_count'], int)
        self.assertIsInstance(info['model_version'], str)

class TestModelValidator(unittest.TestCase):
    """Test the model validation system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = BioluminescenceModel()
        self.validator = ModelValidator(self.model)
    
    def test_test_conditions(self):
        """Test that test conditions are properly defined."""
        conditions = self.validator.test_conditions
        
        # Check that all required conditions are present
        condition_names = [c.name for c in conditions]
        expected_conditions = ['Calm', 'Windy', 'Rainy', 'Storm', 'Cold']
        
        for expected in expected_conditions:
            self.assertIn(expected, condition_names)
        
        # Check condition structure
        for condition in conditions:
            self.assertIsInstance(condition.wind_speed, tuple)
            self.assertIsInstance(condition.precipitation, tuple)
            self.assertIsInstance(condition.wave_height, tuple)
            self.assertIsInstance(condition.water_temp, float)
            self.assertIsInstance(condition.replicates, int)
            self.assertIsInstance(condition.description, str)
    
    def test_validation_tests(self):
        """Test validation test execution."""
        # Run validation tests with simulated data
        report = self.validator.run_validation_tests()
        
        # Check report structure
        required_keys = ['validation_metrics', 'condition_metrics', 'test_summary', 
                        'performance_assessment', 'recommendations']
        for key in required_keys:
            self.assertIn(key, report)
        
        # Check metrics
        metrics = report['validation_metrics']
        self.assertIn('MAE', metrics)
        self.assertIn('MAPE', metrics)
        self.assertIn('R2', metrics)
        self.assertIn('Coverage', metrics)
        self.assertIn('Operational_Accuracy', metrics)
        
        # Check that tests were run
        self.assertGreater(len(self.validator.test_results), 0)
        
        # Check performance assessment
        assessment = report['performance_assessment']
        self.assertIn('overall_grade', assessment)
        self.assertIn('strengths', assessment)
        self.assertIn('weaknesses', assessment)
    
    def test_validation_summary(self):
        """Test validation summary generation."""
        # Run some tests first
        self.validator.run_validation_tests()
        
        summary = self.validator.get_validation_summary()
        
        # Check summary structure
        self.assertIn('status', summary)
        self.assertIn('total_tests', summary)
        self.assertIn('conditions_tested', summary)
        
        # Check that summary reflects test execution
        self.assertEqual(summary['status'], 'Validation completed')
        self.assertGreater(summary['total_tests'], 0)

class TestDeploymentController(unittest.TestCase):
    """Test the deployment controller."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = BioluminescenceModel()
        self.controller = DeploymentController(self.model)
    
    def test_initialization(self):
        """Test controller initialization."""
        self.assertEqual(self.controller.model, self.model)
        self.assertIsNone(self.controller.drone_api)
        self.assertEqual(self.controller.search_altitude, 50.0)
        self.assertEqual(self.controller.search_speed, 5.0)
        self.assertEqual(self.controller.camera_fov, 60.0)
        self.assertEqual(self.controller.detection_interval, 2.0)
    
    def test_set_mission_parameters(self):
        """Test mission parameter setting."""
        self.controller.set_mission_parameters(
            search_altitude=75.0,
            search_speed=8.0,
            camera_fov=45.0,
            detection_interval=1.5
        )
        
        self.assertEqual(self.controller.search_altitude, 75.0)
        self.assertEqual(self.controller.search_speed, 8.0)
        self.assertEqual(self.controller.camera_fov, 45.0)
        self.assertEqual(self.controller.detection_interval, 1.5)
    
    def test_calculate_optimal_range(self):
        """Test optimal range calculation."""
        env_conditions = EnvironmentalConditions(
            wind_speed=6.5,
            wind_direction=180.0,
            precipitation=1.2,
            wave_height=0.8,
            water_temp=12.0,
            ambient_light=0.003,
            timestamp=1234567890.0
        )
        
        distance = self.controller._calculate_optimal_range(env_conditions, 90.0)
        
        self.assertIsInstance(distance, (int, float))
        self.assertGreaterEqual(distance, 0)
    
    def test_generate_search_pattern(self):
        """Test search pattern generation."""
        center = (47.6062, -122.3321)
        max_distance = 500.0
        search_radius = 1000.0
        
        waypoints = self.controller._generate_search_pattern(center, max_distance, search_radius)
        
        self.assertIsInstance(waypoints, list)
        self.assertGreater(len(waypoints), 0)
        
        # Check waypoint structure
        for waypoint in waypoints:
            self.assertIn('latitude', waypoint)
            self.assertIn('longitude', waypoint)
            self.assertIn('altitude', waypoint)
            self.assertIn('speed', waypoint)
            self.assertIn('action', waypoint)
            
            # Check coordinate ranges
            self.assertGreaterEqual(waypoint['latitude'], -90)
            self.assertLessEqual(waypoint['latitude'], 90)
            self.assertGreaterEqual(waypoint['longitude'], -180)
            self.assertLessEqual(waypoint['longitude'], 180)
    
    def test_simulate_search_mission(self):
        """Test simulated search mission."""
        waypoints = [
            {'latitude': 47.6062, 'longitude': -122.3321, 'altitude': 50.0, 'speed': 5.0, 'action': 'search'},
            {'latitude': 47.6063, 'longitude': -122.3322, 'altitude': 50.0, 'speed': 5.0, 'action': 'search'}
        ]
        
        results = self.controller._simulate_search_mission(waypoints)
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(waypoints))
        
        # Check result structure
        for result in results:
            self.assertIsInstance(result.detected, bool)
            self.assertIsInstance(result.confidence, float)
            self.assertIsInstance(result.distance, float)
            self.assertIsInstance(result.bearing, float)
            self.assertIsInstance(result.timestamp, float)
            
            # Check value ranges
            self.assertGreaterEqual(result.confidence, 0)
            self.assertLessEqual(result.confidence, 1)
            self.assertGreaterEqual(result.distance, 0)
            self.assertGreaterEqual(result.bearing, 0)
            self.assertLessEqual(result.bearing, 360)
    
    def test_mission_statistics(self):
        """Test mission statistics generation."""
        stats = self.controller.get_mission_statistics()
        
        self.assertIn('total_missions', stats)
        self.assertIn('total_detections', stats)
        self.assertIn('success_rate', stats)
        self.assertIn('avg_prediction_accuracy', stats)
        self.assertIn('model_info', stats)
        
        # Check data types
        self.assertIsInstance(stats['total_missions'], int)
        self.assertIsInstance(stats['total_detections'], int)
        self.assertIsInstance(stats['success_rate'], float)
        self.assertIsInstance(stats['avg_prediction_accuracy'], float)

if __name__ == '__main__':
    unittest.main() 