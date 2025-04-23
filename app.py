from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from utils.pdf_generator import PDFGenerator
import time

app = Flask(__name__)
pdf_generator = PDFGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        form_data = request.form.to_dict()
        form_data['timestamp'] = time.strftime("%Y%m%d_%H%M%S")
        
        # Generate the PDF
        pdf_path = pdf_generator.generate_pdf(form_data)
        
        # Create a formatted filename with Sales Order, Customer Name, and Switchboard Name
        sales_order = form_data.get('sales_order', 'Unknown')
        customer_name = form_data.get('customer_name', 'Unknown')
        switchboard_name = form_data.get('switchboard_name', 'Unknown')
        
        # Clean the values to make them safe for filenames
        sales_order = ''.join(c for c in sales_order if c.isalnum() or c in ' -_')
        customer_name = ''.join(c for c in customer_name if c.isalnum() or c in ' -_')
        switchboard_name = ''.join(c for c in switchboard_name if c.isalnum() or c in ' -_')
        
        # Create the formatted filename
        download_name = f"{sales_order} - {customer_name} - {switchboard_name} - Factory Packet.pdf"
        
        # Return the PDF file
        return send_file(pdf_path, as_attachment=True, download_name=download_name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(
            os.path.join('output', filename),
            as_attachment=True
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404

if __name__ == '__main__':
    app.run(debug=True) 