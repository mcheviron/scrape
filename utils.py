import json
import logging
import os
import tempfile
from typing import Dict, List

import pandas as pd


def setup_logging() -> None:
    """
    Set up the logging configuration.

    This function initializes the logging module with a basic configuration.
    It sets the logging level to INFO and the log message format to include
    the timestamp, log level, and log message.
    Parameters:
    None

    Returns:
    None
    """

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def get_num_pages() -> int:
    """
    Prompts the user to enter the number of pages they wish to scrape and
    returns the input as an integer.
    Returns:
        int: The number of pages to scrape.

    Raises:
        None
    """

    while True:
        try:
            num_pages = int(
                input("Enter the number of pages you wish to scrape: ")
            )
            if num_pages > 0:
                return num_pages
            print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")


def should_overwrite(json_file: str, csv_file: str) -> bool:
    """
    Check if either the json_file or csv_file already exists. If any of them
    exists, prompt the user to confirm if they want to overwrite the files.
    If the user confirms, return True. Otherwise, return False.

    Parameters:
    - json_file (str): The path to the json file.
    - csv_file (str): The path to the csv file.

    Returns:
    - bool: True if the user confirmed to overwrite the files, False otherwise.
    """

    if os.path.isfile(json_file) or os.path.isfile(csv_file):
        overwrite = input(
            "Files already exist. Do you want to overwrite them? (y/n): "
        )
        return overwrite.lower() == "y"
    return True


def save_data(
    scraped_data: List[Dict[str, str]], json_file: str, csv_file: str
) -> None:
    """
    Save scraped data to JSON and CSV files.

    Parameters:
        scraped_data (List[Dict[str, str]]): The scraped data to be saved.
        json_file (str): The path to the JSON file where the data will be
        saved.
        csv_file (str): The path to the CSV file where the data will be saved.

    Returns:
        None

    Notes:
        - If the scraped_data list is not empty, the function saves the data
        to temporary files, converts it to a DataFrame,
        and then saves it to the specified JSON and CSV files.

        - If the scraped_data list is empty, the function logs a warning
          message indicating that no data was scraped and the original files
          remain untouched.
    """

    if scraped_data:
        with tempfile.NamedTemporaryFile(
            "w", delete=False
        ) as temp_json, tempfile.NamedTemporaryFile(
            "w", delete=False, suffix=".csv"
        ) as temp_csv:
            json.dump(scraped_data, temp_json)
            temp_json.close()

            df = pd.DataFrame(scraped_data)
            df.to_csv(temp_csv.name, index=False)
            temp_csv.close()

            os.replace(temp_json.name, json_file)
            os.replace(temp_csv.name, csv_file)

            logging.info("Scraping completed. Data saved.")
    else:
        logging.warning("No data scraped. Original files remain untouched.")
