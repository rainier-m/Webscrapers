# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import re # Import regular expressions module

# The URL to scrape
url = "https://www.jarvis-protocol.com/team-tactics-cards"

# --- Function to Scrape and Parse ---
def scrape_team_tactics_cards(target_url):
    """
    Scrapes the given URL, finds elements with a class containing
    'team-tactics-card-container', and prints information about them.
    """
    print(f"Attempting to scrape: {target_url}")

    try:
        # Send an HTTP GET request to the URL
        # Add a User-Agent header to mimic a browser visit
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(target_url, headers=headers, timeout=10) # Added timeout

        # Check if the request was successful (status code 200)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        print("Successfully fetched the page.")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        print("Successfully parsed HTML.")

        # --- Find elements containing the specified class ---
        # We use a regular expression within find_all to match any class
        # attribute that *contains* 'team-tactics-card-container'.
        # This is more flexible than an exact match.
        card_containers = soup.find_all(class_=re.compile(r'team-tactics-card-container'))

        print(f"\nFound {len(card_containers)} elements containing 'team-tactics-card-container' in their class.")

        if not card_containers:
            print("Could not find any elements matching the criteria. The class name or page structure might have changed.")
            # Optional: Print a snippet of the HTML to help debug
            # print("\nPage Snippet (first 1000 chars):\n", soup.prettify()[:1000])
            return

        # --- Process the found elements (Example) ---
        print("\n--- Parsed Card Containers (showing first 5) ---")
        for i, container in enumerate(card_containers[:5]): # Limit output to first 5 for brevity
            print(f"\nElement {i+1}:")
            # Print the full tag for context
            print(f"  Tag: {container.name}")
            # Print the classes to verify
            print(f"  Classes: {container.get('class', 'N/A')}")

            # --- Example: Extracting potential data ---
            # You'll need to inspect the actual HTML structure within these
            # containers on the website (e.g., using browser developer tools)
            # to accurately extract specific data like card names, text, images.
            # Below are examples of how you might find common elements:

            # Example: Find an image source (img tag with src attribute)
            image = container.find('img')
            if image and image.get('src'):
                print(f"  Found Image Src: {image['src']}")

            # Example: Find a title (e.g., in an h3 tag)
            title = container.find(['h2', 'h3', 'h4']) # Look for common heading tags
            if title:
                print(f"  Found Title/Header: {title.get_text(strip=True)}")

            # Example: Find some descriptive text (e.g., in a p tag)
            description = container.find('p')
            if description:
                print(f"  Found Description: {description.get_text(strip=True)}")

            # You can add more specific parsing logic here based on the
            # actual structure inside the 'team-tactics-card-container' divs.

    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {target_url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Run the scraper ---
if __name__ == "__main__":
    scrape_team_tactics_cards(url)