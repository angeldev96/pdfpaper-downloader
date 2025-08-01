#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Production server for PDF Paper Downloader using Waitress

This script runs the Flask application using Waitress, a production-ready WSGI server.
"""

import os
from waitress import serve
from app import create_app

if __name__ == '__main__':
    # Get port from environment variable or use default 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Create the Flask application
    app = create_app()
    
    print(f"Starting Waitress production server on port {port}")
    print(f"Server running at: http://127.0.0.1:{port}")
    
    # Run the application with Waitress
    serve(app, host='0.0.0.0', port=port, threads=4)