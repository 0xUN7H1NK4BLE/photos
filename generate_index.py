import os

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
EXCLUDE_DIRS = {'.github', '__pycache__'}

html_head = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Travel Gallery</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>My Travel Gallery</h1>
'''

html_tail = '''
  <script src="script.js"></script>
</body>
</html>
'''

def is_image(filename):
    return os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS

def main():
    places = []
    for entry in os.listdir('.'):
        if os.path.isdir(entry) and entry not in EXCLUDE_DIRS and not entry.startswith('.'):
            images = [f for f in os.listdir(entry) if is_image(f)]
            if images:
                places.append((entry, images))

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_head)
        for place, images in sorted(places):
            f.write(f'<section class="place-section">\n')
            f.write(f'  <div class="place-title">{place.replace("-", " ").title()}</div>\n')
            f.write('  <div class="gallery">\n')
            for img in sorted(images):
                img_path = f'{place}/{img}'
                f.write(f'    <img class="gallery-img" src="{img_path}" alt="{place} image">\n')
            f.write('  </div>\n')
            f.write('</section>\n')
        f.write(html_tail)

if __name__ == '__main__':
    main() 