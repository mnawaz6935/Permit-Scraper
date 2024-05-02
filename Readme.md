# Permit Scraper

## Overview
Permit Scraper is a sophisticated Python Selenium-based tool designed to automate the process of scraping permit-related information from a designated website. It efficiently checks the status of each permit listed in an Excel sheet, providing a streamlined solution for managing and updating permit records.

## Features
- **Automated Browsing**: Navigate through web pages and interact with web elements using Selenium.
- **Excel Integration**: Read and update Excel sheets with permit status using openpyxl.
- **Data Extraction**: Collect detailed information about permits, including status, type, owner, and related inspections.
- **Robust Error Handling**: Gracefully handles web-related errors and exceptions.
- **JSON Outputs**: Generate major outputs in JSON format for other integrations.

## Installation

To set up the Permit Scraper, follow these steps:

1. Clone the repository:
   ```shell
   git clone https://github.com/your-username/permit-scraper.git

2. Navigate to the project directory:
    ```shell
    cd permit-scraper
    ```
   
3. Install the required dependencies:
    ```shell
    pip install -r requirements.txt
    ```

## Usage
To start the scraping process, run the following command:
```shell
python src/main.py
```

