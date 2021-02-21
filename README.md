# Amazon Rreview Scraper

Simple amazon review scraper to extract product reviews (rating, reviews, etc).

The scraper requires ChromeDriver to run and execure necessary HTTP request.
https://sites.google.com/a/chromium.org/chromedriver/

The drives is included as part of the source code that can be extracted in the current 
directory. Othwerise, download it from the link above.

It is important to place the .exe file in the root directoy of this project.

## Usage
1. Install Requirements `pip3 install -r dependencies.txt`
1. Add Amazon Product ASIN to [products.txt](products.txt) 
   Product ASIN [(Amazon Standard Identification Number)](https://www.nchannel.com/blog/amazon-asin-what-is-an-asin-number/)
   An ASIN is a 10-character alphanumeric unique identifier that is assigned to each product on amazon.
   
   **Examples**:
   * https<span>://ww</span>w.amazon.i<span>n/Grand-Theft-Auto-V-PS4/dp/<code><b><ins>B00L8XUDIC</ins></b></code>/ref=sr_1_1
   * http</span>s://ww<span>w.amazon.</span>in/Renewed-Sony-Cybershot-DSC-RX100-Digital/dp/<code><b><ins>B07XRVR9B9</ins></b></code>/ref=lp_20690678031_1_14?srs=20690678031&ie=UTF8&qid=1598553991&sr=8-14
1. Update if necessary the `amazon_site`, `sleep_time`, `start_page`, `end_page` arguments in `amazon-review-scraper.py`
1. Run `python amazon-review-scraper.py`
1. Get data from [amazon_product_asin].csv]


The solution was inspired by https://github.com/scrapehero-code/amazon-review-scraper and 
https://github.com/SinghalHarsh/amazon-product-review-scraper repositories.