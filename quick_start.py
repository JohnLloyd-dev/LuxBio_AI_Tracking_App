#!/usr/bin/env python3
"""
Quick Start Script for Bioluminescent Detection AI Model

This script provides a simple demonstration of the core functionality
for users who want to get started quickly.
"""

import numpy as np
from bioluminescence_model import BioluminescenceModel

def main():
    """Quick start demonstration."""
    print("🚀 Bioluminescent Detection AI Model - Quick Start")
    print("=" * 50)
    
    # Initialize the model
    print("\n1. Initializing AI Model...")
    model = BioluminescenceModel()
    print("✓ Model ready!")
    
    # Example 1: Basic prediction
    print("\n2. Basic Prediction Example")
    print("-" * 30)
    
    result = model.predict(
        activation_time=45,      # minutes
        water_temp=8.5,          # °C
        wind_speed=5.2,          # m/s
        precipitation=2.4,       # mm/hr
        wave_height=1.2,         # m
        ambient_light=0.002,     # lux (moonless night)
        sensor_type='drone'      # DJI M30T
    )
    
    print(f"Predicted max detection distance: {result['distance']:.0f} meters")
    print(f"Confidence interval: {result['confidence_interval'][0]:.0f} - {result['confidence_interval'][2]:.0f} m")
    print(f"Performance score: {result['performance_score']:.1f}%")
    
    if result['failure_flags']:
        print(f"⚠ Warnings: {', '.join(result['failure_flags'])}")
    
    # Example 2: Environmental comparison
    print("\n3. Environmental Conditions Comparison")
    print("-" * 40)
    
    conditions = {
        'Calm Night': {'wind_speed': 1.0, 'precipitation': 0.0, 'wave_height': 0.1},
        'Windy Night': {'wind_speed': 12.0, 'precipitation': 0.0, 'wave_height': 1.5},
        'Rainy Night': {'wind_speed': 3.0, 'precipitation': 8.0, 'wave_height': 0.8},
        'Storm Night': {'wind_speed': 18.0, 'precipitation': 25.0, 'wave_height': 3.0}
    }
    
    base_params = {
        'activation_time': 60,
        'water_temp': 10.0,
        'ambient_light': 0.005,
        'sensor_type': 'drone'
    }
    
    for condition_name, env_params in conditions.items():
        test_params = {**base_params, **env_params}
        result = model.predict(**test_params)
        print(f"{condition_name:12}: {result['distance']:5.0f} m")
    
    # Example 3: Sensor comparison
    print("\n4. Sensor Type Comparison")
    print("-" * 30)
    
    sensors = ['human', 'drone', 'nvg']
    sensor_names = ['Human Eye', 'Drone Camera', 'Night Vision']
    
    base_params = {
        'activation_time': 45,
        'water_temp': 8.5,
        'wind_speed': 5.2,
        'precipitation': 2.4,
        'wave_height': 1.2,
        'ambient_light': 0.002
    }
    
    for sensor, name in zip(sensors, sensor_names):
        result = model.predict(**base_params, sensor_type=sensor)
        print(f"{name:12}: {result['distance']:5.0f} m")
    
    # Example 4: Time decay analysis
    print("\n5. Bioluminescence Time Decay Analysis")
    print("-" * 40)
    
    times = [0, 30, 60, 90, 120, 180, 240, 300, 360]  # minutes
    
    base_params = {
        'water_temp': 10.0,
        'wind_speed': 5.0,
        'precipitation': 0.0,
        'wave_height': 0.5,
        'ambient_light': 0.005,
        'sensor_type': 'drone'
    }
    
    print("Time (min) | Distance (m) | Performance (%)")
    print("-" * 40)
    
    for t in times:
        result = model.predict(activation_time=t, **base_params)
        print(f"{t:9} | {result['distance']:11.0f} | {result['performance_score']:13.1f}")
    
    print("\n" + "=" * 50)
    print("🎯 Quick Start Complete!")
    print("\nNext steps:")
    print("• Run 'python example_usage.py' for comprehensive examples")
    print("• Start the API server: 'uvicorn api.main:app --reload'")
    print("• View API documentation: http://localhost:8000/docs")
    print("• Run tests: 'python run_tests.py'")

if __name__ == "__main__":
    main() 