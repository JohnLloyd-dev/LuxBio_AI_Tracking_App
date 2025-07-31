# CSV Data Format Files for Bioluminescent Detection AI Model

This directory contains comprehensive CSV templates and examples for the bioluminescent detection AI model system.

## 📁 File Overview

| File                                 | Purpose                 | Format          | Use Case                 |
| ------------------------------------ | ----------------------- | --------------- | ------------------------ |
| `single_prediction_template.csv`     | Single prediction input | Parameter-based | Individual predictions   |
| `bulk_predictions_template.csv`      | Bulk predictions input  | Row-based       | Multiple scenarios       |
| `weather_station_template.csv`       | Weather station data    | Time-series     | Environmental monitoring |
| `field_data_collection_template.csv` | Complete field data     | Comprehensive   | Field testing            |
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

### 4. `field_data_collection_template.csv`

**Format:** Comprehensive field testing data

```csv
test_id,timestamp,location_lat,location_lon,activation_time,water_temperature,...,actual_distance,detection_confidence,...
TEST-001,2024-01-15T22:30:00Z,48.423,-123.367,45.0,8.5,...,427,0.85,...
```

**Usage:**

- Complete field test documentation
- Validation data collection
- Performance analysis

**Includes:**

- Test identification
- Location data
- Input parameters
- Detection results
- Confidence scores
- Notes and observations

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

### For Field Data Collection

1. **Use `field_data_collection_template.csv`** as your base template
2. **Fill in environmental data** from your sensors
3. **Record actual detection distances** and confidence scores
4. **Upload to API** for model calibration

### For Model Calibration

1. **Collect field data** using the templates
2. **Ensure data quality** with proper validation
3. **Upload calibration data** to the API
4. **Monitor model improvement** through validation metrics

---

## 📊 Data Validation Rules

### Required Field Validation

- All required fields must be present
- Values must be within specified ranges
- Units must be correct (m/s, mm/hr, etc.)

### Range Validation

```python
# Activation time: 0-360 minutes
# Water temperature: -2 to 30°C
# Wind speed: 0-25 m/s (capped at 25)
# Precipitation: 0-50 mm/hr
# Wave height: 0-10 m (capped at 10)
# Ambient light: 0.0001-0.1 lux
```

### Sensor Type Validation

```python
VALID_SENSOR_TYPES = ["human", "drone", "nvg"]
```

### Unit Conversion

- Current speed: knots → m/s (× 0.514)
- Temperature: °F → °C if needed
- Spectral range: nm (350-900)

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
