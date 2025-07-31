"""
FastAPI application for bioluminescent bead detection distance prediction.

This module provides REST API endpoints for the AI model, including prediction,
calibration, and model management functionality with enhanced data validation.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Union
import numpy as np
import pandas as pd
from datetime import datetime
import json
import os

# Import the bioluminescence model and data processors
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bioluminescence_model import BioluminescenceModel, ModelParameters
from data_models import DetectionInput, DataProcessor, ValidationResult, SensorType

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

# Initialize the model and data processor
model = BioluminescenceModel()
data_processor = DataProcessor()

# Enhanced Pydantic models for request/response validation
class PredictionRequest(BaseModel):
    """Enhanced prediction request with comprehensive data structure"""
    temporal_parameters: Dict[str, float] = Field(..., description="Temporal parameters")
    environmental_conditions: Dict[str, float] = Field(..., description="Environmental conditions")
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
    environmental_conditions: Dict[str, float] = Field(..., description="Environmental conditions")
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
    environmental_conditions: Dict[str, float] = Field(..., description="Environmental conditions")
    sensor_parameters: Dict[str, Union[str, List[float]]] = Field(..., description="Sensor parameters")
    product_parameters: Optional[Dict[str, Union[int, str]]] = Field(None, description="Product parameters")

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Bioluminescent Detection AI API v2.0",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Enhanced data validation",
            "Multiple input formats",
            "Bulk prediction support",
            "Comprehensive error handling"
        ],
        "endpoints": {
            "predict": "/predict",
            "predict_bulk": "/predict/bulk",
            "calibrate": "/calibrate",
            "model_info": "/model/info",
            "add_validation": "/validation/add",
            "validate_input": "/validate/input",
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
        
        # Convert to model input format
        model_input = data_processor.convert_to_model_input(validation_result.processed_data)
        
        # Make prediction
        result = model.predict(**model_input)
        
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
                
                # Convert to model input format
                model_input = data_processor.convert_to_model_input(validation_result.processed_data)
                
                # Make prediction
                result = model.predict(**model_input)
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": True,
        "data_processor_ready": True
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