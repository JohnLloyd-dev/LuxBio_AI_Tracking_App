# Data Format Files for LuxBio AI Tracking App

This directory contains comprehensive templates and examples for the LuxBio AI Tracking App, optimized for field data collection and model training.

## 📁 File Overview

| File                                 | Purpose                 | Format          | Use Case                 |
| ------------------------------------ | ----------------------- | --------------- | ------------------------ |
| `field_data_collection_template.csv` | **Primary field data**  | Simplified CSV  | **Field testing**        |
| `FIELD_DATA_COLLECTION_GUIDE.md`     | **Measurement guide**   | Documentation   | **Field protocols**      |
| `bulk_predictions_template.csv`      | Bulk predictions input  | Row-based       | Multiple scenarios       |
| `weather_station_template.csv`       | Weather station data    | Time-series     | Environmental monitoring |
| `calibration_data_template.csv`      | Model calibration       | Training data   | Model improvement        |
| `validation_scenarios.csv`           | Test scenarios          | Validation      | System testing           |

---

## 📋 File Details

### 1. `single_prediction_template.csv`

**Format:** Parameter-based with categories

```csv
parameter_category,parameter,value,units
temporal,activation_time,45.0,minutes
temporal,water_temperature,8.5,C
environmental,wind_speed,5.2,m/s
...
```

**Usage:**

- Single prediction requests
- API input validation
- Manual data entry

**Required Fields:**

- `activation_time` (0-360 minutes)
- `water_temperature` (-2 to 30°C)
- `wind_speed` (0-25 m/s)
- `precipitation` (0-50 mm/hr)
- `wave_height` (0-10 m)
- `ambient_light` (0.0001-0.1 lux)
- `sensor_type` (human/drone/nvg)

**Optional Fields:**

- `water_turbidity` (0-10 NTU)
- `current_speed` (0-5 knots)
- `sensor_model` (string)
- `spectral_range` (350-900 nm)
- `bead_density` (100-1000 count)
- `batch_id` (string)

### 2. `bulk_predictions_template.csv`

**Format:** Row-based with all parameters

```csv
activation_time,water_temp,wind_speed,precip,wave_ht,ambient_light,sensor_type,...
45.0,8.5,5.2,2.4,1.2,0.002,drone,...
```

**Usage:**

- Multiple scenario predictions
- Batch processing
- Comparative analysis

**Advantages:**

- Compact format
- Easy to edit in spreadsheet software
- Efficient for bulk operations

### 3. `weather_station_template.csv`

**Format:** Time-series environmental data

```csv
timestamp,lat,lon,wind_speed(m/s),precip(mm/hr),wave_height(m),ambient_light(lux),water_temp(C),...
2024-01-15T22:30:00Z,48.423,-123.367,5.2,2.4,1.2,0.002,8.5,...
```

**Usage:**

- Real-time environmental monitoring
- Historical data analysis
- API upload endpoint

**Features:**

- GPS coordinates
- Timestamped data
- Complete environmental parameters

### 1. `field_data_collection_template.csv` ⭐ **PRIMARY FORMAT**

**Format:** Simplified field data collection (8 key parameters)

```csv
test_id,date,lat,lon,actual_distance,activation_time,water_temp,wind_speed,precipitation,wave_height,ambient_light,sensor_type,notes
VH-001,2024-01-15,48.423,-123.367,320,45,8.5,5.2,2.4,1.2,0.002,drone,Moderate conditions - successful detection
```

**Usage:**

- **Primary field data collection**
- **Model training and validation**
- **Performance analysis**

**Key Features:**

- **8 essential parameters** optimized for field measurement
- **GPS coordinates** for location tracking
- **Actual detection distances** for validation
- **Sensor type specification** (human/drone/nvg)
- **Notes field** for observations

**Required Fields:**

- `test_id` - Unique test identifier
- `date` - Test date (YYYY-MM-DD)
- `lat`, `lon` - GPS coordinates
- `actual_distance` - Detection range in meters (0-1000)
- `activation_time` - Minutes since activation (0-360)
- `water_temp` - Water temperature in °C (-2 to 30)
- `wind_speed` - Wind speed in m/s (0-25)
- `precipitation` - Rain intensity in mm/hr (0-50)
- `wave_height` - Wave height in meters (0-10)
- `ambient_light` - Background light in lux (0.0001-0.1)
- `sensor_type` - Detection system (human/drone/nvg)

### 2. `FIELD_DATA_COLLECTION_GUIDE.md` 📋 **MEASUREMENT PROTOCOLS**

**Purpose:** Comprehensive field measurement guide

**Includes:**

- **Detailed measurement protocols** for each parameter
- **Equipment recommendations** ($150 total kit)
- **Troubleshooting guides** for common issues
- **Data validation checklist**
- **Example datasets** and field procedures
- **Quality standards** and acceptable ranges

**Usage:**

- **Field training** for data collectors
- **Protocol reference** during testing
- **Quality assurance** guidelines

### 5. `calibration_data_template.csv`

**Format:** Training data for model calibration

```csv
actual_distance,activation_time,water_temperature,wind_speed,...,test_location,test_date,detection_confidence
427,45.0,8.5,5.2,...,Seattle_Bay,2024-01-15,0.85
```

**Usage:**

- Model parameter calibration
- Performance improvement
- Validation against real data

**Key Features:**

- Actual detection distances
- Comprehensive parameter set
- Location and date tracking
- Confidence scores

### 6. `validation_scenarios.csv`

**Format:** Test scenarios with expected ranges

```csv
scenario_name,activation_time,water_temperature,...,expected_range_min,expected_range_max,notes
Calm_Night_Drone,45.0,8.5,1.0,...,500,600,Optimal conditions for drone detection
```

**Usage:**

- System validation testing
- Performance benchmarking
- Expected range verification

**Features:**

- Named scenarios
- Expected detection ranges
- Detailed notes
- Various environmental conditions

---

## 🔧 Usage Instructions

### For API Integration

**Single Prediction:**

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d @single_prediction_template.json
```

**Bulk Predictions:**

```bash
curl -X POST "http://localhost:8000/predict/bulk" \
     -H "Content-Type: application/json" \
     -d @bulk_predictions_template.json
```

**Weather Station Upload:**

```bash
curl -X POST "http://localhost:8000/upload/weather-station" \
     -F "file=@weather_station_template.csv"
```

### For Python Processing

```python
from data_models import DataProcessor
import pandas as pd

# Load CSV data
df = pd.read_csv('data_formats/bulk_predictions_template.csv')

# Process each row
data_processor = DataProcessor()
for _, row in df.iterrows():
    # Convert row to input format
    input_data = {
        "temporal_parameters": {
            "activation_time": row['activation_time'],
            "water_temperature": row['water_temp']
        },
        "environmental_conditions": {
            "wind_speed": row['wind_speed'],
            "precipitation": row['precip'],
            "wave_height": row['wave_ht'],
            "ambient_light": row['ambient_light']
        },
        "sensor_parameters": {
            "type": row['sensor_type']
        }
    }

    # Validate and predict
    validation_result = data_processor.validate_json_input(input_data)
    if validation_result.is_valid:
        # Make prediction...
        pass
```

### For Field Data Collection ⭐ **PRIMARY WORKFLOW**

1. **Read `FIELD_DATA_COLLECTION_GUIDE.md`** for measurement protocols
2. **Use `field_data_collection_template.csv`** as your base template
3. **Follow the 8-parameter measurement protocol**:
   - Actual distance (GPS measurement)
   - Activation time (stopwatch)
   - Water temperature (thermometer)
   - Wind speed (anemometer)
   - Precipitation (rain gauge)
   - Wave height (visual estimate)
   - Ambient light (lux meter)
   - Sensor type (human/drone/nvg)
4. **Validate data** using the checklist in the guide
5. **Upload to API** for model training and validation

### For Model Calibration

1. **Collect field data** using the templates
2. **Ensure data quality** with proper validation
3. **Upload calibration data** to the API
4. **Monitor model improvement** through validation metrics

---

## 📊 Data Validation Rules

### Required Field Validation

- All 12 required fields must be present
- Values must be within specified ranges
- Units must be correct (m/s, mm/hr, etc.)

### Range Validation (8 Key Parameters)

```python
# Actual distance: 0-1000 meters
# Activation time: 0-360 minutes
# Water temperature: -2 to 30°C
# Wind speed: 0-25 m/s
# Precipitation: 0-50 mm/hr
# Wave height: 0-10 meters
# Ambient light: 0.0001-0.1 lux
# Sensor type: human/drone/nvg
```

### GPS Coordinate Validation

```python
# Latitude: -90 to 90 degrees
# Longitude: -180 to 180 degrees
```

### Sensor Type Validation

```python
VALID_SENSOR_TYPES = ["human", "drone", "nvg"]
```

### Data Quality Standards

- **Distance**: ±10m accuracy for GPS measurements
- **Time**: ±1 minute for activation timing
- **Temperature**: ±0.5°C for water temperature
- **Wind**: ±1 m/s for wind speed
- **Precipitation**: ±1 mm/hr for rain gauge
- **Waves**: ±0.2m for visual estimates
- **Light**: ±20% for lux meter readings

---

## 🚀 Quick Start

1. **Choose the appropriate template** for your use case
2. **Fill in your data** following the format
3. **Validate the data** using the API or Python SDK
4. **Upload or process** the data as needed

### Example Workflow

```bash
# 1. Download template
cp data_formats/single_prediction_template.csv my_prediction.csv

# 2. Edit with your data
# (Use spreadsheet software or text editor)

# 3. Validate and predict
python -c "
from data_models import DataProcessor
import pandas as pd
df = pd.read_csv('my_prediction.csv')
# Process your data...
"
```

---

## 📈 Data Quality Guidelines

### Best Practices

- ✅ Use consistent units throughout
- ✅ Record timestamps in UTC
- ✅ Include location data when possible
- ✅ Document environmental conditions accurately
- ✅ Record detection confidence scores
- ✅ Add notes for unusual conditions

### Common Issues to Avoid

- ❌ Missing required fields
- ❌ Values outside valid ranges
- ❌ Inconsistent units
- ❌ Missing timestamps
- ❌ Incomplete environmental data

---

## 🔄 File Updates

These templates are designed to be:

- **Extensible**: Easy to add new fields
- **Compatible**: Work with the API and Python SDK
- **Validated**: Include proper data validation
- **Documented**: Clear field descriptions and units

For questions or customizations, refer to the main documentation or contact the development team.
