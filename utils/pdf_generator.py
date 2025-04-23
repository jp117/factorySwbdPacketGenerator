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
        
        # Image name to label mapping
        self.image_labels = {
            '38x4spectraHorizontalABC.png': 'Spectra Horizontal ABC',
            '38x4spectraHorizontalNuetral.png': 'Spectra Horizontal Neutral',
            '43x4spectraHorizontalABC.png': 'Spectra Horizontal ABC',
            '43x4spectraHorizontalNuetral.png': 'Spectra Horizontal Neutral',
            '95x4spectraBLink.png': 'Spectra B-Link',
            '115x4spectraACLink1.png': 'Spectra AC-Link 1',
            '115x4spectraACLink2.png': 'Spectra AC-Link 2',
            '1225x4spectraACPhaseVerticalLink4in.png': 'Spectra AC Phase Vertical Link',
            '44375SpectraInnerSteel44Wide.png': 'Spectra Inner Steel 44" Wide',
            '44375SpectraInnerSteel44WideSideView.png': 'Spectra Inner Steel 44" Wide Side View',
            '36x4MLOHorizontalABC.png': 'MLO Horizontal ABC',
            '36x4MLOHorizontalNuetral.png': 'MLO Horizontal Neutral',
            '95x4MLOBLink.png': 'MLO B-Link',
            '115x4MLOACLink1.png': 'MLO AC-Link 1',
            '115x4MLOACLink2.png': 'MLO AC-Link 2',
            '1225x4MLOACPhaseVerticalLink4in.png': 'MLO AC Phase Vertical Link',
            '675x4SpectraHorizontalConnection4BarStack30deep.png': 'Spectra Horizontal Connection 4 Bar Stack 30" Deep',
            '725x4SpectraHorizontalConnection3BarStack30deep.png': 'Spectra Horizontal Connection 3 Bar Stack 30" Deep',
            '775x4SpectraHorizontalConnection2BarStack30deep.png': 'Spectra Horizontal Connection 2 Bar Stack 30" Deep',
            '825x4SpectraHorizontalConnection1BarStack30Deep.png': 'Spectra Horizontal Connection 1 Bar Stack 30" Deep',
            '1275x4SpectraHorizontalConnection4BarStack36deep.png': 'Spectra Horizontal Connection 4 Bar Stack 36" Deep',
            '1325x4SpectraHorizontalConnection3BarStack36deep.png': 'Spectra Horizontal Connection 3 Bar Stack 36" Deep',
            '1375x4SpectraHorizontalConnection2BarStack36deep.png': 'Spectra Horizontal Connection 2 Bar Stack 36" Deep',
            '1425x4SpectraHorizontalConnection1BarStack36deep.png': 'Spectra Horizontal Connection 1 Bar Stack 36" Deep',
            'mlo2bar4inchabc.png': 'MLO 2 Bar 4" ABC',
            'mlo2bar4inchneutral.png': 'MLO 2 Bar 4" Neutral',
            'mlo3bar4inchabc.png': 'MLO 3 Bar 4" ABC',
            'mlo3bar4inchneutral.png': 'MLO 3 Bar 4" Neutral',
            'mlo4bar4inchabc.png': 'MLO 4 Bar 4" ABC',
            'mlo4bar4inchneutral.png': 'MLO 4 Bar 4" Neutral',
            'mlo4bar4inchcphaseextra1.png': 'MLO 4 Bar 4" C Phase Extra 1',
            'mlo4bar4inchcphaseextra2.png': 'MLO 4 Bar 4" C Phase Extra 2',
            '36375MLOInnerSteel36Wide.png': 'MLO Inner Steel 36" Wide',
            '44375SpectraInnerSteel44WideSideView.png': 'MLO Inner Steel 36" Wide Side View'
        }

    def get_section_images(self, section_number, total_sections, section_type, width, amperage, depth, bus_size):
        """Get the images for a given section based on its configuration."""
        images = []
        
        if section_type == 'MLO':
            # Verify all required MLO images exist before proceeding
            required_images = [
                'mlo2bar4inchabc.png',
                'mlo2bar4inchneutral.png',
                'mlo3bar4inchabc.png',
                'mlo3bar4inchneutral.png',
                'mlo4bar4inchabc.png',
                'mlo4bar4inchneutral.png',
                'mlo4bar4inchcphaseextra1.png',
                'mlo4bar4inchcphaseextra2.png',
                '36375MLOInnerSteel36Wide.png',
                '44375SpectraInnerSteel44WideSideView.png'
            ]
            
            missing_images = [img for img in required_images if not os.path.exists(os.path.join(self.images_dir, img))]
            if missing_images:
                print(f"WARNING: Missing required MLO images: {missing_images}")
            
            # Add MLO-specific images based on amperage
            if amperage in ['1200', '2000']:
                images.append({
                    'name': 'mlo2bar4inchabc.png',
                    'quantity': self.get_quantity_for_amperage(amperage, is_abc=True)
                })
                images.append({
                    'name': 'mlo2bar4inchneutral.png',
                    'quantity': self.get_quantity_for_amperage(amperage, is_abc=False)
                })
            elif amperage in ['2500', '3000']:
                images.append({
                    'name': 'mlo3bar4inchabc.png',
                    'quantity': self.get_quantity_for_amperage(amperage, is_abc=True)
                })
                images.append({
                    'name': 'mlo3bar4inchneutral.png',
                    'quantity': self.get_quantity_for_amperage(amperage, is_abc=False)
                })
            elif amperage == '4000':
                images.append({
                    'name': 'mlo4bar4inchabc.png',
                    'quantity': self.get_quantity_for_amperage(amperage, is_abc=True)
                })
                images.append({
                    'name': 'mlo4bar4inchneutral.png',
                    'quantity': self.get_quantity_for_amperage(amperage, is_abc=False)
                })
            
            # Add common MLO images
            images.append({
                'name': 'mlo4bar4inchcphaseextra1.png',
                'quantity': 1
            })
            images.append({
                'name': 'mlo4bar4inchcphaseextra2.png',
                'quantity': 1
            })
            
            # Add inner steel images - updated quantity to 2
            images.append({
                'name': '36375MLOInnerSteel36Wide.png',
                'quantity': 2
            })
            images.append({
                'name': '44375SpectraInnerSteel44WideSideView.png',
                'quantity': 1
            })
            
            # MLO sections do not have B-links, AC-links, or connection bar stacks
            
        elif section_type == 'Spectra':
            # Check if this is a first or last section
            is_first_or_last = section_number == 1 or section_number == total_sections
            
            # Add ABC and Neutral images for first/last sections
            if is_first_or_last:
                if width == '44' or width == '40':
                    images.append({
                        'name': '38x4spectraHorizontalABC.png',
                        'quantity': self.get_quantity_for_amperage(amperage, is_abc=True)
                    })
                    images.append({
                        'name': '38x4spectraHorizontalNuetral.png',
                        'quantity': self.get_quantity_for_amperage(amperage, is_abc=False)
                    })
            else:
                # Middle section images
                if width == '44' or width == '40':
                    images.append({
                        'name': '43x4spectraHorizontalABC.png',
                        'quantity': self.get_quantity_for_amperage(amperage, is_abc=True)
                    })
                    images.append({
                        'name': '43x4spectraHorizontalNuetral.png',
                        'quantity': self.get_quantity_for_amperage(amperage, is_abc=False)
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
        
        return images
    
    def get_quantity_for_amperage(self, amperage, is_abc=False):
        """Get quantity based on amperage."""
        base_quantity = 1
        if amperage == '4000':
            base_quantity = 4
        elif amperage in ['3000', '2500']:
            base_quantity = 3
        elif amperage in ['2000', '1200']:
            base_quantity = 2
        elif amperage == '1000':
            base_quantity = 1
        
        # For horizontal ABC bus only, multiply by 3
        if is_abc:
            return base_quantity * 3
        return base_quantity
    
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
        start_time = time.time()
        
        # Create a temporary file instead of saving to output directory
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_path = temp_file.name
        temp_file.close()
        
        try:
            # Create PDF
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
            
            # Get common settings
            common_depth = form_data.get('common_depth', '')
            common_height = form_data.get('common_height', '')
            common_amperage = form_data.get('common_amperage', '')
            common_bus = form_data.get('common_bus', '')
            
            # Get total number of sections
            total_sections = int(form_data.get('num_sections', 0))
            
            # Add section details and images
            for i in range(1, total_sections + 1):
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
                
                # Get bus size value
                if common_bus == 'no':
                    bus_size = form_data.get(f'bus_{i}', '')
                else:
                    bus_size = common_bus
                
                # Get images for this section
                section_images = self.get_section_images(i, total_sections, section_type, width, amperage, depth, bus_size)
                
                # Start with the first page for this section
                page_num = 1
                images_processed = 0
                max_pages_per_section = 10  # Safety limit to prevent infinite loops
                pages_created = 0
                
                while images_processed < len(section_images) and pages_created < max_pages_per_section:
                    pages_created += 1
                    
                    # Add header with packet title
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(1*inch, 10.5*inch, "FACTORY SWITCHBOARD PACKET")
                    
                    # Section title
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(1*inch, 9.8*inch, f"{form_data.get('switchboard_name', '')} - Section {i}: {section_type}")
                    
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
                        
                        # Check if this is a bus size text entry
                        if img['name'].startswith('Bus Size:'):
                            # Add bus size text
                            c.setFont("Helvetica-Bold", 12)
                            c.drawString(1*inch, y_position - 0.3*inch, img['name'])
                            y_position -= 0.5*inch
                            images_processed += 1
                            images_on_this_page += 1
                            continue
                        
                        if os.path.exists(image_path):
                            try:
                                img_reader = ImageReader(image_path)
                                img_width, img_height = img_reader.getSize()
                                aspect = img_height / img_width
                                
                                # Check if this is an MLO ABC or neutral image
                                is_mlo_special = any(img['name'].startswith(prefix) for prefix in ['mlo2bar4inch', 'mlo3bar4inch', 'mlo4bar4inch']) and \
                                               any(suffix in img['name'] for suffix in ['abc.png', 'neutral.png'])
                                
                                if is_mlo_special:
                                    # For MLO ABC and neutral images, use full page
                                    available_height = 8*inch  # Leave space for header and footer
                                    available_width = 6.5*inch  # Leave margins
                                    
                                    # Calculate dimensions to fit the page while maintaining aspect ratio
                                    if aspect > available_height/available_width:
                                        # Height limited
                                        display_height = available_height
                                        display_width = display_height / aspect
                                    else:
                                        # Width limited
                                        display_width = available_width
                                        display_height = display_width * aspect
                                    
                                    # Center the image horizontally
                                    x_position = (8.5*inch - display_width) / 2
                                    
                                    # Draw the image
                                    c.drawImage(img_reader, x_position, y_position - display_height,
                                              width=display_width, height=display_height, preserveAspectRatio=True)
                                    
                                    # Start a new page after each MLO ABC/neutral image
                                    c.showPage()
                                    page_num += 1
                                    
                                    # Reset y_position for the new page
                                    y_position = 9.0*inch
                                    
                                    # Add header with packet title on new page
                                    c.setFont("Helvetica-Bold", 14)
                                    c.drawString(1*inch, 10.5*inch, "FACTORY SWITCHBOARD PACKET")
                                    
                                    # Section title
                                    c.setFont("Helvetica-Bold", 16)
                                    c.drawString(1*inch, 9.8*inch, f"{form_data.get('switchboard_name', '')} - Section {i}: {section_type}")
                                    
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
                                    
                                else:
                                    # Original image handling for non-MLO ABC/neutral images
                                    # Calculate maximum display height to ensure at least 2 images per page
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
                                        break
                                    
                                    # Draw the image
                                    c.drawImage(img_reader, 1*inch, y_position - display_height, 
                                              width=display_width, height=display_height, preserveAspectRatio=True)
                                    
                                    # Add quantity and label under the image
                                    c.setFont("Helvetica-Bold", 12)
                                    label = self.image_labels.get(img['name'], img['name'])
                                    c.drawString(1*inch, y_position - display_height - 0.3*inch, f"QTY: {img['quantity']} - {label}")
                                    
                                    # Update y_position for next image
                                    y_position -= display_height + 0.5*inch
                                
                                images_processed += 1
                                images_on_this_page += 1
                            except Exception as e:
                                print(f"Error adding image {img['name']} for section {i}: {str(e)}")
                                images_processed += 1
                        else:
                            print(f"Warning: Image not found: {image_path}")
                            images_processed += 1
                    
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
            c.save()
            
            elapsed_time = time.time() - start_time
            
            return pdf_path
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise 