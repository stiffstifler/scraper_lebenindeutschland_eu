# "Leben in Deutschland" - Test question scraper "Leben in Deutschland"

This project is designed to assist in developing a program for preparing foreigners for the **Leben in Deutschland** exam. It includes tools for scraping, processing, and organizing exam questions, answers, and related images from the website.

## Features

- **Data Collection**: 
  - Fetches HTML content from the official website.
  - Extracts question categories, regions, and details.
  - Saves data in structured JSON format.
  
- **Data Processing**: 
  - Parses questions, answer options, and images.
  - Compiles a unified dataset with correct answers.

- **Image Downloading**: 
  - Automates downloading and storing question-related images.

## Usage

1. **Scraper**: Collect categories and HTML files from the website.
2. **Processor**: Extract and structure data into JSON files.
3. **Image Downloader**: Download images and associate them with questions.

## Example Workflow

- Combine HTML data for basic and regional questions.
- Process all questions into a sorted dataset.
- Download and store images in a designated directory.

## Requirements

- Python 3.9+
- Dependencies: `requests`, `BeautifulSoup`, `json`, `os`, `re`

## How to Run

1. Clone the repository.
   ```bash
   git clone https://github.com/stiffstifler/scraper_lebenindeutschland_eu.git  
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
3. Run the main script:
   ```bash
   python main.py
4. Processed data will be available in the "data" directory.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

