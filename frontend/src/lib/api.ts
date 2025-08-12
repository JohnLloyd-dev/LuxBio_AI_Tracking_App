import axios from "axios";
import type {
  PredictionRequest,
  PredictionResponse,
  TrainingFormData,
  TrainingResponse,
  TrainingStatusResponse,
} from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Simple API client without singleton pattern
export const ApiClient = {
  // Prediction endpoints
  async predictDistance(
    request: PredictionRequest
  ): Promise<PredictionResponse> {
    const response = await axios.post(`${API_BASE_URL}/predict`, request);
    return response.data;
  },

  async predictBulk(
    requests: PredictionRequest[]
  ): Promise<PredictionResponse[]> {
    const response = await axios.post(`${API_BASE_URL}/predict/bulk`, {
      predictions: requests,
    });
    return response.data.results;
  },

  // Training endpoints
  async downloadTrainingTemplate(): Promise<string> {
    const response = await axios.get(`${API_BASE_URL}/train/template`);
    return response.data;
  },

  async validateTrainingData(data: { training_data: any[] }): Promise<{
    is_valid: boolean;
    errors: string[];
    warnings: string[];
  }> {
    const response = await axios.post(`${API_BASE_URL}/train/validate`, data);
    return response.data;
  },

  async startTraining(data: {
    training_data: any[];
    max_iterations: number;
    target_mae: number;
  }): Promise<TrainingResponse> {
    const response = await axios.post(`${API_BASE_URL}/train/start`, data);
    return response.data;
  },

  async getTrainingStatus(trainingId: string): Promise<TrainingStatusResponse> {
    const response = await axios.get(
      `${API_BASE_URL}/train/status/${trainingId}`
    );
    return response.data;
  },

  async getTrainingHistory(): Promise<TrainingResponse[]> {
    const response = await axios.get(`${API_BASE_URL}/train/history`);
    return response.data.trainings;
  },

  async stopTraining(trainingId: string): Promise<{ status: string }> {
    const response = await axios.post(
      `${API_BASE_URL}/train/stop/${trainingId}`
    );
    return response.data;
  },

  // Wind speed conversion endpoints
  async convertWindSpeed(
    value: number,
    fromUnit: string,
    toUnit: string
  ): Promise<{ converted_value: number; unit: string }> {
    const response = await axios.post(`${API_BASE_URL}/wind-speed/convert`, {
      value,
      from_unit: fromUnit,
      to_unit: toUnit,
    });
    return response.data;
  },

  async getWindSpeedUnits(): Promise<{ units: string[] }> {
    const response = await axios.get(`${API_BASE_URL}/wind-speed/units`);
    return response.data;
  },

  async getBeaufortScale(): Promise<{ scale: Record<string, any> }> {
    const response = await axios.get(
      `${API_BASE_URL}/wind-speed/beaufort-scale`
    );
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  },
};
