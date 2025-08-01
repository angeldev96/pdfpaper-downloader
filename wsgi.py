#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WSGI entry point for the PDF Downloader API

This file is used by Gunicorn to serve the Flask application in production.
Example usage: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""

from app import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # This block is only executed when running this file directly
    # It's not used by Gunicorn
    app.run()