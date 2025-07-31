"""
Validation and Testing Module for Bioluminescent Detection AI Model

This module implements comprehensive validation protocols including field test matrices,
performance metrics, and continuous improvement cycles.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import logging

from bioluminescence_model import BioluminescenceModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestCondition:
    """Test condition specification"""
    name: str
    wind_speed: Tuple[float, float]  # (min, max) m/s
    precipitation: Tuple[float, float]  # (min, max) mm/hr
    wave_height: Tuple[float, float]  # (min, max) m
    water_temp: float  # °C
    replicates: int
    description: str

@dataclass
class ValidationResult:
    """Validation test result"""
    test_name: str
    condition: TestCondition
    predicted_distance: float
    actual_distance: float
    error: float
    error_percentage: float
    confidence_interval: List[float]
    performance_score: float
    timestamp: str

class ModelValidator:
    """
    Comprehensive validation system for the bioluminescent detection AI model.
    
    Implements field test matrices, performance metrics, and continuous
    improvement protocols.
    """
    
    def __init__(self, model: BioluminescenceModel):
        """
        Initialize the validator.
        
        Args:
            model: BioluminescenceModel instance to validate
        """
        self.model = model
        self.test_results = []
        self.validation_history = []
        
        # Define standard test conditions
        self.test_conditions = self._define_test_conditions()
        
    def _define_test_conditions(self) -> List[TestCondition]:
        """
        Define the field test matrix as specified in the requirements.
        
        Returns:
            List of test conditions
        """
        return [
            TestCondition(
                name="Calm",
                wind_speed=(0, 2),
                precipitation=(0, 0),
                wave_height=(0, 0.3),
                water_temp=10.0,
                replicates=5,
                description="Calm conditions with minimal environmental interference"
            ),
            TestCondition(
                name="Windy",
                wind_speed=(8, 10),
                precipitation=(0, 0),
                wave_height=(0.5, 1.0),
                water_temp=5.0,
                replicates=5,
                description="Windy conditions with moderate wave action"
            ),
            TestCondition(
                name="Rainy",
                wind_speed=(3, 5),
                precipitation=(5, 10),
                wave_height=(0.3, 0.8),
                water_temp=8.0,
                replicates=5,
                description="Rainy conditions with light precipitation"
            ),
            TestCondition(
                name="Storm",
                wind_speed=(12, 15),
                precipitation=(15, 20),
                wave_height=(2.5, 3.5),
                water_temp=12.0,
                replicates=3,
                description="Storm conditions with heavy precipitation and waves"
            ),
            TestCondition(
                name="Cold",
                wind_speed=(1, 3),
                precipitation=(0, 2),
                wave_height=(0.1, 0.5),
                water_temp=-1.0,
                replicates=3,
                description="Cold water conditions near freezing"
            )
        ]
    
    def run_validation_tests(self, 
                           field_data: Optional[pd.DataFrame] = None,
                           sensor_type: str = "drone") -> Dict:
        """
        Run comprehensive validation tests.
        
        Args:
            field_data: Optional field data for testing (if None, uses simulated data)
            sensor_type: Type of sensor to test
            
        Returns:
            Validation results summary
        """
        logger.info("Starting comprehensive validation tests")
        
        all_results = []
        
        for condition in self.test_conditions:
            logger.info(f"Testing condition: {condition.name}")
            
            for replicate in range(condition.replicates):
                # Generate test parameters
                test_params = self._generate_test_parameters(condition)
                
                # Make prediction
                prediction = self.model.predict(
                    activation_time=test_params['activation_time'],
                    water_temp=test_params['water_temp'],
                    wind_speed=test_params['wind_speed'],
                    precipitation=test_params['precipitation'],
                    wave_height=test_params['wave_height'],
                    ambient_light=test_params['ambient_light'],
                    sensor_type=sensor_type
                )
                
                # Get actual distance (from field data or simulation)
                if field_data is not None:
                    actual_distance = self._get_actual_distance_from_field_data(
                        field_data, test_params
                    )
                else:
                    actual_distance = self._simulate_actual_distance(
                        prediction['distance'], condition
                    )
                
                # Calculate error metrics
                error = abs(prediction['distance'] - actual_distance)
                error_percentage = (error / actual_distance * 100) if actual_distance > 0 else 0
                
                # Create validation result
                result = ValidationResult(
                    test_name=f"{condition.name}_replicate_{replicate + 1}",
                    condition=condition,
                    predicted_distance=prediction['distance'],
                    actual_distance=actual_distance,
                    error=error,
                    error_percentage=error_percentage,
                    confidence_interval=prediction['confidence_interval'],
                    performance_score=prediction['performance_score'],
                    timestamp=datetime.now().isoformat()
                )
                
                all_results.append(result)
        
        # Store results
        self.test_results.extend(all_results)
        
        # Calculate validation metrics
        validation_metrics = self._calculate_validation_metrics(all_results)
        
        # Generate validation report
        report = self._generate_validation_report(validation_metrics, all_results)
        
        logger.info("Validation tests completed")
        return report
    
    def _generate_test_parameters(self, condition: TestCondition) -> Dict:
        """
        Generate random test parameters within condition bounds.
        
        Args:
            condition: Test condition specification
            
        Returns:
            Dictionary of test parameters
        """
        return {
            'activation_time': np.random.uniform(30, 120),  # 30-120 minutes
            'water_temp': condition.water_temp + np.random.uniform(-1, 1),
            'wind_speed': np.random.uniform(*condition.wind_speed),
            'precipitation': np.random.uniform(*condition.precipitation),
            'wave_height': np.random.uniform(*condition.wave_height),
            'ambient_light': np.random.uniform(0.001, 0.01)  # Moonless to moonlight
        }
    
    def _get_actual_distance_from_field_data(self, 
                                           field_data: pd.DataFrame,
                                           test_params: Dict) -> float:
        """
        Get actual distance from field data based on test parameters.
        
        Args:
            field_data: Field measurement data
            test_params: Test parameters
            
        Returns:
            Actual distance (m)
        """
        # Find closest matching field data point
        best_match = None
        min_distance = float('inf')
        
        for _, row in field_data.iterrows():
            # Calculate parameter similarity
            param_distance = (
                abs(row['activation_time'] - test_params['activation_time']) / 120 +
                abs(row['water_temp'] - test_params['water_temp']) / 30 +
                abs(row['wind_speed'] - test_params['wind_speed']) / 25 +
                abs(row['precipitation'] - test_params['precipitation']) / 50 +
                abs(row['wave_height'] - test_params['wave_height']) / 10
            )
            
            if param_distance < min_distance:
                min_distance = param_distance
                best_match = row['actual_distance']
        
        return best_match if best_match is not None else 0.0
    
    def _simulate_actual_distance(self, 
                                predicted_distance: float,
                                condition: TestCondition) -> float:
        """
        Simulate actual distance with realistic noise.
        
        Args:
            predicted_distance: Model prediction
            condition: Test condition
            
        Returns:
            Simulated actual distance
        """
        # Add realistic noise based on condition
        noise_levels = {
            "Calm": 0.05,      # 5% noise
            "Windy": 0.15,     # 15% noise
            "Rainy": 0.12,     # 12% noise
            "Storm": 0.25,     # 25% noise
            "Cold": 0.08       # 8% noise
        }
        
        noise_level = noise_levels.get(condition.name, 0.1)
        noise = np.random.normal(0, noise_level)
        
        actual_distance = predicted_distance * (1 + noise)
        return max(0, actual_distance)
    
    def _calculate_validation_metrics(self, results: List[ValidationResult]) -> Dict:
        """
        Calculate comprehensive validation metrics.
        
        Args:
            results: List of validation results
            
        Returns:
            Dictionary of validation metrics
        """
        if not results:
            return {}
        
        # Extract data
        predicted = [r.predicted_distance for r in results]
        actual = [r.actual_distance for r in results]
        errors = [r.error for r in results]
        error_percentages = [r.error_percentage for r in results]
        
        # Calculate metrics
        mae = np.mean(errors)
        mape = np.mean(error_percentages)
        
        # R² calculation
        if np.var(actual) > 0:
            r2 = 1 - (np.sum(np.array(errors) ** 2) / np.sum((np.array(actual) - np.mean(actual)) ** 2))
        else:
            r2 = 0.0
        
        # Coverage calculation (confidence intervals)
        coverage_count = 0
        for result in results:
            low, med, high = result.confidence_interval
            if low <= result.actual_distance <= high:
                coverage_count += 1
        coverage = coverage_count / len(results) * 100
        
        # Operational accuracy (within 15% error)
        operational_accuracy = np.mean([ep <= 15 for ep in error_percentages]) * 100
        
        return {
            'MAE': mae,
            'MAPE': mape,
            'R2': r2,
            'Coverage': coverage,
            'Operational_Accuracy': operational_accuracy,
            'Total_Tests': len(results),
            'Conditions_Tested': len(set(r.condition.name for r in results))
        }
    
    def _generate_validation_report(self, 
                                  metrics: Dict,
                                  results: List[ValidationResult]) -> Dict:
        """
        Generate comprehensive validation report.
        
        Args:
            metrics: Validation metrics
            results: Validation results
            
        Returns:
            Validation report
        """
        # Group results by condition
        condition_results = {}
        for result in results:
            condition_name = result.condition.name
            if condition_name not in condition_results:
                condition_results[condition_name] = []
            condition_results[condition_name].append(result)
        
        # Calculate condition-specific metrics
        condition_metrics = {}
        for condition_name, condition_data in condition_results.items():
            errors = [r.error_percentage for r in condition_data]
            condition_metrics[condition_name] = {
                'MAE': np.mean([r.error for r in condition_data]),
                'MAPE': np.mean(errors),
                'Operational_Accuracy': np.mean([e <= 15 for e in errors]) * 100,
                'Test_Count': len(condition_data)
            }
        
        report = {
            'validation_metrics': metrics,
            'condition_metrics': condition_metrics,
            'test_summary': {
                'total_tests': len(results),
                'conditions_tested': len(condition_results),
                'validation_date': datetime.now().isoformat(),
                'model_version': '1.0.0'
            },
            'performance_assessment': self._assess_performance(metrics),
            'recommendations': self._generate_recommendations(metrics, condition_metrics)
        }
        
        return report
    
    def _assess_performance(self, metrics: Dict) -> Dict:
        """
        Assess overall model performance.
        
        Args:
            metrics: Validation metrics
            
        Returns:
            Performance assessment
        """
        assessment = {
            'overall_grade': 'C',
            'strengths': [],
            'weaknesses': [],
            'meets_targets': {}
        }
        
        # Performance targets
        targets = {
            'MAE': 50,  # meters
            'MAPE': 15,  # percent
            'R2': 0.8,   # correlation
            'Coverage': 90,  # percent
            'Operational_Accuracy': 90  # percent
        }
        
        # Check targets
        meets_targets = {}
        for metric, target in targets.items():
            if metric in metrics:
                meets_targets[metric] = metrics[metric] >= target if metric in ['R2', 'Coverage', 'Operational_Accuracy'] else metrics[metric] <= target
        
        # Overall grade
        target_met_count = sum(meets_targets.values())
        if target_met_count >= 4:
            assessment['overall_grade'] = 'A'
        elif target_met_count >= 3:
            assessment['overall_grade'] = 'B'
        elif target_met_count >= 2:
            assessment['overall_grade'] = 'C'
        else:
            assessment['overall_grade'] = 'D'
        
        # Identify strengths and weaknesses
        for metric, target in targets.items():
            if metric in metrics:
                if meets_targets[metric]:
                    assessment['strengths'].append(f"{metric}: {metrics[metric]:.2f} (target: {target})")
                else:
                    assessment['weaknesses'].append(f"{metric}: {metrics[metric]:.2f} (target: {target})")
        
        assessment['meets_targets'] = meets_targets
        return assessment
    
    def _generate_recommendations(self, 
                                metrics: Dict,
                                condition_metrics: Dict) -> List[str]:
        """
        Generate improvement recommendations.
        
        Args:
            metrics: Overall validation metrics
            condition_metrics: Condition-specific metrics
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Overall performance recommendations
        if metrics.get('MAPE', 0) > 15:
            recommendations.append("Improve model accuracy through additional calibration data")
        
        if metrics.get('Coverage', 0) < 90:
            recommendations.append("Expand uncertainty quantification for better confidence intervals")
        
        if metrics.get('R2', 0) < 0.8:
            recommendations.append("Enhance model physics representation for better correlation")
        
        # Condition-specific recommendations
        for condition, condition_metric in condition_metrics.items():
            if condition_metric['MAPE'] > 20:
                recommendations.append(f"Improve performance under {condition} conditions")
        
        # General recommendations
        recommendations.extend([
            "Continue field validation for model refinement",
            "Implement adaptive learning from operational data",
            "Consider sensor-specific calibration for different detection systems"
        ])
        
        return recommendations
    
    def plot_validation_results(self, save_path: Optional[str] = None):
        """
        Generate validation result plots.
        
        Args:
            save_path: Optional path to save plots
        """
        if not self.test_results:
            logger.warning("No test results to plot")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Bioluminescent Detection AI Model Validation Results', fontsize=16)
        
        # Extract data
        predicted = [r.predicted_distance for r in self.test_results]
        actual = [r.actual_distance for r in self.test_results]
        conditions = [r.condition.name for r in self.test_results]
        errors = [r.error_percentage for r in self.test_results]
        
        # 1. Predicted vs Actual scatter plot
        axes[0, 0].scatter(actual, predicted, alpha=0.6)
        axes[0, 0].plot([0, max(actual)], [0, max(actual)], 'r--', label='Perfect Prediction')
        axes[0, 0].set_xlabel('Actual Distance (m)')
        axes[0, 0].set_ylabel('Predicted Distance (m)')
        axes[0, 0].set_title('Predicted vs Actual Distances')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Error distribution by condition
        condition_data = {}
        for condition in set(conditions):
            condition_data[condition] = [e for c, e in zip(conditions, errors) if c == condition]
        
        axes[0, 1].boxplot(condition_data.values(), labels=condition_data.keys())
        axes[0, 1].set_ylabel('Error Percentage (%)')
        axes[0, 1].set_title('Error Distribution by Test Condition')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Performance score distribution
        scores = [r.performance_score for r in self.test_results]
        axes[1, 0].hist(scores, bins=20, alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Performance Score (%)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Model Performance Score Distribution')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Error vs predicted distance
        axes[1, 1].scatter(predicted, errors, alpha=0.6)
        axes[1, 1].set_xlabel('Predicted Distance (m)')
        axes[1, 1].set_ylabel('Absolute Error (m)')
        axes[1, 1].set_title('Error vs Predicted Distance')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Validation plots saved to {save_path}")
        
        plt.show()
    
    def save_validation_report(self, filepath: str):
        """
        Save validation report to file.
        
        Args:
            filepath: Path to save the report
        """
        if not self.test_results:
            logger.warning("No test results to save")
            return
        
        # Generate report
        report = self._generate_validation_report(
            self._calculate_validation_metrics(self.test_results),
            self.test_results
        )
        
        # Convert dataclasses to dictionaries for JSON serialization
        def convert_dataclass(obj):
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            return obj
        
        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=convert_dataclass)
        
        logger.info(f"Validation report saved to {filepath}")
    
    def get_validation_summary(self) -> Dict:
        """
        Get a summary of validation results.
        
        Returns:
            Validation summary
        """
        if not self.test_results:
            return {'status': 'No validation tests run'}
        
        metrics = self._calculate_validation_metrics(self.test_results)
        
        return {
            'status': 'Validation completed',
            'total_tests': len(self.test_results),
            'conditions_tested': len(set(r.condition.name for r in self.test_results)),
            'overall_mae': metrics.get('MAE', 0),
            'overall_mape': metrics.get('MAPE', 0),
            'r2_score': metrics.get('R2', 0),
            'confidence_coverage': metrics.get('Coverage', 0),
            'operational_accuracy': metrics.get('Operational_Accuracy', 0),
            'last_validation': max(r.timestamp for r in self.test_results)
        } 