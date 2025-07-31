# PDF Paper Downloader

This script automatically downloads the daily PDF from [dailyluach.com](https://dailyluach.com/) by simulating a request from a mobile device to access the "Today" link. It is designed to be executed via n8n webhook automation.

## Features

- Simulates mobile device navigation to access the dropdown menu
- Implements techniques to avoid being banned:
  - Random delays between requests
  - User-Agent rotation
  - Human behavior simulation
- Detects and downloads the current day's PDF
- Avoids duplicate downloads by checking existing files
- Detailed logging of the process
- Compatible with n8n webhook automation

## Requirements

```
requests
beautifulsoup4
fake-useragent
```

## Installation

1. Make sure you have Python 3.6 or higher installed
2. Install the dependencies:

```
pip install -r requirements.txt
```

Alternatively, you can install dependencies directly:

```
pip install requests beautifulsoup4 fake-useragent
```

## Usage

### Direct Execution

Run the script directly:

```
python downloader.py
```

By default, the PDF will be downloaded to the same folder where the script is located.

You can specify a custom output directory:

```
python downloader.py --output-dir /path/to/save/pdfs
# or using the short form
python downloader.py -o /path/to/save/pdfs
```

### n8n Webhook Integration

There are two ways to execute this script via n8n:

#### Method 1: Direct Python Execution

1. Set up an n8n workflow with an HTTP Request node
2. Configure the HTTP Request node to execute a shell command
3. Set the command to: `python /path/to/downloader.py`
4. Trigger the workflow via webhook or schedule it to run automatically

#### Method 2: Import as a Module

You can also create a custom script that imports the downloader module. An example script `custom_n8n_script.py` is included in this repository:

```python
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
```

This script creates a "downloads" subdirectory and saves all PDFs there. It also provides proper exit codes for n8n to detect success or failure.

## Automation with n8n

### Setting up n8n Webhook Automation

1. In your n8n workflow, add a trigger node:
   - **Schedule Trigger**: For daily automatic execution
   - **Webhook Trigger**: For manual or event-based execution

2. Add an **Execute Command** node (or equivalent in your n8n version):

   **Option A: Using the main script directly**
   - Command: `python /full/path/to/downloader.py`
   - Working Directory: The directory where your script is located
   
   To specify a custom output directory:
   - Command: `python /full/path/to/downloader.py --output-dir /path/to/save/pdfs`

   **Option B: Using the custom n8n script**
   - Command: `python /full/path/to/custom_n8n_script.py`
   - Working Directory: The directory where your script is located
   
   The custom script will automatically create a "downloads" subdirectory and save PDFs there.

3. Optional: Add a **Slack** or **Email** node to send notifications about the download status

4. Connect the nodes in sequence and activate the workflow

#### Example n8n Workflow:

```
Schedule Trigger (Daily at 8 AM) → Execute Command → IF → (Success) → Success Notification
                                                    └→ (Error) → Error Notification
```

#### Complete n8n Workflow Example

1. **Schedule Trigger**:
   - Mode: Basic
   - Trigger at: 8:00 AM
   - Trigger on days: Monday-Friday

2. **Execute Command**:
   - Command: `python /path/to/custom_n8n_script.py`
   - Working Directory: `/path/to/script/directory`

3. **IF**:
   - Condition: `{{$node["Execute Command"].json["exitCode"] === 0}}`

4. **Success Notification** (Slack, Email, or other):
   - Message: `PDF Download Successful: {{$node["Execute Command"].json["stdout"]}}`

5. **Error Notification** (Slack, Email, or other):
   - Message: `PDF Download Failed: {{$node["Execute Command"].json["stderr"]}}`

This setup allows the script to be executed automatically according to your n8n workflow schedule or when triggered by an event.

## Notes

- The script is designed to be respectful to the server by implementing random delays.
- If the "Today" link is not found, the script will try to find any available PDF link.
- The script is optimized for automated execution via n8n webhook.
- Make sure the server running n8n has the required Python dependencies installed.
- Ensure the n8n workflow has proper permissions to execute the Python script.
- The script will download the PDF to the same directory where it's located.

## Troubleshooting

### Common Issues

1. **Script fails to find PDF link**
   - The website structure may have changed
   - Solution: Check the website manually and update the script if needed

2. **Dependencies not found**
   - Error message: `ModuleNotFoundError: No module named 'xxx'`
   - Solution: Install the missing dependency with `pip install xxx`

3. **Permission errors**
   - Error when creating directories or writing files
   - Solution: Ensure the user running n8n has write permissions to the output directory

4. **n8n cannot execute the script**
   - Check that the path to the script is correct
   - Ensure Python is in the PATH of the user running n8n
   - Try using absolute paths for both the Python executable and the script

### Debugging

If you encounter issues, you can modify the custom script to add more detailed logging:

```python
# Add this to the top of custom_n8n_script.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='pdf_downloader_debug.log'
)
```

## Error Handling and Notifications

When using this script with n8n, you can implement error handling and notifications:

### Basic Error Handling

The script returns `True` if the download was successful and `False` otherwise. You can use this return value in your n8n workflow to implement conditional logic.

### Example n8n Workflow with Error Handling

1. **Schedule Trigger**: Runs daily at a specific time
2. **Execute Command**: Runs the Python script
3. **IF**: Checks if the command was successful (using the `exitCode` property)
   - If exitCode equals 0: Send a success notification
   - If exitCode does not equal 0: Send an error notification

#### n8n IF Node Configuration

When using the custom script, you can check the exit code in the IF node:

```
// Success condition
{{$node["Execute Command"].json["exitCode"] === 0}}

// Error condition
{{$node["Execute Command"].json["exitCode"] !== 0}}
```

You can also include the command output in your notifications:

```
// For success notification
{{$node["Execute Command"].json["stdout"]}}

// For error notification
{{$node["Execute Command"].json["stderr"]}}
```

### Logging

The script logs all activities with timestamps. You can capture this output in n8n and include it in your notifications for detailed troubleshooting information.

## Security and Best Practices

### Security Considerations

1. **Server Permissions**
   - Run the script with minimal required permissions
   - Do not run as root/administrator unless absolutely necessary

2. **Network Security**
   - Consider using a proxy if making many requests
   - Implement proper error handling for network issues

3. **Data Storage**
   - Be mindful of where you store downloaded PDFs
   - Implement retention policies if needed

### Best Practices for n8n Integration

1. **Error Handling**
   - Always check exit codes from the script
   - Implement proper notification for failures

2. **Monitoring**
   - Set up monitoring for your n8n workflows
   - Consider implementing a "heartbeat" to verify the automation is running

3. **Maintenance**
   - Regularly check that the script still works with the website
   - Update dependencies periodically
   - Consider implementing version control for your scripts