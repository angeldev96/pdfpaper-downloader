#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom script for n8n integration with the PDF Paper Downloader

This script can be executed by n8n to download the daily PDF from dailyluach.com
It handles errors and returns appropriate exit codes for n8n to process.
"""

import sys
import os
from datetime import datetime
from downloader import run_download

# You can define a custom output directory
# If not specified, it will use the script's directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

# Add timestamp to log messages
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    try:
        log("Starting PDF download process")
        
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            log(f"Created output directory: {OUTPUT_DIR}")
        
        # Run the download function
        log(f"Downloading PDF to: {OUTPUT_DIR}")
        success = run_download(output_dir=OUTPUT_DIR)
        
        if success:
            log("Download completed successfully")
            # Exit with success code for n8n to detect
            return 0
        else:
            log("Download failed")
            # Exit with error code for n8n to detect
            return 1
            
    except Exception as e:
        log(f"Error: {str(e)}")
        # Exit with error code for n8n to detect
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)