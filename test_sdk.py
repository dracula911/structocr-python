
import os
import sys
import json
from structocr import StructOCR

# Add current directory to path to allow importing structocr
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_sdk():
    # 1. Api Key Configuration
    api_key = ""

    # 2. Initialize Client
    client = StructOCR(api_key=api_key)

    # 3. Define Image Path (relative to this script, pointing to ../test/v22.jpeg)
    # The script is in structocr-python/, image is in structocr/test/
    # So path is ../test/v22.jpeg
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "..", "test", "ct01.png")
    
    if not os.path.exists(image_path):
        print(f"Error: Test image not found at: {image_path}")
        return

    print(f"Testing SDK with image: {image_path}")

    # 4. Call SDK Method
    try:
        # Assuming v22.jpeg is a VIN image based on filename pattern and recent tasks
        print("Calling scan_vin()...")
        result = client.scan_container(image_path)
        
        # 5. Output Result
        if result:
            print("\nSDK Call Successful!")
            print("Response Data:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("\nSDK returned empty result.")
            
    except Exception as e:
        print(f"\nSDK Call Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sdk()
