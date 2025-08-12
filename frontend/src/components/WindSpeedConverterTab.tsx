"use client";

import { useState } from "react";
import { Wind, ArrowRight } from "lucide-react";

export default function WindSpeedConverterTab() {
  const [inputValue, setInputValue] = useState("");
  const [inputUnit, setInputUnit] = useState("m/s");
  const [results, setResults] = useState<Record<string, number> | null>(null);

  const units = [
    { value: "m/s", label: "Meters per second (m/s)" },
    { value: "knots", label: "Knots" },
    { value: "mph", label: "Miles per hour (mph)" },
    { value: "km/h", label: "Kilometers per hour (km/h)" },
    { value: "beaufort", label: "Beaufort Scale" },
  ];

  const convertWindSpeed = () => {
    const value = parseFloat(inputValue);
    if (isNaN(value) || value < 0) return;

    const conversions: Record<string, number> = {};

    // Convert from input unit to all other units
    switch (inputUnit) {
      case "m/s":
        conversions["m/s"] = value;
        conversions["knots"] = value * 1.94384;
        conversions["mph"] = value * 2.23694;
        conversions["km/h"] = value * 3.6;
        conversions["beaufort"] = getBeaufortScale(value);
        break;
      case "knots":
        conversions["m/s"] = value / 1.94384;
        conversions["knots"] = value;
        conversions["mph"] = value * 1.15078;
        conversions["km/h"] = value * 1.852;
        conversions["beaufort"] = getBeaufortScale(value / 1.94384);
        break;
      case "mph":
        conversions["m/s"] = value / 2.23694;
        conversions["knots"] = value / 1.15078;
        conversions["mph"] = value;
        conversions["km/h"] = value * 1.60934;
        conversions["beaufort"] = getBeaufortScale(value / 2.23694);
        break;
      case "km/h":
        conversions["m/s"] = value / 3.6;
        conversions["knots"] = value / 1.852;
        conversions["mph"] = value / 1.60934;
        conversions["km/h"] = value;
        conversions["beaufort"] = getBeaufortScale(value / 3.6);
        break;
      case "beaufort":
        const mps = getMpsFromBeaufort(value);
        conversions["m/s"] = mps;
        conversions["knots"] = mps * 1.94384;
        conversions["mph"] = mps * 2.23694;
        conversions["km/h"] = mps * 3.6;
        conversions["beaufort"] = value;
        break;
    }

    setResults(conversions);
  };

  const getBeaufortScale = (mps: number): number => {
    if (mps < 0.3) return 0;
    if (mps < 1.6) return 1;
    if (mps < 3.4) return 2;
    if (mps < 5.5) return 3;
    if (mps < 8.0) return 4;
    if (mps < 10.8) return 5;
    if (mps < 13.9) return 6;
    if (mps < 17.2) return 7;
    if (mps < 20.8) return 8;
    if (mps < 24.5) return 9;
    if (mps < 28.5) return 10;
    if (mps < 32.7) return 11;
    return 12;
  };

  const getMpsFromBeaufort = (beaufort: number): number => {
    const ranges = [
      0, 0.3, 1.6, 3.4, 5.5, 8.0, 10.8, 13.9, 17.2, 20.8, 24.5, 28.5, 32.7,
    ];
    return ranges[Math.min(Math.floor(beaufort), 12)] || 0;
  };

  const getBeaufortDescription = (scale: number): string => {
    const descriptions = [
      "Calm",
      "Light air",
      "Light breeze",
      "Gentle breeze",
      "Moderate breeze",
      "Fresh breeze",
      "Strong breeze",
      "Near gale",
      "Gale",
      "Strong gale",
      "Storm",
      "Violent storm",
      "Hurricane",
    ];
    return descriptions[Math.min(Math.floor(scale), 12)] || "Unknown";
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Wind Speed Converter
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Convert wind speed between different units including the Beaufort
          scale for marine operations.
        </p>
      </div>

      <div className="max-w-2xl mx-auto">
        <div className="card">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Wind className="w-5 h-5 mr-2 text-primary-600" />
                Convert Wind Speed
              </h3>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Wind Speed Value</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    className="input-field"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Enter wind speed"
                  />
                </div>
                <div>
                  <label className="form-label">Input Unit</label>
                  <select
                    className="input-field"
                    value={inputUnit}
                    onChange={(e) => setInputUnit(e.target.value)}
                  >
                    {units.map((unit) => (
                      <option key={unit.value} value={unit.value}>
                        {unit.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <button
                onClick={convertWindSpeed}
                disabled={!inputValue || parseFloat(inputValue) < 0}
                className="btn-primary mt-4 disabled:opacity-50"
              >
                Convert
              </button>
            </div>

            {results && (
              <div>
                <h4 className="text-md font-semibold text-gray-900 mb-3">
                  Conversion Results
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {Object.entries(results).map(([unit, value]) => (
                    <div key={unit} className="bg-gray-50 p-3 rounded-lg">
                      <div className="text-sm font-medium text-gray-500 capitalize">
                        {unit === "beaufort" ? "Beaufort Scale" : unit}
                      </div>
                      <div className="text-lg font-semibold text-gray-900">
                        {unit === "beaufort"
                          ? `${value} - ${getBeaufortDescription(value)}`
                          : value.toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
