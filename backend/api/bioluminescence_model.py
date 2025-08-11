"""
Bioluminescent Bead Detection Distance Prediction AI Model

This module implements the core AI model for predicting maximum detection distances
of bioluminescent beads under various environmental conditions.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from scipy.optimize import minimize
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Physical constants
R = 8.314  # Gas constant (J/mol·K)

@dataclass
class ModelParameters:
    """Default calibrated parameters for the bioluminescence model"""
    # Light decay parameters
    I0: float = 10.0      # Initial intensity (lux)
    A: float = 0.015      # Arrhenius prefactor
    Ea: float = 50000     # Activation energy (J/mol)
    
    # Environmental attenuation parameters
    alpha0: float = 0.002  # Base attenuation (m^-1)
    alpha1: float = 0.018  # Wind coefficient
    alpha2: float = 0.025  # Precipitation coefficient
    alpha3: float = 0.032  # Wave height coefficient
    alpha4: float = 0.008  # Precipitation-wave interaction
    beta: float = 1.2      # Wind exponent
    
    # Detection threshold parameters
    k_sensor: Dict[str, float] = None  # Sensor-specific constants
    gamma: float = 1.5     # Ambient scaling factor
    
    def __post_init__(self):
        if self.k_sensor is None:
            self.k_sensor = {
                'human': 0.001,
                'drone': 0.005,
                'nvg': 0.0005
            }

class BioluminescenceModel:
    """
    AI Model for predicting bioluminescent bead detection distances.
    
    This model combines physics-based light decay modeling with machine learning
    calibration to provide accurate distance predictions under various environmental
    conditions.
    """
    
    def __init__(self, parameters: Optional[ModelParameters] = None):
        """
        Initialize the bioluminescence model.
        
        Args:
            parameters: Model parameters (uses defaults if None)
        """
        self.params = parameters or ModelParameters()
        self.calibration_history = []
        self.validation_data = []
        
    def light_decay(self, t: float, T: float) -> float:
        """
        Calculate current bioluminescence intensity using Arrhenius kinetics.
        
        Args:
            t: Time since activation (minutes)
            T: Water temperature (°C)
            
        Returns:
            Current intensity (lux)
        """
        T_k = T + 273.15  # Convert to Kelvin
        decay_rate = self.params.A * np.exp(-self.params.Ea / (R * T_k))
        intensity = self.params.I0 * np.exp(-decay_rate * t)
        return max(intensity, 0.0)  # Ensure non-negative
    
    def environmental_attenuation(self, Uw: float, P: float, Hs: float) -> float:
        """
        Calculate environmental attenuation coefficient.
        
        Args:
            Uw: Wind speed (m/s)
            P: Precipitation rate (mm/hr)
            Hs: Significant wave height (m)
            
        Returns:
            Attenuation coefficient (m^-1)
        """
        c = (self.params.alpha0 + 
             self.params.alpha1 * (Uw ** self.params.beta) +
             self.params.alpha2 * P +
             self.params.alpha3 * Hs +
             self.params.alpha4 * P * Hs)
        return max(c, 0.001)  # Minimum attenuation
    
    def detection_threshold(self, I_ambient: float, sensor_type: str) -> float:
        """
        Calculate minimum detectable light intensity.
        
        Args:
            I_ambient: Ambient light level (lux)
            sensor_type: Type of sensor ('human', 'drone', 'nvg')
            
        Returns:
            Detection threshold (lux)
        """
        k_sensor = self.params.k_sensor.get(sensor_type, self.params.k_sensor['drone'])
        threshold = k_sensor + self.params.gamma * I_ambient
        return max(threshold, 0.0001)  # Minimum threshold
    
    def max_distance(self, I_current: float, I_threshold: float, c: float) -> float:
        """
        Calculate maximum detection distance.
        
        Args:
            I_current: Current bioluminescence intensity (lux)
            I_threshold: Detection threshold (lux)
            c: Attenuation coefficient (m^-1)
            
        Returns:
            Maximum detection distance (m)
        """
        if I_current <= I_threshold:
            return 0.0
        
        distance = (1.0 / c) * np.log(I_current / I_threshold)
        return np.clip(distance, 0.0, 10000.0)  # Physical limits
    
    def predict(self, 
                activation_time: float,
                water_temp: float,
                wind_speed: float,
                precipitation: float,
                wave_height: float,
                ambient_light: float,
                sensor_type: str = "drone") -> Dict[str, Union[float, List[float], str]]:
        """
        Predict maximum detection distance for given conditions.
        
        Args:
            activation_time: Time since activation (minutes)
            water_temp: Water temperature (°C)
            wind_speed: Wind speed (m/s)
            precipitation: Precipitation rate (mm/hr)
            wave_height: Significant wave height (m)
            ambient_light: Ambient light level (lux)
            sensor_type: Type of sensor ('human', 'drone', 'nvg')
            
        Returns:
            Dictionary containing prediction results
        """
        # Calculate current bioluminescence intensity
        I_current = self.light_decay(activation_time, water_temp)
        
        # Calculate environmental attenuation
        c = self.environmental_attenuation(wind_speed, precipitation, wave_height)
        
        # Calculate detection threshold
        I_threshold = self.detection_threshold(ambient_light, sensor_type)
        
        # Calculate maximum distance
        distance = self.max_distance(I_current, I_threshold, c)
        
        # Calculate confidence interval using Monte Carlo simulation
        confidence_interval = self._uncertainty_analysis(
            activation_time, water_temp, wind_speed, precipitation, 
            wave_height, ambient_light, sensor_type
        )
        
        # Calculate performance score
        performance_score = self._calculate_performance_score(
            I_current, I_threshold, c, distance
        )
        
        # Generate failure flags
        failure_flags = self._generate_failure_flags(
            I_current, I_threshold, c, distance
        )
        
        return {
            'distance': distance,
            'confidence_interval': confidence_interval,
            'performance_score': performance_score,
            'system_conditions': [
                f"Brightness: {I_current:.1f} lux",
                f"Attenuation: {c:.4f} m⁻¹",
                f"Detection threshold: {I_threshold:.3f} lux"
            ],
            'failure_flags': failure_flags,
            'validation_status': "Requires field verification"
        }
    
    def _uncertainty_analysis(self, *args) -> List[float]:
        """
        Perform Monte Carlo uncertainty analysis.
        
        Returns:
            [5th percentile, median, 95th percentile] distances
        """
        distances = []
        n_samples = 100  # Reduced for faster execution
        
        # Parameter uncertainties (standard deviations)
        param_uncertainties = {
            'I0': 0.5,
            'A': 0.002,
            'Ea': 2000,
            'alpha1': 0.005,
            'alpha2': 0.008,
            'alpha3': 0.010,
            'gamma': 0.2
        }
        
        for _ in range(n_samples):
            # Sample parameters from normal distributions
            sampled_params = ModelParameters()
            sampled_params.I0 = np.random.normal(self.params.I0, param_uncertainties['I0'])
            sampled_params.A = np.random.normal(self.params.A, param_uncertainties['A'])
            sampled_params.Ea = np.random.normal(self.params.Ea, param_uncertainties['Ea'])
            sampled_params.alpha1 = np.random.normal(self.params.alpha1, param_uncertainties['alpha1'])
            sampled_params.alpha2 = np.random.normal(self.params.alpha2, param_uncertainties['alpha2'])
            sampled_params.alpha3 = np.random.normal(self.params.alpha3, param_uncertainties['alpha3'])
            sampled_params.gamma = np.random.normal(self.params.gamma, param_uncertainties['gamma'])
            
            # Calculate prediction directly without recursion
            activation_time, water_temp, wind_speed, precipitation, wave_height, ambient_light, sensor_type = args
            
            # Light decay
            I_current = sampled_params.I0 * np.exp(-sampled_params.A * np.exp(-sampled_params.Ea / (8.314 * (water_temp + 273.15))) * activation_time)
            
            # Environmental attenuation
            c = (sampled_params.alpha0 + 
                 sampled_params.alpha1 * (wind_speed ** sampled_params.beta) + 
                 sampled_params.alpha2 * precipitation + 
                 sampled_params.alpha3 * wave_height + 
                 sampled_params.alpha4 * precipitation * wave_height)
            
            # Detection threshold
            I_threshold = sampled_params.k_sensor.get(sensor_type, 0.005) + sampled_params.gamma * ambient_light
            
            # Max distance
            if I_current > I_threshold and c > 0:
                distance = (1 / c) * np.log(I_current / I_threshold)
                distance = np.clip(distance, 0.0, 10000.0)
            else:
                distance = 0.0
            
            distances.append(distance)
        
        return [
            np.percentile(distances, 5),
            np.percentile(distances, 50),
            np.percentile(distances, 95)
        ]
    
    def _calculate_performance_score(self, I_current: float, I_threshold: float, 
                                   c: float, distance: float) -> float:
        """
        Calculate model performance score based on signal quality and conditions.
        
        Returns:
            Performance score (0-100%)
        """
        # Signal-to-noise ratio
        snr = I_current / I_threshold if I_threshold > 0 else 0
        
        # Attenuation quality (lower is better)
        attenuation_score = max(0, 100 - c * 1000)
        
        # Distance quality (higher is better, up to reasonable limits)
        distance_score = min(100, distance / 10)
        
        # Overall score
        score = (0.4 * min(100, snr * 10) + 
                0.3 * attenuation_score + 
                0.3 * distance_score)
        
        return np.clip(score, 0, 100)
    
    def _generate_failure_flags(self, I_current: float, I_threshold: float,
                               c: float, distance: float) -> List[str]:
        """
        Generate diagnostic failure flags.
        
        Returns:
            List of failure flag messages
        """
        flags = []
        
        if I_current < I_threshold:
            flags.append("Low brightness")
        
        if c > 0.05:
            flags.append("Heavy attenuation")
        
        if distance < 50:
            flags.append("Very short range")
        
        if I_current < 0.1:
            flags.append("Weak signal")
        
        return flags
    
    def calibrate_parameters(self, field_data: pd.DataFrame) -> Dict[str, float]:
        """
        Calibrate model parameters using field data.
        
        Args:
            field_data: DataFrame with columns [actual_distance, activation_time, 
                        water_temp, wind_speed, precipitation, wave_height, 
                        ambient_light, sensor_type]
                        
        Returns:
            Dictionary of optimized parameters
        """
        def objective_function(params):
            # Update model parameters
            self.params.I0 = params[0]
            self.params.A = params[1]
            self.params.Ea = params[2]
            self.params.alpha1 = params[3]
            self.params.alpha2 = params[4]
            self.params.alpha3 = params[5]
            self.params.gamma = params[6]
            
            # Calculate predictions
            predictions = []
            for _, row in field_data.iterrows():
                result = self.predict(
                    activation_time=row['activation_time'],
                    water_temp=row['water_temp'],
                    wind_speed=row['wind_speed'],
                    precipitation=row['precipitation'],
                    wave_height=row['wave_height'],
                    ambient_light=row['ambient_light'],
                    sensor_type=row['sensor_type']
                )
                predictions.append(result['distance'])
            
            # Calculate error metric
            mae = mean_absolute_error(field_data['actual_distance'], predictions)
            return mae
        
        # Initial parameter values
        initial_params = [
            self.params.I0, self.params.A, self.params.Ea,
            self.params.alpha1, self.params.alpha2, self.params.alpha3,
            self.params.gamma
        ]
        
        # Parameter bounds
        bounds = [
            (8, 12),      # I0
            (0.01, 0.02), # A
            (40000, 60000), # Ea
            (0.01, 0.03), # alpha1
            (0.015, 0.035), # alpha2
            (0.02, 0.04), # alpha3
            (1.0, 2.0)    # gamma
        ]
        
        # Optimize parameters
        result = minimize(
            objective_function,
            initial_params,
            bounds=bounds,
            method='L-BFGS-B',
            options={'maxiter': 50}
        )
        
        # Update model with optimized parameters
        optimized_params = {
            'I0': result.x[0],
            'A': result.x[1],
            'Ea': result.x[2],
            'alpha1': result.x[3],
            'alpha2': result.x[4],
            'alpha3': result.x[5],
            'gamma': result.x[6]
        }
        
        # Update model parameters
        for key, value in optimized_params.items():
            setattr(self.params, key, value)
        
        # Store calibration history
        self.calibration_history.append({
            'iteration': len(self.calibration_history) + 1,
            'parameters': optimized_params.copy(),
            'error': result.fun,
            'success': result.success
        })
        
        return optimized_params
    
    def add_validation_data(self, field_data: Dict[str, float]):
        """
        Add new validation data point for continuous learning.
        
        Args:
            field_data: Dictionary containing field measurement data
        """
        self.validation_data.append(field_data)
        
        # Retrain model if enough new data
        if len(self.validation_data) >= 10:
            self._retrain_from_validation_data()
    
    def _retrain_from_validation_data(self):
        """
        Retrain model using accumulated validation data.
        """
        if len(self.validation_data) < 10:
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(self.validation_data)
        
        # Calibrate parameters
        self.calibrate_parameters(df)
        
        # Clear validation data after retraining
        self.validation_data = []
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get comprehensive model information and statistics.
        
        Returns:
            Dictionary containing model information
        """
        return {
            'parameters': {
                'I0': self.params.I0,
                'A': self.params.A,
                'Ea': self.params.Ea,
                'alpha0': self.params.alpha0,
                'alpha1': self.params.alpha1,
                'alpha2': self.params.alpha2,
                'alpha3': self.params.alpha3,
                'alpha4': self.params.alpha4,
                'beta': self.params.beta,
                'gamma': self.params.gamma,
                'k_sensor': self.params.k_sensor
            },
            'calibration_history': self.calibration_history,
            'validation_data_count': len(self.validation_data),
            'model_version': '1.0.0'
        } 