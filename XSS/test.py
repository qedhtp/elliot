import requests
import re
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from ratelimit import limits, sleep_and_retry
import sys

# Define the rate limit: 100 calls per second
MAX_CALLS_PER_SECOND = 100

# Function to check if the response contains the pattern, with rate limiting
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_SECOND, period=1)
def check_response_for_pattern(url, pattern, headers):
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            if re.search(pattern, response.text):
                return f"The response from {url} contains the pattern: '{pattern}'"
            else:
                return f"The response from {url} does not contain the pattern: '{pattern}'"
        elif response.status_code == 403:
            return f"Access forbidden for {url}. Status code: {response.status_code}"
        else:
            return f"Failed to retrieve the page at {url}. Status code: {response.status_code}"
    
    except requests.RequestException as e:
        return f"An error occurred while accessing {url}: {e}"

def main():
    parser = argparse.ArgumentParser(description='Check URLs for a specific regex pattern.')
    parser.add_argument('file', help='The file containing a list of URLs to check')
    parser.add_argument('--pattern', required=True, help='The regex pattern to search for in the responses')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1 second)')
    parser.add_argument('--threads', type=int, default=4, help='Number of concurrent threads (default: 4)')
    
    args = parser.parse_args()
    
    # Read URLs from the file
    with open(args.file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    pattern = args.pattern
    delay = args.delay
    num_threads = args.threads
    
    # Define headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://google.com',
        'Connection': 'keep-alive'
    }
    
    # Initialize the ThreadPoolExecutor with the specified number of threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the executor and map futures to URLs
        future_to_url = {executor.submit(check_response_for_pattern, url, pattern, headers): url for url in urls}
        
        # Process completed futures as they finish
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                print(data, file=sys.stdout)  # Output the result to stdout
            except Exception as exc:
                print(f"An error occurred while accessing {url}: {exc}", file=sys.stdout)  # Output the error to stdout
            time.sleep(delay)

if __name__ == "__main__":
    main()
