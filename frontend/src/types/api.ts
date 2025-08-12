// API Request/Response types for the bioluminescent detection system

export interface PredictionRequest {
  temporal_parameters: {
    activation_time: number;
    water_temperature: number;
  };
  environmental_conditions: {
    wind_speed: number;
    wind_speed_unit: string;
    precipitation: number;
    wave_height: number;
    ambient_light: number;
  };
  sensor_parameters: {
    type: string;
    model?: string;
  };
  product_parameters?: Record<string, any>;
}

export interface PredictionResponse {
  distance: number;
  confidence_interval: number[];
  performance_score: number;
  system_conditions: string[];
  failure_flags: string[];
  validation_status: string;
  timestamp: string;
  input_validation: Record<string, any>;
  warnings: string[];
}

export interface TrainingFormData {
  trainingData: string; // CSV content
  csvFile?: File; // Optional CSV file
  validationSplit: number;
  maxIterations: number;
  targetMae: number;
  calibrationMethod: string;
}

export interface TrainingResponse {
  training_id: string;
  status: string;
  progress: number;
  current_mae: number;
  best_mae: number;
  iterations_completed: number;
  total_iterations: number;
  estimated_time_remaining: string;
  warnings: string[];
  errors: string[];
  parameters_before: Record<string, any>;
  parameters_after?: Record<string, any>;
  validation_results?: Record<string, any>;
  training_history: any[];
  timestamp: string;
  request: any;
}

export interface TrainingStatusResponse {
  training_id: string;
  status: string;
  progress: number;
  current_mae: number;
  best_mae: number;
  iterations_completed: number;
  total_iterations: number;
  estimated_time_remaining: string;
  warnings: string[];
  errors: string[];
}

export interface TrainingData {
  activation_time: number;
  water_temperature: number;
  wind_speed: number;
  wind_speed_unit: string;
  precipitation: number;
  wave_height: number;
  ambient_light: number;
  sensor_type: string;
  actual_distance: number;
  notes?: string;
}

export interface WindSpeedConversionRequest {
  value: number;
  from_unit: string;
  to_unit: string;
}

export interface WindSpeedConversionResponse {
  converted_value: number;
  unit: string;
  original_value: number;
  original_unit: string;
}

export interface ModelInfoResponse {
  model_version: string;
  parameters: Record<string, any>;
  training_history: any[];
  performance_metrics: Record<string, any>;
}
