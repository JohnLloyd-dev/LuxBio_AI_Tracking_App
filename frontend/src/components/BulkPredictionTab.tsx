"use client";

import { useState } from "react";
import {
  FileText,
  Upload,
  Download,
  Zap,
  Loader2,
  CheckCircle,
  AlertCircle,
} from "lucide-react";
import { toast } from "react-hot-toast";
import { ApiClient } from "@/lib/api";
import type { PredictionRequest, PredictionResponse } from "@/types/api";

export default function BulkPredictionTab() {
  const [csvData, setCsvData] = useState("");
  const [csvPreviewData, setCsvPreviewData] = useState<{
    headers: string[];
    rows: string[][];
  } | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [predictions, setPredictions] = useState<PredictionResponse[]>([]);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);

  // Function to parse CSV and create preview data
  const parseCsvForPreview = (csvContent: string) => {
    if (!csvContent.trim()) {
      setCsvPreviewData(null);
      return;
    }

    const lines = csvContent.trim().split("\n");
    if (lines.length === 0) {
      setCsvPreviewData(null);
      return;
    }

    const headers = lines[0].split(",").map((h) => h.trim());
    const rows = lines.slice(1, 6).map(
      (
        line // Show first 5 rows for preview
      ) => line.split(",").map((cell) => cell.trim())
    );

    setCsvPreviewData({ headers, rows });
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFileName(file.name);
      const reader = new FileReader();
      reader.onload = (e) => {
        const csvContent = e.target?.result as string;
        setCsvData(csvContent);
        parseCsvForPreview(csvContent);
      };
      reader.readAsText(file);
    }
  };

  const clearUploadedFile = () => {
    setCsvData("");
    setCsvPreviewData(null);
    setUploadedFileName(null);
    setPredictions([]);
  };

  const downloadTemplate = () => {
    const template = `activation_time,water_temperature,wind_speed,wind_speed_unit,precipitation,wave_height,ambient_light,sensor_type,sensor_model
45.0,8.5,5.2,m/s,2.4,1.2,0.002,drone,DJI M30T
60.0,10.2,3.1,knots,0.0,0.5,0.0005,nvg,Standard NVG
30.0,5.8,12.4,beaufort,8.7,2.3,0.01,human,Unaided Eye`;

    const blob = new Blob([template], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "bulk_prediction_template.csv";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const processPredictions = async () => {
    if (!csvData.trim()) {
      toast.error("No CSV data to process");
      return;
    }

    setIsProcessing(true);
    try {
      // Parse CSV data
      const lines = csvData.trim().split("\n");
      const headers = lines[0].split(",").map((h) => h.trim());
      const bulkRequests: PredictionRequest[] = [];

      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(",");
        const row: any = {};
        headers.forEach((header, index) => {
          row[header.trim()] = values[index]?.trim() || "";
        });

        // Convert CSV data to PredictionRequest format
        const request: PredictionRequest = {
          temporal_parameters: {
            activation_time: parseFloat(row.activation_time) || 45.0,
            water_temperature: parseFloat(row.water_temperature) || 8.5,
          },
          environmental_conditions: {
            wind_speed: parseFloat(row.wind_speed) || 5.2,
            wind_speed_unit: row.wind_speed_unit || "m/s",
            precipitation: parseFloat(row.precipitation) || 2.4,
            wave_height: parseFloat(row.wave_height) || 1.2,
            ambient_light: parseFloat(row.ambient_light) || 0.002,
          },
          sensor_parameters: {
            type: row.sensor_type || "drone", // Convert sensor_type to type
            model: row.sensor_model || "",
          },
          product_parameters: {},
        };

        bulkRequests.push(request);
      }

      // Send bulk prediction request
      const results = await ApiClient.predictBulk(bulkRequests);
      setPredictions(results);
      toast.success(`Successfully processed ${results.length} predictions!`);
    } catch (error) {
      console.error("Bulk prediction failed:", error);
      toast.error(
        "Failed to process predictions. Please check your data format."
      );
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Bulk Prediction
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Upload CSV files with multiple environmental conditions for batch
          prediction processing.
        </p>
      </div>

      <div className="max-w-6xl mx-auto">
        <div className="card">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <FileText className="w-5 h-5 mr-2 text-primary-600" />
                Bulk Prediction Interface
              </h3>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-md font-medium text-gray-900 mb-3">
                    Download Template
                  </h4>
                  <p className="text-sm text-gray-600 mb-3">
                    Use this CSV template to prepare your bulk prediction data.
                  </p>
                  <button
                    onClick={downloadTemplate}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download Template</span>
                  </button>
                </div>

                <div>
                  <h4 className="text-md font-medium text-gray-900 mb-3">
                    Upload CSV File
                  </h4>
                  <p className="text-sm text-gray-600 mb-3">
                    Upload your prepared CSV file for bulk processing.
                  </p>
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileUpload}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
                  />

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
              </div>
            </div>

            {/* CSV Preview Table */}
            {csvPreviewData && (
              <div>
                <h4 className="text-md font-medium text-gray-900 mb-3">
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
                <p className="text-xs text-gray-500 mt-2">
                  Showing first 5 rows of {csvPreviewData.rows.length + 1} total
                  rows
                </p>
              </div>
            )}

            {csvData && (
              <div className="mt-4">
                <button
                  onClick={processPredictions}
                  disabled={isProcessing}
                  className="btn-primary flex items-center space-x-2 disabled:opacity-50"
                >
                  {isProcessing ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Zap className="w-4 h-4" />
                  )}
                  <span>
                    {isProcessing ? "Processing..." : "Process Predictions"}
                  </span>
                </button>
              </div>
            )}

            {/* Predictions Results */}
            {predictions.length > 0 && (
              <div>
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  Prediction Results ({predictions.length} predictions)
                </h4>
                <div className="overflow-x-auto border border-gray-200 rounded-lg">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          #
                        </th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Distance (m)
                        </th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Performance Score
                        </th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Validation Status
                        </th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Warnings
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {predictions.map((prediction, index) => (
                        <tr
                          key={index}
                          className={
                            index % 2 === 0 ? "bg-white" : "bg-gray-50"
                          }
                        >
                          <td className="px-3 py-2 text-sm text-gray-900">
                            {index + 1}
                          </td>
                          <td className="px-3 py-2 text-sm font-medium text-gray-900">
                            {prediction.distance.toFixed(1)}
                          </td>
                          <td className="px-3 py-2 text-sm text-gray-900">
                            {prediction.performance_score.toFixed(1)}%
                          </td>
                          <td className="px-3 py-2 text-sm text-gray-900">
                            {prediction.validation_status}
                          </td>
                          <td className="px-3 py-2 text-sm text-gray-900">
                            {prediction.warnings.length > 0 ? (
                              <div className="flex items-center space-x-1">
                                <AlertCircle className="w-4 h-4 text-yellow-500" />
                                <span className="text-yellow-700">
                                  {prediction.warnings.length} warning(s)
                                </span>
                              </div>
                            ) : (
                              <div className="flex items-center space-x-1">
                                <CheckCircle className="w-4 h-4 text-green-500" />
                                <span className="text-green-700">
                                  No warnings
                                </span>
                              </div>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
