#!/usr/bin/env python3
"""
Launcher script for the LuxBio AI Tracking Store Data App
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from store_data_app import main
    
    print("Starting LuxBio AI Tracking - Store Data App...")
    print("=" * 50)
    print("This app allows you to input field measurement data")
    print("for bioluminescent detection analysis.")
    print("=" * 50)
    
    # Run the main application
    main()
    
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all required packages are installed:")
    print("pip install tkinter")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1) 