#!/usr/bin/env python3
"""
SignalTap Setup Test Script
This script tests that all dependencies are properly installed and the application can be imported.
"""

import sys
import importlib

def test_imports():
    """Test that all required packages can be imported"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pylogix',
        'pydantic',
        'python-dotenv'
    ]
    
    print("🔍 Testing package imports...")
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError as e:
            print(f"❌ {package} - FAILED: {e}")
            return False
    
    return True

def test_app_imports():
    """Test that our application modules can be imported"""
    app_modules = [
        'app.main',
        'app.routes.plc',
        'app.services.pylogix_service',
        'app.models.tag'
    ]
    
    print("\n🔍 Testing application imports...")
    
    for module in app_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")
            return False
    
    return True

def test_fastapi_app():
    """Test that the FastAPI app can be created"""
    try:
        from app.main import app
        print("✅ FastAPI app creation - OK")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation - FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SignalTap Setup Test")
    print("=" * 40)
    
    # Test package imports
    if not test_imports():
        print("\n❌ Package import test failed!")
        sys.exit(1)
    
    # Test app imports
    if not test_app_imports():
        print("\n❌ Application import test failed!")
        sys.exit(1)
    
    # Test FastAPI app
    if not test_fastapi_app():
        print("\n❌ FastAPI app test failed!")
        sys.exit(1)
    
    print("\n🎉 All tests passed! SignalTap is ready to run.")
    print("\n📖 Next steps:")
    print("1. Run './run.sh' (Linux/macOS) or 'run.bat' (Windows)")
    print("2. Open http://localhost:8000/docs in your browser")
    print("3. Test the API endpoints with your PLC")

if __name__ == "__main__":
    main() 