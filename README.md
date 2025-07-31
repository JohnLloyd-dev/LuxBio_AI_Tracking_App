# Bioluminescent Bead Detection Distance Prediction AI Model

## Overview

This AI system predicts the maximum detection distance for bioluminescent beads under various environmental conditions. The model combines physics-based light decay modeling with machine learning calibration to provide accurate distance predictions for drone-based search and rescue operations.

## Key Features

- **Physics-based light decay modeling** using Arrhenius kinetics
- **Environmental attenuation modeling** for wind, rain, and wave effects
- **Bayesian optimization** for parameter calibration
- **Uncertainty quantification** with Monte Carlo simulation
- **Real-time API** for operational deployment
- **Continuous learning** from field validation data

## Architecture

The system consists of several interconnected modules:

1. **Light Decay Module**: Models bioluminescence intensity over time and temperature
2. **Environmental Attenuation Module**: Calculates light attenuation from environmental factors
3. **Detection Threshold Module**: Determines minimum detectable light levels
4. **Distance Solver**: Computes maximum detection distance
5. **Calibration Engine**: Optimizes model parameters using field data
6. **API Interface**: Provides real-time prediction capabilities

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from bioluminescence_model import BioluminescenceModel

# Initialize model
model = BioluminescenceModel()

# Make prediction
result = model.predict(
    activation_time=45,      # minutes
    water_temp=8.5,          # °C
    wind_speed=5.2,          # m/s
    precipitation=2.4,       # mm/hr
    wave_height=1.2,         # m
    ambient_light=0.002,     # lux
    sensor_type="drone"
)

print(f"Max detection distance: {result['distance']:.0f} m")
print(f"Confidence interval: {result['confidence_interval']}")
```

## API Usage

Start the API server:

```bash
uvicorn api.main:app --reload
```

Make predictions via HTTP:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "activation_time": 45,
       "water_temp": 8.5,
       "wind_speed": 5.2,
       "precipitation": 2.4,
       "wave_height": 1.2,
       "ambient_light": 0.002,
       "sensor_type": "drone"
     }'
```

## Model Components

### Core Mathematical Framework

1. **Light Decay**: `I(t,T) = I₀ · e^(-[A·e^(-Eₐ/(R·Tₖ))]·t)`
2. **Attenuation**: `c = α₀ + α₁·U_w^β + α₂·P + α₃·H_s + α₄·P·H_s`
3. **Detection Threshold**: `I_th = k_sensor + γ·I_ambient`
4. **Max Distance**: `d_max = (1/c) · ln(I(t,T)/I_th)`

### Input Parameters

| Category      | Parameters        | Units | Range           |
| ------------- | ----------------- | ----- | --------------- |
| Temporal      | Activation time   | min   | 0-360           |
|               | Water temperature | °C    | -2 to 30        |
| Environmental | Wind speed        | m/s   | 0-25            |
|               | Precipitation     | mm/hr | 0-50            |
|               | Wave height       | m     | 0-10            |
|               | Ambient light     | lux   | 0.0001-0.1      |
| Sensor        | Type              | -     | human/drone/nvg |

### Output Specifications

| Output              | Format           | Description             |
| ------------------- | ---------------- | ----------------------- |
| Max distance        | Meters           | Detection limit         |
| Confidence interval | [low, med, high] | 90% prediction interval |
| Performance score   | 0-100%           | Model confidence        |
| Failure flags       | Text             | Diagnostic messages     |

## Validation Protocol

The model includes comprehensive validation procedures:

- **Field Test Matrix**: Systematic testing across environmental conditions
- **Validation Metrics**: MAE, MAPE, R², Coverage, Operational Accuracy
- **Continuous Improvement**: Adaptive learning from new field data

## Performance Targets

- Prediction time: < 100 ms per scenario
- Accuracy: > 90% within 15% error
- Calibration convergence: < 50 iterations

## License

This project is proprietary to Lux Bio and contains confidential algorithms for bioluminescent detection systems.
