# 🚀 How to Run the Bioluminescent Detection AI Model Project

This guide provides step-by-step instructions for running the bioluminescent detection AI model project in various configurations.

## 📋 Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **OS**: Linux, macOS, or Windows
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space

### Required Software

- Python 3.8+
- pip (Python package installer)
- Git (for cloning the repository)

## 🛠️ Installation Options

### Option 1: Standard Installation (Recommended)

```bash
# 1. Clone or navigate to the project directory
cd /path/to/your/project

# 2. Create a virtual environment (recommended)
python -m venv bioluminescence_env

# 3. Activate the virtual environment
# On Linux/macOS:
source bioluminescence_env/bin/activate
# On Windows:
bioluminescence_env\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python -c "import numpy, fastapi, bioluminescence_model; print('Installation successful!')"
```

### Option 2: Docker Installation

```bash
# 1. Build the Docker image
docker build -t bioluminescence-ai .

# 2. Run the container
docker run -p 8000:8000 bioluminescence-ai

# 3. Or use Docker Compose (recommended)
docker-compose up --build
```

### Option 3: Development Installation

```bash
# 1. Install in development mode
pip install -e .

# 2. Install additional development dependencies
pip install pytest pytest-cov black flake8
```

## 🎯 Running Options

### 1. Quick Start Demo

**Purpose**: Test basic functionality and see immediate results

```bash
# Run the quick start script
python quick_start.py
```

**Expected Output**:

```
=== Bioluminescent Detection AI Model - Quick Start ===

Basic Prediction:
Max detection distance: 427 m
Confidence interval: [398, 427, 456]
Performance score: 85.2%
Model status: Operational

Environmental Analysis:
Wind effect: -12.3% (reduces detection by 60 m)
Precipitation effect: -8.7% (reduces detection by 41 m)
Wave effect: -5.2% (reduces detection by 23 m)

Quick start completed successfully!
```

### 2. Enhanced Input Examples

**Purpose**: Test the new comprehensive input data format

```bash
# Run the enhanced input examples
python example_enhanced_input.py
```

**Expected Output**:

```
=== Enhanced Input Format Examples ===

Example 1: JSON Input Format
✅ Validation successful
✅ Prediction completed: 427 m

Example 2: CSV Single Prediction
✅ CSV parsing successful
✅ Prediction completed: 398 m

Example 3: CSV Bulk Predictions
✅ Bulk processing completed
✅ 8 predictions processed successfully

Example 4: Field Data Collection
✅ Field data template created

Example 5: Weather Station Integration
✅ Weather data processed successfully

Example 6: Input Validation Edge Cases
✅ Edge case validation completed

Example 7: Data Export
✅ Data exported to sample_validation_data.csv

All examples completed successfully!
```

### 3. Full System Demo

**Purpose**: Comprehensive demonstration of all system capabilities

```bash
# Run the complete example
python example_usage.py
```

**Expected Output**:

```
=== Bioluminescent Detection AI Model - Complete System Demo ===

1. Basic Prediction:
   Distance: 427 m
   Confidence: [398, 427, 456]
   Performance: 85.2%

2. Environmental Analysis:
   Wind impact: -12.3%
   Precipitation impact: -8.7%
   Wave impact: -5.2%

3. Validation Tests:
   ✅ All validation tests passed
   ✅ Model accuracy: 92.3%

4. Calibration:
   ✅ Parameters calibrated successfully
   ✅ Model performance improved

5. Deployment Simulation:
   ✅ Mission planning completed
   ✅ Search pattern generated
   ✅ Simulated execution successful

Complete system demo finished successfully!
```

### 4. API Server

**Purpose**: Start the web API for real-time predictions

```bash
# Start the FastAPI server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Access the API**:

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 5. Testing

**Purpose**: Run comprehensive tests to verify system functionality

```bash
# Run all tests
python run_tests.py

# Or run specific test modules
python -m pytest tests/test_model.py -v
python -m pytest tests/ -v --cov=.
```

**Expected Output**:

```
=== Running Bioluminescent Detection AI Model Tests ===

test_light_decay (__main__.TestBioluminescenceModel) ... ok
test_environmental_attenuation (__main__.TestBioluminescenceModel) ... ok
test_detection_threshold (__main__.TestBioluminescenceModel) ... ok
test_prediction (__main__.TestBioluminescenceModel) ... ok
test_calibration (__main__.TestBioluminescenceModel) ... ok
test_validation (__main__.TestModelValidator) ... ok
test_deployment (__main__.TestDeploymentController) ... ok

----------------------------------------------------------------------
Ran 7 tests in 2.3s

OK
All tests passed successfully!
```

## 🌐 API Usage Examples

### Using the Web Interface

1. **Start the server**:

   ```bash
   uvicorn api.main:app --reload
   ```

2. **Open your browser** to http://localhost:8000/docs

3. **Try the interactive API**:
   - Click on `/predict` endpoint
   - Click "Try it out"
   - Enter your parameters
   - Click "Execute"

### Using cURL

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
           "activation_time": 45.0,
           "water_temp": 8.5,
           "wind_speed": 5.2,
           "precip": 2.4,
           "wave_ht": 1.2,
           "ambient_light": 0.002,
           "sensor_type": "drone"
         }
       ]
     }'

# Upload weather station data
curl -X POST "http://localhost:8000/upload/weather-station" \
     -F "file=@data_formats/weather_station_template.csv"
```

### Using Python Requests

```python
import requests
import json

# Single prediction
url = "http://localhost:8000/predict"
data = {
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
}

response = requests.post(url, json=data)
result = response.json()
print(f"Detection distance: {result['distance']} m")
```

## 📊 Data Processing Examples

### Using CSV Files

```python
from data_models import DataProcessor
import pandas as pd

# Load and process CSV data
data_processor = DataProcessor()

# Single prediction from CSV
with open('data_formats/single_prediction_template.csv', 'r') as f:
    csv_data = f.read()
    result = data_processor.parse_csv_single(csv_data)
    if result.is_valid:
        print("CSV validation successful!")

# Bulk predictions from CSV
with open('data_formats/bulk_predictions_template.csv', 'r') as f:
    csv_data = f.read()
    results = data_processor.parse_csv_bulk(csv_data)
    print(f"Processed {len(results)} predictions")
```

### Field Data Collection

```python
# Create field data collection template
field_template = data_processor.create_field_data_collector()

# Export to CSV
data_processor.export_to_csv(field_template, "my_field_data.csv")
```

## 🔧 Configuration Options

### Environment Variables

```bash
# Set environment variables (optional)
export BIOLUMINESCENCE_LOG_LEVEL=INFO
export BIOLUMINESCENCE_API_HOST=0.0.0.0
export BIOLUMINESCENCE_API_PORT=8000
export BIOLUMINESCENCE_DEBUG=true
```

### Docker Configuration

```bash
# Custom Docker run
docker run -p 8000:8000 \
  -e BIOLUMINESCENCE_LOG_LEVEL=DEBUG \
  -v $(pwd)/data:/app/data \
  bioluminescence-ai

# Docker Compose with custom config
docker-compose -f docker-compose.yml up --build
```

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**

```bash
# Solution: Reinstall dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

**2. Port Already in Use**

```bash
# Solution: Use different port
uvicorn api.main:app --reload --port 8001
```

**3. Permission Errors (Linux/macOS)**

```bash
# Solution: Fix permissions
chmod +x run_tests.py
chmod +x quick_start.py
```

**4. Memory Issues**

```bash
# Solution: Reduce batch size or use smaller datasets
# Edit the model parameters in bioluminescence_model.py
```

### Debug Mode

```bash
# Enable debug logging
export BIOLUMINESCENCE_DEBUG=true
python quick_start.py

# Or run with verbose output
python -v example_usage.py
```

## 📈 Performance Monitoring

### Check System Status

```bash
# API health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model/info
```

### Monitor Performance

```python
import time
from bioluminescence_model import BioluminescenceModel

model = BioluminescenceModel()

# Time prediction performance
start_time = time.time()
result = model.predict(activation_time=45, water_temp=8.5, wind_speed=5.2,
                      precipitation=2.4, wave_height=1.2, ambient_light=0.002,
                      sensor_type="drone")
end_time = time.time()

print(f"Prediction time: {(end_time - start_time)*1000:.2f} ms")
```

## 🎯 Next Steps

After successfully running the project:

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Try different scenarios**: Use the CSV templates in `data_formats/`
3. **Run validation tests**: Use `python run_tests.py`
4. **Collect field data**: Use the field data collection templates
5. **Calibrate the model**: Upload real-world data for improvement

## 📞 Support

If you encounter issues:

1. **Check the logs**: Look for error messages in the console
2. **Verify dependencies**: Ensure all packages are installed correctly
3. **Test individual components**: Run specific modules separately
4. **Check the documentation**: Refer to `README.md` and `INPUT_FORMAT_SPECIFICATION.md`

---

**Happy detecting! 🦠✨**
