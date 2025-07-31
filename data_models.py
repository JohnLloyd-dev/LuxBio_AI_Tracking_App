"""
Data Models for Bioluminescent Detection AI Model

This module defines the comprehensive data structures for input parameters,
validation rules, and data processing according to the detailed specification.
"""

from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import csv
import pandas as pd
from pydantic import BaseModel, Field, validator, root_validator
import numpy as np

class SensorType(str, Enum):
    """Supported sensor types"""
    HUMAN = "human"
    DRONE = "drone"
    NVG = "nvg"

class TemporalParameters(BaseModel):
    """Temporal parameters for bioluminescent detection"""
    activation_time: float = Field(..., ge=0, le=360, description="Time since activation (minutes)")
    water_temperature: float = Field(..., ge=-2, le=30, description="Water temperature (°C)")
    
    @validator('activation_time')
    def validate_activation_time(cls, v):
        if not (0 <= v <= 360):
            raise ValueError("Activation time must be 0-360 minutes")
        return v
    
    @validator('water_temperature')
    def validate_water_temperature(cls, v):
        if not (-2 <= v <= 30):
            raise ValueError("Water temperature must be -2 to 30°C")
        return v

class EnvironmentalConditions(BaseModel):
    """Environmental conditions affecting detection"""
    wind_speed: float = Field(..., ge=0, le=25, description="Wind speed at 10m height (m/s)")
    precipitation: float = Field(..., ge=0, le=50, description="Precipitation rate (mm/hr)")
    wave_height: float = Field(..., ge=0, le=10, description="Significant wave height (m)")
    ambient_light: float = Field(..., ge=0.0001, le=0.1, description="Background illuminance (lux)")
    water_turbidity: Optional[float] = Field(1.5, ge=0, le=10, description="Water clarity (NTU)")
    current_speed: Optional[float] = Field(0.0, ge=0, le=5, description="Surface current speed (knots)")
    
    @validator('wind_speed')
    def validate_wind_speed(cls, v):
        if v > 25:
            # Cap at 25 m/s with warning flag
            return 25.0
        return v
    
    @validator('wave_height')
    def validate_wave_height(cls, v):
        if v > 10:
            # Cap at 10m with warning flag
            return 10.0
        return v
    
    @validator('ambient_light')
    def validate_ambient_light(cls, v):
        if v < 0.0001:
            return 0.0001  # Set to minimum detectable
        return v
    
    @validator('current_speed')
    def convert_current_speed(cls, v):
        if v is not None:
            # Convert knots to m/s if needed
            return v * 0.514  # knots → m/s
        return v

class SensorParameters(BaseModel):
    """Sensor-specific parameters"""
    type: SensorType = Field(..., description="Detection system type")
    model: Optional[str] = Field(None, description="Specific sensor model")
    spectral_range: Optional[Tuple[float, float]] = Field(None, ge=350, le=900, description="Detection wavelength range (nm)")
    
    @validator('spectral_range')
    def validate_spectral_range(cls, v):
        if v is not None:
            min_wavelength, max_wavelength = v
            if not (350 <= min_wavelength <= max_wavelength <= 900):
                raise ValueError("Spectral range must be 350-900 nm")
        return v

class ProductParameters(BaseModel):
    """Product-specific parameters"""
    bead_density: Optional[int] = Field(350, ge=100, le=1000, description="Beads per deployment unit")
    batch_id: Optional[str] = Field(None, description="Manufacturing batch ID")

class DetectionInput(BaseModel):
    """Complete input data structure for bioluminescent detection"""
    temporal_parameters: TemporalParameters
    environmental_conditions: EnvironmentalConditions
    sensor_parameters: SensorParameters
    product_parameters: Optional[ProductParameters] = Field(default_factory=ProductParameters)
    
    class Config:
        schema_extra = {
            "example": {
                "temporal_parameters": {
                    "activation_time": 45.0,
                    "water_temperature": 8.5
                },
                "environmental_conditions": {
                    "wind_speed": 5.2,
                    "precipitation": 2.4,
                    "wave_height": 1.2,
                    "ambient_light": 0.002,
                    "water_turbidity": 1.8,
                    "current_speed": 0.4
                },
                "sensor_parameters": {
                    "type": "drone",
                    "model": "DJI_M30T",
                    "spectral_range": [450, 550]
                },
                "product_parameters": {
                    "bead_density": 350,
                    "batch_id": "LXB-2025-08"
                }
            }
        }

@dataclass
class ValidationResult:
    """Result of data validation"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    processed_data: Optional[Dict] = None

class DataProcessor:
    """
    Data processor for handling various input formats and validation
    """
    
    # Sensor-specific detection thresholds
    SENSOR_THRESHOLDS = {
        "human": 0.001,
        "drone": 0.005,
        "nvg": 0.0005
    }
    
    # Default values for optional parameters
    DEFAULT_VALUES = {
        "water_turbidity": 1.5,
        "current_speed": 0.0,
        "bead_density": 350
    }
    
    @staticmethod
    def validate_json_input(data: Dict) -> ValidationResult:
        """
        Validate JSON input data according to specification
        """
        errors = []
        warnings = []
        
        try:
            # Validate using Pydantic model
            detection_input = DetectionInput(**data)
            processed_data = detection_input.dict()
            
            # Additional business logic validation
            if processed_data['environmental_conditions']['wind_speed'] == 25.0:
                warnings.append("Wind speed capped at 25 m/s")
            
            if processed_data['environmental_conditions']['wave_height'] == 10.0:
                warnings.append("Wave height capped at 10 m")
            
            # Special handling for NVG
            if processed_data['sensor_parameters']['type'] == 'nvg':
                ambient_light = processed_data['environmental_conditions']['ambient_light']
                if ambient_light < 1e-5:
                    processed_data['environmental_conditions']['ambient_light'] = 1e-5
                    warnings.append("Ambient light adjusted for NVG operation")
            
            return ValidationResult(
                is_valid=True,
                warnings=warnings,
                processed_data=processed_data
            )
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=errors
            )
    
    @staticmethod
    def parse_csv_single(csv_data: str) -> ValidationResult:
        """
        Parse single prediction CSV format
        """
        try:
            # Parse CSV
            lines = csv_data.strip().split('\n')
            reader = csv.DictReader(lines)
            
            data = {}
            for row in reader:
                category = row['parameter_category']
                parameter = row['parameter']
                value = row['value']
                
                # Convert value to appropriate type
                if parameter in ['activation_time', 'water_temperature', 'wind_speed', 
                               'precipitation', 'wave_height', 'ambient_light']:
                    value = float(value)
                elif parameter == 'type':
                    value = str(value)
                
                # Organize by category
                if category not in data:
                    data[category] = {}
                
                data[category][parameter] = value
            
            # Convert to standard format
            standard_data = {
                "temporal_parameters": data.get('temporal', {}),
                "environmental_conditions": data.get('environmental', {}),
                "sensor_parameters": data.get('sensor', {}),
                "product_parameters": data.get('product', {})
            }
            
            return DataProcessor.validate_json_input(standard_data)
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"CSV parsing error: {str(e)}"]
            )
    
    @staticmethod
    def parse_csv_bulk(csv_data: str) -> List[ValidationResult]:
        """
        Parse bulk predictions CSV format
        """
        try:
            # Parse CSV
            lines = csv_data.strip().split('\n')
            reader = csv.DictReader(lines)
            
            results = []
            for row in reader:
                # Convert to standard format
                standard_data = {
                    "temporal_parameters": {
                        "activation_time": float(row['activation_time']),
                        "water_temperature": float(row['water_temp'])
                    },
                    "environmental_conditions": {
                        "wind_speed": float(row['wind_speed']),
                        "precipitation": float(row['precip']),
                        "wave_height": float(row['wave_ht']),
                        "ambient_light": float(row['ambient_light'])
                    },
                    "sensor_parameters": {
                        "type": row['sensor_type']
                    }
                }
                
                result = DataProcessor.validate_json_input(standard_data)
                results.append(result)
            
            return results
            
        except Exception as e:
            return [ValidationResult(
                is_valid=False,
                errors=[f"Bulk CSV parsing error: {str(e)}"]
            )]
    
    @staticmethod
    def convert_to_model_input(processed_data: Dict) -> Dict:
        """
        Convert validated data to model input format
        """
        temporal = processed_data['temporal_parameters']
        environmental = processed_data['environmental_conditions']
        sensor = processed_data['sensor_parameters']
        
        return {
            'activation_time': temporal['activation_time'],
            'water_temp': temporal['water_temperature'],
            'wind_speed': environmental['wind_speed'],
            'precipitation': environmental['precipitation'],
            'wave_height': environmental['wave_height'],
            'ambient_light': environmental['ambient_light'],
            'sensor_type': sensor['type']
        }
    
    @staticmethod
    def create_field_data_collector() -> Dict:
        """
        Create template for field data collection
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "location": {
                "latitude": None,
                "longitude": None,
                "altitude": None
            },
            "temporal_parameters": {
                "activation_time": None,
                "water_temperature": None
            },
            "environmental_conditions": {
                "wind_speed": None,
                "wind_direction": None,
                "precipitation": None,
                "wave_height": None,
                "ambient_light": None,
                "water_turbidity": None,
                "current_speed": None,
                "air_temperature": None,
                "humidity": None
            },
            "sensor_parameters": {
                "type": None,
                "model": None,
                "spectral_range": None
            },
            "product_parameters": {
                "bead_density": None,
                "batch_id": None
            },
            "detection_results": {
                "actual_distance": None,
                "detection_confidence": None,
                "detection_method": None,
                "false_positives": None,
                "missed_detections": None
            }
        }
    
    @staticmethod
    def export_to_csv(data: List[Dict], filename: str):
        """
        Export validation data to CSV format
        """
        if not data:
            return
        
        # Flatten data for CSV export
        flattened_data = []
        for entry in data:
            flat_entry = {
                'timestamp': entry.get('timestamp', ''),
                'activation_time': entry.get('temporal_parameters', {}).get('activation_time', ''),
                'water_temperature': entry.get('temporal_parameters', {}).get('water_temperature', ''),
                'wind_speed': entry.get('environmental_conditions', {}).get('wind_speed', ''),
                'precipitation': entry.get('environmental_conditions', {}).get('precipitation', ''),
                'wave_height': entry.get('environmental_conditions', {}).get('wave_height', ''),
                'ambient_light': entry.get('environmental_conditions', {}).get('ambient_light', ''),
                'sensor_type': entry.get('sensor_parameters', {}).get('type', ''),
                'actual_distance': entry.get('detection_results', {}).get('actual_distance', '')
            }
            flattened_data.append(flat_entry)
        
        # Write to CSV
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")

# Utility functions for data handling
def load_weather_station_data(filename: str) -> List[Dict]:
    """
    Load data from marine weather station CSV format
    """
    df = pd.read_csv(filename)
    data = []
    
    for _, row in df.iterrows():
        entry = {
            "timestamp": row['timestamp'],
            "temporal_parameters": {
                "activation_time": None,  # Will be calculated
                "water_temperature": row['water_temp(C)']
            },
            "environmental_conditions": {
                "wind_speed": row['wind_speed(m/s)'],
                "precipitation": row['precip(mm/hr)'],
                "wave_height": row['wave_height(m)'],
                "ambient_light": row['ambient_light(lux)'],
                "water_turbidity": 1.5,  # Default
                "current_speed": 0.0     # Default
            },
            "sensor_parameters": {
                "type": "drone"  # Default
            },
            "product_parameters": {
                "bead_density": 350,
                "batch_id": None
            }
        }
        data.append(entry)
    
    return data

def calculate_activation_time(activation_timestamp: str, measurement_timestamp: str) -> float:
    """
    Calculate activation time in minutes between two timestamps
    """
    activation_dt = datetime.fromisoformat(activation_timestamp.replace('Z', '+00:00'))
    measurement_dt = datetime.fromisoformat(measurement_timestamp.replace('Z', '+00:00'))
    
    time_diff = measurement_dt - activation_dt
    return time_diff.total_seconds() / 60.0  # Convert to minutes 