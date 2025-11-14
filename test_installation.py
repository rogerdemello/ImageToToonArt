"""
Test script for Image to Cartoon Converter
Run this to verify your installation is working correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🧪 Testing Python package imports...")
    
    required_packages = [
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('PIL', 'Pillow'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
    ]
    
    optional_packages = [
        ('torch', 'torch'),
        ('torchvision', 'torchvision'),
    ]
    
    failed = []
    
    for module, package in required_packages:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            failed.append(package)
    
    print("\n🔧 Testing optional packages (for AI features)...")
    for module, package in optional_packages:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ⚠️  {package} - Not installed (AI features may be limited)")
    
    if failed:
        print(f"\n❌ Missing required packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages are installed!")
    return True


def test_converters():
    """Test if converters can be initialized"""
    print("\n🧪 Testing converter modules...")
    
    try:
        from backend.cartoon_converter import CartoonConverter
        converter = CartoonConverter()
        styles = converter.get_available_styles()
        print(f"  ✅ CartoonConverter - {len(styles)} styles available")
    except Exception as e:
        print(f"  ❌ CartoonConverter failed: {e}")
        return False
    
    try:
        from backend.ai_converter import AICartoonConverter
        ai_converter = AICartoonConverter()
        ai_styles = ai_converter.get_available_styles()
        print(f"  ✅ AICartoonConverter - {len(ai_styles)} styles available")
        print(f"     Device: {ai_converter.device}")
    except Exception as e:
        print(f"  ❌ AICartoonConverter failed: {e}")
        return False
    
    return True


def test_directories():
    """Test if required directories exist"""
    print("\n🧪 Testing directory structure...")
    
    required_dirs = ['uploads', 'outputs', 'models', 'backend', 'frontend']
    
    all_exist = True
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ - MISSING")
            all_exist = False
    
    return all_exist


def test_sample_conversion():
    """Test a sample conversion if test image exists"""
    print("\n🧪 Testing sample image conversion...")
    
    try:
        import cv2
        import numpy as np
        from backend.cartoon_converter import CartoonConverter
        
        # Create a simple test image
        test_image = np.zeros((200, 200, 3), dtype=np.uint8)
        test_image[50:150, 50:150] = [100, 150, 200]  # Add a colored square
        
        converter = CartoonConverter()
        result = converter.convert(test_image, 'classic')
        
        if result is not None and result.shape == test_image.shape:
            print("  ✅ Image conversion successful")
            return True
        else:
            print("  ❌ Image conversion failed - invalid output")
            return False
            
    except Exception as e:
        print(f"  ❌ Conversion test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🎨 Image to Cartoon Converter - Installation Test")
    print("=" * 50)
    
    results = []
    
    # Test imports
    results.append(("Package Imports", test_imports()))
    
    # Test directories
    results.append(("Directory Structure", test_directories()))
    
    # Test converters
    results.append(("Converter Modules", test_converters()))
    
    # Test sample conversion
    results.append(("Sample Conversion", test_sample_conversion()))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✅ All tests passed! Your installation is ready.")
        print("\n🚀 Next steps:")
        print("1. Run the backend: cd backend && python app.py")
        print("2. Run the frontend: cd frontend && npm start")
        print("3. Open http://localhost:3000 in your browser")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        print("📚 See QUICKSTART.md for troubleshooting tips.")
        sys.exit(1)


if __name__ == "__main__":
    main()
