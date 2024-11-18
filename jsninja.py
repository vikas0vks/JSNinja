import requests
import re
import json
import signal
import sys
import os
from urllib.parse import urlparse
from colorama import Fore, Style, init
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Initialize Colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = r"""
     ____.         _______  .__            __        
    |    | ______  \      \ |__| ____     |__|____   
    |    |/  ___/  /   |   \|  |/    \    |  \__  \  
/\__|    |\___ \  /    |    \  |   |  \   |  |/ __ \_
\________/____  > \____|__  /__|___|  /\__|  (____  /  
              \/          \/        \/\______|    \/ 
    """
    terminal_width = os.get_terminal_size().columns
    banner_lines = banner.strip().splitlines()

    for i, line in enumerate(banner_lines):
        color = [Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX][i % 4]
        print(color + line.center(terminal_width))

    quote = f"{Fore.CYAN}JSNinja - \"Hunting Bugs in JavaScript Modified by Vikas!!\"{Style.RESET_ALL}"
    print(quote.center(terminal_width))

def extract_links_from_js(js_content):
    url_pattern = r'(https?://[^\s\'"<>]+)'
    return re.findall(url_pattern, js_content)

def extract_secrets(js_content):
    secret_patterns = {
        'AWS Access Key': r'(?i)AWS_Access_Key\s*:\s*[\'"]?([A-Z0-9]{20})[\'"]?',
        'AWS Secret Key': r'(?i)AWS_Secret_Key\s*:\s*[\'"]?([A-Za-z0-9/+=]{40})[\'"]?',
        'Stripe Secret Key': r'(?i)Stripe_Secret_Key\s*:\s*[\'"]?([A-Za-z0-9]{24})[\'"]?',
        'GitHub Token': r'(?i)GitHub Token\s*:\s*[\'"]?([A-Za-z0-9]{36})[\'"]?',
        'Facebook Token': r'(?i)Facebook_Token\s*:\s*[\'"]?([A-Za-z0-9\.]+)[\'"]?',
        'Telegram Bot Token': r'(?i)Telegram Bot Token\s*:\s*[\'"]?([A-Za-z0-9:]+)[\'"]?',
        'Google Maps API Key': r'(?i)Google Maps API Key\s*:\s*[\'"]?([A-Za-z0-9_-]+)[\'"]?',
        'Google reCAPTCHA Key': r'(?i)Google reCAPTCHA Key\s*:\s*[\'"]?([A-Za-z0-9_-]+)[\'"]?',
        'API Key': r'(?i)API_Key\s*:\s*[\'"]?([A-Za-z0-9_-]{32,})[\'"]?',
        'Secret Key': r'(?i)Secret_Key\s*:\s*[\'"]?([A-Za-z0-9_-]{32,})[\'"]?',
        'Auth Domain': r'(?i)Auth_Domain\s*:\s*[\'"]?([A-Za-z0-9\-]+\.[a-z]{2,})[\'"]?',
        'Database URL': r'(?i)Database_URL\s*:\s*[\'"]?([^\'" ]+)[\'"]?',
        'Storage Bucket': r'(?i)Storage_Bucket\s*:\s*[\'"]?([^\'" ]+)[\'"]?',
        'Cloud Storage API Key': r'(?i)Cloud Storage API Key\s*:\s*[\'"]?([A-Za-z0-9_-]{32,})[\'"]?'
    }

    found_secrets = {}
    for key, pattern in secret_patterns.items():
        matches = re.findall(pattern, js_content)
        if matches:
            unique_matches = list(set(matches))
            found_secrets[key] = unique_matches

    return found_secrets

def signal_handler(sig, frame):
    choice = input(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Do you want to close JSNinja? (Y/N): ").strip().lower()
    if choice == 'y':
        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Closing JSNinja...")
        sys.exit(0)
    else:
        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Continuing execution...")

def process_js_links(js_links, output_dir, cookies=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for js_link in js_links:
        js_link = js_link.strip()
        if not js_link:
            continue

        try:
            headers = {'Cookie': cookies} if cookies else {}
            response = requests.get(js_link, headers=headers, verify=False)
            
            status_code = response.status_code
            if status_code == 200:
                print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Processing {js_link}...")

                # Extract domain for file naming
                domain = urlparse(js_link).netloc

                # Create separate files for URLs and Secrets
                urls_file = os.path.join(output_dir, f"{domain}_urls.txt")
                secrets_file = os.path.join(output_dir, f"{domain}_secrets.json")

                # Extract URLs
                links = extract_links_from_js(response.text)
                if links:
                    with open(urls_file, 'w') as file:
                        file.write(f"URLs extracted from: {js_link}\n\n")
                        file.writelines([link + '\n' for link in links])
                    print(f"{Fore.GREEN}[+] Extracted {len(links)} URLs from {js_link}{Style.RESET_ALL}")
                    for link in links:
                        print(f"{Fore.CYAN}[URL]{Style.RESET_ALL} {link}")
                else:
                    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} No URLs found in {js_link}")

                # Extract Secrets
                secrets = extract_secrets(response.text)
                if secrets:
                    with open(secrets_file, 'w') as file:
                        json.dump({js_link: secrets}, file, indent=2)
                    print(f"{Fore.GREEN}[+] Extracted secrets from {js_link}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Secrets:{Style.RESET_ALL} {json.dumps(secrets, indent=2)}")
                else:
                    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} No secrets found in {js_link}")
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to process {js_link}. Status Code: {status_code}")

        except requests.RequestException as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Could not fetch {js_link}: {e}")

def main():
    clear_screen()
    print_banner()

    while True:
        print("\nSelect an option:")
        print("1. Process a single JavaScript URL")
        print("2. Process a list of JavaScript URLs from a file")
        print("3. Exit")
        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == "1":
            single_url = input("Enter the JavaScript URL: ").strip()
            cookies = input("Enter cookies (or press Enter to skip): ").strip()
            output_dir = ""

            while not output_dir:
                output_dir = input("Enter the name of the directory to save results: ").strip()
                if not output_dir:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Directory name cannot be empty. Please try again.")

            process_js_links([single_url], output_dir, cookies)

        elif choice == "2":
            input_file = input("Enter the file name containing URLs: ").strip()
            if not os.path.exists(input_file):
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} File not found: {input_file}")
                continue

            with open(input_file, 'r') as file:
                js_links = file.readlines()

            cookies = input("Enter cookies (or press Enter to skip): ").strip()
            output_dir = ""

            while not output_dir:
                output_dir = input("Enter the name of the directory to save results: ").strip()
                if not output_dir:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Directory name cannot be empty. Please try again.")

            process_js_links(js_links, output_dir, cookies)

        elif choice == "3":
            print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Exiting JSNinja...")
            break

        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid choice. Please try again.")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
    main()
