from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from utils.pdf_generator import PDFGenerator

app = Flask(__name__)
pdf_generator = PDFGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data
        form_data = request.form.to_dict()
        print("Form data received:", form_data)  # Debug log
        
        # Add timestamp to the data
        form_data['timestamp'] = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate the PDF
        pdf_path = pdf_generator.generate_pdf(form_data)
        print("PDF generated at:", pdf_path)  # Debug log
        
        # Return the PDF file directly to the browser
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"packet_{form_data['timestamp']}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print("Error generating PDF:", str(e))  # Debug log
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

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