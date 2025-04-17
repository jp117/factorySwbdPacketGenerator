from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(section_type, width=800, height=600):
    # Create a new image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a border
    draw.rectangle([0, 0, width-1, height-1], outline='black')
    
    # Draw some placeholder content
    draw.line([(100, 100), (700, 100)], fill='black', width=2)  # Top line
    draw.line([(100, 500), (700, 500)], fill='black', width=2)  # Bottom line
    draw.line([(100, 100), (100, 500)], fill='black', width=2)  # Left line
    draw.line([(700, 100), (700, 500)], fill='black', width=2)  # Right line
    
    # Add text
    draw.text((400, 300), f"Section Type {section_type}", fill='black', anchor='mm')
    
    return image

def main():
    # Create the images directory if it doesn't exist
    images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Create placeholder images for each section type
    section_types = ['A', 'B', 'C']
    for section_type in section_types:
        image = create_placeholder_image(section_type)
        image_path = os.path.join(images_dir, f'section_{section_type.lower()}.png')
        image.save(image_path)
        print(f"Created placeholder image: {image_path}")
    
    # Create a default section image
    image = create_placeholder_image('Default')
    image_path = os.path.join(images_dir, 'default_section.png')
    image.save(image_path)
    print(f"Created default image: {image_path}")

if __name__ == '__main__':
    main() 