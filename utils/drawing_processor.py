import os
import ezdxf
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
from datetime import datetime

def convert_dwg_to_image(dwg_path, output_size=(800, 600)):
    """Convert a DWG file to a PIL Image."""
    try:
        # Read the DWG file
        doc = ezdxf.readfile(dwg_path)
        msp = doc.modelspace()
        
        # Create a new image with white background
        image = Image.new('RGB', output_size, 'white')
        draw = ImageDraw.Draw(image)
        
        # Get the drawing bounds
        bounds = None
        for entity in msp:
            if hasattr(entity, 'get_bbox'):
                entity_bounds = entity.get_bbox()
                if entity_bounds:
                    if bounds is None:
                        bounds = entity_bounds
                    else:
                        bounds = (
                            min(bounds[0], entity_bounds[0]),
                            min(bounds[1], entity_bounds[1]),
                            max(bounds[2], entity_bounds[2]),
                            max(bounds[3], entity_bounds[3])
                        )
        
        if bounds is None:
            raise ValueError("No drawable entities found in the DWG file")
        
        # Calculate scale factor
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        scale_x = (output_size[0] - 40) / width
        scale_y = (output_size[1] - 40) / height
        scale = min(scale_x, scale_y)
        
        # Draw entities
        for entity in msp:
            if entity.dxftype() == 'LINE':
                start = entity.dxf.start
                end = entity.dxf.end
                
                # Transform coordinates
                x1 = (start[0] - bounds[0]) * scale + 20
                y1 = output_size[1] - ((start[1] - bounds[1]) * scale + 20)
                x2 = (end[0] - bounds[0]) * scale + 20
                y2 = output_size[1] - ((end[1] - bounds[1]) * scale + 20)
                
                draw.line([(x1, y1), (x2, y2)], fill='black', width=1)
            
            # Add support for other entity types as needed
        
        return image
    except Exception as e:
        raise Exception(f"Error converting DWG to image: {str(e)}")

def process_drawings(assemblies):
    """Generate a PDF packet from the assembly list."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join('output', f'packet_{timestamp}.pdf')
    
    c = canvas.Canvas(output_file, pagesize=letter)
    
    for assembly in assemblies:
        # Add assembly information
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, f"Assembly: {assembly['name']}")
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Quantity: {assembly['quantity']}")
        
        # Process each part in the assembly
        y_position = 700
        for part in assembly['parts']:
            try:
                dwg_path = os.path.join('drawings', f"{part['drawing']}.dwg")
                if not os.path.exists(dwg_path):
                    raise FileNotFoundError(f"Drawing file not found: {dwg_path}")
                
                # Convert DWG to image
                image = convert_dwg_to_image(dwg_path)
                
                # Save image to temporary file
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    image.save(tmp.name)
                    
                    # Add part information
                    c.drawString(50, y_position, f"Part: {part['name']}")
                    c.drawString(50, y_position - 20, f"Quantity: {part['quantity']}")
                    
                    # Add image to PDF
                    c.drawImage(tmp.name, 50, y_position - 220, width=500, height=180)
                    
                    # Clean up temporary file
                    os.unlink(tmp.name)
                
                y_position -= 250
                
                # Check if we need a new page
                if y_position < 100:
                    c.showPage()
                    y_position = 700
                
            except Exception as e:
                print(f"Error processing part {part['name']}: {str(e)}")
                c.drawString(50, y_position, f"Error processing part {part['name']}: {str(e)}")
                y_position -= 50
        
        # Start a new page for the next assembly
        c.showPage()
    
    c.save()
    return output_file 