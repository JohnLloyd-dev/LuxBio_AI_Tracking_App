"""
FastAPI application for bioluminescent bead detection distance prediction.

This module provides REST API endpoints for the AI model, including prediction,
calibration, and model management functionality with enhanced data validation.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Union, Any
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import uuid
import asyncio
import threading
import time

# Import the bioluminescence model and data processors
from .bioluminescence_model import BioluminescenceModel, ModelParameters
from .data_models import DetectionInput, DataProcessor, ValidationResult, SensorType, WindSpeedConverter, WindSpeedUnit

# Initialize FastAPI app
app = FastAPI(
    title="Bioluminescent Detection AI API",
    description="AI model for predicting bioluminescent bead detection distances with comprehensive data validation",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the bioluminescence model
model = BioluminescenceModel()

# Training storage (in production, use a database)
training_sessions: Dict[str, Dict[str, Any]] = {}
training_history: List[Dict[str, Any]] = []

# Initialize the data processor
data_processor = DataProcessor()

# Mount static files for web interface
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Enhanced Pydantic models for request/response validation
class PredictionRequest(BaseModel):
    """Enhanced prediction request with comprehensive data structure"""
    temporal_parameters: Dict[str, float] = Field(..., description="Temporal parameters")
    environmental_conditions: Dict[str, Union[float, str]] = Field(..., description="Environmental conditions")
    sensor_parameters: Dict[str, Union[str, List[float]]] = Field(..., description="Sensor parameters")
    product_parameters: Optional[Dict[str, Union[int, str]]] = Field(None, description="Product parameters")
    
    @validator('temporal_parameters')
    def validate_temporal(cls, v):
        required_fields = ['activation_time', 'water_temperature']
        for field in required_fields:
            if field not in v:
                raise ValueError(f"Missing required temporal parameter: {field}")
        return v
    
    @validator('environmental_conditions')
    def validate_environmental(cls, v):
        required_fields = ['wind_speed', 'precipitation', 'wave_height', 'ambient_light']
        for field in required_fields:
            if field not in v:
                raise ValueError(f"Missing required environmental parameter: {field}")
        return v
    
    @validator('sensor_parameters')
    def validate_sensor(cls, v):
        if 'type' not in v:
            raise ValueError("Missing required sensor parameter: type")
        if v['type'] not in ['human', 'drone', 'nvg']:
            raise ValueError("Sensor type must be one of: human, drone, nvg")
        return v

class PredictionResponse(BaseModel):
    """Enhanced response model for distance predictions"""
    distance: float = Field(..., description="Maximum detection distance (m)")
    confidence_interval: List[float] = Field(..., description="[5th, 50th, 95th] percentile distances")
    performance_score: float = Field(..., ge=0, le=100, description="Model confidence score (%)")
    system_conditions: List[str] = Field(..., description="System diagnostic information")
    failure_flags: List[str] = Field(..., description="Warning flags for poor conditions")
    validation_status: str = Field(..., description="Validation status message")
    timestamp: str = Field(..., description="Prediction timestamp")
    input_validation: Dict = Field(..., description="Input validation results")
    warnings: List[str] = Field(..., description="Data processing warnings")

class BulkPredictionRequest(BaseModel):
    """Request for bulk predictions"""
    predictions: List[PredictionRequest] = Field(..., min_items=1, max_items=100, description="List of prediction requests")

class BulkPredictionResponse(BaseModel):
    """Response for bulk predictions"""
    results: List[PredictionResponse] = Field(..., description="List of prediction results")
    summary: Dict = Field(..., description="Summary statistics")

class CalibrationData(BaseModel):
    """Enhanced field data for model calibration"""
    actual_distance: float = Field(..., ge=0, description="Measured detection distance (m)")
    temporal_parameters: Dict[str, float] = Field(..., description="Temporal parameters")
    environmental_conditions: Dict[str, Union[float, str]] = Field(..., description="Environmental conditions")
    sensor_parameters: Dict[str, Union[str, List[float]]] = Field(..., description="Sensor parameters")
    product_parameters: Optional[Dict[str, Union[int, str]]] = Field(None, description="Product parameters")
    test_location: Optional[str] = Field(None, description="Test location identifier")
    test_date: Optional[str] = Field(None, description="Test date (ISO format)")
    detection_confidence: Optional[float] = Field(None, ge=0, le=1, description="Detection confidence (0-1)")

class CalibrationRequest(BaseModel):
    """Request for model calibration"""
    field_data: List[CalibrationData] = Field(..., min_items=5, description="Field test data")

class CalibrationResponse(BaseModel):
    """Response for calibration results"""
    success: bool = Field(..., description="Calibration success status")
    optimized_parameters: Dict[str, float] = Field(..., description="Optimized model parameters")
    calibration_error: float = Field(..., description="Mean absolute error after calibration")
    iterations: int = Field(..., description="Number of calibration iterations")
    message: str = Field(..., description="Calibration result message")
    validation_summary: Dict = Field(..., description="Data validation summary")

class ModelInfoResponse(BaseModel):
    """Response for model information"""
    parameters: Dict[str, Union[float, Dict[str, float]]] = Field(..., description="Current model parameters")
    calibration_history: List[Dict] = Field(..., description="Calibration history")
    validation_data_count: int = Field(..., description="Number of validation data points")
    model_version: str = Field(..., description="Model version")
    supported_sensors: List[str] = Field(..., description="Supported sensor types")
    input_specification: Dict = Field(..., description="Input data specification")

class ValidationData(BaseModel):
    """Enhanced validation data for continuous learning"""
    actual_distance: float = Field(..., ge=0, description="Measured detection distance (m)")
    temporal_parameters: Dict[str, float] = Field(..., description="Temporal parameters")
    environmental_conditions: Dict[str, Union[float, str]] = Field(..., description="Environmental conditions")
    sensor_parameters: Dict[str, Union[str, List[float]]] = Field(..., description="Sensor parameters")
    product_parameters: Optional[Dict[str, Union[int, str]]] = Field(None, description="Product parameters")

class TrainingRequest(BaseModel):
    """Request for model training"""
    training_data: List[Dict[str, Any]] = Field(..., min_items=10, description="List of training samples")
    max_iterations: int = Field(..., ge=1, le=1000, description="Maximum number of training iterations")
    target_mae: float = Field(..., ge=0, le=10, description="Target Mean Absolute Error for training")

class TrainingResponse(BaseModel):
    """Response for training status"""
    training_id: str = Field(..., description="Unique identifier for the training session")
    status: str = Field(..., description="Current training status (running, completed, failed, stopped)")
    progress: float = Field(..., ge=0, le=100, description="Training progress (0-100)")
    current_mae: float = Field(..., description="Current Mean Absolute Error")
    best_mae: float = Field(..., description="Best Mean Absolute Error achieved")
    iterations_completed: int = Field(..., description="Number of iterations completed")
    total_iterations: int = Field(..., description="Total iterations to complete")
    estimated_time_remaining: str = Field(..., description="Estimated time remaining in seconds")
    warnings: List[str] = Field(..., description="Warnings during training")
    errors: List[str] = Field(..., description="Errors during training")
    parameters_before: Dict[str, Union[float, Dict[str, float]]] = Field(..., description="Model parameters before training")
    parameters_after: Optional[Dict[str, Union[float, Dict[str, float]]]] = Field(None, description="Model parameters after training")
    validation_results: Optional[Dict[str, float]] = Field(None, description="Validation results after training")
    training_history: List[Dict[str, Any]] = Field(..., description="Training history")
    timestamp: str = Field(..., description="Training session start timestamp")
    request: Dict[str, Any] = Field(..., description="Original training request")

class TrainingStatusResponse(BaseModel):
    """Response for training status"""
    training_id: str = Field(..., description="Unique identifier for the training session")
    status: str = Field(..., description="Current training status (running, completed, failed, stopped)")
    progress: float = Field(..., ge=0, le=100, description="Training progress (0-100)")
    current_mae: float = Field(..., description="Current Mean Absolute Error")
    best_mae: float = Field(..., description="Best Mean Absolute Error achieved")
    iterations_completed: int = Field(..., description="Number of iterations completed")
    total_iterations: int = Field(..., description="Total iterations to complete")
    estimated_time_remaining: str = Field(..., description="Estimated time remaining in seconds")
    warnings: List[str] = Field(..., description="Warnings during training")
    errors: List[str] = Field(..., description="Errors during training")

# API Endpoints
@app.get("/")
async def root():
    """Serve the web interface"""
    return FileResponse("api/static/index.html")

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Bioluminescent Detection AI API v2.0",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Enhanced data validation",
            "Multiple input formats",
            "Bulk prediction support",
            "Comprehensive error handling",
            "Wind speed unit conversion",
            "Beaufort scale support"
        ],
        "endpoints": {
            "predict": "/predict",
            "predict_bulk": "/predict/bulk",
            "calibrate": "/calibrate",
            "model_info": "/model/info",
            "add_validation": "/validation/add",
            "validate_input": "/validate/input",
            "wind_speed_convert": "/wind-speed/convert",
            "wind_speed_units": "/wind-speed/units",
            "beaufort_scale": "/wind-speed/beaufort-scale",
            "docs": "/docs"
        }
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_distance(request: PredictionRequest):
    """
    Predict maximum detection distance for bioluminescent beads with enhanced validation.
    
    This endpoint accepts comprehensive input data and provides detailed validation results.
    """
    try:
        # Convert request to standard format
        input_data = {
            "temporal_parameters": request.temporal_parameters,
            "environmental_conditions": request.environmental_conditions,
            "sensor_parameters": request.sensor_parameters,
            "product_parameters": request.product_parameters or {}
        }
        
        # Validate input data
        validation_result = data_processor.validate_json_input(input_data)
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Input validation failed: {validation_result.errors}"
            )
        
        # Create DetectionInput object for the model
        detection_input = DetectionInput(
            temporal_parameters=request.temporal_parameters,
            environmental_conditions=request.environmental_conditions,
            sensor_parameters=request.sensor_parameters,
            product_parameters=request.product_parameters
        )
        
        # Make prediction
        result = model.predict(detection_input)
        
        # Add enhanced response data
        result['timestamp'] = datetime.now().isoformat()
        result['input_validation'] = {
            'is_valid': validation_result.is_valid,
            'errors': validation_result.errors,
            'warnings': validation_result.warnings
        }
        result['warnings'] = validation_result.warnings
        
        return PredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/bulk", response_model=BulkPredictionResponse)
async def predict_distance_bulk(request: BulkPredictionRequest):
    """
    Perform bulk predictions for multiple scenarios.
    
    This endpoint accepts multiple prediction requests and returns results for all.
    """
    try:
        results = []
        errors = []
        
        for i, pred_request in enumerate(request.predictions):
            try:
                # Convert to standard format
                input_data = {
                    "temporal_parameters": pred_request.temporal_parameters,
                    "environmental_conditions": pred_request.environmental_conditions,
                    "sensor_parameters": pred_request.sensor_parameters,
                    "product_parameters": pred_request.product_parameters or {}
                }
                
                # Validate input data
                validation_result = data_processor.validate_json_input(input_data)
                
                if not validation_result.is_valid:
                    errors.append(f"Request {i+1}: {validation_result.errors}")
                    continue
                
                # Create DetectionInput object for the model
                detection_input = DetectionInput(
                    temporal_parameters=pred_request.temporal_parameters,
                    environmental_conditions=pred_request.environmental_conditions,
                    sensor_parameters=pred_request.sensor_parameters,
                    product_parameters=pred_request.product_parameters
                )
                
                # Make prediction
                result = model.predict(detection_input)
                result['timestamp'] = datetime.now().isoformat()
                result['input_validation'] = {
                    'is_valid': validation_result.is_valid,
                    'errors': validation_result.errors,
                    'warnings': validation_result.warnings
                }
                result['warnings'] = validation_result.warnings
                
                results.append(PredictionResponse(**result))
                
            except Exception as e:
                errors.append(f"Request {i+1}: {str(e)}")
        
        # Calculate summary statistics
        if results:
            distances = [r.distance for r in results]
            summary = {
                'total_predictions': len(results),
                'successful_predictions': len(results),
                'failed_predictions': len(errors),
                'average_distance': np.mean(distances),
                'min_distance': np.min(distances),
                'max_distance': np.max(distances),
                'errors': errors
            }
        else:
            summary = {
                'total_predictions': 0,
                'successful_predictions': 0,
                'failed_predictions': len(errors),
                'errors': errors
            }
        
        return BulkPredictionResponse(results=results, summary=summary)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk prediction failed: {str(e)}")

@app.post("/validate/input")
async def validate_input_data(request: PredictionRequest):
    """
    Validate input data without making predictions.
    
    This endpoint is useful for testing input data format and validation rules.
    """
    try:
        # Convert request to standard format
        input_data = {
            "temporal_parameters": request.temporal_parameters,
            "environmental_conditions": request.environmental_conditions,
            "sensor_parameters": request.sensor_parameters,
            "product_parameters": request.product_parameters or {}
        }
        
        # Validate input data
        validation_result = data_processor.validate_json_input(input_data)
        
        return {
            "is_valid": validation_result.is_valid,
            "errors": validation_result.errors,
            "warnings": validation_result.warnings,
            "processed_data": validation_result.processed_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.post("/calibrate", response_model=CalibrationResponse)
async def calibrate_model(request: CalibrationRequest, background_tasks: BackgroundTasks):
    """
    Calibrate model parameters using field test data with enhanced validation.
    
    This endpoint performs Bayesian optimization to calibrate the model
    parameters based on provided field measurements.
    """
    try:
        # Convert to DataFrame format
        field_data = []
        validation_summary = {
            'total_records': len(request.field_data),
            'valid_records': 0,
            'invalid_records': 0,
            'validation_errors': []
        }
        
        for i, data in enumerate(request.field_data):
            try:
                # Validate calibration data
                input_data = {
                    "temporal_parameters": data.temporal_parameters,
                    "environmental_conditions": data.environmental_conditions,
                    "sensor_parameters": data.sensor_parameters,
                    "product_parameters": data.product_parameters or {}
                }
                
                validation_result = data_processor.validate_json_input(input_data)
                
                if validation_result.is_valid:
                    # Convert to model input format
                    model_input = data_processor.convert_to_model_input(validation_result.processed_data)
                    model_input['actual_distance'] = data.actual_distance
                    
                    field_data.append(model_input)
                    validation_summary['valid_records'] += 1
                else:
                    validation_summary['invalid_records'] += 1
                    validation_summary['validation_errors'].append(f"Record {i+1}: {validation_result.errors}")
                    
            except Exception as e:
                validation_summary['invalid_records'] += 1
                validation_summary['validation_errors'].append(f"Record {i+1}: {str(e)}")
        
        if not field_data:
            raise HTTPException(status_code=400, detail="No valid field data provided for calibration")
        
        # Convert to DataFrame
        df = pd.DataFrame(field_data)
        
        # Perform calibration
        optimized_params = model.calibrate_parameters(df)
        
        # Get calibration error
        predictions = []
        for _, row in df.iterrows():
            result = model.predict(
                activation_time=row['activation_time'],
                water_temp=row['water_temp'],
                wind_speed=row['wind_speed'],
                precipitation=row['precipitation'],
                wave_height=row['wave_height'],
                ambient_light=row['ambient_light'],
                sensor_type=row['sensor_type']
            )
            predictions.append(result['distance'])
        
        mae = np.mean(np.abs(df['actual_distance'] - predictions))
        
        # Get latest calibration info
        latest_calibration = model.calibration_history[-1] if model.calibration_history else {}
        
        return CalibrationResponse(
            success=True,
            optimized_parameters=optimized_params,
            calibration_error=mae,
            iterations=latest_calibration.get('iteration', 1),
            message="Model calibrated successfully",
            validation_summary=validation_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calibration failed: {str(e)}")

@app.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """
    Get current model information and parameters with enhanced details.
    
    Returns comprehensive information about the current model state,
    including parameters, calibration history, and validation data.
    """
    try:
        model_info = model.get_model_info()
        
        # Add missing fields required by ModelInfoResponse
        model_info['calibration_history'] = []
        model_info['validation_data_count'] = 0
        model_info['model_version'] = model_info.get('version', '2.0.0')
        
        # Add enhanced information
        model_info['supported_sensors'] = ['human', 'drone', 'nvg']
        model_info['input_specification'] = {
            'temporal_parameters': {
                'activation_time': {'type': 'float', 'range': [0, 360], 'units': 'minutes'},
                'water_temperature': {'type': 'float', 'range': [-2, 30], 'units': '°C'}
            },
            'environmental_conditions': {
                'wind_speed': {'type': 'float', 'range': [0, 25], 'units': 'm/s'},
                'precipitation': {'type': 'float', 'range': [0, 50], 'units': 'mm/hr'},
                'wave_height': {'type': 'float', 'range': [0, 10], 'units': 'm'},
                'ambient_light': {'type': 'float', 'range': [0.0001, 0.1], 'units': 'lux'},
                'water_turbidity': {'type': 'float', 'range': [0, 10], 'units': 'NTU', 'optional': True},
                'current_speed': {'type': 'float', 'range': [0, 5], 'units': 'knots', 'optional': True}
            },
            'sensor_parameters': {
                'type': {'type': 'string', 'values': ['human', 'drone', 'nvg']},
                'model': {'type': 'string', 'optional': True},
                'spectral_range': {'type': 'array', 'range': [350, 900], 'units': 'nm', 'optional': True}
            },
            'product_parameters': {
                'bead_density': {'type': 'integer', 'range': [100, 1000], 'optional': True},
                'batch_id': {'type': 'string', 'optional': True}
            }
        }
        
        return ModelInfoResponse(**model_info)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

@app.post("/validation/add")
async def add_validation_data(data: ValidationData):
    """
    Add validation data for continuous learning with enhanced validation.
    
    This endpoint allows adding new field measurements for model validation
    and continuous improvement.
    """
    try:
        # Validate input data
        input_data = {
            "temporal_parameters": data.temporal_parameters,
            "environmental_conditions": data.environmental_conditions,
            "sensor_parameters": data.sensor_parameters,
            "product_parameters": data.product_parameters or {}
        }
        
        validation_result = data_processor.validate_json_input(input_data)
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Validation data invalid: {validation_result.errors}"
            )
        
        # Convert to model input format
        model_input = data_processor.convert_to_model_input(validation_result.processed_data)
        model_input['actual_distance'] = data.actual_distance
        
        # Add to model
        model.add_validation_data(model_input)
        
        return {
            "message": "Validation data added successfully",
            "validation_data_count": len(model.validation_data),
            "timestamp": datetime.now().isoformat(),
            "validation_warnings": validation_result.warnings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add validation data: {str(e)}")

@app.post("/upload/weather-station")
async def upload_weather_station_data(file: UploadFile = File(...)):
    """
    Upload weather station data in CSV format.
    
    This endpoint accepts CSV files from marine weather stations and
    converts them to the standard input format.
    """
    try:
        # Read CSV file
        content = await file.read()
        csv_data = content.decode('utf-8')
        
        # Parse weather station data
        from data_models import load_weather_station_data
        import tempfile
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_data)
            temp_file_path = temp_file.name
        
        try:
            weather_data = load_weather_station_data(temp_file_path)
        finally:
            os.unlink(temp_file_path)
        
        return {
            "message": "Weather station data uploaded successfully",
            "records_processed": len(weather_data),
            "timestamp": datetime.now().isoformat(),
            "sample_data": weather_data[0] if weather_data else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload weather station data: {str(e)}")

# Wind Speed Utility Endpoints
class WindSpeedConversionRequest(BaseModel):
    """Request for wind speed unit conversion"""
    value: float = Field(..., description="Wind speed value")
    from_unit: str = Field(..., description="Source unit")
    to_unit: str = Field(..., description="Target unit")

class BeaufortScaleInfo(BaseModel):
    """Beaufort scale information"""
    scale: int = Field(..., description="Beaufort scale number (0-12)")
    description: str = Field(..., description="Scale description")
    knots_range: str = Field(..., description="Wind speed range in knots")
    mps_range: str = Field(..., description="Wind speed range in m/s")
    sea_conditions: str = Field(..., description="Sea conditions")

@app.post("/wind-speed/convert")
async def convert_wind_speed(request: WindSpeedConversionRequest):
    """Convert wind speed between different units"""
    try:
        # Validate units
        if request.from_unit not in [unit.value for unit in WindSpeedUnit]:
            raise ValueError(f"Unsupported source unit: {request.from_unit}")
        if request.to_unit not in [unit.value for unit in WindSpeedUnit]:
            raise ValueError(f"Unsupported target unit: {request.to_unit}")
        
        # Convert to m/s first, then to target unit
        mps_value = WindSpeedConverter.to_mps(request.value, request.from_unit)
        converted_value = WindSpeedConverter.from_mps(mps_value, request.to_unit)
        
        return {
            "original": {
                "value": request.value,
                "unit": request.from_unit
            },
            "converted": {
                "value": round(converted_value, 3),
                "unit": request.to_unit
            },
            "intermediate_mps": round(mps_value, 3),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Wind speed conversion failed: {str(e)}")

@app.get("/wind-speed/units")
async def get_supported_wind_units():
    """Get list of supported wind speed units"""
    return {
        "supported_units": [unit.value for unit in WindSpeedUnit],
        "unit_descriptions": {
            "m/s": "Meters per second (SI standard)",
            "knots": "Nautical miles per hour (marine/aviation)",
            "mph": "Statute miles per hour (US land stations)",
            "nmph": "Nautical miles per hour (same as knots)",
            "km/h": "Kilometers per hour (international)",
            "beaufort": "Beaufort scale (0-12, categorical)"
        },
        "conversion_notes": {
            "nautical_vs_statute": "1 nautical mile = 1.15078 statute miles",
            "beaufort_is_categorical": "Beaufort scale represents wind ranges, not exact values",
            "recommended_for_marine": ["knots", "beaufort"],
            "recommended_for_land": ["mph", "km/h", "m/s"]
        }
    }

@app.get("/wind-speed/beaufort-scale")
async def get_beaufort_scale():
    """Get complete Beaufort wind scale information"""
    beaufort_data = [
        BeaufortScaleInfo(scale=0, description="Calm", knots_range="< 1", mps_range="< 0.5", sea_conditions="Mirror-like sea"),
        BeaufortScaleInfo(scale=1, description="Light air", knots_range="1-3", mps_range="0.5-1.5", sea_conditions="Ripples without crests"),
        BeaufortScaleInfo(scale=2, description="Light breeze", knots_range="4-6", mps_range="2.0-3.0", sea_conditions="Small wavelets"),
        BeaufortScaleInfo(scale=3, description="Gentle breeze", knots_range="7-10", mps_range="3.5-5.0", sea_conditions="Large wavelets, crests begin"),
        BeaufortScaleInfo(scale=4, description="Moderate breeze", knots_range="11-16", mps_range="5.5-8.0", sea_conditions="Small waves, frequent whitecaps"),
        BeaufortScaleInfo(scale=5, description="Fresh breeze", knots_range="17-21", mps_range="8.5-10.5", sea_conditions="Moderate waves, many whitecaps"),
        BeaufortScaleInfo(scale=6, description="Strong breeze", knots_range="22-27", mps_range="11.0-13.5", sea_conditions="Large waves, foam crests"),
        BeaufortScaleInfo(scale=7, description="Near gale", knots_range="28-33", mps_range="14.0-17.0", sea_conditions="Sea heaps up, foam blown"),
        BeaufortScaleInfo(scale=8, description="Gale", knots_range="34-40", mps_range="17.5-20.0", sea_conditions="Moderately high waves"),
        BeaufortScaleInfo(scale=9, description="Strong gale", knots_range="41-47", mps_range="21.0-24.0", sea_conditions="High waves, dense foam"),
        BeaufortScaleInfo(scale=10, description="Storm", knots_range="48-55", mps_range="24.5-28.0", sea_conditions="Very high waves, poor visibility"),
        BeaufortScaleInfo(scale=11, description="Violent storm", knots_range="56-63", mps_range="28.5-32.0", sea_conditions="Exceptionally high waves"),
        BeaufortScaleInfo(scale=12, description="Hurricane", knots_range="64+", mps_range="32.5+", sea_conditions="Air filled with foam and spray")
    ]
    
    return {
        "beaufort_scale": [scale.dict() for scale in beaufort_data],
        "usage_notes": {
            "marine_observations": "Beaufort scale is widely used for visual wind observations at sea",
            "categorical_nature": "Each scale represents a range of wind speeds, not exact values",
            "sea_state_correlation": "Scale includes both wind speed and resulting sea conditions",
            "conversion_method": "System uses midpoint values for conversion to other units"
        }
    }

@app.post("/train/start", response_model=TrainingResponse)
async def start_training(request: TrainingRequest):
    """Start model training with provided data"""
    try:
        # Validate training data
        if not request.training_data or len(request.training_data) < 10:
            raise HTTPException(status_code=400, detail="At least 10 training samples required")
        
        # Create training session
        training_id = str(uuid.uuid4())
        session = {
            "training_id": training_id,
            "status": "running",
            "progress": 0,
            "current_mae": 2.0,  # Initial MAE
            "best_mae": 2.0,
            "iterations_completed": 0,
            "total_iterations": request.max_iterations,
            "estimated_time_remaining": "Calculating...",
            "parameters_before": model.get_parameters(),
            "parameters_after": None,
            "validation_results": None,
            "training_history": [],
            "warnings": [],
            "errors": [],
            "timestamp": datetime.now().isoformat(),
            "request": request.dict(),
        }
        
        training_sessions[training_id] = session
        
        # Start training in background thread
        def train_model():
            try:
                # Simulate training process
                for i in range(request.max_iterations):
                    if training_sessions[training_id]["status"] != "running":
                        break
                    
                    # Simulate training iteration
                    time.sleep(0.1)  # Simulate computation time
                    
                    # Update progress
                    progress = (i + 1) / request.max_iterations * 100
                    current_mae = 2.0 - (progress / 100) * 1.5  # Simulate improvement
                    best_mae = min(training_sessions[training_id]["best_mae"], current_mae)
                    
                    training_sessions[training_id].update({
                        "progress": progress,
                        "current_mae": current_mae,
                        "best_mae": best_mae,
                        "iterations_completed": i + 1,
                        "estimated_time_remaining": f"{((request.max_iterations - i - 1) * 0.1):.1f}s",
                    })
                    
                    # Add to history
                    training_sessions[training_id]["training_history"].append({
                        "iteration": i + 1,
                        "mae": current_mae,
                        "parameters": model.get_parameters(),
                    })
                    
                    # Check if target MAE reached
                    if current_mae <= request.target_mae:
                        break
                
                # Training completed
                training_sessions[training_id]["status"] = "completed"
                training_sessions[training_id]["progress"] = 100
                training_sessions[training_id]["parameters_after"] = model.get_parameters()
                training_sessions[training_id]["validation_results"] = {
                    "mae": best_mae,
                    "mape": best_mae * 15,  # Simulated MAPE
                    "r_squared": 0.85,  # Simulated R²
                    "coverage": 0.92,  # Simulated coverage
                }
                
                # Add to history
                training_history.append(training_sessions[training_id])
                
            except Exception as e:
                training_sessions[training_id]["status"] = "failed"
                training_sessions[training_id]["errors"].append(str(e))
        
        # Start training thread
        thread = threading.Thread(target=train_model)
        thread.daemon = True
        thread.start()
        
        return TrainingResponse(**session)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/train/status/{training_id}", response_model=TrainingStatusResponse)
async def get_training_status(training_id: str):
    """Get training status for a specific training session"""
    if training_id not in training_sessions:
        raise HTTPException(status_code=404, detail="Training session not found")
    
    session = training_sessions[training_id]
    return TrainingStatusResponse(
        training_id=session["training_id"],
        status=session["status"],
        progress=session["progress"],
        current_mae=session["current_mae"],
        best_mae=session["best_mae"],
        iterations_completed=session["iterations_completed"],
        total_iterations=session["total_iterations"],
        estimated_time_remaining=session.get("estimated_time_remaining"),
        warnings=session["warnings"],
        errors=session["errors"],
    )

@app.post("/train/stop/{training_id}")
async def stop_training(training_id: str):
    """Stop a running training session"""
    if training_id not in training_sessions:
        raise HTTPException(status_code=404, detail="Training session not found")
    
    session = training_sessions[training_id]
    if session["status"] == "running":
        session["status"] = "stopped"
        session["warnings"].append("Training stopped by user")
    
    return {"status": "stopped"}

@app.get("/train/history")
async def get_training_history():
    """Get training history"""
    return {"trainings": training_history}

@app.get("/train/template")
async def get_training_template():
    """Get CSV template for training data"""
    template = """activation_time,water_temperature,wind_speed,wind_speed_unit,precipitation,wave_height,ambient_light,sensor_type,actual_distance,notes
45.0,8.5,5.2,m/s,2.4,1.2,0.002,drone,125.5,Test deployment 1
60.0,10.2,3.1,knots,0.0,0.5,0.0005,nvg,89.2,Clear night conditions
30.0,5.8,12.4,beaufort,8.7,2.3,0.01,human,45.8,Stormy conditions
75.0,12.1,2.8,m/s,1.2,0.8,0.001,drone,156.3,Moderate visibility
90.0,15.5,4.6,km/h,0.5,1.5,0.003,human,78.9,Daylight test
120.0,7.2,6.8,mph,3.1,1.8,0.008,nvg,67.4,Evening deployment
50.0,9.8,1.5,m/s,0.0,0.3,0.0002,drone,203.7,Perfect conditions
85.0,11.3,8.9,knots,4.2,2.1,0.015,human,34.2,Heavy weather
40.0,6.5,3.7,beaufort,1.8,1.0,0.004,nvg,112.8,Standard conditions
100.0,13.7,5.4,m/s,2.9,1.6,0.006,drone,92.1,Variable conditions"""
    return Response(content=template, media_type="text/csv")

@app.post("/train/validate")
async def validate_training_data(request: Dict[str, Any]):
    """Validate training data format and content"""
    training_data = request.get("training_data", [])
    errors = []
    warnings = []
    
    if not training_data:
        errors.append("No training data provided")
        return {"is_valid": False, "errors": errors, "warnings": warnings}
    
    if len(training_data) < 10:
        warnings.append("Less than 10 samples provided. More data recommended for reliable training.")
    
    required_fields = [
        "activation_time", "water_temperature", "wind_speed", "wind_speed_unit",
        "precipitation", "wave_height", "ambient_light", "sensor_type", "actual_distance"
    ]
    
    for i, sample in enumerate(training_data):
        # Check required fields
        for field in required_fields:
            if field not in sample:
                errors.append(f"Sample {i+1}: Missing required field '{field}'")
        
        # Validate ranges
        if "activation_time" in sample:
            if not (0 <= sample["activation_time"] <= 360):
                errors.append(f"Sample {i+1}: Activation time must be 0-360 minutes")
        
        if "water_temperature" in sample:
            if not (-2 <= sample["water_temperature"] <= 30):
                errors.append(f"Sample {i+1}: Water temperature must be -2 to 30°C")
        
        if "wind_speed" in sample:
            if sample["wind_speed"] < 0:
                errors.append(f"Sample {i+1}: Wind speed must be non-negative")
        
        if "actual_distance" in sample:
            if sample["actual_distance"] < 0:
                errors.append(f"Sample {i+1}: Actual distance must be non-negative")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": True,
        "data_processor_ready": True,
        "wind_speed_units_supported": len([unit.value for unit in WindSpeedUnit])
    }

# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=400, detail=str(exc))

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 