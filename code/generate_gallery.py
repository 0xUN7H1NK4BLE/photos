#!/usr/bin/env python3
"""
Travel Photo Gallery Generator
Scans folder structure and generates index.html with actual photos
"""

import os
import glob
from datetime import datetime
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener, HeifImage
import hashlib
import os

def calculate_file_hash(filepath, chunk_size=8192):
    """Calculate MD5 hash of a file's content."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def remove_duplicate_files(directory):
    """Find and remove duplicate files in a directory (recursively)."""
    print(f"🔍 Scanning for duplicates in: {directory}")
    hashes = {}
    duplicates = []

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)

            try:
                file_hash = calculate_file_hash(filepath)

                if file_hash in hashes:
                    # Duplicate found
                    print(f"❌ Duplicate: {filepath} (same as {hashes[file_hash]})")
                    duplicates.append(filepath)
                else:
                    hashes[file_hash] = filepath
            except Exception as e:
                print(f"⚠️ Could not read {filepath}: {e}")

    # Delete duplicates
    for dup in duplicates:
        try:
            os.remove(dup)
            print(f"🗑️ Removed: {dup}")
        except Exception as e:
            print(f"⚠️ Failed to delete {dup}: {e}")

    print(f"✅ Done. Removed {len(duplicates)} duplicates.")



register_heif_opener()

def get_image_files(folder_path):
    """Get all image files from a folder and convert .heic to .jpg"""
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.bmp', '*.heic']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))

    # Remove duplicates before processing
    unique_files = []
    seen_hashes = set()
    
    for file_path in sorted(image_files):
        try:
            file_hash = calculate_file_hash(file_path)
            if file_hash not in seen_hashes:
                seen_hashes.add(file_hash)
                unique_files.append(file_path)
            else:
                print(f"🗑️ Skipping duplicate: {file_path}")
        except Exception as e:
            print(f"⚠️ Could not read {file_path}: {e}")

    converted_files = []
    for file_path in unique_files:
        if file_path.lower().endswith(".heic"):
            jpg_path = os.path.splitext(file_path)[0] + ".jpg"
            
            # Check if JPG already exists and has same content
            if os.path.exists(jpg_path):
                try:
                    heic_hash = calculate_file_hash(file_path)
                    jpg_hash = calculate_file_hash(jpg_path)
                    if heic_hash == jpg_hash:
                        print(f"🗑️ Skipping HEIC (JPG exists): {file_path}")
                        continue
                except Exception as e:
                    print(f"⚠️ Could not compare hashes: {e}")
            
            try:
                image = Image.open(file_path)
                image = image.convert("RGB")  # Convert to JPEG-compatible format
                image.save(jpg_path, "JPEG", quality=95)
                converted_files.append(jpg_path)
                print(f"✅ Converted: {file_path} → {jpg_path}")
            except Exception as e:
                print(f"❌ Failed to convert {file_path}: {e}")
        else:
            converted_files.append(file_path)

    return converted_files


# def get_image_files(folder_path):
#     """Get all image files from a folder"""
#     image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.bmp', '*.*']
#     image_files = []
    
#     for ext in image_extensions:
#         image_files.extend(glob.glob(os.path.join(folder_path, ext)))
#         image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
#     return sorted(image_files)



def generate_html(places_data):
    """Generate the HTML content"""
    
    # Get current date for the header
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Calculate gallery statistics
    total_photos = sum(len(images) for images in places_data.values())
    total_places = len(places_data)
    places_list = ", ".join(places_data.keys())
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Travel Gallery</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<header>
  <div class="header-left">
    <div class="gallery-title">Travel Gallery</div>
    <div class="gallery-stats">
      <span class="stat-item">📸 {total_photos} photos</span>
      <span class="stat-item">📍 {total_places} places</span>
      <span class="stat-item">🌍 {places_list}</span>
    </div>
    <div class="gallery-updated">Updated on {current_date}</div>
  </div>
  <div class="header-right">
    <div class="search-container">
      <input type="text" class="search-bar" placeholder="Search places, cities, or memories...">
    </div>
  </div>
</header>

<main>
  <div class="gallery-grid">
'''
    
    # Generate gallery items
    for place, images in places_data.items():
        for i, image_path in enumerate(images):
            # Get image filename without extension
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            # Clean up the image name for display
            # display_name = image_name.replace('_', ' ').replace('-', ' ').title()
            # Use the folder name (place) as the display name
            display_name = place
            
            # Use place name as location display
            location_display = place
            
            html_content += f'''    <div class="gallery-item" data-place="{place}" data-title="{display_name}">
      <img src="{image_path}" alt="{place} - {display_name}">
      <div class="image-overlay">
        <div class="image-title">{display_name}</div>
        <div class="image-location">{location_display}</div>
      </div>
    </div>
'''
    
    html_content += '''  </div>
</main>

<!-- Modal -->
<div class="modal" id="imageModal">
  <div class="modal-background" id="modalBackground"></div>
  <div class="modal-content">
    <button class="modal-close" id="modalClose">&times;</button>
    <img class="modal-image" id="modalImage" src="" alt="">
  </div>
</div>

<script src="script.js"></script>
</body>
</html>'''
    
    return html_content

def main():
    """Main function to generate the gallery"""
    
    # Define the photos directory (change this to your photos folder)
    photos_dir = "photos"
    
    if not os.path.exists(photos_dir):
        print(f"Error: '{photos_dir}' directory not found!")
        print("Please create a 'photos' folder with your travel photos organized by place.")
        print("Example structure:")
        print("photos/")
        print("  Paris/")
        print("    eiffel_tower.jpg")
        print("    louvre_museum.jpg")
        print("  London/")
        print("    big_ben.jpg")
        print("    tower_bridge.jpg")
        return
    
    places_data = {}
    
    # Scan the photos directory
    for place_folder in os.listdir(photos_dir):
        place_path = os.path.join(photos_dir, place_folder)
        
        if os.path.isdir(place_path):
            # Get all images from this place folder
            images = get_image_files(place_path)
            
            if images:
                # Final duplicate check to ensure no duplicates in the final list
                unique_images = []
                seen_hashes = set()
                
                for image_path in images:
                    try:
                        file_hash = calculate_file_hash(image_path)
                        if file_hash not in seen_hashes:
                            seen_hashes.add(file_hash)
                            unique_images.append(image_path)
                        else:
                            print(f"🗑️ Final duplicate check - skipping: {image_path}")
                    except Exception as e:
                        print(f"⚠️ Could not hash {image_path}: {e}")
                
                if unique_images:
                    # Clean up place name for display
                    place_name = place_folder.replace('_', ' ').replace('-', ' ').title()
                    places_data[place_name] = unique_images
    
    if not places_data:
        print("No photos found!")
        print("Please add some photos to your 'photos' folder organized by place.")
        return
    
    # Generate the HTML
    html_content = generate_html(places_data)
    
    # Write to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Print summary
    total_photos = sum(len(images) for images in places_data.values())
    print(f"✅ Gallery generated successfully!")
    print(f"📸 Found {total_photos} photos in {len(places_data)} places:")
    
    for place, images in places_data.items():
        print(f"   • {place}: {len(images)} photos")
    
    print(f"\n🎉 Your gallery is ready! Open 'index.html' in your browser to view it.")

if __name__ == "__main__":
    main() 