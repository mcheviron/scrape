from scraper import scrape_data
from utils import get_num_pages, save_data, setup_logging, should_overwrite

if __name__ == "__main__":
    try:
        setup_logging()

        BASE_URL = "https://psa.wf/page/"
        HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            )
        }
        JSON_FILE = "scraped_data.json"
        CSV_FILE = "scraped_data.csv"

        if should_overwrite(JSON_FILE, CSV_FILE):
            num_pages = get_num_pages()
            scraped_data = scrape_data(num_pages, BASE_URL, HEADERS)
            save_data(scraped_data, JSON_FILE, CSV_FILE)
    except KeyboardInterrupt:
        pass
