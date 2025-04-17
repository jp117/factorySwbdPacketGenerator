# Drawing Packet Generator

A web application that generates PDF packets from AutoCAD .dwg files based on user inputs.

## Features

- Web interface for user inputs
- Process AutoCAD .dwg files
- Generate PDF packets with drawings and quantities
- Modern UI with Tailwind CSS
- Dockerized deployment

## Running with Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed

2. Place your .dwg files in the `drawings` directory

3. Build and start the container:
   ```bash
   docker-compose up --build
   ```

4. Access the application at http://localhost:5000

5. Generated PDFs will be available in the `output` directory

## Manual Setup (Development)

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Build Tailwind CSS:
   ```bash
   npm run build
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

- `app.py` - Main Flask application
- `static/` - Static files (CSS, JS, images)
- `templates/` - HTML templates
- `drawings/` - Directory for .dwg files
- `output/` - Directory for generated PDFs
- `utils/` - Utility functions for processing drawings

## Docker Volumes

The application uses two Docker volumes:
- `./drawings`: Mount your local drawings directory here
- `./output`: Generated PDFs will be saved here

## Environment Variables

The following environment variables can be set in docker-compose.yml:
- `FLASK_APP`: The Flask application entry point (default: app.py)
- `FLASK_ENV`: The environment to run Flask in (default: production) 