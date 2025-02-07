#!/bin/python3

import requests
import re
import argparse
import time
import sys

# grep the string, and the determin if character in side it
pattern_1 = r"test\"\<\'qed"  # reflect all three special symbol
pattern_2 = r"test\"\<[^\'\r\n]*qed" # reflect " and <
pattern_3 = r"test[^\"\r\n]*\<\'qed" # reflect < and '
pattern_4 = r"test\"[^\<\r\n]*\'qed" # reflect  " and '

pattern_5 = r"test\"[^\<\'\r\n]*qed" # reflect "
pattern_6 = r"test[^\"\r\n]*\<[^\'\r\n]*qed" # reflect <
pattern_7 = r"test[^\"\<\r\n]*\'qed" # reflect '


def check_special(url, headers):
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            if re.search(pattern_1, response.text):
                return f"{url} | Not filter: All"
            elif re.search(pattern_2, response.text):
                
                return f"{url} | not filter: \" and <"
            elif re.search(pattern_3, response.text):
                return f"{url} | not filter: < and \'"
            elif re.search(pattern_4, response.text):
                return f"{url} | not filter: \" and \'"
            elif re.search(pattern_5, response.text):
                return f"{url} | not filter: \" "
            elif re.search(pattern_6, response.text):
                return f"{url} | not filter: < "
            elif re.search(pattern_7, response.text):
                return f"{url} | not filter: \' "
            else:
                return f"{url} | All be encode"
        else:
            return f"{url}Failed to retrieve the page. Status code: {response.status_code}"
    
    except requests.RequestException as e:
        return f"An error occurred: {e}"



def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Check URLs for a specific regex pattern.')
    parser.add_argument('-l','--list',help='The file containing a list of URLs to check',required='True')
    parser.add_argument('-d','--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1 second)')
    
    # Parse arguments
    args = parser.parse_args()
    

    # Define headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    
    # Read the list of URLs from the file
    with open(args.list, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    # Get the pattern from the arguments
    delay = args.delay
    
    # Iterate over the list of URLs and check each one
    for url in urls:
        try:
            result = check_special(url, headers)
            print(result, file=sys.stdout,flush=True)  # Output the result to stdout
        except Exception as exc:
            print(f"An error occurred while accessing {url}: {exc}", file=sys.stdout)  # Output the error to stdout
        
        # time.sleep(delay)

if __name__ == "__main__":
    main()
