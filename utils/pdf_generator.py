import os
import time
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
        print(f"Output directory: {self.output_dir}")
        print(f"Images directory: {self.images_dir}")
        print(f"Images directory exists: {os.path.exists(self.images_dir)}")
        print(f"Images in directory: {os.listdir(self.images_dir) if os.path.exists(self.images_dir) else 'Directory not found'}")

    def get_section_images(self, section_number, total_sections, section_type, width, amperage, depth):
        """Get the images for a given section based on its configuration."""
        images = []
        
        if section_type == 'Spectra':
            # Check if this is a first or last section
            is_first_or_last = section_number == 1 or section_number == total_sections
            
            # Add ABC and Neutral images for first/last sections
            if is_first_or_last:
                if width == '44' or width == '40':
                    images.append({
                        'name': '38x4spectraHorizontalABC.png',
                        'quantity': self.get_quantity_for_amperage(amperage)
                    })
                    images.append({
                        'name': '38x4spectraHorizontalNuetral.png',
                        'quantity': self.get_quantity_for_amperage(amperage)
                    })
            else:
                # Middle section images
                if width == '44' or width == '40':
                    images.append({
                        'name': '43x4spectraHorizontalABC.png',
                        'quantity': self.get_quantity_for_amperage(amperage)
                    })
                    images.append({
                        'name': '43x4spectraHorizontalNuetral.png',
                        'quantity': self.get_quantity_for_amperage(amperage)
                    })
            
            # Add B-link images (2 per section)
            images.append({
                'name': '95x4spectraBLink.png',
                'quantity': 2
            })
            
            # Add AC-link images (2 of each per section)
            images.append({
                'name': '115x4spectraACLink1.png',
                'quantity': 2
            })
            images.append({
                'name': '115x4spectraACLink2.png',
                'quantity': 2
            })
            
            # Add connection bar stack images based on depth and amperage
            if depth == '30':
                images.append({
                    'name': self.get_connection_bar_stack_image(amperage, '30'),
                    'quantity': 6
                })
            elif depth == '36':
                images.append({
                    'name': self.get_connection_bar_stack_image(amperage, '36'),
                    'quantity': 6
                })
            
            # Add AC phase vertical link (4 per section)
            images.append({
                'name': '1225x4spectraACPhaseVerticalLink4in.png',
                'quantity': 4
            })
            
            # Add inner steel images for 44" width
            if width == '44':
                images.append({
                    'name': '44375SpectraInnerSteel44Wide.png',
                    'quantity': 2
                })
                images.append({
                    'name': '44375SpectraInnerSteel44WideSideView.png',
                    'quantity': 1
                })
        
        elif section_type == 'MLO':
            # Add MLO-specific images
            if width == '36':
                images.append({
                    'name': '36x4MLOHorizontalABC.png',
                    'quantity': self.get_quantity_for_amperage(amperage)
                })
                images.append({
                    'name': '36x4MLOHorizontalNuetral.png',
                    'quantity': self.get_quantity_for_amperage(amperage)
                })
                
                # Add B-link images (2 per section)
                images.append({
                    'name': '95x4MLOBLink.png',
                    'quantity': 2
                })
                
                # Add AC-link images (2 of each per section)
                images.append({
                    'name': '115x4MLOACLink1.png',
                    'quantity': 2
                })
                images.append({
                    'name': '115x4MLOACLink2.png',
                    'quantity': 2
                })
                
                # Add connection bar stack images based on depth and amperage
                if depth == '30':
                    images.append({
                        'name': self.get_connection_bar_stack_image(amperage, '30'),
                        'quantity': 6
                    })
                elif depth == '36':
                    images.append({
                        'name': self.get_connection_bar_stack_image(amperage, '36'),
                        'quantity': 6
                    })
                
                # Add AC phase vertical link (4 per section)
                images.append({
                    'name': '1225x4MLOACPhaseVerticalLink4in.png',
                    'quantity': 4
                })
        
        print(f"Generated {len(images)} images for section {section_number} ({section_type})")
        return images
    
    def get_quantity_for_amperage(self, amperage):
        """Get quantity based on amperage."""
        if amperage == '4000':
            return 4
        elif amperage in ['3000', '2500']:
            return 3
        elif amperage in ['2000', '1200']:
            return 2
        elif amperage == '1000':
            return 1
        else:
            return 1
    
    def get_connection_bar_stack_image(self, amperage, depth):
        """Get connection bar stack image based on amperage and depth."""
        if depth == '30':
            if amperage == '4000':
                return '675x4SpectraHorizontalConnection4BarStack30deep.png'
            elif amperage in ['3000', '2500']:
                return '725x4SpectraHorizontalConnection3BarStack30deep.png'
            elif amperage in ['2000', '1200']:
                return '775x4SpectraHorizontalConnection2BarStack30deep.png'
            elif amperage == '1000':
                return '825x4SpectraHorizontalConnection1BarStack30Deep.png'
            else:
                return '825x4SpectraHorizontalConnection1BarStack30Deep.png'
        elif depth == '36':
            if amperage == '4000':
                return '1275x4SpectraHorizontalConnection4BarStack36deep.png'
            elif amperage in ['3000', '2500']:
                return '1325x4SpectraHorizontalConnection3BarStack36deep.png'
            elif amperage in ['2000', '1200']:
                return '1375x4SpectraHorizontalConnection2BarStack36deep.png'
            elif amperage == '1000':
                return '1425x4SpectraHorizontalConnection1BarStack36deep.png'
            else:
                return '1425x4SpectraHorizontalConnection1BarStack36deep.png'

    def generate_pdf(self, form_data):
        print("Generating PDF...")
        start_time = time.time()
        
        # Use the output_dir instead of Downloads
        pdf_path = os.path.join(self.output_dir, f"packet_{form_data.get('timestamp', 'output')}.pdf")
        print(f"PDF will be saved to: {pdf_path}")
        
        try:
            # Create PDF
            print("Creating PDF canvas...")
            c = canvas.Canvas(pdf_path, pagesize=letter)
            print("PDF canvas created successfully")
            
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
            
            # Get common settings
            common_depth = form_data.get('common_depth', '')
            common_height = form_data.get('common_height', '')
            common_amperage = form_data.get('common_amperage', '')
            
            # Get total number of sections
            total_sections = int(form_data.get('num_sections', 0))
            print(f"Processing {total_sections} sections")
            
            # Add section details and images
            for i in range(1, total_sections + 1):
                print(f"Processing section {i} of {total_sections}")
                section_type = form_data.get(f'section_type_{i}', '')
                width = form_data.get(f'width_{i}', '')
                
                # Get depth value
                if common_depth == 'no':
                    depth = form_data.get(f'depth_{i}', '')
                else:
                    depth = common_depth
                
                # Get height value
                if common_height == 'no':
                    height = form_data.get(f'height_{i}', '')
                else:
                    height = common_height
                
                # Get amperage value
                if common_amperage == 'no':
                    amperage = form_data.get(f'amperage_{i}', '')
                else:
                    amperage = common_amperage
                
                print(f"Section {i}: Type={section_type}, Width={width}, Depth={depth}, Height={height}, Amperage={amperage}")
                
                # Get images for this section
                section_images = self.get_section_images(i, total_sections, section_type, width, amperage, depth)
                
                # Start with the first page for this section
                page_num = 1
                images_processed = 0
                max_pages_per_section = 10  # Safety limit to prevent infinite loops
                pages_created = 0
                
                while images_processed < len(section_images) and pages_created < max_pages_per_section:
                    pages_created += 1
                    print(f"Creating page {page_num} for section {i} (page {pages_created} of max {max_pages_per_section})")
                    
                    # Add header with company name
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(1*inch, 10.5*inch, "FACTORY SWITCHBOARD PACKET")
                    
                    # Add section number at top left
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(1*inch, 9.8*inch, f"Section {i}: {section_type}")
                    
                    # Add a horizontal line at the top
                    c.setStrokeColor(colors.gray)
                    c.setLineWidth(0.5)
                    c.line(1*inch, 10.2*inch, 7.5*inch, 10.2*inch)
                    
                    # Add project details at bottom right
                    c.setFont("Helvetica", 10)
                    c.drawString(5*inch, 1*inch, f"Sales Order: {form_data.get('sales_order', '')}")
                    c.drawString(5*inch, 0.7*inch, f"Customer: {form_data.get('customer_name', '')}")
                    c.drawString(5*inch, 0.4*inch, f"Job: {form_data.get('job_address', '')}")
                    c.drawString(5*inch, 0.1*inch, f"Switchboard: {form_data.get('switchboard_name', '')}")
                    
                    # Add page number
                    c.setFont("Helvetica", 8)
                    c.drawString(7*inch, 0.5*inch, f"Page {page_num} of Section {i}")
                    
                    # Add a horizontal line at the bottom
                    c.line(1*inch, 1.2*inch, 7.5*inch, 1.2*inch)
                    
                    # Start position for images (reduced gap from section label)
                    y_position = 9.0*inch
                    images_on_this_page = 0
                    
                    # Add section images if available
                    while images_processed < len(section_images) and y_position > 2*inch:
                        img = section_images[images_processed]
                        image_path = os.path.join(self.images_dir, img['name'])
                        print(f"Processing image: {img['name']} (path: {image_path})")
                        
                        if os.path.exists(image_path):
                            try:
                                print(f"Loading image: {image_path}")
                                img_reader = ImageReader(image_path)
                                img_width, img_height = img_reader.getSize()
                                aspect = img_height / img_width
                                
                                # Calculate maximum display height to ensure at least 2 images per page
                                # Available space is from y_position down to 2*inch
                                available_height = y_position - 2*inch
                                max_display_height = available_height / 2  # Ensure at least 2 images
                                
                                # Calculate display width based on aspect ratio and max height
                                display_height = min(max_display_height, 4*inch)  # Cap at 4 inches
                                display_width = display_height / aspect
                                
                                # Set minimum size constraints
                                min_height = 2.5*inch  # Minimum height of 2.5 inches
                                min_width = 3*inch     # Minimum width of 3 inches
                                
                                # If height is too small, adjust both dimensions proportionally
                                if display_height < min_height:
                                    display_height = min_height
                                    display_width = display_height / aspect
                                
                                # If width is too small after height adjustment, adjust both dimensions
                                if display_width < min_width:
                                    display_width = min_width
                                    display_height = display_width * aspect
                                
                                # If width is too large, scale down proportionally
                                if display_width > 6*inch:
                                    display_width = 6*inch
                                    display_height = display_width * aspect
                                
                                # Final check to ensure we don't exceed available space
                                if y_position - display_height < 2*inch:
                                    # Not enough space, start a new page
                                    print(f"Not enough space for image {img['name']}, starting new page")
                                    break
                                
                                # Draw the image
                                print(f"Drawing image: {img['name']} at y_position={y_position}, size={display_width}x{display_height}")
                                c.drawImage(img_reader, 1*inch, y_position - display_height, 
                                          width=display_width, height=display_height, preserveAspectRatio=True)
                                
                                # Add quantity under the image
                                c.setFont("Helvetica-Bold", 12)
                                c.drawString(1*inch, y_position - display_height - 0.3*inch, f"QTY: {img['quantity']}")
                                
                                # Update y_position for next image
                                y_position -= display_height + 0.5*inch
                                images_processed += 1
                                images_on_this_page += 1
                                print(f"Image {img['name']} processed successfully")
                            except Exception as e:
                                print(f"Error adding image {img['name']} for section {i}: {str(e)}")
                                images_processed += 1
                        else:
                            print(f"Warning: Image not found: {image_path}")
                            images_processed += 1
                    
                    # If we've processed all images, add dimensions and amperage
                    if images_processed == len(section_images):
                        # Add dimensions based on available values
                        dimensions = []
                        if width:
                            dimensions.append(f"{width}\"")
                        if depth:
                            dimensions.append(f"{depth}\"")
                        if height:
                            dimensions.append(f"{height}\"")
                        
                        if dimensions:
                            c.setFont("Helvetica-Bold", 12)
                            c.drawString(1*inch, y_position - 0.3*inch, f"{' x '.join(dimensions)} x 1/4\"")
                            y_position -= 0.5*inch
                        
                        # Add amperage
                        if amperage:
                            c.setFont("Helvetica-Bold", 12)
                            c.drawString(1*inch, y_position - 0.3*inch, f"Amperage: {amperage}A")
                            y_position -= 0.5*inch
                    
                    # If we still have images to process, start a new page
                    if images_processed < len(section_images):
                        c.showPage()
                        page_num += 1
                    else:
                        # We're done with this section
                        c.showPage()
                
                # Safety check - if we hit the page limit, log a warning
                if images_processed < len(section_images):
                    print(f"WARNING: Hit maximum page limit ({max_pages_per_section}) for section {i}. {len(section_images) - images_processed} images not processed.")
            
            # Save the PDF
            print("Saving PDF...")
            c.save()
            print(f"PDF saved successfully at {pdf_path}")
            
            elapsed_time = time.time() - start_time
            print(f"PDF generation completed in {elapsed_time:.2f} seconds")
            
            return pdf_path
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise 