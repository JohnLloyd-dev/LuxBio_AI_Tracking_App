#!/usr/bin/env python3
"""
Bioluminescent Detection AI Model - Project Startup Script

This script provides an interactive menu to run different components of the project.
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print the project banner."""
    print("=" * 60)
    print("🦠 Bioluminescent Detection AI Model")
    print("   Distance Prediction System")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'numpy', 'scipy', 'fastapi', 'uvicorn', 'pydantic', 
        'pandas', 'matplotlib', 'bioluminescence_model'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing dependencies: {', '.join(missing_modules)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def run_quick_start():
    """Run the quick start demo."""
    print("\n🚀 Running Quick Start Demo...")
    try:
        result = subprocess.run([sys.executable, "quick_start.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Quick start completed successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Quick start failed!")
            print("Error:", result.stderr)
    except subprocess.TimeoutExpired:
        print("❌ Quick start timed out!")
    except Exception as e:
        print(f"❌ Error running quick start: {e}")

def run_enhanced_examples():
    """Run the enhanced input examples."""
    print("\n📊 Running Enhanced Input Examples...")
    try:
        result = subprocess.run([sys.executable, "example_enhanced_input.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Enhanced examples completed successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Enhanced examples failed!")
            print("Error:", result.stderr)
    except subprocess.TimeoutExpired:
        print("❌ Enhanced examples timed out!")
    except Exception as e:
        print(f"❌ Error running enhanced examples: {e}")

def run_full_demo():
    """Run the complete system demo."""
    print("\n🎯 Running Complete System Demo...")
    try:
        result = subprocess.run([sys.executable, "example_usage.py"], 
                              capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Complete demo finished successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Complete demo failed!")
            print("Error:", result.stderr)
    except subprocess.TimeoutExpired:
        print("❌ Complete demo timed out!")
    except Exception as e:
        print(f"❌ Error running complete demo: {e}")

def run_tests():
    """Run the test suite."""
    print("\n🧪 Running Tests...")
    try:
        result = subprocess.run([sys.executable, "run_tests.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ All tests passed!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Some tests failed!")
            print("Error:", result.stderr)
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out!")
    except Exception as e:
        print(f"❌ Error running tests: {e}")

def start_api_server():
    """Start the FastAPI server."""
    print("\n🌐 Starting API Server...")
    print("The server will be available at: http://localhost:8000")
    print("Interactive docs: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "api.main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def show_menu():
    """Show the main menu."""
    print("📋 Available Options:")
    print("1. 🚀 Quick Start Demo")
    print("2. 📊 Enhanced Input Examples")
    print("3. 🎯 Complete System Demo")
    print("4. 🧪 Run Tests")
    print("5. 🌐 Start API Server")
    print("6. 📁 Show Project Structure")
    print("7. 📖 Show Documentation")
    print("8. 🛠️  Install Dependencies")
    print("9. ❌ Exit")
    print()

def show_project_structure():
    """Show the project file structure."""
    print("\n📁 Project Structure:")
    print("bioluminescence_ai/")
    print("├── 📄 bioluminescence_model.py    # Core AI model")
    print("├── 📄 data_models.py              # Data validation & processing")
    print("├── 📄 api/                        # Web API")
    print("│   ├── 📄 main.py                 # FastAPI server")
    print("│   └── 📄 __init__.py")
    print("├── 📄 data_formats/               # CSV templates")
    print("│   ├── 📄 single_prediction_template.csv")
    print("│   ├── 📄 bulk_predictions_template.csv")
    print("│   ├── 📄 weather_station_template.csv")
    print("│   ├── 📄 field_data_collection_template.csv")
    print("│   ├── 📄 calibration_data_template.csv")
    print("│   ├── 📄 validation_scenarios.csv")
    print("│   └── 📄 README.md")
    print("├── 📄 tests/                      # Test suite")
    print("│   ├── 📄 test_model.py")
    print("│   └── 📄 __init__.py")
    print("├── 📄 quick_start.py              # Quick demo")
    print("├── 📄 example_usage.py            # Full demo")
    print("├── 📄 example_enhanced_input.py   # Enhanced examples")
    print("├── 📄 validation.py               # Validation system")
    print("├── 📄 deployment_controller.py    # Drone deployment")
    print("├── 📄 requirements.txt            # Dependencies")
    print("├── 📄 README.md                   # Main documentation")
    print("├── 📄 RUN_GUIDE.md                # Running instructions")
    print("├── 📄 INPUT_FORMAT_SPECIFICATION.md")
    print("├── 📄 Dockerfile                  # Docker configuration")
    print("├── 📄 docker-compose.yml")
    print("└── 📄 setup.py                    # Package setup")

def show_documentation():
    """Show documentation options."""
    print("\n📖 Documentation:")
    print("📄 README.md                    - Main project overview")
    print("📄 RUN_GUIDE.md                 - How to run the project")
    print("📄 INPUT_FORMAT_SPECIFICATION.md - Data format details")
    print("📄 data_formats/README.md       - CSV format guide")
    print("📄 IMPLEMENTATION_SUMMARY.md    - Technical implementation")
    print()
    print("🌐 Online Documentation:")
    print("   API Docs: http://localhost:8000/docs (when server is running)")
    print("   Alternative: http://localhost:8000/redoc")

def install_dependencies():
    """Install project dependencies."""
    print("\n🛠️ Installing Dependencies...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
        else:
            print("❌ Failed to install dependencies!")
            print("Error:", result.stderr)
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out!")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")

def main():
    """Main function."""
    print_banner()
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first.")
        print("Run option 8 to install dependencies.")
        print()
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice == "1":
                run_quick_start()
            elif choice == "2":
                run_enhanced_examples()
            elif choice == "3":
                run_full_demo()
            elif choice == "4":
                run_tests()
            elif choice == "5":
                start_api_server()
            elif choice == "6":
                show_project_structure()
            elif choice == "7":
                show_documentation()
            elif choice == "8":
                install_dependencies()
            elif choice == "9":
                print("\n👋 Goodbye! Thanks for using the Bioluminescent Detection AI Model!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1-9.")
            
            if choice in ["1", "2", "3", "4", "8"]:
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using the Bioluminescent Detection AI Model!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 