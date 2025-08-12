"use client";

import { useState } from "react";
import { Zap, Wind, FileText, Info, Menu, X, Brain } from "lucide-react";
import { cn } from "@/lib/utils";
import PredictionTab from "@/components/PredictionTab";
import WindSpeedConverterTab from "@/components/WindSpeedConverterTab";
import BulkPredictionTab from "@/components/BulkPredictionTab";
import ModelInfoTab from "@/components/ModelInfoTab";
import TrainingTab from "@/components/TrainingTab";

type TabType =
  | "prediction"
  | "wind-converter"
  | "bulk"
  | "model-info"
  | "training";
const tabs = [
  { id: "prediction", label: "Prediction", icon: Zap },
  { id: "wind-converter", label: "Wind Converter", icon: Wind },
  { id: "bulk", label: "Bulk Prediction", icon: FileText },
  { id: "training", label: "Model Training", icon: Brain },
  { id: "model-info", label: "Model Info", icon: Info },
] as const;

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<TabType>("prediction");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const renderTabContent = () => {
    switch (activeTab) {
      case "prediction":
        return <PredictionTab />;
      case "wind-converter":
        return <WindSpeedConverterTab />;
      case "bulk":
        return <BulkPredictionTab />;
      case "training":
        return <TrainingTab />;
      case "model-info":
        return <ModelInfoTab />;
      default:
        return <PredictionTab />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-xl font-bold text-gray-900">
                  Bioluminescent Detection AI
                </h1>
              </div>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as TabType)}
                    className={cn(
                      "flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                      activeTab === tab.id
                        ? "bg-primary-100 text-primary-700"
                        : "text-gray-500 hover:text-gray-700 hover:bg-gray-100"
                    )}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </nav>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="text-gray-500 hover:text-gray-700"
              >
                {isMobileMenuOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMobileMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => {
                        setActiveTab(tab.id as TabType);
                        setIsMobileMenuOpen(false);
                      }}
                      className={cn(
                        "flex items-center space-x-2 w-full px-3 py-2 rounded-md text-base font-medium transition-colors",
                        activeTab === tab.id
                          ? "bg-primary-100 text-primary-700"
                          : "text-gray-500 hover:text-gray-700 hover:bg-gray-100"
                      )}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-fade-in">{renderTabContent()}</div>
      </div>
    </div>
  );
}
