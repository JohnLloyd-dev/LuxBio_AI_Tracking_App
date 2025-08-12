"""
Bioluminescence Detection AI Model

This module provides the core AI model for predicting bioluminescent bead detection distances
based on environmental conditions, sensor parameters, and temporal factors.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from .data_models import DetectionInput, ValidationResult

@dataclass
class ModelParameters:
    """Model configuration parameters"""
    base_detection_range: float = 1000.0  # Base detection range in meters
    temperature_factor: float = 0.95       # Temperature effect multiplier
    wind_penalty: float = 0.02            # Wind speed penalty per m/s
    wave_penalty: float = 0.15            # Wave height penalty per meter
    light_penalty: float = 0.1            # Ambient light penalty per lux
    activation_decay: float = 0.001       # Activation time decay per minute

class BioluminescenceModel:
    """AI model for bioluminescent detection distance prediction"""
    
    def __init__(self, parameters: Optional[ModelParameters] = None):
        """Initialize the model with parameters"""
        self.parameters = parameters or ModelParameters()
        self.is_trained = False
        self.training_data = []
        
    def predict(self, input_data: DetectionInput) -> Dict[str, Any]:
        """
        Make a prediction based on input parameters
        
        Args:
            input_data: DetectionInput object containing all parameters
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Extract parameters
            temp = input_data.temporal_parameters.water_temperature
            wind = input_data.environmental_conditions.wind_speed
            waves = input_data.environmental_conditions.wave_height
            light = input_data.environmental_conditions.ambient_light
            activation = input_data.temporal_parameters.activation_time
            sensor_type = input_data.sensor_parameters.type
            
            # Calculate base detection range
            base_range = self.parameters.base_detection_range
            
            # Apply environmental factors
            temp_factor = self.parameters.temperature_factor ** (abs(temp - 20) / 10)
            wind_effect = 1 - (wind * self.parameters.wind_penalty)
            wave_effect = 1 - (waves * self.parameters.wave_penalty)
            light_effect = 1 - (light * self.parameters.light_penalty)
            activation_effect = np.exp(-activation * self.parameters.activation_decay)
            
            # Sensor type multipliers
            sensor_multipliers = {
                "human": 1.0,
                "drone": 1.2,
                "nvg": 1.5
            }
            sensor_multiplier = sensor_multipliers.get(sensor_type, 1.0)
            
            # Calculate final detection distance
            detection_distance = (
                base_range *
                temp_factor *
                wind_effect *
                wave_effect *
                light_effect *
                activation_effect *
                sensor_multiplier
            )
            
            # Ensure reasonable bounds
            detection_distance = max(10.0, min(detection_distance, 5000.0))
            
            # Calculate confidence intervals (simplified)
            confidence_95 = detection_distance * 0.9
            confidence_50 = detection_distance
            confidence_5 = detection_distance * 1.1
        
            # Calculate performance score
            performance_score = self._calculate_performance_score(
                temp, wind, waves, light, activation
            )
            
            # Generate system conditions and warnings
            system_conditions = self._generate_system_conditions(
                temp, wind, waves, light, activation
            )
            
            failure_flags = self._generate_failure_flags(
                temp, wind, waves, light, activation
            )
            
            return {
                "distance": round(detection_distance, 2),
                "confidence_interval": [
                    round(confidence_5, 2),
                    round(confidence_50, 2),
                    round(confidence_95, 2)
                ],
                "performance_score": round(performance_score, 1),
                "system_conditions": system_conditions,
                "failure_flags": failure_flags,
                "model_confidence": "high" if self.is_trained else "medium",
                "validation_status": "Model prediction completed successfully"
            }
            
        except Exception as e:
            return {
                "error": f"Prediction failed: {str(e)}",
                "distance": 0.0,
                "confidence_interval": [0.0, 0.0, 0.0],
                "performance_score": 0.0,
                "system_conditions": ["Model error occurred"],
                "failure_flags": ["Prediction failed"]
            }
    
    def _calculate_performance_score(self, temp: float, wind: float, waves: float, 
                                   light: float, activation: float) -> float:
        """Calculate overall performance score (0-100)"""
        # Base score starts at 100
        score = 100.0
        
        # Temperature penalty (optimal around 20°C)
        temp_penalty = abs(temp - 20) * 2
        score -= temp_penalty
        
        # Wind penalty
        wind_penalty = wind * 3
        score -= wind_penalty
        
        # Wave penalty
        wave_penalty = waves * 8
        score -= wave_penalty
        
        # Light penalty
        light_penalty = light * 50
        score -= light_penalty
        
        # Activation time penalty
        activation_penalty = activation * 0.1
        score -= activation_penalty
        
        return max(0.0, min(100.0, score))
    
    def _generate_system_conditions(self, temp: float, wind: float, waves: float,
                                  light: float, activation: float) -> List[str]:
        """Generate system diagnostic information"""
        conditions = []
        
        if temp < 5:
            conditions.append("Low water temperature may reduce bioluminescence")
        elif temp > 25:
            conditions.append("High water temperature may affect sensor performance")
        
        if wind > 15:
            conditions.append("High wind speed may cause surface disturbances")
        
        if waves > 3:
            conditions.append("High wave activity may interfere with detection")
        
        if light > 0.05:
            conditions.append("High ambient light may reduce detection sensitivity")
        
        if activation > 300:
            conditions.append("Long activation time may reduce signal strength")
        
        if not conditions:
            conditions.append("All parameters within optimal ranges")
        
        return conditions
    
    def _generate_failure_flags(self, temp: float, wind: float, waves: float,
                               light: float, activation: float) -> List[str]:
        """Generate warning flags for poor conditions"""
        flags = []
        
        if temp < -1 or temp > 30:
            flags.append("Water temperature outside operational range")
        
        if wind > 25:
            flags.append("Wind speed exceeds operational limits")
        
        if waves > 8:
            flags.append("Wave height exceeds operational limits")
        
        if light > 0.1:
            flags.append("Ambient light too high for reliable detection")
        
        if activation > 360:
            flags.append("Activation time exceeds operational limits")
        
        return flags
    
    def get_parameters(self) -> Dict[str, float]:
        """Get current model parameters"""
        return {
            "base_detection_range": self.parameters.base_detection_range,
            "temperature_factor": self.parameters.temperature_factor,
            "wind_penalty": self.parameters.wind_penalty,
            "wave_penalty": self.parameters.wave_penalty,
            "light_penalty": self.parameters.light_penalty,
            "activation_decay": self.parameters.activation_decay
        }
    
    def update_parameters(self, new_parameters: Dict[str, float]) -> None:
        """Update model parameters with new values"""
        if 'base_detection_range' in new_parameters:
            self.parameters.base_detection_range = new_parameters['base_detection_range']
        if 'temperature_factor' in new_parameters:
            self.parameters.temperature_factor = new_parameters['temperature_factor']
        if 'wind_penalty' in new_parameters:
            self.parameters.wind_penalty = new_parameters['wind_penalty']
        if 'wave_penalty' in new_parameters:
            self.parameters.wave_penalty = new_parameters['wave_penalty']
        if 'light_penalty' in new_parameters:
            self.parameters.light_penalty = new_parameters['light_penalty']
        if 'activation_decay' in new_parameters:
            self.parameters.activation_decay = new_parameters['activation_decay']

    def train(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train the model with historical data"""
        if not training_data:
            return {"error": "No training data provided"}
        
        try:
            # Store training data
            self.training_data = training_data
            
            # Simple parameter optimization based on training data
            # Calculate average performance and adjust parameters
            total_score = 0
            valid_samples = 0
            
            for data_point in training_data:
                if 'performance_score' in data_point and 'distance' in data_point:
                    total_score += data_point['performance_score']
                    valid_samples += 1
            
            if valid_samples == 0:
                return {"error": "No valid training samples with performance scores"}
            
            avg_score = total_score / valid_samples
            
            # Simple parameter adjustment based on average performance
            if avg_score < 70:  # Poor performance
                # Increase base detection range slightly
                self.parameters.base_detection_range *= 1.05
                # Reduce penalties slightly
                self.parameters.wind_penalty *= 0.95
                self.parameters.wave_penalty *= 0.95
                self.parameters.light_penalty *= 0.95
            elif avg_score > 90:  # Excellent performance
                # Fine-tune parameters
                self.parameters.temperature_factor *= 1.02
                self.parameters.activation_decay *= 0.98
            
            # Ensure parameters stay within reasonable bounds
            self.parameters.base_detection_range = max(500.0, min(2000.0, self.parameters.base_detection_range))
            self.parameters.temperature_factor = max(0.8, min(1.1, self.parameters.temperature_factor))
            self.parameters.wind_penalty = max(0.01, min(0.05, self.parameters.wind_penalty))
            self.parameters.wave_penalty = max(0.1, min(0.2, self.parameters.wave_penalty))
            self.parameters.light_penalty = max(0.05, min(0.15, self.parameters.light_penalty))
            self.parameters.activation_decay = max(0.0005, min(0.002, self.parameters.activation_decay))
            
            # Mark as trained
            self.is_trained = True
            
            return {
                "status": "success",
                "training_samples": valid_samples,
                "average_performance": round(avg_score, 2),
                "model_confidence": "high",
                "parameters_updated": True,
                "new_parameters": self.get_parameters()
            }
            
        except Exception as e:
            return {"error": f"Training failed: {str(e)}"}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get current model information and status"""
        return {
            "model_type": "Bioluminescence Detection AI",
            "version": "2.0.0",
            "is_trained": self.is_trained,
            "training_samples": len(self.training_data),
            "parameters": {
                "base_detection_range": self.parameters.base_detection_range,
                "temperature_factor": self.parameters.temperature_factor,
                "wind_penalty": self.parameters.wind_penalty,
                "wave_penalty": self.parameters.wave_penalty,
                "light_penalty": self.parameters.light_penalty,
                "activation_decay": self.parameters.activation_decay
            },
            "supported_sensors": ["human", "drone", "nvg"],
            "operational_ranges": {
                "water_temperature": "(-2°C to 30°C)",
                "wind_speed": "(0 to 25 m/s)",
                "wave_height": "(0 to 10 m)",
                "ambient_light": "(0.0001 to 0.1 lux)",
                "activation_time": "(0 to 360 minutes)"
            }
        } 