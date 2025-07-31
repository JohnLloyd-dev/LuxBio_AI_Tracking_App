"""
Deployment Controller for Bioluminescent Bead Detection

This module provides integration between the AI model and drone operations,
enabling automated search patterns and real-time validation.
"""

import numpy as np
import cv2
import json
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# Import the bioluminescence model
from bioluminescence_model import BioluminescenceModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DronePosition:
    """Drone position and orientation data"""
    latitude: float
    longitude: float
    altitude: float
    heading: float
    pitch: float
    roll: float
    timestamp: float

@dataclass
class EnvironmentalConditions:
    """Real-time environmental conditions"""
    wind_speed: float
    wind_direction: float
    precipitation: float
    wave_height: float
    water_temp: float
    ambient_light: float
    timestamp: float

@dataclass
class DetectionResult:
    """Detection result from drone sensors"""
    detected: bool
    confidence: float
    distance: float
    bearing: float
    timestamp: float
    image_path: Optional[str] = None

class DeploymentController:
    """
    Controller for deploying bioluminescent detection missions.
    
    This class integrates the AI model with drone operations to provide
    automated search patterns and real-time validation capabilities.
    """
    
    def __init__(self, model: BioluminescenceModel, drone_api=None):
        """
        Initialize the deployment controller.
        
        Args:
            model: BioluminescenceModel instance
            drone_api: Drone API interface (DJI Enterprise API or similar)
        """
        self.model = model
        self.drone_api = drone_api
        self.mission_data = []
        self.detection_history = []
        self.current_position = None
        self.current_conditions = None
        
        # Mission parameters
        self.search_altitude = 50.0  # meters
        self.search_speed = 5.0      # m/s
        self.camera_fov = 60.0       # degrees
        self.detection_interval = 2.0 # seconds
        
        # Initialize detection parameters
        self.activation_time = 0.0
        self.sensor_type = "drone"
        
    def set_mission_parameters(self, 
                              search_altitude: float = 50.0,
                              search_speed: float = 5.0,
                              camera_fov: float = 60.0,
                              detection_interval: float = 2.0):
        """
        Set mission-specific parameters.
        
        Args:
            search_altitude: Drone altitude for search (m)
            search_speed: Drone speed during search (m/s)
            camera_fov: Camera field of view (degrees)
            detection_interval: Time between detections (s)
        """
        self.search_altitude = search_altitude
        self.search_speed = search_speed
        self.camera_fov = camera_fov
        self.detection_interval = detection_interval
        
    def execute_marker_test(self, 
                           env_conditions: EnvironmentalConditions,
                           activation_time: float,
                           search_center: Tuple[float, float],
                           search_radius: float = 1000.0) -> Dict:
        """
        Execute a complete marker detection test.
        
        Args:
            env_conditions: Current environmental conditions
            activation_time: Time since bead activation (minutes)
            search_center: (latitude, longitude) of search center
            search_radius: Search radius in meters
            
        Returns:
            Dictionary containing test results
        """
        logger.info(f"Starting marker test at {search_center} with radius {search_radius}m")
        
        # Update current conditions
        self.current_conditions = env_conditions
        self.activation_time = activation_time
        
        # Calculate optimal deployment using AI model
        d_max = self._calculate_optimal_range(env_conditions, activation_time)
        
        # Generate search pattern
        waypoints = self._generate_search_pattern(search_center, d_max, search_radius)
        
        # Execute search mission
        mission_results = self._execute_search_mission(waypoints)
        
        # Analyze results
        analysis = self._analyze_mission_results(mission_results, d_max)
        
        # Update model with validation data
        self._update_model_with_results(mission_results, d_max)
        
        return {
            'predicted_distance': d_max,
            'search_pattern': waypoints,
            'detections': mission_results,
            'analysis': analysis,
            'mission_duration': time.time() - mission_results[0]['timestamp'] if mission_results else 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_optimal_range(self, 
                                env_conditions: EnvironmentalConditions,
                                activation_time: float) -> float:
        """
        Calculate optimal detection range using AI model.
        
        Args:
            env_conditions: Environmental conditions
            activation_time: Time since activation (minutes)
            
        Returns:
            Predicted maximum detection distance (m)
        """
        result = self.model.predict(
            activation_time=activation_time,
            water_temp=env_conditions.water_temp,
            wind_speed=env_conditions.wind_speed,
            precipitation=env_conditions.precipitation,
            wave_height=env_conditions.wave_height,
            ambient_light=env_conditions.ambient_light,
            sensor_type=self.sensor_type
        )
        
        logger.info(f"AI model predicts max distance: {result['distance']:.0f}m")
        return result['distance']
    
    def _generate_search_pattern(self, 
                                center: Tuple[float, float],
                                max_distance: float,
                                search_radius: float) -> List[Dict]:
        """
        Generate optimal search pattern based on predicted range.
        
        Args:
            center: Search center (lat, lon)
            max_distance: Predicted maximum detection distance
            search_radius: Maximum search radius
            
        Returns:
            List of waypoint dictionaries
        """
        # Use the smaller of predicted range or search radius
        effective_radius = min(max_distance * 0.8, search_radius)
        
        # Generate spiral search pattern
        waypoints = []
        center_lat, center_lon = center
        
        # Spiral parameters
        spiral_spacing = max_distance * 0.3  # 30% of max distance between passes
        num_rotations = int(effective_radius / spiral_spacing)
        
        for i in range(num_rotations + 1):
            angle = i * 2 * np.pi / 8  # 8 points per rotation
            radius = i * spiral_spacing
            
            if radius > effective_radius:
                break
                
            # Convert polar to lat/lon (approximate)
            dlat = radius * np.cos(angle) / 111000  # Rough conversion
            dlon = radius * np.sin(angle) / (111000 * np.cos(np.radians(center_lat)))
            
            waypoint = {
                'latitude': center_lat + dlat,
                'longitude': center_lon + dlon,
                'altitude': self.search_altitude,
                'speed': self.search_speed,
                'action': 'search'
            }
            waypoints.append(waypoint)
        
        logger.info(f"Generated {len(waypoints)} waypoints for search pattern")
        return waypoints
    
    def _execute_search_mission(self, waypoints: List[Dict]) -> List[Dict]:
        """
        Execute the search mission using drone API.
        
        Args:
            waypoints: List of waypoints to visit
            
        Returns:
            List of detection results
        """
        if self.drone_api is None:
            logger.warning("No drone API available, simulating mission")
            return self._simulate_search_mission(waypoints)
        
        detection_results = []
        
        try:
            # Take off
            self.drone_api.takeoff()
            logger.info("Drone takeoff completed")
            
            # Execute waypoints
            for i, waypoint in enumerate(waypoints):
                logger.info(f"Executing waypoint {i+1}/{len(waypoints)}")
                
                # Navigate to waypoint
                self.drone_api.fly_to(
                    waypoint['latitude'],
                    waypoint['longitude'],
                    waypoint['altitude']
                )
                
                # Update current position
                self.current_position = DronePosition(
                    latitude=waypoint['latitude'],
                    longitude=waypoint['longitude'],
                    altitude=waypoint['altitude'],
                    heading=0.0,  # Would get from drone
                    pitch=0.0,
                    roll=0.0,
                    timestamp=time.time()
                )
                
                # Perform detection
                detection = self._perform_detection()
                detection_results.append(detection)
                
                # Wait for next detection
                time.sleep(self.detection_interval)
            
            # Return to home
            self.drone_api.return_to_home()
            logger.info("Mission completed, returning to home")
            
        except Exception as e:
            logger.error(f"Mission execution failed: {str(e)}")
            # Emergency landing
            if self.drone_api:
                self.drone_api.emergency_land()
        
        return detection_results
    
    def _simulate_search_mission(self, waypoints: List[Dict]) -> List[Dict]:
        """
        Simulate search mission for testing without drone hardware.
        
        Args:
            waypoints: List of waypoints
            
        Returns:
            Simulated detection results
        """
        detection_results = []
        
        for i, waypoint in enumerate(waypoints):
            # Simulate flight time
            time.sleep(0.1)  # Faster for simulation
            
            # Simulate detection with some probability
            detection_probability = 0.1  # 10% chance of detection per waypoint
            detected = np.random.random() < detection_probability
            
            if detected:
                # Simulate detection result
                detection = DetectionResult(
                    detected=True,
                    confidence=np.random.uniform(0.7, 0.95),
                    distance=np.random.uniform(50, 300),
                    bearing=np.random.uniform(0, 360),
                    timestamp=time.time(),
                    image_path=f"simulated_detection_{i}.jpg"
                )
            else:
                detection = DetectionResult(
                    detected=False,
                    confidence=0.0,
                    distance=0.0,
                    bearing=0.0,
                    timestamp=time.time()
                )
            
            detection_results.append(detection)
        
        return detection_results
    
    def _perform_detection(self) -> DetectionResult:
        """
        Perform bioluminescent detection at current position.
        
        Returns:
            Detection result
        """
        if self.drone_api is None:
            # Simulate detection
            return DetectionResult(
                detected=np.random.random() < 0.05,  # 5% detection rate
                confidence=np.random.uniform(0.0, 0.9),
                distance=np.random.uniform(0, 500),
                bearing=np.random.uniform(0, 360),
                timestamp=time.time()
            )
        
        try:
            # Capture image
            image = self.drone_api.capture_image()
            
            # Analyze image for bioluminescence
            detection_result = self._analyze_image_for_bioluminescence(image)
            
            # Save image if detection found
            if detection_result.detected:
                image_path = f"detection_{int(time.time())}.jpg"
                cv2.imwrite(image_path, image)
                detection_result.image_path = image_path
            
            return detection_result
            
        except Exception as e:
            logger.error(f"Detection failed: {str(e)}")
            return DetectionResult(
                detected=False,
                confidence=0.0,
                distance=0.0,
                bearing=0.0,
                timestamp=time.time()
            )
    
    def _analyze_image_for_bioluminescence(self, image: np.ndarray) -> DetectionResult:
        """
        Analyze image for bioluminescent signals.
        
        Args:
            image: Captured image array
            
        Returns:
            Detection result
        """
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define bioluminescent color range (blue-green)
        lower_biolum = np.array([80, 50, 50])   # Blue-green lower bound
        upper_biolum = np.array([120, 255, 255]) # Blue-green upper bound
        
        # Create mask for bioluminescent regions
        mask = cv2.inRange(hsv, lower_biolum, upper_biolum)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Calculate confidence based on area and intensity
            confidence = min(1.0, area / 1000.0)  # Normalize to 0-1
            
            if confidence > 0.3:  # Detection threshold
                # Calculate distance and bearing (simplified)
                center = cv2.moments(largest_contour)
                if center['m00'] != 0:
                    cx = int(center['m10'] / center['m00'])
                    cy = int(center['m01'] / center['m00'])
                    
                    # Distance estimation (simplified)
                    distance = self._estimate_distance_from_image(area, self.current_position.altitude)
                    
                    # Bearing calculation
                    image_center_x = image.shape[1] / 2
                    bearing = np.arctan2(cx - image_center_x, image_center_x) * 180 / np.pi
                    
                    return DetectionResult(
                        detected=True,
                        confidence=confidence,
                        distance=distance,
                        bearing=bearing,
                        timestamp=time.time()
                    )
        
        return DetectionResult(
            detected=False,
            confidence=0.0,
            distance=0.0,
            bearing=0.0,
            timestamp=time.time()
        )
    
    def _estimate_distance_from_image(self, area: float, altitude: float) -> float:
        """
        Estimate distance to bioluminescent source from image analysis.
        
        Args:
            area: Area of detected region in pixels
            altitude: Drone altitude
            
        Returns:
            Estimated distance (m)
        """
        # Simplified distance estimation
        # In practice, this would use camera calibration and more sophisticated algorithms
        if area == 0:
            return 0.0
        
        # Inverse relationship: larger area = closer distance
        distance = altitude * 1000 / area  # Simplified formula
        return np.clip(distance, 10, 1000)  # Reasonable bounds
    
    def _analyze_mission_results(self, 
                                detection_results: List[DetectionResult],
                                predicted_distance: float) -> Dict:
        """
        Analyze mission results and compare with predictions.
        
        Args:
            detection_results: List of detection results
            predicted_distance: AI model predicted distance
            
        Returns:
            Analysis results
        """
        detections = [r for r in detection_results if r.detected]
        
        if not detections:
            return {
                'detections_found': 0,
                'max_detection_distance': 0,
                'prediction_accuracy': 'No detections to compare',
                'mission_success': False
            }
        
        # Calculate statistics
        max_detection_distance = max(r.distance for r in detections)
        avg_confidence = np.mean([r.confidence for r in detections])
        
        # Compare with prediction
        prediction_error = abs(max_detection_distance - predicted_distance)
        prediction_accuracy = max(0, 100 - (prediction_error / predicted_distance * 100))
        
        return {
            'detections_found': len(detections),
            'max_detection_distance': max_detection_distance,
            'avg_confidence': avg_confidence,
            'prediction_error': prediction_error,
            'prediction_accuracy': f"{prediction_accuracy:.1f}%",
            'mission_success': True
        }
    
    def _update_model_with_results(self, 
                                  detection_results: List[DetectionResult],
                                  predicted_distance: float):
        """
        Update AI model with mission results for continuous learning.
        
        Args:
            detection_results: Mission detection results
            predicted_distance: Original prediction
        """
        if not self.current_conditions:
            return
        
        # Find actual maximum detection distance
        actual_distance = 0.0
        for result in detection_results:
            if result.detected:
                actual_distance = max(actual_distance, result.distance)
        
        if actual_distance > 0:
            # Add validation data to model
            validation_data = {
                'actual_distance': actual_distance,
                'activation_time': self.activation_time,
                'water_temp': self.current_conditions.water_temp,
                'wind_speed': self.current_conditions.wind_speed,
                'precipitation': self.current_conditions.precipitation,
                'wave_height': self.current_conditions.wave_height,
                'ambient_light': self.current_conditions.ambient_light,
                'sensor_type': self.sensor_type
            }
            
            self.model.add_validation_data(validation_data)
            logger.info(f"Added validation data: predicted={predicted_distance:.0f}m, actual={actual_distance:.0f}m")
    
    def get_mission_statistics(self) -> Dict:
        """
        Get comprehensive mission statistics.
        
        Returns:
            Mission statistics dictionary
        """
        return {
            'total_missions': len(self.mission_data),
            'total_detections': len(self.detection_history),
            'success_rate': len([m for m in self.mission_data if m['analysis']['mission_success']]) / max(1, len(self.mission_data)),
            'avg_prediction_accuracy': np.mean([m['analysis'].get('prediction_accuracy', 0) for m in self.mission_data if 'prediction_accuracy' in m['analysis']]),
            'model_info': self.model.get_model_info()
        } 