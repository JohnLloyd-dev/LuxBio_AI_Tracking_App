# Input Data Format Specification for Bioluminescent Detection AI Model

## Overview

This document provides the complete specification for input data formats accepted by the Bioluminescent Detection AI Model. The system supports multiple input formats with comprehensive validation and processing capabilities.

## Table of Contents

1. [Core Data Structure](#1-core-data-structure)
2. [Detailed Field Specifications](#2-detailed-field-specifications)
3. [Accepted Input Formats](#3-accepted-input-formats)
4. [Data Validation Rules](#4-data-validation-rules)
5. [Data Collection Protocol](#5-data-collection-protocol)
6. [Example Field Data Collection](#6-example-field-data-collection)
7. [Special Cases Handling](#7-special-cases-handling)
8. [API Integration](#8-api-integration)
9. [Error Handling](#9-error-handling)

---

## 1. Core Data Structure

### CSV Format (Recommended for Field Data)

The system accepts a simplified CSV format optimized for field data collection with 8 key parameters:

```csv
test_id,date,lat,lon,actual_distance,activation_time,water_temp,wind_speed,precipitation,wave_height,ambient_light,sensor_type,notes
VH-001,2024-01-15,48.423,-123.367,320,45,8.5,5.2,2.4,1.2,0.002,drone,Moderate conditions - successful detection
```

### JSON Format (For API Integration)

```json
{
  "test_id": "VH-001",
  "date": "2024-01-15",
  "location": {
    "lat": 48.423,
    "lon": -123.367
  },
  "actual_distance": 320,
  "activation_time": 45,
  "water_temp": 8.5,
  "wind_speed": 5.2,
  "precipitation": 2.4,
  "wave_height": 1.2,
  "ambient_light": 0.002,
  "sensor_type": "drone",
  "notes": "Moderate conditions - successful detection"
}
```

---

## 2. Detailed Field Specifications

Based on the Comprehensive Field Data Collection Guide, the system uses 8 key parameters optimized for field measurement:

| **Parameter**     | **Type**       | **Units** | **Range**  | **Required** | **Description**                       | **Measurement Method**                |
| ----------------- | -------------- | --------- | ---------- | ------------ | ------------------------------------- | ------------------------------------- |
| **actual_distance** | float          | meters    | 0-1000     | Yes          | Maximum visibility range where markers detectable | GPS distance from activation point to detection boundary |
| **activation_time** | float          | minutes   | 0-360      | Yes          | Time elapsed since bead activation    | Stopwatch from activation moment      |
| **water_temp**    | float          | °C        | -2 to 30   | Yes          | Water temperature at deployment depth | Digital thermometer 0.5m below surface |
| **wind_speed**    | float          | m/s       | 0-25       | Yes          | Sustained wind speed at 10m height    | Anemometer app or handheld device     |
| **precipitation** | float          | mm/hr     | 0-50       | Yes          | Liquid precipitation intensity        | Rain gauge or visual estimation       |
| **wave_height**   | float          | m         | 0-10       | Yes          | Significant wave height (trough to crest) | Visual reference or wave timing method |
| **ambient_light** | float          | lux       | 0.0001-0.1 | Yes          | Background illumination level        | Lux meter app pointing straight up    |
| **sensor_type**   | string         | -         | enum       | Yes          | Detection technology used             | Record as "human", "drone", or "nvg"  |

### Sensor Type Definitions

```python
SENSOR_TYPES = {
    "human": "Unaided vision (even with binoculars)",
    "drone": "Any UAV camera system", 
    "nvg": "Any night vision device"
}

SENSOR_THRESHOLDS = {
    "human": 0.001,    # Human eye detection threshold (lux)
    "drone": 0.005,    # Drone camera detection threshold (lux)
    "nvg": 0.0005      # Night vision goggles threshold (lux)
}
```

---

## 3. Accepted Input Formats

### Option 1: CSV (Recommended for Field Data)

**Single Test Record:**

```csv
test_id,date,lat,lon,actual_distance,activation_time,water_temp,wind_speed,precipitation,wave_height,ambient_light,sensor_type,notes
VH-001,2024-01-15,48.423,-123.367,320,45,8.5,5.2,2.4,1.2,0.002,drone,Moderate conditions - successful detection
```

**Bulk Test Records:**

```csv
test_id,date,lat,lon,actual_distance,activation_time,water_temp,wind_speed,precipitation,wave_height,ambient_light,sensor_type,notes
VH-001,2024-01-15,48.423,-123.367,320,45,8.5,5.2,2.4,1.2,0.002,drone,Moderate conditions
VH-001,2024-01-15,48.423,-123.367,520,45,8.5,5.2,2.4,1.2,0.002,nvg,Same conditions with NVG
VH-002,2024-01-15,48.425,-123.365,280,60,8.4,5.5,2.1,1.3,0.002,human,Clear conditions
```

### Option 2: JSON (For API Integration)

**Single Prediction:**

```json
{
  "test_id": "VH-001",
  "date": "2024-01-15",
  "location": {
    "lat": 48.423,
    "lon": -123.367
  },
  "actual_distance": 320,
  "activation_time": 45,
  "water_temp": 8.5,
  "wind_speed": 5.2,
  "precipitation": 2.4,
  "wave_height": 1.2,
  "ambient_light": 0.002,
  "sensor_type": "drone",
  "notes": "Moderate conditions - successful detection"
}
```
```

**Bulk Predictions:**

```json
[
  {
    "test_id": "VH-001",
    "date": "2024-01-15",
    "location": {
      "lat": 48.423,
      "lon": -123.367
    },
    "actual_distance": 320,
    "activation_time": 45,
    "water_temp": 8.5,
    "wind_speed": 5.2,
    "precipitation": 2.4,
    "wave_height": 1.2,
    "ambient_light": 0.002,
    "sensor_type": "drone",
    "notes": "Moderate conditions"
  },
  {
    "test_id": "VH-001",
    "date": "2024-01-15",
    "location": {
      "lat": 48.423,
      "lon": -123.367
    },
    "actual_distance": 520,
    "activation_time": 45,
    "water_temp": 8.5,
    "wind_speed": 5.2,
    "precipitation": 2.4,
    "wave_height": 1.2,
    "ambient_light": 0.002,
    "sensor_type": "nvg",
    "notes": "Same conditions with NVG"
  }
]
```

### Option 3: Legacy CSV Format (Deprecated)

For backward compatibility, the system still accepts the legacy format:

```csv
parameter_category,parameter,value,units
temporal,activation_time,45.0,minutes
temporal,water_temperature,8.5,C
environmental,wind_speed,5.2,m/s
environmental,precipitation,2.4,mm/hr
environmental,wave_height,1.2,m
environmental,ambient_light,0.002,lux
sensor,type,drone,na
```

### Option 4: Legacy Bulk CSV Format (Deprecated)

```csv
activation_time,water_temp,wind_speed,precip,wave_ht,ambient_light,sensor_type
45.0,8.5,5.2,2.4,1.2,0.002,drone
60.0,10.2,3.1,0.0,0.5,0.0005,nvg
30.0,5.8,12.4,8.7,2.3,0.01,human
```

> **Note**: The new simplified CSV format (Option 1) is recommended for all new field data collection.

---

## 4. Data Validation Rules

### Range Validation

```python
# Actual distance validation (0-1000m)
if not (0 <= actual_distance <= 1000):
    raise ValueError("Actual distance must be 0-1000 meters")

# Activation time validation (0-360 minutes)
if not (0 <= activation_time <= 360):
    raise ValueError("Activation time must be 0-360 minutes")

# Water temperature validation (-2 to 30°C)
if not (-2 <= water_temp <= 30):
    raise ValueError("Water temperature must be -2 to 30°C")

# Wind speed validation (0-25 m/s)
if not (0 <= wind_speed <= 25):
    raise ValueError("Wind speed must be 0-25 m/s")

# Precipitation validation (0-50 mm/hr)
if not (0 <= precipitation <= 50):
    raise ValueError("Precipitation must be 0-50 mm/hr")

# Wave height validation (0-10 m)
if not (0 <= wave_height <= 10):
    raise ValueError("Wave height must be 0-10 meters")

# Ambient light validation (0.0001-0.1 lux)
if not (0.0001 <= ambient_light <= 0.1):
    raise ValueError("Ambient light must be 0.0001-0.1 lux")
```

### Sensor Type Validation

```python
VALID_SENSOR_TYPES = ["human", "drone", "nvg"]

if sensor_type not in VALID_SENSOR_TYPES:
    raise ValueError(f"Sensor type must be one of: {VALID_SENSOR_TYPES}")
```

### GPS Coordinate Validation

```python
# Latitude validation (-90 to 90)
if not (-90 <= lat <= 90):
    raise ValueError("Latitude must be -90 to 90 degrees")

# Longitude validation (-180 to 180)
if not (-180 <= lon <= 180):
    raise ValueError("Longitude must be -180 to 180 degrees")
```

### Data Quality Checks

```python
# Check for missing required fields
REQUIRED_FIELDS = [
    'test_id', 'date', 'lat', 'lon', 'actual_distance',
    'activation_time', 'water_temp', 'wind_speed', 
    'precipitation', 'wave_height', 'ambient_light', 'sensor_type'
]

for field in REQUIRED_FIELDS:
    if field not in data or data[field] is None:
        raise ValueError(f"Missing required field: {field}")
```

---

## 5. Data Collection Protocol

### Field Data Collection Kit ($150 Total)

Based on the Comprehensive Field Data Collection Guide, the following equipment is recommended:

| **Item** | **Purpose** | **Cost** | **Measurement Method** |
|----------|-------------|----------|------------------------|
| Waterproof phone case | All measurements | $15 | Protection for all devices |
| Digital thermometer | Water temperature | $8 | Submerge 0.5m below surface |
| Rain gauge | Precipitation | $5 | Measure mm collected in 10 minutes |
| Stopwatch | Activation timing | $10 | Start at bead activation |
| Anemometer | Wind speed | $25 | 1-minute average at 10m height |
| GPS app | Distance/location | Free | Calculate GPS distance |
| Lux Light Meter app | Ambient light | Free | Point phone straight up |
| Field notebook | Manual recording | $5 | Backup data recording |

### Measurement Protocols

#### 1. Actual Distance (0-1000 m)
- Activate beads at Point A (record GPS)
- Move observer/drone to increasing distances
- Record GPS at detection boundary (Point B)
- Calculate: `distance = GPS_distance(A,B)`

#### 2. Activation Time (0-360 min)
- Start stopwatch at activation ("t=0")
- Record test time relative to activation
- Round to nearest minute

#### 3. Water Temperature (-2 to 30°C)
- Submerge thermometer 0.5m below surface
- Wait 1 minute for stabilization
- Measure within 5m of marker deployment

#### 4. Wind Speed (0-25 m/s)
- Use anemometer app or handheld device
- Record 1-minute average at 10m height
- Cross-check with Beaufort scale

#### 5. Precipitation (0-50 mm/hr)
- Place rain gauge in open area
- Measure mm collected in 10 minutes
- Multiply by 6 for mm/hr

#### 6. Wave Height (0-10 m)
- Use visual reference or wave timing method
- Estimate average of highest 1/3 waves
- Boat reference: waist-height = ~1.2m

#### 7. Ambient Light (0.0001-0.1 lux)
- Open light meter app
- Point phone straight up
- Record stable reading

#### 8. Sensor Type (human/drone/nvg)
- Record detection technology used
- Test all available sensors separately
- Note model if known

### Data Validation Checklist

Before submitting data:
1. GPS coordinates within 10m accuracy ✅
2. All values within physical ranges ✅
3. Timestamps consistent across measurements ✅
4. Sensor type clearly specified ✅
5. Wave height matches precipitation/wind ✅

---

## 6. Example Field Data Collection

### Complete Field Dataset Example

Based on the Comprehensive Field Data Collection Guide, here's a complete example:

```csv
test_id,date,lat,lon,actual_distance,activation_time,water_temp,wind_speed,precipitation,wave_height,ambient_light,sensor_type,notes
VH-23,2023-08-15,48.423,-123.367,320,45,8.5,5.2,2.4,1.2,0.002,drone,Moderate conditions - successful detection
VH-23,2023-08-15,48.423,-123.367,520,45,8.5,5.2,2.4,1.2,0.002,nvg,Same conditions with NVG - better range
VH-24,2023-08-15,48.425,-123.365,180,60,8.4,5.5,2.1,1.3,0.002,human,Clear conditions - human observer
VH-25,2023-08-15,48.427,-123.363,450,75,8.6,5.8,1.8,1.1,0.002,drone,Calming conditions - optimal detection
```

### Field Measurement Process

1. **Setup (22:00)**: Deploy weather station, calibrate instruments
2. **Activation (22:15)**: Activate bioluminescent beads, start stopwatch
3. **Test Series (22:30-23:30)**: 
   - Measure environmental conditions every 5 minutes
   - Test detection range with different sensors
   - Record GPS coordinates at detection boundaries
4. **Data Compilation**: Combine all measurements into CSV format

### Environmental Conditions Log

```csv
timestamp,lat,lon,wind_speed,precipitation,wave_height,ambient_light,water_temp
2023-08-15T22:30:00Z,48.423,-123.367,5.2,2.4,1.2,0.002,8.5
2023-08-15T22:35:00Z,48.423,-123.367,5.5,2.1,1.3,0.002,8.4
2023-08-15T22:40:00Z,48.423,-123.367,5.8,1.8,1.1,0.002,8.6
```

### Detection Results Summary

| Test ID | Sensor | Distance (m) | Conditions | Notes |
|---------|--------|--------------|------------|-------|
| VH-23 | Drone | 320 | Moderate | Successful detection |
| VH-23 | NVG | 520 | Moderate | 62% range improvement |
| VH-24 | Human | 180 | Clear | Limited by human vision |
| VH-25 | Drone | 450 | Calm | Optimal conditions |
    "ambient_light": 0.002
  },
  "sensor_parameters": {
    "type": "drone"
  }
}
```

---

## 7. Special Cases Handling

### Missing Data

```python
# Default values for optional parameters
DEFAULT_VALUES = {
    "water_turbidity": 1.5,    # Default coastal water
    "current_speed": 0.0,      # Default no current
    "bead_density": 350,       # Default bead count
    "spectral_range": None     # Default no spectral range
}

# Apply defaults for missing data
for param, default_value in DEFAULT_VALUES.items():
    if param not in data:
        data[param] = default_value
```

### Extreme Conditions

```python
# Wind speed handling
if wind_speed > 25:
    wind_speed = 25.0
    warnings.append("Wind speed capped at 25 m/s")

# Wave height handling
if wave_height > 10:
    wave_height = 10.0
    warnings.append("Wave height capped at 10 m")

# Return "0 visibility" for extreme conditions
if wind_speed > 20 and wave_height > 5:
    return {"distance": 0, "warning": "Extreme conditions - no visibility"}
```

### Night Vision Goggles (NVG)

```python
# Special handling for NVG
if sensor_type == "nvg":
    ambient_light = max(ambient_light, 1e-5)  # Avoid division by zero
    warnings.append("Ambient light adjusted for NVG operation")
```

---

## 8. API Integration

### REST API Endpoints

```bash
# Single prediction
POST /predict
Content-Type: application/json

# Bulk predictions
POST /predict/bulk
Content-Type: application/json

# Input validation only
POST /validate/input
Content-Type: application/json

# Upload weather station data
POST /upload/weather-station
Content-Type: multipart/form-data
```

### Example API Calls

```bash
# Single prediction
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "temporal_parameters": {
         "activation_time": 45.0,
         "water_temperature": 8.5
       },
       "environmental_conditions": {
         "wind_speed": 5.2,
         "precipitation": 2.4,
         "wave_height": 1.2,
         "ambient_light": 0.002
       },
       "sensor_parameters": {
         "type": "drone"
       }
     }'

# Bulk predictions
curl -X POST "http://localhost:8000/predict/bulk" \
     -H "Content-Type: application/json" \
     -d '{
       "predictions": [
         {
           "temporal_parameters": {"activation_time": 45.0, "water_temperature": 8.5},
           "environmental_conditions": {"wind_speed": 5.2, "precipitation": 2.4, "wave_height": 1.2, "ambient_light": 0.002},
           "sensor_parameters": {"type": "drone"}
         }
       ]
     }'
```

### Python SDK Usage

```python
from data_models import DataProcessor, DetectionInput
from bioluminescence_model import BioluminescenceModel

# Initialize components
data_processor = DataProcessor()
model = BioluminescenceModel()

# Validate input
input_data = {
    "temporal_parameters": {"activation_time": 45.0, "water_temperature": 8.5},
    "environmental_conditions": {"wind_speed": 5.2, "precipitation": 2.4, "wave_height": 1.2, "ambient_light": 0.002},
    "sensor_parameters": {"type": "drone"}
}

validation_result = data_processor.validate_json_input(input_data)

if validation_result.is_valid:
    # Convert to model input
    model_input = data_processor.convert_to_model_input(validation_result.processed_data)

    # Make prediction
    result = model.predict(**model_input)
    print(f"Predicted distance: {result['distance']:.0f} m")
else:
    print(f"Validation errors: {validation_result.errors}")
```

---

## 9. Error Handling

### Validation Error Types

```python
class ValidationError(Exception):
    """Base class for validation errors"""
    pass

class RangeError(ValidationError):
    """Parameter value outside valid range"""
    pass

class MissingFieldError(ValidationError):
    """Required field missing"""
    pass

class UnitConversionError(ValidationError):
    """Error in unit conversion"""
    pass
```

### Error Response Format

```json
{
  "error": "Validation failed",
  "details": {
    "field": "wind_speed",
    "value": 30.0,
    "message": "Wind speed exceeds maximum of 25 m/s",
    "suggestion": "Value will be capped at 25 m/s"
  },
  "warnings": [
    "Wind speed capped at 25 m/s",
    "Ambient light adjusted for NVG operation"
  ]
}
```

### Common Error Codes

| **Error Code**       | **Description**             | **Solution**                    |
| -------------------- | --------------------------- | ------------------------------- |
| `MISSING_FIELD`      | Required field not provided | Add missing field               |
| `INVALID_RANGE`      | Value outside valid range   | Adjust value to valid range     |
| `INVALID_SENSOR`     | Unsupported sensor type     | Use: human, drone, or nvg       |
| `UNIT_CONVERSION`    | Error in unit conversion    | Check unit specification        |
| `EXTREME_CONDITIONS` | Conditions too extreme      | Reduce environmental parameters |

---

## Summary

This input format specification ensures:

✅ **Consistent Data Structure**: Standardized format across all inputs
✅ **Comprehensive Validation**: Range checks, type validation, and unit conversion
✅ **Flexible Input Methods**: JSON, CSV, and bulk processing support
✅ **Error Handling**: Clear error messages and suggestions
✅ **Extensibility**: Easy to add new parameters and validation rules
✅ **Integration Ready**: Compatible with existing systems and APIs

The specification supports both simple single predictions and complex bulk processing scenarios, making it suitable for both research and operational deployment environments.
