#!/usr/bin/env python3
"""
Test runner for the bioluminescent detection AI model.

This script runs all unit tests and provides a summary of results.
"""

import unittest
import sys
import os

def run_tests():
    """Run all tests and return results."""
    # Add the project root to the Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def main():
    """Main function to run tests."""
    print("Running Bioluminescent Detection AI Model Tests")
    print("=" * 50)
    
    try:
        result = run_tests()
        
        print("\n" + "=" * 50)
        print("Test Results Summary:")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
        
        if result.wasSuccessful():
            print("\n✓ All tests passed!")
            return 0
        else:
            print("\n✗ Some tests failed!")
            return 1
            
    except Exception as e:
        print(f"\n✗ Test execution failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 