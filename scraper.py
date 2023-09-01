import logging
import time
from typing import Dict, List

from bs4 import BeautifulSoup
from requests import Response, get


def scrape_data(
    num_pages: int, base_url: str, headers: Dict[str, str]
) -> List[Dict[str, str]]:
    """
    Scrapes data from multiple pages of a website.

    Args:
        num_pages (int): The number of pages to scrape.
        base_url (str): The base URL of the website.
        headers (Dict[str, str]): The headers to be included in the HTTP
        request.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing scraped data.
        Each dictionary represents a post and contains the following keys:
            - "Title": The title of the post.
            - "URL": The URL of the post.

    Raises:
        Exception: If an error occurs while scraping a page.

    Note:
        - The function uses the `get` method from the `requests` library to
          make HTTP requests.
        - The function uses the `BeautifulSoup` library to parse the HTML
          content of the website.
        - The function logs information using the `logging` module.
        - The function sleeps for 2 seconds after each scrape to avoid
          overwhelming the server.
    """

    scraped_data: List[Dict[str, str]] = []
    current_page = 1
    while current_page <= num_pages:
        try:
            logging.info("Starting to scrape page %s", current_page)
            response: Response = get(
                f"{base_url}{current_page}", headers=headers, timeout=30
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            posts = soup.find_all(class_="post-title entry-title")
            for post in posts:
                a_tag = post.find("a")
                if a_tag:
                    title = a_tag.string if a_tag.string else "N/A"
                    url = a_tag.get("href", "N/A")
                    scraped_data.append({"Title": title, "URL": url})

            logging.info("Successfully scraped page %s", current_page)

            next_button = soup.find(
                "a", {"class": "nextpostslink", "rel": "next"}
            )
            if next_button:
                current_page += 1
            else:
                logging.info("No more pages found. Exiting.")
                break

        except Exception as error:
            logging.error(
                "An error occurred while scraping page %s: %s",
                current_page,
                error,
            )

        finally:
            time.sleep(2)
    return scraped_data
