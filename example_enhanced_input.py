#!/usr/bin/env python3
"""
Enhanced Input Format Example for Bioluminescent Detection AI Model

This script demonstrates the comprehensive input data format specification
and validation capabilities for the bioluminescent detection system.
"""

import json
import csv
import numpy as np
from datetime import datetime
from data_models import DataProcessor, DetectionInput, ValidationResult
from bioluminescence_model import BioluminescenceModel

def main():
    """
    Demonstrate the enhanced input format and validation capabilities.
    """
    print("🔬 Enhanced Input Format Demonstration")
    print("=" * 50)
    
    # Initialize components
    data_processor = DataProcessor()
    model = BioluminescenceModel()
    
    # Example 1: JSON Input Format (Recommended)
    print("\n1. JSON Input Format Example")
    print("-" * 30)
    
    json_input = {
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
    
    print("Input JSON:")
    print(json.dumps(json_input, indent=2))
    
    # Validate input
    validation_result = data_processor.validate_json_input(json_input)
    
    print(f"\nValidation Result:")
    print(f"✓ Valid: {validation_result.is_valid}")
    if validation_result.warnings:
        print(f"⚠ Warnings: {validation_result.warnings}")
    
    if validation_result.is_valid:
        # Convert to model input
        model_input = data_processor.convert_to_model_input(validation_result.processed_data)
        
        # Make prediction
        result = model.predict(**model_input)
        
        print(f"\nPrediction Result:")
        print(f"✓ Distance: {result['distance']:.0f} m")
        print(f"✓ Confidence: {result['confidence_interval']}")
        print(f"✓ Performance: {result['performance_score']:.1f}%")
    
    # Example 2: CSV Single Prediction Format
    print("\n\n2. CSV Single Prediction Format")
    print("-" * 35)
    
    csv_single_data = """parameter_category,parameter,value,units
temporal,activation_time,60.0,minutes
temporal,water_temperature,10.2,C
environmental,wind_speed,3.1,m/s
environmental,precipitation,0.0,mm/hr
environmental,wave_height,0.5,m
environmental,ambient_light,0.0005,lux
sensor,type,nvg,na"""
    
    print("CSV Input:")
    print(csv_single_data)
    
    # Parse CSV
    csv_result = data_processor.parse_csv_single(csv_single_data)
    
    print(f"\nCSV Parsing Result:")
    print(f"✓ Valid: {csv_result.is_valid}")
    if csv_result.warnings:
        print(f"⚠ Warnings: {csv_result.warnings}")
    
    if csv_result.is_valid:
        model_input = data_processor.convert_to_model_input(csv_result.processed_data)
        result = model.predict(**model_input)
        
        print(f"\nPrediction Result:")
        print(f"✓ Distance: {result['distance']:.0f} m")
        print(f"✓ Confidence: {result['confidence_interval']}")
    
    # Example 3: CSV Bulk Predictions Format
    print("\n\n3. CSV Bulk Predictions Format")
    print("-" * 35)
    
    csv_bulk_data = """activation_time,water_temp,wind_speed,precip,wave_ht,ambient_light,sensor_type
45.0,8.5,5.2,2.4,1.2,0.002,drone
60.0,10.2,3.1,0.0,0.5,0.0005,nvg
30.0,5.8,12.4,8.7,2.3,0.01,human
90.0,15.0,1.5,0.0,0.2,0.001,drone
120.0,20.0,8.0,5.0,1.0,0.005,human"""
    
    print("Bulk CSV Input:")
    print(csv_bulk_data)
    
    # Parse bulk CSV
    bulk_results = data_processor.parse_csv_bulk(csv_bulk_data)
    
    print(f"\nBulk CSV Parsing Results:")
    valid_count = sum(1 for r in bulk_results if r.is_valid)
    print(f"✓ Valid predictions: {valid_count}/{len(bulk_results)}")
    
    # Make predictions for valid inputs
    predictions = []
    for i, result in enumerate(bulk_results):
        if result.is_valid:
            model_input = data_processor.convert_to_model_input(result.processed_data)
            pred_result = model.predict(**model_input)
            predictions.append(pred_result['distance'])
            print(f"  Prediction {i+1}: {pred_result['distance']:.0f} m")
    
    if predictions:
        print(f"\nSummary Statistics:")
        print(f"✓ Average distance: {np.mean(predictions):.0f} m")
        print(f"✓ Min distance: {np.min(predictions):.0f} m")
        print(f"✓ Max distance: {np.max(predictions):.0f} m")
    
    # Example 4: Field Data Collection Template
    print("\n\n4. Field Data Collection Template")
    print("-" * 35)
    
    field_template = data_processor.create_field_data_collector()
    
    print("Field Data Collection Template:")
    print(json.dumps(field_template, indent=2))
    
    # Example 5: Weather Station Data Integration
    print("\n\n5. Weather Station Data Integration")
    print("-" * 35)
    
    # Simulate weather station data
    weather_station_csv = """timestamp,lat,lon,wind_speed(m/s),precip(mm/hr),wave_height(m),ambient_light(lux),water_temp(C)
2024-01-15T22:30:00Z,48.423,-123.367,5.2,2.4,1.2,0.002,8.5
2024-01-15T22:35:00Z,48.423,-123.367,5.5,2.1,1.3,0.002,8.4
2024-01-15T22:40:00Z,48.423,-123.367,5.8,1.8,1.1,0.002,8.6"""
    
    print("Weather Station Data:")
    print(weather_station_csv)
    
    # Save to temporary file and load
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_file.write(weather_station_csv)
        temp_file_path = temp_file.name
    
    try:
        from data_models import load_weather_station_data
        weather_data = load_weather_station_data(temp_file_path)
        
        print(f"\nProcessed Weather Data:")
        print(f"✓ Records loaded: {len(weather_data)}")
        
        # Show first record
        if weather_data:
            print("\nFirst record:")
            print(json.dumps(weather_data[0], indent=2))
            
            # Calculate activation time
            activation_time = calculate_activation_time(
                "2024-01-15T22:15:00Z",  # Bead activation
                "2024-01-15T22:30:00Z"   # Measurement time
            )
            
            print(f"\nCalculated activation time: {activation_time:.1f} minutes")
            
    finally:
        os.unlink(temp_file_path)
    
    # Example 6: Input Validation Edge Cases
    print("\n\n6. Input Validation Edge Cases")
    print("-" * 35)
    
    edge_cases = [
        {
            "name": "Extreme Wind Speed",
            "data": {
                "temporal_parameters": {"activation_time": 45.0, "water_temperature": 8.5},
                "environmental_conditions": {"wind_speed": 30.0, "precipitation": 2.4, "wave_height": 1.2, "ambient_light": 0.002},
                "sensor_parameters": {"type": "drone"}
            }
        },
        {
            "name": "Very Low Ambient Light",
            "data": {
                "temporal_parameters": {"activation_time": 45.0, "water_temperature": 8.5},
                "environmental_conditions": {"wind_speed": 5.2, "precipitation": 2.4, "wave_height": 1.2, "ambient_light": 0.00001},
                "sensor_parameters": {"type": "nvg"}
            }
        },
        {
            "name": "Invalid Sensor Type",
            "data": {
                "temporal_parameters": {"activation_time": 45.0, "water_temperature": 8.5},
                "environmental_conditions": {"wind_speed": 5.2, "precipitation": 2.4, "wave_height": 1.2, "ambient_light": 0.002},
                "sensor_parameters": {"type": "invalid_sensor"}
            }
        }
    ]
    
    for case in edge_cases:
        print(f"\nTesting: {case['name']}")
        result = data_processor.validate_json_input(case['data'])
        print(f"✓ Valid: {result.is_valid}")
        if result.errors:
            print(f"✗ Errors: {result.errors}")
        if result.warnings:
            print(f"⚠ Warnings: {result.warnings}")
    
    # Example 7: Data Export
    print("\n\n7. Data Export Example")
    print("-" * 25)
    
    # Create sample validation data
    sample_data = []
    for i in range(3):
        sample_data.append({
            "timestamp": datetime.now().isoformat(),
            "temporal_parameters": {"activation_time": 45.0 + i*15, "water_temperature": 8.5},
            "environmental_conditions": {"wind_speed": 5.2, "precipitation": 2.4, "wave_height": 1.2, "ambient_light": 0.002},
            "sensor_parameters": {"type": "drone"},
            "detection_results": {"actual_distance": 400 + i*50}
        })
    
    # Export to CSV
    data_processor.export_to_csv(sample_data, "sample_validation_data.csv")
    print("✓ Sample data exported to 'sample_validation_data.csv'")
    
    print("\n" + "=" * 50)
    print("🎯 Enhanced Input Format Demonstration Complete!")
    print("\nKey Features Demonstrated:")
    print("• JSON input format with comprehensive validation")
    print("• CSV parsing for single and bulk predictions")
    print("• Field data collection templates")
    print("• Weather station data integration")
    print("• Input validation with edge case handling")
    print("• Data export capabilities")

def calculate_activation_time(activation_timestamp: str, measurement_timestamp: str) -> float:
    """Calculate activation time in minutes between two timestamps"""
    from datetime import datetime
    
    activation_dt = datetime.fromisoformat(activation_timestamp.replace('Z', '+00:00'))
    measurement_dt = datetime.fromisoformat(measurement_timestamp.replace('Z', '+00:00'))
    
    time_diff = measurement_dt - activation_dt
    return time_diff.total_seconds() / 60.0  # Convert to minutes

if __name__ == "__main__":
    main() 