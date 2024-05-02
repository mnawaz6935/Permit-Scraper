from scraper import PermitScraper

if __name__ == '__main__':
    baseUrl = 'https://www.marionfl.org/agencies-departments/departments-facilities-offices/building-safety/permit-inspections'
    scraper = PermitScraper()
    scraper.start_scraping(baseUrl)
