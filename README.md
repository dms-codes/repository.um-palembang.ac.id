# repository.um-palembang.ac.id
# Web Scraper for UM Palembang Repository

This Python script is a web scraper that collects information from the UM Palembang Repository website. It retrieves data about research documents and saves it to a CSV file.

## Prerequisites

- Python 3
- Required Python libraries: requests, BeautifulSoup

## Usage

1. Clone this repository to your local machine.

2. Install the required Python libraries using pip:


The script will scrape data from the UM Palembang Repository and save it to a CSV file named `data.csv`.

## Configuration

You can modify the following constants in the script to customize its behavior:

- `TIMEOUT`: Adjust the timeout for HTTP requests.
- `START_URL`: The starting URL for scraping.
- `BASE_URL`: The base URL for constructing other URLs.

## Output

The scraped data will be saved in a CSV file named `data.csv`. The CSV file will contain the following columns:

- Name
- NIM
- Judul (Title)
- Tipe Item (Item Type)
- Tahun (Year)
- Additional Information
- Uncontrolled Keywords
- Subjects
- Divisions
- Depositing User
- Date Deposited
- Last Modified
- URL
- Document File Names
- Document Links


