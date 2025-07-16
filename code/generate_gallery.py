#!/usr/bin/env python3
"""
Travel Photo Gallery Generator
Scans folder structure and generates index.html with actual photos
"""

import os
import glob
from datetime import datetime
from pathlib import Path

def get_image_files(folder_path):
    """Get all image files from a folder"""
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    return sorted(image_files)

def getCountry(place):
    """Get country name for a place"""
    countries = {
        'Paris': 'France',
        'London': 'UK',
        'Tokyo': 'Japan',
        'New York': 'USA',
        'Venice': 'Italy',
        'Barcelona': 'Spain',
        'Rome': 'Italy',
        'Amsterdam': 'Netherlands',
        'Berlin': 'Germany',
        'Prague': 'Czech Republic',
        'Vienna': 'Austria',
        'Budapest': 'Hungary',
        'Krakow': 'Poland',
        'Istanbul': 'Turkey',
        'Dubai': 'UAE',
        'Singapore': 'Singapore',
        'Bangkok': 'Thailand',
        'Hong Kong': 'China',
        'Seoul': 'South Korea',
        'Sydney': 'Australia',
        'Melbourne': 'Australia',
        'Toronto': 'Canada',
        'Vancouver': 'Canada',
        'Montreal': 'Canada',
        'Mexico City': 'Mexico',
        'Rio de Janeiro': 'Brazil',
        'Buenos Aires': 'Argentina',
        'Cape Town': 'South Africa',
        'Marrakech': 'Morocco',
        'Cairo': 'Egypt'
    }
    return countries.get(place, '')

def generate_html(places_data):
    """Generate the HTML content"""
    
    # Get current date for the header
    current_date = datetime.now().strftime("%B %d, %Y")
    
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
            
            # Get country for the location display
            country = getCountry(place)
            location_display = f"{place}, {country}" if country else place
            
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
                # Clean up place name for display
                place_name = place_folder.replace('_', ' ').replace('-', ' ').title()
                places_data[place_name] = images
    
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