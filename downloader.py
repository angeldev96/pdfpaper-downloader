import requests
import os
import time
import random
import re
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Default configuration
URL = "https://dailyluach.com/"
DEFAULT_OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# List of user agents for rotation
def get_random_user_agent():
    try:
        ua = UserAgent()
        # Use a mobile user agent
        return ua.random
    except:
        # Fallback in case fake_useragent fails
        mobile_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
            "Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/96.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/96.0.4664.53 Mobile/15E148 Safari/604.1"
        ]
        return random.choice(mobile_agents)

# Function to add random delays to avoid detection
def random_delay():
    # Random delay between 2 and 5 seconds
    delay = random.uniform(2, 5)
    time.sleep(delay)
    return delay

# Function to download the PDF
def download_pdf(output_dir=None, return_path=False):
    """Download the daily PDF from dailyluach.com
    
    Args:
        output_dir (str, optional): Directory to save the downloaded PDF. Defaults to script directory.
        return_path (bool, optional): Whether to return the path to the downloaded file. Defaults to False.
        
    Returns:
        If return_path is False:
            bool: True if download was successful, False otherwise.
        If return_path is True:
            tuple: (bool, str) - Success status and path to the downloaded file (or None if failed).
    """
    # Use default output directory if none specified
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
        
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Configure session with mobile device headers
    session = requests.Session()
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        # Simulate a mobile device
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }
    session.headers.update(headers)
    
    try:
        print(f"[{datetime.now()}] Connecting to {URL}...")
        # Add a random delay before the request
        delay = random_delay()
        print(f"[{datetime.now()}] Waiting {delay:.2f} seconds...")
        
        # Make the request to the main page
        response = session.get(URL)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the "Today" link in the dropdown menu
        today_link = None
        download_div = soup.find('div', class_='topnav download_pdf')
        
        if download_div:
            links_div = download_div.find('div', id='myLinks2')
            if links_div:
                # Find the link with "Today" text
                today_anchor = links_div.find('a', string=lambda s: s and 'Today' in s)
                if today_anchor and 'href' in today_anchor.attrs:
                    today_link = today_anchor['href'].strip()
        
        # If we don't find the specific link, try to extract any PDF link
        if not today_link:
            print(f"[{datetime.now()}] 'Today' link not found, searching for any PDF link...")
            pdf_links = re.findall(r'href=["\']([^"\']*/issue-\d+\.pdf)["\']', response.text)
            if pdf_links:
                # Take the first PDF link found
                today_link = pdf_links[0]
        
        if not today_link:
            print(f"[{datetime.now()}] Could not find any PDF link.")
            return False
        
        # Clean the link (remove spaces and extra quotes)
        today_link = today_link.strip().strip('"').strip("'").strip()
        
        # Make sure the link is absolute
        if not today_link.startswith('http'):
            if today_link.startswith('/'):
                today_link = f"https://dailyluach.com{today_link}"
            else:
                today_link = f"https://dailyluach.com/{today_link}"
        
        print(f"[{datetime.now()}] PDF link found: {today_link}")
        
        # Extract the filename from the link
        filename = os.path.basename(today_link)
        output_path = os.path.join(output_dir, filename)
        
        # Check if the file already exists
        if os.path.exists(output_path):
            print(f"[{datetime.now()}] File {filename} already exists. Skipping download.")
            if return_path:
                return True, output_path
            return True
        
        # Add another random delay before downloading
        delay = random_delay()
        print(f"[{datetime.now()}] Waiting {delay:.2f} seconds before downloading...")
        
        # Download the PDF
        print(f"[{datetime.now()}] Downloading {filename}...")
        pdf_response = session.get(today_link, stream=True)
        pdf_response.raise_for_status()
        
        # Save the PDF
        with open(output_path, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"[{datetime.now()}] Download completed: {output_path}")
        if return_path:
            return True, output_path
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Error making the request: {e}")
        if return_path:
            return False, None
        return False
    except Exception as e:
        print(f"[{datetime.now()}] Unexpected error: {e}")
        if return_path:
            return False, None
        return False

# Main function
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download daily PDF from dailyluach.com')
    parser.add_argument('--output-dir', '-o', help='Directory to save the downloaded PDF')
    args = parser.parse_args()
    
    print(f"[{datetime.now()}] Starting daily PDF download from dailyluach.com")
    success = download_pdf(output_dir=args.output_dir)
    if success:
        print(f"[{datetime.now()}] Process completed successfully.")
    else:
        print(f"[{datetime.now()}] Process failed.")
    return success

# Run the script if called directly
if __name__ == "__main__":
    main()

# Function to be called from external scripts or n8n
def run_download(output_dir=None, return_path=False):
    """Function that can be imported and called from external scripts or n8n
    
    Args:
        output_dir (str, optional): Directory to save the downloaded PDF. Defaults to script directory.
        return_path (bool, optional): Whether to return the path to the downloaded file. Defaults to False.
        
    Returns:
        If return_path is False:
            bool: True if download was successful, False otherwise.
        If return_path is True:
            tuple: (bool, str) - Success status and path to the downloaded file (or None if failed).
    """
    return download_pdf(output_dir=output_dir, return_path=return_path)