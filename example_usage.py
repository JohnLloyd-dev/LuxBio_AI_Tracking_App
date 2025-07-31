"""
Example Usage of Bioluminescent Detection AI Model

This script demonstrates the complete functionality of the bioluminescent
bead detection distance prediction system, including model prediction,
validation, calibration, and deployment scenarios.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json

# Import the model components
from bioluminescence_model import BioluminescenceModel, ModelParameters
from validation import ModelValidator, TestCondition
from deployment_controller import DeploymentController, EnvironmentalConditions

def main():
    """
    Main demonstration function showing all system capabilities.
    """
    print("=== Bioluminescent Detection AI Model Demonstration ===\n")
    
    # 1. Initialize the model
    print("1. Initializing AI Model...")
    model = BioluminescenceModel()
    print("✓ Model initialized with default parameters\n")
    
    # 2. Basic prediction example
    print("2. Basic Prediction Example...")
    basic_prediction_demo(model)
    
    # 3. Environmental condition analysis
    print("\n3. Environmental Condition Analysis...")
    environmental_analysis_demo(model)
    
    # 4. Model validation
    print("\n4. Model Validation...")
    validation_demo(model)
    
    # 5. Model calibration
    print("\n5. Model Calibration...")
    calibration_demo(model)
    
    # 6. Deployment scenario
    print("\n6. Deployment Scenario...")
    deployment_demo(model)
    
    # 7. Performance analysis
    print("\n7. Performance Analysis...")
    performance_analysis_demo(model)
    
    print("\n=== Demonstration Complete ===")

def basic_prediction_demo(model):
    """Demonstrate basic prediction functionality."""
    
    # Example scenario from the specification
    scenario = {
        'activation_time': 45,      # minutes
        'water_temp': 8.5,          # °C
        'wind_speed': 5.2,          # m/s
        'precipitation': 2.4,       # mm/hr
        'wave_height': 1.2,         # m
        'ambient_light': 0.002,     # lux (moonless night)
        'sensor_type': 'drone'      # DJI M30T
    }
    
    print(f"Scenario: {scenario}")
    
    # Make prediction
    result = model.predict(**scenario)
    
    print(f"✓ Predicted max distance: {result['distance']:.0f} m")
    print(f"✓ Confidence interval: [{result['confidence_interval'][0]:.0f}, "
          f"{result['confidence_interval'][1]:.0f}, {result['confidence_interval'][2]:.0f}] m")
    print(f"✓ Performance score: {result['performance_score']:.1f}%")
    print(f"✓ System conditions: {result['system_conditions']}")
    
    if result['failure_flags']:
        print(f"⚠ Warning flags: {result['failure_flags']}")

def environmental_analysis_demo(model):
    """Demonstrate how environmental conditions affect detection."""
    
    # Base conditions
    base_conditions = {
        'activation_time': 60,
        'water_temp': 10.0,
        'wind_speed': 5.0,
        'precipitation': 0.0,
        'wave_height': 0.5,
        'ambient_light': 0.005,
        'sensor_type': 'drone'
    }
    
    # Test different environmental conditions
    conditions = {
        'Calm': {'wind_speed': 1.0, 'precipitation': 0.0, 'wave_height': 0.1},
        'Windy': {'wind_speed': 12.0, 'precipitation': 0.0, 'wave_height': 1.5},
        'Rainy': {'wind_speed': 3.0, 'precipitation': 8.0, 'wave_height': 0.8},
        'Storm': {'wind_speed': 18.0, 'precipitation': 25.0, 'wave_height': 3.0}
    }
    
    results = {}
    
    for condition_name, env_params in conditions.items():
        test_conditions = base_conditions.copy()
        test_conditions.update(env_params)
        
        result = model.predict(**test_conditions)
        results[condition_name] = result['distance']
        
        print(f"  {condition_name}: {result['distance']:.0f} m "
              f"(attenuation: {result['system_conditions'][1]})")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    conditions_list = list(results.keys())
    distances = list(results.values())
    
    bars = plt.bar(conditions_list, distances, color=['green', 'yellow', 'orange', 'red'])
    plt.title('Detection Distance vs Environmental Conditions')
    plt.ylabel('Detection Distance (m)')
    plt.xlabel('Environmental Condition')
    
    # Add value labels on bars
    for bar, distance in zip(bars, distances):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f'{distance:.0f}m', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('environmental_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Environmental analysis plot saved as 'environmental_analysis.png'")

def validation_demo(model):
    """Demonstrate model validation capabilities."""
    
    print("Running comprehensive validation tests...")
    
    # Initialize validator
    validator = ModelValidator(model)
    
    # Run validation tests
    validation_report = validator.run_validation_tests()
    
    # Display key metrics
    metrics = validation_report['validation_metrics']
    print(f"✓ MAE: {metrics['MAE']:.1f} m")
    print(f"✓ MAPE: {metrics['MAPE']:.1f}%")
    print(f"✓ R²: {metrics['R2']:.3f}")
    print(f"✓ Coverage: {metrics['Coverage']:.1f}%")
    print(f"✓ Operational Accuracy: {metrics['Operational_Accuracy']:.1f}%")
    
    # Display performance assessment
    assessment = validation_report['performance_assessment']
    print(f"✓ Overall Grade: {assessment['overall_grade']}")
    
    # Generate plots
    validator.plot_validation_results('validation_results.png')
    print("✓ Validation plots saved as 'validation_results.png'")
    
    # Save report
    validator.save_validation_report('validation_report.json')
    print("✓ Validation report saved as 'validation_report.json'")

def calibration_demo(model):
    """Demonstrate model calibration with field data."""
    
    print("Generating synthetic field data for calibration...")
    
    # Generate synthetic field data
    np.random.seed(42)  # For reproducible results
    
    field_data = []
    for i in range(20):
        # Generate realistic field conditions
        activation_time = np.random.uniform(30, 180)
        water_temp = np.random.uniform(-1, 25)
        wind_speed = np.random.uniform(0, 20)
        precipitation = np.random.uniform(0, 30)
        wave_height = np.random.uniform(0, 5)
        ambient_light = np.random.uniform(0.001, 0.05)
        sensor_type = np.random.choice(['human', 'drone', 'nvg'])
        
        # Generate "actual" distance with some noise
        test_params = {
            'activation_time': activation_time,
            'water_temp': water_temp,
            'wind_speed': wind_speed,
            'precipitation': precipitation,
            'wave_height': wave_height,
            'ambient_light': ambient_light,
            'sensor_type': sensor_type
        }
        
        # Get prediction and add realistic noise
        prediction = model.predict(**test_params)
        actual_distance = prediction['distance'] * np.random.uniform(0.8, 1.2)
        
        field_data.append({
            'actual_distance': actual_distance,
            **test_params
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(field_data)
    
    print(f"✓ Generated {len(field_data)} field data points")
    
    # Perform calibration
    print("Calibrating model parameters...")
    optimized_params = model.calibrate_parameters(df)
    
    print("✓ Calibration completed")
    print("Optimized parameters:")
    for param, value in optimized_params.items():
        print(f"  {param}: {value:.6f}")
    
    # Test improvement
    print("\nTesting calibration improvement...")
    before_errors = []
    after_errors = []
    
    for _, row in df.iterrows():
        # Calculate error before calibration
        before_result = model.predict(
            activation_time=row['activation_time'],
            water_temp=row['water_temp'],
            wind_speed=row['wind_speed'],
            precipitation=row['precipitation'],
            wave_height=row['wave_height'],
            ambient_light=row['ambient_light'],
            sensor_type=row['sensor_type']
        )
        before_errors.append(abs(before_result['distance'] - row['actual_distance']))
    
    print(f"✓ Before calibration MAE: {np.mean(before_errors):.1f} m")
    print(f"✓ After calibration MAE: {model.calibration_history[-1]['error']:.1f} m")

def deployment_demo(model):
    """Demonstrate deployment controller functionality."""
    
    print("Initializing deployment controller...")
    
    # Initialize deployment controller
    controller = DeploymentController(model)
    
    # Set mission parameters
    controller.set_mission_parameters(
        search_altitude=75.0,
        search_speed=8.0,
        camera_fov=45.0,
        detection_interval=1.5
    )
    
    # Create environmental conditions
    env_conditions = EnvironmentalConditions(
        wind_speed=6.5,
        wind_direction=180.0,
        precipitation=1.2,
        wave_height=0.8,
        water_temp=12.0,
        ambient_light=0.003,
        timestamp=datetime.now().timestamp()
    )
    
    # Define search area
    search_center = (47.6062, -122.3321)  # Seattle coordinates
    search_radius = 800.0  # meters
    
    print(f"Executing marker test at {search_center}...")
    
    # Execute marker test
    mission_result = controller.execute_marker_test(
        env_conditions=env_conditions,
        activation_time=90,  # 90 minutes since activation
        search_center=search_center,
        search_radius=search_radius
    )
    
    print(f"✓ Mission completed in {mission_result['mission_duration']:.1f} seconds")
    print(f"✓ Predicted distance: {mission_result['predicted_distance']:.0f} m")
    print(f"✓ Detections found: {len([d for d in mission_result['detections'] if d['detected']])}")
    
    # Display analysis
    analysis = mission_result['analysis']
    print(f"✓ Mission success: {analysis['mission_success']}")
    if analysis['mission_success']:
        print(f"✓ Max detection distance: {analysis['max_detection_distance']:.0f} m")
        print(f"✓ Prediction accuracy: {analysis['prediction_accuracy']}")

def performance_analysis_demo(model):
    """Demonstrate comprehensive performance analysis."""
    
    print("Performing comprehensive performance analysis...")
    
    # Test different activation times
    activation_times = np.linspace(0, 360, 37)  # 0 to 6 hours
    distances = []
    performance_scores = []
    
    base_conditions = {
        'water_temp': 10.0,
        'wind_speed': 5.0,
        'precipitation': 0.0,
        'wave_height': 0.5,
        'ambient_light': 0.005,
        'sensor_type': 'drone'
    }
    
    for t in activation_times:
        result = model.predict(activation_time=t, **base_conditions)
        distances.append(result['distance'])
        performance_scores.append(result['performance_score'])
    
    # Create performance plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Distance vs time
    ax1.plot(activation_times, distances, 'b-', linewidth=2)
    ax1.set_xlabel('Activation Time (minutes)')
    ax1.set_ylabel('Detection Distance (m)')
    ax1.set_title('Detection Distance vs Activation Time')
    ax1.grid(True, alpha=0.3)
    
    # Performance score vs time
    ax2.plot(activation_times, performance_scores, 'r-', linewidth=2)
    ax2.set_xlabel('Activation Time (minutes)')
    ax2.set_ylabel('Performance Score (%)')
    ax2.set_title('Model Performance Score vs Activation Time')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Performance analysis plots saved as 'performance_analysis.png'")
    
    # Display key insights
    max_distance_idx = np.argmax(distances)
    max_distance_time = activation_times[max_distance_idx]
    max_distance = distances[max_distance_idx]
    
    print(f"✓ Peak detection distance: {max_distance:.0f} m at {max_distance_time:.0f} minutes")
    print(f"✓ Average performance score: {np.mean(performance_scores):.1f}%")
    
    # Model information
    model_info = model.get_model_info()
    print(f"✓ Model version: {model_info['model_version']}")
    print(f"✓ Calibration iterations: {len(model_info['calibration_history'])}")

if __name__ == "__main__":
    main() 