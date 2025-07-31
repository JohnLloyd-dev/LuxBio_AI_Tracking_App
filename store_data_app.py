#!/usr/bin/env python3
"""
Store Data App for LuxBio AI Tracking App
Individual data input application with validation and guidance
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
from datetime import datetime
import os
import re

class StoreDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LuxBio AI Tracking - Data Input App")
        self.root.geometry("800x900")
        
        # Data storage
        self.current_data = {}
        self.validation_errors = []
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self.setup_ui()
        self.load_validation_rules()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="LuxBio AI Tracking - Field Data Input",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Create input fields
        self.create_input_fields()
        
        # Create buttons
        self.create_buttons()
        
        # Create status area
        self.create_status_area()
        
    def create_input_fields(self):
        """Create all input fields with labels and validation"""
        
        # Test ID
        self.create_field("test_id", "Test ID:", "VH-001", 2, 
                         "Unique identifier for this test (e.g., VH-001)")
        
        # Date
        self.create_field("date", "Date:", datetime.now().strftime("%Y-%m-%d"), 3,
                         "Test date (YYYY-MM-DD format)")
        
        # GPS Coordinates
        self.create_field("lat", "Latitude:", "48.423", 4,
                         "GPS latitude (-90 to 90 degrees)")
        self.create_field("lon", "Longitude:", "-123.367", 5,
                         "GPS longitude (-180 to 180 degrees)")
        
        # Actual Distance
        self.create_field("actual_distance", "Actual Distance (m):", "320", 6,
                         "Detection range in meters (0-1000)")
        
        # Activation Time
        self.create_field("activation_time", "Activation Time (min):", "45", 7,
                         "Minutes since bead activation (0-360)")
        
        # Water Temperature
        self.create_field("water_temp", "Water Temperature (°C):", "8.5", 8,
                         "Water temperature (-2 to 30°C)")
        
        # Wind Speed
        self.create_field("wind_speed", "Wind Speed (m/s):", "5.2", 9,
                         "Wind speed at 10m height (0-25 m/s)")
        
        # Precipitation
        self.create_field("precipitation", "Precipitation (mm/hr):", "2.4", 10,
                         "Rain intensity (0-50 mm/hr)")
        
        # Wave Height
        self.create_field("wave_height", "Wave Height (m):", "1.2", 11,
                         "Significant wave height (0-10 m)")
        
        # Ambient Light
        self.create_field("ambient_light", "Ambient Light (lux):", "0.002", 12,
                         "Background illumination (0.0001-0.1 lux)")
        
        # Sensor Type
        self.create_sensor_type_field(13)
        
        # Notes
        self.create_field("notes", "Notes:", "", 14,
                         "Additional observations or comments")
        
    def create_field(self, field_name, label_text, default_value, row, tooltip_text):
        """Create a labeled input field with validation"""
        
        # Label
        label = ttk.Label(self.main_frame, text=label_text, font=('Arial', 10, 'bold'))
        label.grid(row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        
        # Entry field
        entry = ttk.Entry(self.main_frame, width=30, font=('Arial', 10))
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Tooltip label
        tooltip = ttk.Label(self.main_frame, text=tooltip_text, 
                           font=('Arial', 8), foreground='gray')
        tooltip.grid(row=row, column=2, sticky=tk.W, pady=5)
        
        # Store reference
        setattr(self, f"{field_name}_entry", entry)
        
        # Bind validation
        entry.bind('<FocusOut>', lambda e: self.validate_field(field_name))
        entry.bind('<KeyRelease>', lambda e: self.clear_field_error(field_name))
        
    def create_sensor_type_field(self, row):
        """Create sensor type dropdown field"""
        
        # Label
        label = ttk.Label(self.main_frame, text="Sensor Type:", 
                         font=('Arial', 10, 'bold'))
        label.grid(row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        
        # Dropdown
        sensor_types = ["drone", "human", "nvg"]
        combo = ttk.Combobox(self.main_frame, values=sensor_types, 
                            state="readonly", width=27, font=('Arial', 10))
        combo.set("drone")
        combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Tooltip
        tooltip = ttk.Label(self.main_frame, 
                           text="Detection technology used (human/drone/nvg)",
                           font=('Arial', 8), foreground='gray')
        tooltip.grid(row=row, column=2, sticky=tk.W, pady=5)
        
        # Store reference
        self.sensor_type_combo = combo
        
    def create_buttons(self):
        """Create action buttons"""
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=15, column=0, columnspan=3, pady=20)
        
        # Validate button
        validate_btn = ttk.Button(
            button_frame, 
            text="Validate Data", 
            command=self.validate_all_fields
        )
        validate_btn.pack(side=tk.LEFT, padx=5)
        
        # Save to CSV button
        save_csv_btn = ttk.Button(
            button_frame, 
            text="Save to CSV", 
            command=self.save_to_csv
        )
        save_csv_btn.pack(side=tk.LEFT, padx=5)
        
        # Save to JSON button
        save_json_btn = ttk.Button(
            button_frame, 
            text="Save to JSON", 
            command=self.save_to_json
        )
        save_json_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(
            button_frame, 
            text="Clear Form", 
            command=self.clear_form
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Help button
        help_btn = ttk.Button(
            button_frame, 
            text="Help", 
            command=self.show_help
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        
    def create_status_area(self):
        """Create status display area"""
        
        # Status label
        status_label = ttk.Label(self.main_frame, text="Status:", 
                                font=('Arial', 10, 'bold'))
        status_label.grid(row=16, column=0, sticky=tk.W, pady=(20, 5))
        
        # Status text
        self.status_text = tk.Text(self.main_frame, height=8, width=80, 
                                  font=('Arial', 9), wrap=tk.WORD)
        self.status_text.grid(row=17, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, 
                                 command=self.status_text.yview)
        scrollbar.grid(row=17, column=3, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
    def load_validation_rules(self):
        """Load validation rules for each field"""
        
        self.validation_rules = {
            'test_id': {
                'pattern': r'^[A-Z]{2}-\d{3}$',
                'message': 'Test ID must be in format XX-XXX (e.g., VH-001)',
                'required': True
            },
            'date': {
                'pattern': r'^\d{4}-\d{2}-\d{2}$',
                'message': 'Date must be in YYYY-MM-DD format',
                'required': True
            },
            'lat': {
                'min': -90,
                'max': 90,
                'message': 'Latitude must be between -90 and 90 degrees',
                'required': True
            },
            'lon': {
                'min': -180,
                'max': 180,
                'message': 'Longitude must be between -180 and 180 degrees',
                'required': True
            },
            'actual_distance': {
                'min': 0,
                'max': 1000,
                'message': 'Actual distance must be between 0 and 1000 meters',
                'required': True
            },
            'activation_time': {
                'min': 0,
                'max': 360,
                'message': 'Activation time must be between 0 and 360 minutes',
                'required': True
            },
            'water_temp': {
                'min': -2,
                'max': 30,
                'message': 'Water temperature must be between -2 and 30°C',
                'required': True
            },
            'wind_speed': {
                'min': 0,
                'max': 25,
                'message': 'Wind speed must be between 0 and 25 m/s',
                'required': True
            },
            'precipitation': {
                'min': 0,
                'max': 50,
                'message': 'Precipitation must be between 0 and 50 mm/hr',
                'required': True
            },
            'wave_height': {
                'min': 0,
                'max': 10,
                'message': 'Wave height must be between 0 and 10 meters',
                'required': True
            },
            'ambient_light': {
                'min': 0.0001,
                'max': 0.1,
                'message': 'Ambient light must be between 0.0001 and 0.1 lux',
                'required': True
            },
            'sensor_type': {
                'values': ['human', 'drone', 'nvg'],
                'message': 'Sensor type must be human, drone, or nvg',
                'required': True
            },
            'notes': {
                'required': False
            }
        }
        
    def validate_field(self, field_name):
        """Validate a single field"""
        
        # Get field value
        if field_name == 'sensor_type':
            value = self.sensor_type_combo.get()
        else:
            value = getattr(self, f"{field_name}_entry").get().strip()
        
        # Get validation rules
        rules = self.validation_rules.get(field_name, {})
        
        # Check if required
        if rules.get('required', False) and not value:
            self.show_field_error(field_name, f"{field_name} is required")
            return False
        
        # Skip validation if not required and empty
        if not rules.get('required', False) and not value:
            return True
        
        # Pattern validation
        if 'pattern' in rules:
            if not re.match(rules['pattern'], value):
                self.show_field_error(field_name, rules['message'])
                return False
        
        # Range validation
        if 'min' in rules or 'max' in rules:
            try:
                num_value = float(value)
                if 'min' in rules and num_value < rules['min']:
                    self.show_field_error(field_name, rules['message'])
                    return False
                if 'max' in rules and num_value > rules['max']:
                    self.show_field_error(field_name, rules['message'])
                    return False
            except ValueError:
                self.show_field_error(field_name, f"{field_name} must be a number")
                return False
        
        # Values validation
        if 'values' in rules:
            if value not in rules['values']:
                self.show_field_error(field_name, rules['message'])
                return False
        
        # Clear any previous errors
        self.clear_field_error(field_name)
        return True
        
    def show_field_error(self, field_name, message):
        """Show error for a specific field"""
        
        if field_name == 'sensor_type':
            entry = self.sensor_type_combo
        else:
            entry = getattr(self, f"{field_name}_entry")
        
        # Add to validation errors
        if field_name not in [err['field'] for err in self.validation_errors]:
            self.validation_errors.append({'field': field_name, 'message': message})
        
        self.update_status()
        
    def clear_field_error(self, field_name):
        """Clear error for a specific field"""
        
        # Remove from validation errors
        self.validation_errors = [err for err in self.validation_errors 
                                 if err['field'] != field_name]
        
        self.update_status()
        
    def validate_all_fields(self):
        """Validate all fields and show results"""
        
        self.validation_errors = []
        all_valid = True
        
        # Validate each field
        for field_name in self.validation_rules.keys():
            if not self.validate_field(field_name):
                all_valid = False
        
        if all_valid:
            messagebox.showinfo("Validation", "All fields are valid! ✅")
            self.update_status("All fields validated successfully!")
        else:
            messagebox.showerror("Validation Errors", 
                               f"Found {len(self.validation_errors)} validation errors. "
                               "Please check the status area for details.")
        
        self.update_status()
        
    def collect_data(self):
        """Collect all data from the form"""
        
        data = {}
        
        # Collect from entry fields
        for field_name in self.validation_rules.keys():
            if field_name == 'sensor_type':
                data[field_name] = self.sensor_type_combo.get()
            elif field_name == 'notes':
                data[field_name] = getattr(self, f"{field_name}_entry").get().strip()
            else:
                value = getattr(self, f"{field_name}_entry").get().strip()
                # Convert numeric fields
                if field_name in ['lat', 'lon', 'actual_distance', 'activation_time', 
                                'water_temp', 'wind_speed', 'precipitation', 
                                'wave_height', 'ambient_light']:
                    try:
                        data[field_name] = float(value) if value else None
                    except ValueError:
                        data[field_name] = value
                else:
                    data[field_name] = value if value else None
        
        return data
        
    def save_to_csv(self):
        """Save data to CSV file"""
        
        # Validate data first
        if not self.validate_all_fields_silent():
            messagebox.showerror("Validation Error", 
                               "Please fix validation errors before saving.")
            return
        
        # Get file path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Data to CSV"
        )
        
        if not file_path:
            return
        
        try:
            # Collect data
            data = self.collect_data()
            
            # Check if file exists to determine if we need headers
            file_exists = os.path.exists(file_path)
            
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['test_id', 'date', 'lat', 'lon', 'actual_distance', 
                             'activation_time', 'water_temp', 'wind_speed', 
                             'precipitation', 'wave_height', 'ambient_light', 
                             'sensor_type', 'notes']
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header if file is new
                if not file_exists:
                    writer.writeheader()
                
                # Write data
                writer.writerow(data)
            
            messagebox.showinfo("Success", f"Data saved to {file_path}")
            self.update_status(f"Data saved to CSV: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV: {str(e)}")
            self.update_status(f"Error saving CSV: {str(e)}")
    
    def save_to_json(self):
        """Save data to JSON file"""
        
        # Validate data first
        if not self.validate_all_fields_silent():
            messagebox.showerror("Validation Error", 
                               "Please fix validation errors before saving.")
            return
        
        # Get file path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Data to JSON"
        )
        
        if not file_path:
            return
        
        try:
            # Collect data
            data = self.collect_data()
            
            # Add timestamp
            data['timestamp'] = datetime.now().isoformat()
            
            # Save to JSON
            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Data saved to {file_path}")
            self.update_status(f"Data saved to JSON: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON: {str(e)}")
            self.update_status(f"Error saving JSON: {str(e)}")
    
    def validate_all_fields_silent(self):
        """Validate all fields without showing message boxes"""
        
        self.validation_errors = []
        
        for field_name in self.validation_rules.keys():
            if not self.validate_field(field_name):
                return False
        
        return True
    
    def clear_form(self):
        """Clear all form fields"""
        
        # Clear entry fields
        for field_name in self.validation_rules.keys():
            if field_name == 'sensor_type':
                self.sensor_type_combo.set("drone")
            else:
                entry = getattr(self, f"{field_name}_entry")
                entry.delete(0, tk.END)
                if field_name == 'date':
                    entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
                elif field_name == 'test_id':
                    entry.insert(0, "VH-001")
                elif field_name == 'lat':
                    entry.insert(0, "48.423")
                elif field_name == 'lon':
                    entry.insert(0, "-123.367")
                elif field_name == 'actual_distance':
                    entry.insert(0, "320")
                elif field_name == 'activation_time':
                    entry.insert(0, "45")
                elif field_name == 'water_temp':
                    entry.insert(0, "8.5")
                elif field_name == 'wind_speed':
                    entry.insert(0, "5.2")
                elif field_name == 'precipitation':
                    entry.insert(0, "2.4")
                elif field_name == 'wave_height':
                    entry.insert(0, "1.2")
                elif field_name == 'ambient_light':
                    entry.insert(0, "0.002")
        
        # Clear validation errors
        self.validation_errors = []
        self.update_status("Form cleared")
        
    def show_help(self):
        """Show help information"""
        
        help_text = """
LuxBio AI Tracking - Data Input Help

FIELD MEASUREMENT GUIDELINES:

1. Actual Distance (0-1000 m):
   - Use GPS to measure distance from activation point to detection boundary
   - Record when marker becomes consistently visible (>3 sightings in 1 min)

2. Activation Time (0-360 min):
   - Start stopwatch at bead activation
   - Record test time relative to activation
   - Maximum 6 hours (360 min)

3. Water Temperature (-2 to 30°C):
   - Submerge thermometer 0.5m below surface
   - Wait 1 minute for stabilization
   - Measure within 5m of marker deployment

4. Wind Speed (0-25 m/s):
   - Use anemometer app or handheld device
   - Record 1-minute average at 10m height

5. Precipitation (0-50 mm/hr):
   - Use rain gauge or visual estimation
   - Record during test period

6. Wave Height (0-10 m):
   - Use visual reference or wave timing method
   - Estimate average of highest 1/3 waves

7. Ambient Light (0.0001-0.1 lux):
   - Use lux meter app
   - Point phone straight up
   - Record stable reading

8. Sensor Type:
   - human: Unaided vision (even with binoculars)
   - drone: Any UAV camera system
   - nvg: Any night vision device

EQUIPMENT KIT ($150):
- Waterproof phone case ($15)
- Digital thermometer ($8)
- Rain gauge ($5)
- Stopwatch ($10)
- Anemometer ($25)
- GPS app (Free)
- Lux Light Meter app (Free)
- Field notebook ($5)

For detailed protocols, see: data_formats/FIELD_DATA_COLLECTION_GUIDE.md
        """
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Field Data Collection")
        help_window.geometry("600x700")
        
        # Help text widget
        help_text_widget = tk.Text(help_window, wrap=tk.WORD, padx=20, pady=20)
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Insert help text
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.configure(state=tk.DISABLED)
        
        # Close button
        close_btn = ttk.Button(help_window, text="Close", 
                              command=help_window.destroy)
        close_btn.pack(pady=10)
    
    def update_status(self, message=None):
        """Update status display"""
        
        self.status_text.delete(1.0, tk.END)
        
        if message:
            self.status_text.insert(tk.END, f"{message}\n\n")
        
        if self.validation_errors:
            self.status_text.insert(tk.END, "Validation Errors:\n")
            for error in self.validation_errors:
                self.status_text.insert(tk.END, f"• {error['field']}: {error['message']}\n")
        else:
            self.status_text.insert(tk.END, "No validation errors ✅\n")
        
        # Add current data preview
        self.status_text.insert(tk.END, "\nCurrent Data Preview:\n")
        data = self.collect_data()
        for key, value in data.items():
            if value:
                self.status_text.insert(tk.END, f"  {key}: {value}\n")

def main():
    """Main application entry point"""
    
    # Create root window
    root = tk.Tk()
    
    # Create and run app
    app = StoreDataApp(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main() 