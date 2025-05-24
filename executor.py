import os
import sys
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
import argparse
from colorama import init, Fore

# Initialize colorama
init()

# Function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ViewBot Functions
def visit_site(url, use_proxy=False, proxies=None, delay=False):
    """
    Visit a website and return the status code
    """
    # Create a random user agent to appear like different browsers
    headers = {
        'User-Agent': generate_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    
    # Add random referrers occasionally
    if random.random() < 0.3:
        possible_referrers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://www.facebook.com/',
            'https://www.reddit.com/',
            'https://www.twitter.com/',
        ]
        headers['Referer'] = random.choice(possible_referrers)
    
    try:
        if use_proxy and proxies:
            proxy = random.choice(proxies)
            response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Visit successful: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error visiting site: {e}")
        return None
    finally:
        if delay:
            # Random delay between 1 and 5 seconds
            time.sleep(random.uniform(1, 5))

def generate_user_agent():
    """
    Generate a random user agent string
    """
    user_agents = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        # Mobile
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0',
    ]
    return random.choice(user_agents)

def load_proxies(proxy_file):
    """
    Load proxies from a file
    """
    try:
        with open(proxy_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading proxy file: {e}")
        return []

def run_viewbot():
    """
    Run the viewbot functionality
    """
    # Ask for the target URL
    print(Fore.CYAN + "Enter the website URL you want to use for the viewbot")
    print(Fore.CYAN + "Example: https://example.com/page")
    TARGET_URL = input(Fore.WHITE + "[?] Target URL: ")
    
    # Validate URL format
    if not TARGET_URL.startswith(('http://', 'https://')):
        print(Fore.YELLOW + "URL should start with http:// or https://")
        TARGET_URL = "https://" + TARGET_URL
        print(Fore.YELLOW + f"URL updated to: {TARGET_URL}")
    
    # Ask for number of views
    try:
        num_views = int(input(Fore.WHITE + "[?] Number of views to generate (default: 50): ") or "50")
    except ValueError:
        num_views = 50
        print(Fore.YELLOW + "Invalid input, using default: 50 views")
    
    # Ask for concurrency
    try:
        concurrency = int(input(Fore.WHITE + "[?] Number of concurrent workers (default: 5): ") or "5")
    except ValueError:
        concurrency = 5
        print(Fore.YELLOW + "Invalid input, using default: 5 workers")
    
    # Ask about delay
    delay_input = input(Fore.WHITE + "[?] Use random delays between requests? (y/n, default: y): ").lower() or "y"
    delay = delay_input.startswith('y')
    
    # For simplicity, keeping proxy options as defaults
    use_proxy = False
    proxy_file = None
    proxies = None
    
    print(f"\n{Fore.GREEN}Starting view bot for {TARGET_URL}")
    print(f"{Fore.GREEN}Generating {num_views} views with {concurrency} concurrent workers")
    print(f"{Fore.GREEN}Using delays: {delay}")
    print(f"{Fore.GREEN}Using proxies: {use_proxy}")
    
    start_time = time.time()
    
    # Use ThreadPoolExecutor to handle concurrent requests
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        for _ in range(num_views):
            futures.append(executor.submit(
                visit_site, TARGET_URL, use_proxy, proxies, delay
            ))
        
        # Wait for all futures to complete
        success_count = 0
        for future in futures:
            if future.result() is not None and 200 <= future.result() < 400:
                success_count += 1
    
    duration = time.time() - start_time
    print(f"\nTest completed in {duration:.2f} seconds")
    print(f"Successful views: {success_count}/{num_views}")
    
    # Wait for user to press Enter before returning to main menu
    input("\nPress Enter to return to main menu...")

def display_main_menu():
    # ASCII Art
    ascii_art = """
      ██╗ ██████╗ ███╗   ██╗ █████╗ ████████╗██╗  ██╗ ██████╗ ███╗   ██╗
      ██║██╔═══██╗████╗  ██║██╔══██╗╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
      ██║██║   ██║██╔██╗ ██║███████║   ██║   ███████║██║   ██║██╔██╗ ██║
 ██   ██║██║   ██║██║╚██╗██║██╔══██║   ██║   ██╔══██║██║   ██║██║╚██╗██║
 ╚█████╔╝╚██████╔╝██║ ╚████║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
  ╚════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

"""
    
    # Clear screen
    clear_screen()
    
    # Print art
    print(Fore.CYAN + ascii_art)
    
    # Print menu
    print(Fore.GREEN + "1. Website View Bot")
    print("2. dead.by.daylight.injects")
    print("3. Twitch View Botad")
    print("4. roblox.menu")
    print(Fore.RED + "5. Exit")
    print()
    
    # Prompt
    option = input(Fore.WHITE + "[?] option? (): ")
    
    # Process the user's choice
    if option == "1":
        clear_screen()
        print(Fore.CYAN + "Running Website View Bot...\n")
        run_viewbot()
        display_main_menu()  # Return to the main menu after viewbot completes
    elif option == "2" or option == "3" or option == "4":
        print(Fore.YELLOW + "Sorry this is currently down, please check the discord and try again later!")
        time.sleep(2)
        display_main_menu()
    elif option == "5":
        print(Fore.RED + "Exiting program. Goodbye!")
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid option. Please try again.")
        time.sleep(1)
        display_main_menu()

# Main program
if __name__ == "__main__":
    try:
        display_main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram interrupted. Exiting...")
        sys.exit(0)