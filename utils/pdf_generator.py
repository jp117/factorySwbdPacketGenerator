import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class PDFGenerator:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        self.images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'images')
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)

    def get_section_image(self, section_type):
        """Get the image path for a given section type."""
        # Use the 4inSpectraHorizontalABC image for all sections
        image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                'static', 'images', '4inSpectraHorizontalABC.png')
        
        if not os.path.exists(image_path):
            print(f"Warning: Image not found: {image_path}")
            return None
            
        return image_path

    def generate_pdf(self, form_data):
        print("Generating PDF...")
        
        # Get the user's home directory and set the Downloads path
        home_dir = os.path.expanduser("~")
        pdf_path = os.path.join(home_dir, "Downloads", f"packet_{form_data.get('timestamp', 'output')}.pdf")
        print(f"PDF will be saved to: {pdf_path}")
        
        try:
            # Create PDF
            print("Creating PDF canvas...")
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=TA_LEFT
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12
            )
            
            # Add section details and images
            for i in range(1, int(form_data.get('num_sections', 0)) + 1):
                section_type = form_data.get(f'section_type_{i}', '')
                width = form_data.get(f'width_{i}', '')
                
                # Add header with company name
                c.setFont("Helvetica-Bold", 14)
                c.drawString(1*inch, 10.5*inch, "FACTORY SWITCHBOARD PACKET")
                
                # Add section number at top left
                c.setFont("Helvetica-Bold", 16)
                c.drawString(1*inch, 9.8*inch, f"Section {i}: {section_type}")
                
                # Add section image if available
                image_path = self.get_section_image(section_type)
                if image_path:
                    try:
                        img_reader = ImageReader(image_path)
                        img_width, img_height = img_reader.getSize()
                        aspect = img_height / img_width
                        display_width = 6*inch
                        display_height = display_width * aspect
                        
                        # Draw the image
                        c.drawImage(img_reader, 1*inch, 7*inch - display_height, 
                                  width=display_width, height=display_height, preserveAspectRatio=True)
                        
                        # Add quantity and dimensions under the image
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(1*inch, 6.5*inch - display_height, f"QTY: 9")
                        c.drawString(1*inch, 6.2*inch - display_height, f"43\" x 4\" x 1/4\"")
                    except Exception as e:
                        print(f"Error adding image for section {i}: {str(e)}")
                
                # Add project details at bottom right
                c.setFont("Helvetica", 10)
                c.drawString(5*inch, 1*inch, f"Sales Order: {form_data.get('sales_order', '')}")
                c.drawString(5*inch, 0.7*inch, f"Customer: {form_data.get('customer_name', '')}")
                c.drawString(5*inch, 0.4*inch, f"Job: {form_data.get('job_address', '')}")
                c.drawString(5*inch, 0.1*inch, f"Switchboard: {form_data.get('switchboard_name', '')}")
                
                # Add page number
                c.setFont("Helvetica", 8)
                c.drawString(7*inch, 0.5*inch, f"Page {i} of {form_data.get('num_sections', '')}")
                
                # Add a horizontal line at the top
                c.setStrokeColor(colors.gray)
                c.setLineWidth(0.5)
                c.line(1*inch, 10.2*inch, 7.5*inch, 10.2*inch)
                
                # Add a horizontal line at the bottom
                c.line(1*inch, 1.2*inch, 7.5*inch, 1.2*inch)
                
                # Start a new page for the next section
                c.showPage()
            
            # Save the PDF
            print("Saving PDF...")
            c.save()
            
            return pdf_path
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise 