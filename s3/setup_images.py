#!/usr/bin/env python3
"""
Script to download sample animal images for the ERA4 frontend
"""
import requests
from pathlib import Path
import os

def download_image(url, filename, save_path):
    """Download an image from URL and save it to the specified path"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def main():
    # Create images directory
    images_dir = Path("static/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample animal images (using free stock photos)
    animal_images = {
        "cat": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop",
        "dog": "https://images.unsplash.com/photo-1547407139-3c921a66005c?w=400&h=300&fit=crop",
        "elephant": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop"
    }
    
    print("🖼️  Downloading animal images...")
    
    success_count = 0
    for animal, url in animal_images.items():
        filename = f"{animal}.jpg"
        save_path = images_dir / filename
        
        if download_image(url, filename, save_path):
            success_count += 1
    
    print(f"\n🎉 Downloaded {success_count}/{len(animal_images)} images successfully!")
    
    if success_count == len(animal_images):
        print("✨ All images are ready! You can now run the FastAPI server.")
    else:
        print("⚠️  Some images failed to download. The app will still work but images won't display.")

if __name__ == "__main__":
    main() 