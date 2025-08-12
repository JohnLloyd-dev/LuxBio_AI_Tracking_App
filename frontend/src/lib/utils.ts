import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(value: number, decimals: number = 2): string {
  return value.toFixed(decimals);
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(1)}%`;
}

export function formatTimestamp(timestamp: string): string {
  return new Date(timestamp).toLocaleString();
}

export function validateWindSpeed(value: number, unit: string): boolean {
  if (unit === "beaufort") {
    return value >= 0 && value <= 12 && Number.isInteger(value);
  }
  return value >= 0 && value <= 25;
}

export function validateActivationTime(value: number): boolean {
  return value >= 0 && value <= 360;
}

export function validateWaterTemperature(value: number): boolean {
  return value >= -2 && value <= 30;
}

export function validatePrecipitation(value: number): boolean {
  return value >= 0 && value <= 50;
}

export function validateWaveHeight(value: number): boolean {
  return value >= 0 && value <= 10;
}

export function validateAmbientLight(value: number): boolean {
  return value >= 0.0001 && value <= 0.1;
}

export function getWindSpeedUnitInfo(unit: string): {
  label: string;
  description: string;
} {
  const unitInfo = {
    "m/s": {
      label: "Meters per second",
      description: "Scientific standard unit for wind speed",
    },
    knots: {
      label: "Nautical miles per hour",
      description: "Marine and aviation standard",
    },
    mph: {
      label: "Statute miles per hour",
      description: "US land-based weather stations",
    },
    nmph: {
      label: "Nautical miles per hour",
      description: "Alternative notation for knots",
    },
    "km/h": {
      label: "Kilometers per hour",
      description: "International metric unit",
    },
    beaufort: {
      label: "Beaufort scale",
      description: "Categorical wind scale (0-12)",
    },
  };

  return (
    unitInfo[unit as keyof typeof unitInfo] || {
      label: "Unknown unit",
      description: "Unsupported wind speed unit",
    }
  );
}

export function getSensorTypeInfo(type: string): {
  label: string;
  description: string;
} {
  const sensorInfo = {
    drone: {
      label: "Drone Camera",
      description: "Aerial detection with camera sensors",
    },
    human: {
      label: "Human Observer",
      description: "Visual detection by trained personnel",
    },
    nvg: {
      label: "Night Vision Goggles",
      description: "Enhanced night-time detection",
    },
  };

  return (
    sensorInfo[type as keyof typeof sensorInfo] || {
      label: "Unknown sensor",
      description: "Unsupported sensor type",
    }
  );
}

export function generateCSVTemplate(): string {
  return `activation_time,water_temp,wind_speed,wind_speed_unit,precip,wave_ht,ambient_light,sensor_type
45.0,8.5,5.2,m/s,2.4,1.2,0.002,drone
60.0,10.2,3.1,knots,0.0,0.5,0.0005,nvg
30.0,5.8,12.4,beaufort,8.7,2.3,0.01,human`;
}

export function downloadCSV(content: string, filename: string): void {
  const blob = new Blob([content], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export function parseCSV(csvContent: string): any[] {
  const lines = csvContent.trim().split("\n");
  const headers = lines[0].split(",");
  const data = [];

  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(",");
    const row: any = {};

    headers.forEach((header, index) => {
      const value = values[index]?.trim();
      row[header.trim()] = isNaN(Number(value)) ? value : Number(value);
    });

    data.push(row);
  }

  return data;
}
