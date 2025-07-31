# Store Data App - LuxBio AI Tracking

A user-friendly desktop application for inputting field measurement data for the LuxBio AI Tracking system.

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation
1. Ensure you have Python installed
2. No additional packages required (uses built-in tkinter)

### Running the App
```bash
# Option 1: Run directly
python store_data_app.py

# Option 2: Use launcher script
python run_store_data_app.py
```

## 📋 Features

### ✅ **8 Key Parameter Input**
- **Actual Distance** (0-1000 m) - GPS measurement
- **Activation Time** (0-360 min) - Stopwatch timing  
- **Water Temperature** (-2 to 30°C) - Digital thermometer
- **Wind Speed** (0-25 m/s) - Anemometer app/device
- **Precipitation** (0-50 mm/hr) - Rain gauge
- **Wave Height** (0-10 m) - Visual estimation
- **Ambient Light** (0.0001-0.1 lux) - Lux meter app
- **Sensor Type** (human/drone/nvg) - Detection technology

### ✅ **Real-time Validation**
- Input validation with helpful error messages
- Range checking for all numeric fields
- Format validation for dates and IDs
- Real-time feedback in status area

### ✅ **Multiple Export Formats**
- **CSV Export** - Append to existing files or create new ones
- **JSON Export** - Single record with timestamp
- Compatible with the main LuxBio AI system

### ✅ **User-Friendly Interface**
- Clear labels and tooltips for each field
- Dropdown selection for sensor types
- Status area showing validation results
- Help system with measurement guidelines

## 🎯 Usage Guide

### 1. **Enter Test Information**
- **Test ID**: Use format XX-XXX (e.g., VH-001)
- **Date**: Automatically set to today's date
- **GPS Coordinates**: Enter latitude and longitude

### 2. **Input Field Measurements**
- **Actual Distance**: Maximum detection range in meters
- **Activation Time**: Minutes since bead activation
- **Environmental Conditions**: Temperature, wind, precipitation, waves, light
- **Sensor Type**: Choose from dropdown (human/drone/nvg)

### 3. **Add Notes**
- Record any additional observations
- Document unusual conditions
- Note equipment used

### 4. **Validate and Save**
- Click "Validate Data" to check all fields
- Save to CSV for bulk processing
- Save to JSON for individual records

## 📊 Data Validation Rules

| Field | Type | Range/Format | Validation |
|-------|------|--------------|------------|
| Test ID | Text | XX-XXX format | Pattern matching |
| Date | Date | YYYY-MM-DD | Format validation |
| Latitude | Number | -90 to 90 | Range check |
| Longitude | Number | -180 to 180 | Range check |
| Actual Distance | Number | 0-1000 m | Range check |
| Activation Time | Number | 0-360 min | Range check |
| Water Temperature | Number | -2 to 30°C | Range check |
| Wind Speed | Number | 0-25 m/s | Range check |
| Precipitation | Number | 0-50 mm/hr | Range check |
| Wave Height | Number | 0-10 m | Range check |
| Ambient Light | Number | 0.0001-0.1 lux | Range check |
| Sensor Type | Dropdown | human/drone/nvg | Value check |

## 💾 Export Formats

### CSV Format
```csv
test_id,date,lat,lon,actual_distance,activation_time,water_temp,wind_speed,precipitation,wave_height,ambient_light,sensor_type,notes
VH-001,2024-01-15,48.423,-123.367,320,45,8.5,5.2,2.4,1.2,0.002,drone,Moderate conditions
```

### JSON Format
```json
{
  "test_id": "VH-001",
  "date": "2024-01-15",
  "lat": 48.423,
  "lon": -123.367,
  "actual_distance": 320,
  "activation_time": 45,
  "water_temp": 8.5,
  "wind_speed": 5.2,
  "precipitation": 2.4,
  "wave_height": 1.2,
  "ambient_light": 0.002,
  "sensor_type": "drone",
  "notes": "Moderate conditions",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🔧 Field Measurement Guidelines

### Equipment Needed ($150 Total)
- Waterproof phone case ($15)
- Digital thermometer ($8)
- Rain gauge ($5)
- Stopwatch ($10)
- Anemometer ($25)
- GPS app (Free)
- Lux Light Meter app (Free)
- Field notebook ($5)

### Measurement Protocols
1. **Actual Distance**: GPS distance from activation to detection boundary
2. **Activation Time**: Stopwatch from bead activation moment
3. **Water Temperature**: Thermometer 0.5m below surface
4. **Wind Speed**: Anemometer at 10m height, 1-minute average
5. **Precipitation**: Rain gauge measurement or visual estimation
6. **Wave Height**: Visual reference or wave timing method
7. **Ambient Light**: Lux meter pointing straight up
8. **Sensor Type**: Record detection technology used

## 🆘 Help and Support

### Built-in Help
- Click the "Help" button for detailed measurement guidelines
- Tooltips provide guidance for each field
- Status area shows validation errors and data preview

### Troubleshooting
- **Validation Errors**: Check the status area for specific error messages
- **Save Issues**: Ensure you have write permissions to the target directory
- **App Won't Start**: Verify Python and tkinter are properly installed

### Additional Resources
- **Field Data Collection Guide**: `data_formats/FIELD_DATA_COLLECTION_GUIDE.md`
- **Input Format Specification**: `INPUT_FORMAT_SPECIFICATION.md`
- **Main Documentation**: `README.md`

## 🔄 Integration with Main System

The Store Data App is designed to work seamlessly with the main LuxBio AI Tracking system:

1. **Data Collection**: Use this app for field data entry
2. **Validation**: Real-time validation ensures data quality
3. **Export**: Save to CSV for bulk processing
4. **Import**: Use exported CSV files with the main system

### Workflow
```
Field Data Collection → Store Data App → CSV Export → Main System Processing
```

## 📝 Example Workflow

1. **Setup**: Launch the app and verify all fields are present
2. **Enter Data**: Fill in all required fields with measured values
3. **Validate**: Click "Validate Data" to check for errors
4. **Review**: Check the status area for data preview
5. **Save**: Export to CSV or JSON format
6. **Process**: Use exported data with the main LuxBio system

## 🎯 Best Practices

### Data Quality
- Always validate data before saving
- Use consistent units and formats
- Record notes for unusual conditions
- Cross-reference related measurements

### Field Work
- Calibrate instruments before use
- Take multiple measurements when possible
- Document environmental conditions
- Use the built-in help for measurement protocols

### File Management
- Use descriptive file names
- Keep backups of important data
- Organize files by date or location
- Use consistent naming conventions

---

**For detailed measurement protocols, see: `data_formats/FIELD_DATA_COLLECTION_GUIDE.md`** 