# Importing packages
import csv
import time
import math
from selectorlib import Extractor
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from dateutil import parser as dateparser
from selenium import webdriver

# Create browser using chromedriver.exe.
# Will be used to request page data in order to scrape reviews.
browser = webdriver.Chrome()

# Create an Extractor by reading from the YAML file
# which contains amazon review layout that we will use to scrape data from HTML page.
extractor = Extractor.from_yaml_file('selectors.yml')

# Class used to perform all amazon review scraping.
class amazon_review_scraper:
    def __init__(self, amazon_site, product_asin, sleep_time=1, start_page=1, end_page=None):
        """[summary]
                Initializes instance.
        Args:
                amazon_site (string): amazon site to target. E.g. amazon.com
                product_asin (string): product number.
                sleep_time (int, optional): [description]. Defaults to 1. Time in seconds between page requests.s
                start_page (int, optional): [description]. Defaults to 1.
                end_page (int, optional): [description]. Defaults to None. If not given, we wil scrape all available pages of a product.
        """
        # Define product number
        self.product_asin = product_asin

        # Build URL from amazon site, product number.
        self.url = f"https://www.{amazon_site}/dp/product-reviews/{product_asin}?pageNumber={{}}"

        # Define sleep time betrween page requests.
        self.sleep_time = sleep_time

        # Define start and end pages of the scrape.
        self.start_page = start_page
        if (end_page == None):
            # If end page number is not given, acquire total page count.
            self.end_page = self.total_pages()
        else:
            self.end_page = min(end_page, self.total_pages())

    def total_pages(self):
        """ Acquire a number of pages we have to triverse based on the number
          of reviews we have on the product.
        Returns:
                int: number of review pages the product has.
        """
        # Make a request and get a HTML page that contains amazon review count.
        page_html = self.request_wrapper(self.url.format(1))

        # Parse HTML response into a objet with tokens.
        soup = BeautifulSoup(page_html, 'html.parser')

        # Find section that contains a number of reviews and read it into a integer
        content = soup.find_all(
            "div", {"data-hook": "cr-filter-info-review-rating-count"})
        total_reviews = int(content[0].find_all("span")[0].get_text(
            "\n").strip().split(" ")[4].replace(',', ''))

        print("Total reviews (all pages): {}".format(total_reviews), flush=True)

        # If number afer division is not a whole, round it to teh greather end.
        total_pages = math.ceil(total_reviews/10)
        return total_pages

    def scrape(self):
        """Start scraping.
        """
        print(f"Total pages: {self.end_page - self.start_page+1}", flush=True)
        print(f"Start page: {self.start_page}; End page: {self.end_page}")
        print()
        print("Started!", flush=True)

        # Create and open CSV file for given product.
        with open(f'{self.product_asin}.csv', 'w', encoding="utf-8", newline="") as outfile:
            # Create CSV fiel writer and define columns.
            writer = csv.DictWriter(outfile, fieldnames=[
                                    "title", "content", "date", "variant", "images", "verified", "author", "rating", "product", "url"], quoting=csv.QUOTE_ALL)
            # Write columns to the CSV file.
            writer.writeheader()

            # Iterate over the pages and display loading bar in terminal.
            for page in tqdm(range(self.start_page, self.end_page+1)):
                # Scape page. Pass on page number and CSV writer
                self.page_scraper(page, writer)

                # Wait before next scrape.
                time.sleep(self.sleep_time)
        print(f"Completed scraping for product {self.product_asin}!")

    def page_scraper(self, page, writer):
        """ Scrape given page into the given CSV writer.
        Args:
                page (string): HTML page.
                writer (DictWriter): CSV file writer
        """
        # Get HTML page
        url = self.url.format(page)
        page_html = self.request_wrapper(url)

        # Extract amazon reviews using extractor into a dictionary.
        data = extractor.extract(page_html)
        if data:
            for review in data['reviews']:
                if review == None:
                    continue                
                review["product"] = data["product_title"]
                review['url'] = url
                if 'verified' in review:
                    if review['verified'] != None and 'Verified Purchase' in review['verified']:
                        review['verified'] = 'Yes'
                    else:
                        review['verified'] = 'No'
                if review['rating'] != None:         
                    review['rating'] = review['rating'].split(' out of')[0]
                if review['date'] != None:
                    date_posted = review['date'].split('on ')[-1]
                if review['images']:
                    review['images'] = "\n".join(review['images'])
                review['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
                writer.writerow(review)

    def request_wrapper(self, url):
        """GET HTTP request wrapper. Makes request to given URL using chromedriver.exe.
        Args:
                url (string): Uri of teh request.

        Raises:
                Exception: Raised when CAPTCHA is encountered.

        Returns:
                [string]: HTML page as string.
        """
        # Perform HTTP GET request using Chrome browser/driver.
        browser.get(url)

        # Extract current page from the browser/driver.
        page_html = browser.page_source

        # Check if returned HTML page contains the fowlling email.
        # We are asked to fill in CAPTCHA
        if "api-services-support@amazon.com" in page_html:
            raise Exception("CAPTCHA is not bypassed")
        return page_html


# HERE WE START OUR SCRAPE
# -------------------------------------------------------------------------

# Read products.txt file to get a list of product reviews to scrape.
with open("products.txt", 'r') as urllist:

    # Iterate over teh rest of the lines which are products.
    for product_asin in urllist.readlines():
        review_scraper = amazon_review_scraper(
            amazon_site="amazon.com", product_asin=product_asin.strip(), sleep_time=1)
        review_scraper.scrape()
