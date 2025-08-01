#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask API for PDF Paper Downloader

This script creates a Flask web server with an endpoint that triggers the PDF download
when accessed. It can be used as an alternative to n8n for automation.
"""

import os
import json
import requests
from datetime import datetime
from flask import Flask, jsonify, request, send_file, Response
from werkzeug.serving import run_simple
from downloader import run_download, download_pdf

app = Flask(__name__)

# Add timestamp to log messages
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    return f"[{timestamp}] {message}"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'PDF Downloader API is running'
    })

@app.route('/download', methods=['GET', 'POST'])
def download_endpoint():
    """Endpoint to trigger the PDF download"""
    logs = []
    
    # Check if client wants direct download or JSON response
    direct_download = request.args.get('direct', 'false').lower() == 'true'
    
    # Get output directory from query parameters or request body
    output_dir = None
    
    if request.method == 'GET':
        output_dir = request.args.get('output_dir')
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            output_dir = data.get('output_dir')
            if 'direct' in data:
                direct_download = data.get('direct', False)
        elif request.form:
            output_dir = request.form.get('output_dir')
            if 'direct' in request.form:
                direct_download = request.form.get('direct', 'false').lower() == 'true'
    
    # If output_dir is not provided, use default (downloads folder)
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logs.append(log(f"Created output directory: {output_dir}"))
    
    # Run the download function
    logs.append(log(f"Downloading PDF to: {output_dir}"))
    
    try:
        # Use a temporary directory for direct downloads
        if direct_download:
            temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # Download the PDF and get the file path
            success, pdf_path = download_pdf(output_dir=temp_dir, return_path=True)
            
            if success and pdf_path:
                logs.append(log(f"Sending file directly to client: {pdf_path}"))
                filename = os.path.basename(pdf_path)
                
                # Send the file to the client
                return send_file(
                    pdf_path,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/pdf'
                )
            else:
                logs.append(log("Download failed, cannot send file to client"))
                return jsonify({
                    'success': False,
                    'message': 'Failed to download PDF for direct download',
                    'logs': logs,
                    'timestamp': datetime.now().isoformat()
                }), 500
        else:
            # Standard download to server storage
            success = run_download(output_dir=output_dir)
            
            if success:
                logs.append(log("Download completed successfully"))
                return jsonify({
                    'success': True,
                    'message': 'PDF downloaded successfully',
                    'output_directory': output_dir,
                    'logs': logs,
                    'timestamp': datetime.now().isoformat()
                }), 200
            else:
                logs.append(log("Download failed"))
                return jsonify({
                    'success': False,
                    'message': 'Failed to download PDF',
                    'output_directory': output_dir,
                    'logs': logs,
                    'timestamp': datetime.now().isoformat()
                }), 500
    
    except Exception as e:
        error_message = str(e)
        logs.append(log(f"Error: {error_message}"))
        return jsonify({
            'success': False,
            'message': 'Error occurred during download',
            'error': error_message,
            'logs': logs,
            'timestamp': datetime.now().isoformat()
        }), 500

# Add a direct download endpoint that streams the PDF directly
@app.route('/direct-download', methods=['GET'])
def direct_download():
    """Endpoint to directly download the PDF without saving it on the server"""
    try:
        log("Starting direct PDF download stream to client")
        
        # Create a temporary directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # Download the PDF and get the file path
        success, pdf_path = download_pdf(output_dir=temp_dir, return_path=True)
        
        if success and pdf_path:
            log(f"Streaming file directly to client: {pdf_path}")
            filename = os.path.basename(pdf_path)
            
            # Stream the file to the client
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/pdf'
            )
        else:
            log("Download failed, cannot stream file to client")
            return jsonify({
                'success': False,
                'message': 'Failed to download PDF for streaming',
                'timestamp': datetime.now().isoformat()
            }), 500
    
    except Exception as e:
        error_message = str(e)
        log(f"Error during direct download: {error_message}")
        return jsonify({
            'success': False,
            'message': 'Error occurred during direct download',
            'error': error_message,
            'timestamp': datetime.now().isoformat()
        }), 500

# Create a production WSGI server
def create_app():
    """Factory function to create the Flask app for WSGI servers"""
    return app

if __name__ == '__main__':
    # Default port is 5000, but can be changed
    port = int(os.environ.get('PORT', 5000))
    
    # Create temp directory for direct downloads
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        log(f"Created temp directory for direct downloads: {temp_dir}")
    
    # Create downloads directory if it doesn't exist
    default_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
        log(f"Created default output directory: {default_dir}")
    
    # Check if running in development or production mode
    production = os.environ.get('FLASK_ENV', 'development').lower() == 'production'
    
    if production:
        # Use Werkzeug's production server (still not recommended for real production)
        log(f"Starting production server on port {port}")
        run_simple('0.0.0.0', port, app, threaded=True)
    else:
        # Show warning about development server
        log(f"Starting Flask development server on port {port}")
        log("WARNING: This is a development server. For production, use Gunicorn or uWSGI.")
        log("Example: gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'")
        app.run(host='0.0.0.0', port=port, debug=False)