# Import necessary libraries
import requests  # To make HTTP requests
from bs4 import BeautifulSoup  # To parse HTML content
import re # Import regular expressions for more flexible text matching if needed

def find_div_by_text(url, search_text):
    """
    Scrapes a given URL to find all div elements containing specific text
    and prints their class and ID attributes.

    Args:
        url (str): The URL of the webpage to scrape.
        search_text (str): The exact text content to search for within div elements.

    Returns:
        list: A list of BeautifulSoup Tag objects representing the found divs,
              or None if an error occurs. Returns an empty list if no matching divs are found.
    """
    print(f"Attempting to scrape URL: {url}")
    print(f"Searching for divs containing text: '{search_text}'")
    try:
        # Send an HTTP GET request to the URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise an exception for bad status codes
        print("Successfully fetched the page.")

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all div elements
        all_divs = soup.find_all('div')
        print(f"Found {len(all_divs)} total div elements. Checking text content...")

        # Filter divs that contain the exact search text (stripping whitespace)
        found_divs = []
        for div in all_divs:
            # Get the text content, remove leading/trailing whitespace
            div_text = div.get_text(strip=True)
            # Check for an exact match with the search text
            if div_text == search_text:
                found_divs.append(div)
                print(f"\n--- Found a matching div ---")

                # Get the class attribute (returns a list or None)
                div_class = div.get('class')
                # Get the id attribute (returns a string or None)
                div_id = div.get('id')

                # Print the class attribute if it exists
                if div_class:
                    # Join the list of classes into a single string
                    print(f"  Class(es): {' '.join(div_class)}")
                else:
                    print("  Class(es): Not found")

                # Print the ID attribute if it exists
                if div_id:
                    print(f"  ID: {div_id}")
                else:
                    print("  ID: Not found")
                # Optionally print the div content for context
                # print(f"  Content Preview: {div.prettify()[:200]}...") # Show first 200 chars
                print("----------------------------")


        print(f"\nFound {len(found_divs)} div(s) containing the exact text '{search_text}'.")
        return found_divs # Return the list of found div Tag objects

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    # Define the target URL and the text to search for
    target_url = "https://www.jarvis-protocol.com/team-tactics-cards"
    text_to_find = "A Better Tomorrow" # Example text, change as needed

    # Call the function to find the divs
    matching_divs = find_div_by_text(target_url, text_to_find)

    # Check if the search was successful (returned a list or None)
    if matching_divs is not None:
        if not matching_divs:
             print(f"\n--- No divs containing the exact text '{text_to_find}' were found. ---")
        # The details (class/ID) are already printed within the function
    else:
        print("\nCould not perform the search due to an error during scraping.")

