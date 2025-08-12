"use client";

import { Info, Brain, Zap, Settings } from "lucide-react";

export default function ModelInfoTab() {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Model Information
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Learn about the bioluminescent detection AI model architecture and
          capabilities.
        </p>
      </div>

      <div className="max-w-4xl mx-auto space-y-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Brain className="w-5 h-5 mr-2 text-primary-600" />
            Model Overview
          </h3>
          <div className="prose prose-gray max-w-none">
            <p className="text-gray-700">
              The Bioluminescent Detection AI model combines physics-based light
              decay modeling with machine learning optimization to predict
              maximum detection distances for bioluminescent beads under various
              environmental conditions.
            </p>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Zap className="w-5 h-5 mr-2 text-primary-600" />
            Key Features
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-medium text-gray-900">
                    Physics-Based Modeling
                  </h4>
                  <p className="text-sm text-gray-600">
                    Arrhenius kinetics for light decay
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-medium text-gray-900">
                    Environmental Factors
                  </h4>
                  <p className="text-sm text-gray-600">
                    Wind, precipitation, wave height, ambient light
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-medium text-gray-900">
                    Multi-Sensor Support
                  </h4>
                  <p className="text-sm text-gray-600">
                    Drone, human observer, NVG compatibility
                  </p>
                </div>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-medium text-gray-900">
                    Machine Learning
                  </h4>
                  <p className="text-sm text-gray-600">
                    Bayesian optimization and adaptive learning
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-medium text-gray-900">
                    Real-Time Updates
                  </h4>
                  <p className="text-sm text-gray-600">
                    Continuous model improvement
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                <div>
                  <h4 className="font-medium text-gray-900">
                    Uncertainty Quantification
                  </h4>
                  <p className="text-sm text-gray-600">
                    Confidence intervals and error bounds
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Settings className="w-5 h-5 mr-2 text-primary-600" />
            Technical Specifications
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">
                Input Parameters
              </h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Activation time: 0-360 minutes</li>
                <li>• Water temperature: -2 to 30°C</li>
                <li>• Wind speed: Multiple units supported</li>
                <li>• Precipitation: 0-50 mm/hr</li>
                <li>• Wave height: 0-10 meters</li>
                <li>• Ambient light: 0.0001-0.1 lux</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Output Metrics</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Maximum detection distance (meters)</li>
                <li>• Prediction confidence (0-1)</li>
                <li>• Uncertainty bounds (±meters)</li>
                <li>• Environmental impact factors</li>
                <li>• Sensor-specific optimizations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
