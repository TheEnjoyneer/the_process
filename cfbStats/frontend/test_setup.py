#!/usr/bin/env python3
"""
Test script to verify the CFB Games Dashboard setup
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import flask_cors
        print(f"✓ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"✗ Flask-CORS import failed: {e}")
        return False
    
    try:
        import gql
        print(f"✓ GQL imported successfully")
    except ImportError as e:
        print(f"✗ GQL import failed: {e}")
        return False
    
    try:
        import aiohttp
        print(f"✓ aiohttp imported successfully")
    except ImportError as e:
        print(f"✗ aiohttp import failed: {e}")
        return False
    
    try:
        import pytz
        print(f"✓ pytz imported successfully")
    except ImportError as e:
        print(f"✗ pytz import failed: {e}")
        return False
    
    return True

def test_cfbStatsLib():
    """Test if cfbStatsLib can be imported"""
    print("\nTesting cfbStatsLib import...")
    
    # Add parent directory to path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    
    try:
        from cfbStatsLib import getCalendarWeekReg
        print("✓ cfbStatsLib imported successfully")
        print("✓ getCalendarWeekReg function available")
        return True
    except ImportError as e:
        print(f"✗ cfbStatsLib import failed: {e}")
        print("  Make sure cfbStatsLib.py is in the parent directory")
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing cfbStatsLib: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask app creation...")
    
    try:
        from flask import Flask
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("CFB Games Dashboard - Setup Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test cfbStatsLib
    if not test_cfbStatsLib():
        all_passed = False
    
    # Test Flask app
    if not test_flask_app():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! Setup is ready.")
        print("\nTo run the application:")
        print("1. python app.py")
        print("2. Open http://localhost:5000 in your browser")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nTo install missing dependencies:")
        print("pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
