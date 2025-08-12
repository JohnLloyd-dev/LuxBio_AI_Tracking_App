"use client";
import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "react-hot-toast";
import {
  Brain,
  Upload,
  Download,
  Play,
  Square,
  BarChart3,
  History,
  Loader2,
  CheckCircle,
  XCircle,
  AlertCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { ApiClient } from "@/lib/api";
import type {
  TrainingFormData,
  TrainingResponse,
  TrainingStatusResponse,
  TrainingData,
} from "@/types/api";

const CALIBRATION_METHODS = [
  {
    value: "bayesian",
    label: "Bayesian Optimization",
    description: "Efficient parameter search using probabilistic models",
  },
  {
    value: "gradient_descent",
    label: "Gradient Descent",
    description: "Traditional optimization using gradients",
  },
  {
    value: "genetic_algorithm",
    label: "Genetic Algorithm",
    description: "Evolutionary approach for global optimization",
  },
] as const;

export default function TrainingTab() {
  const [isLoading, setIsLoading] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [trainingStatus, setTrainingStatus] =
    useState<TrainingStatusResponse | null>(null);
  const [trainingHistory, setTrainingHistory] = useState<TrainingResponse[]>(
    []
  );
  const [validationResults, setValidationResults] = useState<{
    is_valid: boolean;
    errors: string[];
    warnings: string[];
  } | null>(null);
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(
    null
  );
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [csvPreviewData, setCsvPreviewData] = useState<{
    headers: string[];
    rows: string[][];
  } | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    reset,
    setValue,
    formState: { errors },
  } = useForm<TrainingFormData>({
    defaultValues: {
      trainingData: "",
      validationSplit: 0.2,
      maxIterations: 100,
      targetMae: 0.5,
      calibrationMethod: "bayesian",
    },
  });

  const calibrationMethod = watch("calibrationMethod");

  useEffect(() => {
    loadTrainingHistory();
    return () => {
      if (pollingInterval) clearInterval(pollingInterval);
    };
  }, []);

  // Debug effect for CSV preview
  useEffect(() => {
    console.log("csvPreviewData state changed:", csvPreviewData);
  }, [csvPreviewData]);

  // Function to parse CSV and create preview data
  const parseCsvForPreview = (csvContent: string) => {
    console.log("parseCsvForPreview called with:", csvContent);
    if (!csvContent.trim()) {
      console.log("No CSV content, clearing preview");
      setCsvPreviewData(null);
      return;
    }

    const lines = csvContent.trim().split("\n");
    console.log("CSV lines:", lines);
    if (lines.length === 0) {
      console.log("No lines found, clearing preview");
      setCsvPreviewData(null);
      return;
    }

    const headers = lines[0].split(",").map((h) => h.trim());
    const rows = lines.slice(1, 6).map(
      (
        line // Show first 5 rows for preview
      ) => line.split(",").map((cell) => cell.trim())
    );

    console.log("Parsed CSV data:", { headers, rows });
    setCsvPreviewData({ headers, rows });
  };

  // Function to handle CSV content changes
  const handleCsvContentChange = (csvContent: string) => {
    setValue("trainingData", csvContent);
    parseCsvForPreview(csvContent);
  };

  const loadTrainingHistory = async () => {
    try {
      const history = await ApiClient.getTrainingHistory();
      setTrainingHistory(history);
    } catch (error) {
      console.error("Failed to load training history:", error);
    }
  };

  const handleDownloadTemplate = async () => {
    try {
      const template = await ApiClient.downloadTrainingTemplate();
      const blob = new Blob([template], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "training_data_template.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      toast.success("Training template downloaded!");
    } catch (error) {
      toast.error("Failed to download template");
    }
  };

  const validateTrainingData = async (csvContent: string) => {
    setIsValidating(true);
    try {
      const lines = csvContent.trim().split("\n");
      const headers = lines[0].split(",");
      const data: TrainingData[] = [];

      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(",");
        const row: any = {};
        headers.forEach((header, index) => {
          row[header.trim()] = values[index]?.trim() || "";
        });

        data.push({
          activation_time: parseFloat(row.activation_time),
          water_temperature: parseFloat(row.water_temperature),
          wind_speed: parseFloat(row.wind_speed),
          wind_speed_unit: row.wind_speed_unit,
          precipitation: parseFloat(row.precipitation),
          wave_height: parseFloat(row.wave_height),
          ambient_light: parseFloat(row.ambient_light),
          sensor_type: row.sensor_type,
          actual_distance: parseFloat(row.actual_distance),
          notes: row.notes,
        });
      }

      const validation = await ApiClient.validateTrainingData({
        training_data: data,
      });
      setValidationResults(validation);

      if (validation.is_valid) {
        toast.success("Training data is valid!");
      } else {
        toast.error(
          "Training data has errors. Please check the validation results."
        );
      }
    } catch (error) {
      toast.error("Failed to validate training data");
      setValidationResults({
        is_valid: false,
        errors: ["Failed to parse CSV data"],
        warnings: [],
      });
    } finally {
      setIsValidating(false);
    }
  };

  const onSubmit = async (data: TrainingFormData) => {
    setIsLoading(true);
    try {
      // Parse CSV data
      const lines = data.trainingData.trim().split("\n");
      const headers = lines[0].split(",");
      const trainingData: TrainingData[] = [];

      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(",");
        const row: any = {};
        headers.forEach((header, index) => {
          row[header.trim()] = values[index]?.trim() || "";
        });

        trainingData.push({
          activation_time: parseFloat(row.activation_time),
          water_temperature: parseFloat(row.water_temperature),
          wind_speed: parseFloat(row.wind_speed),
          wind_speed_unit: row.wind_speed_unit,
          precipitation: parseFloat(row.precipitation),
          wave_height: parseFloat(row.wave_height),
          ambient_light: parseFloat(row.ambient_light),
          sensor_type: row.sensor_type,
          actual_distance: parseFloat(row.actual_distance),
          notes: row.notes,
        });
      }

      const response = await ApiClient.startTraining({
        training_data: trainingData,
        max_iterations: data.maxIterations,
        target_mae: data.targetMae,
      });

      setTrainingStatus({
        training_id: response.training_id,
        status: response.status,
        progress: response.progress,
        current_mae: response.current_mae,
        best_mae: response.best_mae,
        iterations_completed: response.iterations_completed,
        total_iterations: response.total_iterations,
        estimated_time_remaining: response.estimated_time_remaining,
        warnings: response.warnings,
        errors: response.errors,
      });

      // Start polling for status updates
      const interval = setInterval(async () => {
        try {
          const status = await ApiClient.getTrainingStatus(
            response.training_id
          );
          setTrainingStatus(status);

          if (status.status === "completed" || status.status === "failed") {
            clearInterval(interval);
            setPollingInterval(null);
            loadTrainingHistory();
            if (status.status === "completed") {
              toast.success("Training completed successfully!");
            } else {
              toast.error("Training failed. Check the error details.");
            }
          }
        } catch (error) {
          console.error("Failed to get training status:", error);
        }
      }, 2000);

      setPollingInterval(interval);
      toast.success("Training started successfully!");
    } catch (error) {
      toast.error("Failed to start training");
    } finally {
      setIsLoading(false);
    }
  };

  const clearUploadedFile = () => {
    setUploadedFileName(null);
    setValue("trainingData", "");
    setValue("csvFile", undefined);
    setCsvPreviewData(null);
  };

  const handleStopTraining = async () => {
    if (!trainingStatus?.training_id) return;

    try {
      await ApiClient.stopTraining(trainingStatus.training_id);
      if (pollingInterval) {
        clearInterval(pollingInterval);
        setPollingInterval(null);
      }
      setTrainingStatus(null);
      toast.success("Training stopped");
    } catch (error) {
      toast.error("Failed to stop training");
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "running":
        return "text-blue-600";
      case "completed":
        return "text-green-600";
      case "failed":
        return "text-red-600";
      default:
        return "text-gray-600";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "running":
        return <Loader2 className="w-4 h-4 animate-spin" />;
      case "completed":
        return <CheckCircle className="w-4 h-4" />;
      case "failed":
        return <XCircle className="w-4 h-4" />;
      default:
        return <AlertCircle className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Model Training
        </h1>
        <p className="text-gray-600">
          Upload training data and calibrate the bioluminescence detection model
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Brain className="w-5 h-5 mr-2 text-primary-600" />
              Training Configuration
            </h3>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="form-label">Training Data (CSV)</label>
                <div className="space-y-4">
                  {/* File Upload */}
                  <div
                    className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-400 transition-colors"
                    onDragOver={(e) => {
                      e.preventDefault();
                      e.currentTarget.classList.add(
                        "border-primary-400",
                        "bg-primary-50"
                      );
                    }}
                    onDragLeave={(e) => {
                      e.preventDefault();
                      e.currentTarget.classList.remove(
                        "border-primary-400",
                        "bg-primary-50"
                      );
                    }}
                    onDrop={(e) => {
                      e.preventDefault();
                      e.currentTarget.classList.remove(
                        "border-primary-400",
                        "bg-primary-50"
                      );
                      const file = e.dataTransfer.files[0];
                      if (file && file.type === "text/csv") {
                        const reader = new FileReader();
                        reader.onload = (event) => {
                          const csvContent = event.target?.result as string;
                          setValue("trainingData", csvContent);
                          setValue("csvFile", file);
                          setUploadedFileName(file.name);
                          parseCsvForPreview(csvContent); // Update preview on drop
                        };
                        reader.readAsText(file);
                      }
                    }}
                  >
                    <input
                      type="file"
                      accept=".csv"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) {
                          const reader = new FileReader();
                          reader.onload = (event) => {
                            const csvContent = event.target?.result as string;
                            setValue("trainingData", csvContent);
                            setValue("csvFile", file);
                            setUploadedFileName(file.name);
                            parseCsvForPreview(csvContent); // Update preview on change
                          };
                          reader.readAsText(file);
                        }
                      }}
                      className="hidden"
                      id="csv-upload"
                    />
                    <label
                      htmlFor="csv-upload"
                      className="cursor-pointer flex flex-col items-center space-y-2"
                    >
                      <Upload className="w-6 h-6 text-gray-400" />
                      <div>
                        <span className="text-primary-600 hover:text-primary-700 font-medium">
                          Click to upload CSV file
                        </span>
                        <p className="text-sm text-gray-500">
                          or drag and drop here
                        </p>
                      </div>
                    </label>

                    {/* Show uploaded file name */}
                    {uploadedFileName && (
                      <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded-lg">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2 text-green-700">
                            <CheckCircle className="w-4 h-4" />
                            <span className="text-sm font-medium">
                              File uploaded: {uploadedFileName}
                            </span>
                          </div>
                          <button
                            type="button"
                            onClick={clearUploadedFile}
                            className="text-red-500 hover:text-red-700 text-sm font-medium"
                          >
                            Clear
                          </button>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Or paste text */}
                  <div className="text-center">
                    <span className="text-gray-500 text-sm">or</span>
                  </div>

                  <textarea
                    {...register("trainingData", {
                      required: "Training data is required",
                    })}
                    className="input-field h-32"
                    placeholder="Paste your CSV training data here..."
                    onChange={(e) => handleCsvContentChange(e.target.value)}
                  />

                  {/* CSV Preview Table */}
                  {csvPreviewData && (
                    <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <h4 className="font-medium text-blue-900 mb-3">
                        CSV Preview (First 5 rows)
                      </h4>
                      <div className="overflow-x-auto border border-gray-200 rounded-lg bg-white">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead className="bg-gray-50">
                            <tr>
                              {csvPreviewData.headers.map((header, index) => (
                                <th
                                  key={index}
                                  className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 last:border-r-0"
                                >
                                  {header}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {csvPreviewData.rows.map((row, rowIndex) => (
                              <tr
                                key={rowIndex}
                                className={
                                  rowIndex % 2 === 0 ? "bg-white" : "bg-gray-50"
                                }
                              >
                                {row.map((cell, cellIndex) => (
                                  <td
                                    key={cellIndex}
                                    className="px-3 py-2 text-sm text-gray-900 border-r border-gray-200 last:border-r-0"
                                  >
                                    {cell}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                      <p className="text-xs text-blue-600 mt-2">
                        Showing first 5 rows of {csvPreviewData.rows.length + 1}{" "}
                        total rows
                      </p>
                      <p className="text-xs text-blue-500 mt-1">
                        Debug: csvPreviewData state is set correctly
                      </p>
                    </div>
                  )}

                  {/* Debug display */}
                  <div className="mt-4 p-3 bg-gray-100 border border-gray-300 rounded-lg">
                    <h5 className="font-medium text-gray-700 mb-2">
                      Debug Info:
                    </h5>
                    <p className="text-xs text-gray-600">
                      csvPreviewData: {csvPreviewData ? "SET" : "NULL"}
                    </p>
                    {csvPreviewData && (
                      <p className="text-xs text-gray-600">
                        Headers: {csvPreviewData.headers.length}, Rows:{" "}
                        {csvPreviewData.rows.length}
                      </p>
                    )}
                  </div>
                </div>

                {errors.trainingData && (
                  <p className="text-red-600 text-sm mt-1">
                    {errors.trainingData.message}
                  </p>
                )}

                <div className="flex space-x-2 mt-2">
                  <button
                    type="button"
                    onClick={handleDownloadTemplate}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download Template</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => validateTrainingData(watch("trainingData"))}
                    disabled={isValidating || !watch("trainingData")}
                    className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
                  >
                    {isValidating ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <CheckCircle className="w-4 h-4" />
                    )}
                    <span>
                      {isValidating ? "Validating..." : "Validate Data"}
                    </span>
                  </button>
                  {/* Test button for CSV preview */}
                  <button
                    type="button"
                    onClick={() => {
                      const testCSV = `activation_time,water_temperature,wind_speed,wind_speed_unit,precipitation,wave_height,ambient_light,sensor_type,actual_distance,notes
45.0,8.5,5.2,m/s,2.4,1.2,0.002,drone,125.5,Test deployment 1
60.0,10.2,3.1,knots,0.0,0.5,0.0005,nvg,89.2,Clear night conditions
30.0,5.8,12.4,beaufort,8.7,2.3,0.01,human,45.8,Stormy conditions`;
                      parseCsvForPreview(testCSV);
                    }}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <span>Test CSV Preview</span>
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Validation Split</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0.1"
                    max="0.5"
                    {...register("validationSplit", {
                      required: "Validation split is required",
                      min: { value: 0.1, message: "Minimum 0.1" },
                      max: { value: 0.5, message: "Maximum 0.5" },
                    })}
                    className="input-field"
                  />
                  {errors.validationSplit && (
                    <p className="text-red-600 text-sm mt-1">
                      {errors.validationSplit.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="form-label">Max Iterations</label>
                  <input
                    type="number"
                    min="10"
                    max="1000"
                    {...register("maxIterations", {
                      required: "Max iterations is required",
                      min: { value: 10, message: "Minimum 10" },
                      max: { value: 1000, message: "Maximum 1000" },
                    })}
                    className="input-field"
                  />
                  {errors.maxIterations && (
                    <p className="text-red-600 text-sm mt-1">
                      {errors.maxIterations.message}
                    </p>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Target MAE</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0.1"
                    {...register("targetMae", {
                      required: "Target MAE is required",
                      min: { value: 0.1, message: "Minimum 0.1" },
                    })}
                    className="input-field"
                  />
                  {errors.targetMae && (
                    <p className="text-red-600 text-sm mt-1">
                      {errors.targetMae.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="form-label">Calibration Method</label>
                  <select
                    {...register("calibrationMethod", {
                      required: "Calibration method is required",
                    })}
                    className="input-field"
                  >
                    {CALIBRATION_METHODS.map((method) => (
                      <option key={method.value} value={method.value}>
                        {method.label}
                      </option>
                    ))}
                  </select>
                  {errors.calibrationMethod && (
                    <p className="text-red-600 text-sm mt-1">
                      {errors.calibrationMethod.message}
                    </p>
                  )}
                </div>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">
                  Selected Method:{" "}
                  {
                    CALIBRATION_METHODS.find(
                      (m) => m.value === calibrationMethod
                    )?.label
                  }
                </h4>
                <p className="text-blue-700 text-sm">
                  {
                    CALIBRATION_METHODS.find(
                      (m) => m.value === calibrationMethod
                    )?.description
                  }
                </p>
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
                    <Play className="w-4 h-4" />
                  )}
                  <span>
                    {isLoading ? "Starting Training..." : "Start Training"}
                  </span>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    reset();
                    clearUploadedFile();
                    setCsvPreviewData(null);
                  }}
                  className="btn-secondary"
                >
                  Reset Form
                </button>
                {trainingStatus?.status === "running" && (
                  <button
                    type="button"
                    onClick={handleStopTraining}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <Square className="w-4 h-4" />
                    <span>Stop Training</span>
                  </button>
                )}
              </div>
            </form>
          </div>

          {validationResults && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Data Validation Results
              </h3>
              <div className="space-y-3">
                <div
                  className={cn(
                    "flex items-center space-x-2 p-3 rounded-lg",
                    validationResults.is_valid
                      ? "bg-green-50 text-green-800"
                      : "bg-red-50 text-red-800"
                  )}
                >
                  {validationResults.is_valid ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : (
                    <XCircle className="w-5 h-5" />
                  )}
                  <span className="font-medium">
                    {validationResults.is_valid
                      ? "Data is valid"
                      : "Data has errors"}
                  </span>
                </div>

                {validationResults.errors.length > 0 && (
                  <div>
                    <h4 className="font-medium text-red-800 mb-2">Errors:</h4>
                    <ul className="text-sm text-red-700 space-y-1">
                      {validationResults.errors.map((error, index) => (
                        <li key={index}>• {error}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {validationResults.warnings.length > 0 && (
                  <div>
                    <h4 className="font-medium text-yellow-800 mb-2">
                      Warnings:
                    </h4>
                    <ul className="text-sm text-yellow-700 space-y-1">
                      {validationResults.warnings.map((warning, index) => (
                        <li key={index}>• {warning}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="space-y-6">
          {trainingStatus && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
                Training Progress
              </h3>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="font-medium">Status:</span>
                  <div
                    className={cn(
                      "flex items-center space-x-2",
                      getStatusColor(trainingStatus.status)
                    )}
                  >
                    {getStatusIcon(trainingStatus.status)}
                    <span className="capitalize">{trainingStatus.status}</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{trainingStatus.progress.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${trainingStatus.progress}%` }}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Current MAE:</span>
                    <span className="ml-2 font-medium">
                      {trainingStatus.current_mae.toFixed(3)}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Best MAE:</span>
                    <span className="ml-2 font-medium">
                      {trainingStatus.best_mae.toFixed(3)}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Iterations:</span>
                    <span className="ml-2 font-medium">
                      {trainingStatus.iterations_completed}/
                      {trainingStatus.total_iterations}
                    </span>
                  </div>
                  {trainingStatus.estimated_time_remaining && (
                    <div>
                      <span className="text-gray-600">ETA:</span>
                      <span className="ml-2 font-medium">
                        {trainingStatus.estimated_time_remaining}
                      </span>
                    </div>
                  )}
                </div>

                {trainingStatus.warnings.length > 0 && (
                  <div className="bg-yellow-50 p-3 rounded-lg">
                    <h4 className="font-medium text-yellow-800 mb-2">
                      Warnings:
                    </h4>
                    <ul className="text-sm text-yellow-700 space-y-1">
                      {trainingStatus.warnings.map((warning, index) => (
                        <li key={index}>• {warning}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {trainingStatus.errors.length > 0 && (
                  <div className="bg-red-50 p-3 rounded-lg">
                    <h4 className="font-medium text-red-800 mb-2">Errors:</h4>
                    <ul className="text-sm text-red-700 space-y-1">
                      {trainingStatus.errors.map((error, index) => (
                        <li key={index}>• {error}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <History className="w-5 h-5 mr-2 text-primary-600" />
              Training History
            </h3>

            {trainingHistory.length > 0 ? (
              <div className="space-y-3">
                {trainingHistory.slice(0, 5).map((training) => (
                  <div
                    key={training.training_id}
                    className="border border-gray-200 rounded-lg p-3"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-600">
                        {new Date(training.timestamp).toLocaleDateString()}
                      </span>
                      <div
                        className={cn(
                          "flex items-center space-x-1",
                          getStatusColor(training.status)
                        )}
                      >
                        {getStatusIcon(training.status)}
                        <span className="text-xs capitalize">
                          {training.status}
                        </span>
                      </div>
                    </div>
                    <div className="text-sm space-y-1">
                      <div>Best MAE: {training.best_mae.toFixed(3)}</div>
                      <div>
                        Method:{" "}
                        {training.validation_results
                          ? "Completed"
                          : "In Progress"}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">
                No training history available
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
