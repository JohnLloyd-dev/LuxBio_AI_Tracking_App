"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "react-hot-toast";
import { Zap, Clock, Wind, Camera, Info, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { ApiClient } from "@/lib/api";
import type { PredictionRequest, PredictionResponse } from "@/types/api";

export default function PredictionTab() {
  const [isLoading, setIsLoading] = useState(false);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PredictionRequest>({
    defaultValues: {
      temporal_parameters: {
        activation_time: 45,
        water_temperature: 8.5,
      },
      environmental_conditions: {
        wind_speed: 5.2,
        wind_speed_unit: "m/s",
        precipitation: 2.4,
        wave_height: 1.2,
        ambient_light: 0.002,
      },
      sensor_parameters: {
        type: "drone",
        model: "",
      },
      product_parameters: {},
    },
  });

  const onSubmit = async (data: PredictionRequest) => {
    setIsLoading(true);
    try {
      const result = await ApiClient.predictDistance(data);
      setPrediction(result);
      toast.success("Prediction completed successfully!");
    } catch (error) {
      console.error("Prediction failed:", error);
      toast.error("Prediction failed. Please check your input.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">AI Prediction</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Enter environmental conditions and sensor parameters to predict the
          maximum detection distance for bioluminescent beads.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Clock className="w-5 h-5 mr-2 text-primary-600" />
                Temporal Parameters
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">
                    Activation Time (minutes)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="360"
                    className="input-field"
                    {...register("temporal_parameters.activation_time", {
                      required: true,
                    })}
                  />
                </div>
                <div>
                  <label className="form-label">Water Temperature (°C)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="-2"
                    max="30"
                    className="input-field"
                    {...register("temporal_parameters.water_temperature", {
                      required: true,
                    })}
                  />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Wind className="w-5 h-5 mr-2 text-primary-600" />
                Environmental Conditions
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Wind Speed</label>
                  <div className="flex space-x-2">
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="25"
                      className="input-field flex-1"
                      {...register("environmental_conditions.wind_speed", {
                        required: true,
                      })}
                    />
                    <select
                      className="input-field w-32"
                      {...register("environmental_conditions.wind_speed_unit", {
                        required: true,
                      })}
                    >
                      <option value="m/s">m/s</option>
                      <option value="knots">knots</option>
                      <option value="mph">mph</option>
                      <option value="nmph">nmph</option>
                      <option value="km/h">km/h</option>
                      <option value="beaufort">beaufort</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="form-label">Precipitation (mm/hr)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="50"
                    className="input-field"
                    {...register("environmental_conditions.precipitation", {
                      required: true,
                    })}
                  />
                </div>
                <div>
                  <label className="form-label">Wave Height (m)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="10"
                    className="input-field"
                    {...register("environmental_conditions.wave_height", {
                      required: true,
                    })}
                  />
                </div>
                <div>
                  <label className="form-label">Ambient Light (lux)</label>
                  <input
                    type="number"
                    step="0.0001"
                    min="0.0001"
                    max="0.1"
                    className="input-field"
                    {...register("environmental_conditions.ambient_light", {
                      required: true,
                    })}
                  />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Camera className="w-5 h-5 mr-2 text-primary-600" />
                Sensor Parameters
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Sensor Type</label>
                  <select
                    className="input-field"
                    {...register("sensor_parameters.type", {
                      required: true,
                    })}
                  >
                    <option value="drone">Drone Camera</option>
                    <option value="human">Human Observer</option>
                    <option value="nvg">Night Vision Goggles (NVG)</option>
                  </select>
                </div>
                <div>
                  <label className="form-label">Sensor Model (Optional)</label>
                  <input
                    type="text"
                    placeholder="e.g., DJI M30T"
                    className="input-field"
                    {...register("sensor_parameters.model")}
                  />
                </div>
              </div>
            </div>

            <div className="flex space-x-4 pt-4">
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Zap className="w-4 h-4" />
                )}
                <span>
                  {isLoading ? "Calculating..." : "Calculate Prediction"}
                </span>
              </button>
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="btn-secondary"
              >
                Reset Form
              </button>
            </div>
          </form>
        </div>

        <div className="space-y-6">
          {prediction ? (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Info className="w-5 h-5 mr-2 text-primary-600" />
                Prediction Results
              </h3>
              <div className="space-y-4">
                <div className="bg-primary-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-primary-700">
                    {prediction.distance.toFixed(1)} meters
                  </div>
                  <div className="text-sm text-primary-600">
                    Maximum Detection Distance
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm font-medium text-gray-500">
                      Performance Score
                    </div>
                    <div className="text-lg font-semibold text-gray-900">
                      {prediction.performance_score.toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-500">
                      Validation Status
                    </div>
                    <div className="text-lg font-semibold text-gray-900">
                      {prediction.validation_status}
                    </div>
                  </div>
                </div>
                {prediction.warnings.length > 0 && (
                  <div className="bg-yellow-50 p-3 rounded-lg">
                    <div className="text-sm text-yellow-800">
                      <strong>Warnings:</strong>{" "}
                      {prediction.warnings.join(", ")}
                    </div>
                  </div>
                )}
                {prediction.failure_flags.length > 0 && (
                  <div className="bg-red-50 p-3 rounded-lg">
                    <div className="text-sm text-red-800">
                      <strong>Failure Flags:</strong>{" "}
                      {prediction.failure_flags.join(", ")}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="card text-center text-gray-500">
              <Zap className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>
                Enter parameters and click "Calculate Prediction" to see results
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
