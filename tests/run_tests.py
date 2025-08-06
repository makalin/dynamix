#!/usr/bin/env python3
"""
Test runner for DynaMix
Runs all unit tests and generates coverage reports
"""

import unittest
import sys
import os
import coverage
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests_with_coverage():
    """Run all tests with coverage reporting"""
    # Start coverage measurement
    cov = coverage.Coverage(
        source=['audio_utils', 'playlist_manager', 'dj_tools', 'mix_enhanced'],
        omit=[
            '*/tests/*',
            '*/venv/*',
            '*/env/*',
            '*/__pycache__/*',
            '*/site-packages/*'
        ]
    )
    cov.start()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    print("\n" + "="*60)
    print("COVERAGE REPORT")
    print("="*60)
    
    # Print coverage summary
    cov.report()
    
    # Generate HTML report
    html_dir = os.path.join(os.path.dirname(start_dir), 'coverage_html')
    cov.html_report(directory=html_dir)
    print(f"\nHTML coverage report generated in: {html_dir}")
    
    return result.wasSuccessful()

def run_tests_without_coverage():
    """Run all tests without coverage reporting"""
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_specific_test(test_module):
    """Run a specific test module"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.test_{test_module}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    parser = argparse.ArgumentParser(description='Run DynaMix unit tests')
    parser.add_argument('--no-coverage', action='store_true', 
                       help='Run tests without coverage reporting')
    parser.add_argument('--module', type=str, 
                       help='Run tests for specific module (audio_utils, playlist_manager, dj_tools)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    print("🎵 DynaMix Test Suite")
    print("="*40)
    
    if args.module:
        print(f"Running tests for module: {args.module}")
        success = run_specific_test(args.module)
    elif args.no_coverage:
        print("Running tests without coverage...")
        success = run_tests_without_coverage()
    else:
        print("Running tests with coverage...")
        success = run_tests_with_coverage()
    
    print("\n" + "="*40)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 