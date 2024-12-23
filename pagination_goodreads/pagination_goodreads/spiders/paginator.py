# import scrapy
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from scrapy.http import HtmlResponse
# from selenium.webdriver.chrome.options import Options

# class PaginatorSpider(scrapy.Spider):
#     name = "paginator"
#     allowed_domains = ["goodreads.com"]
#     start_urls = ["https://goodreads.com/quotes"]

#     def __init__(self):
#         options = Options()
#         options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
#         options.add_experimental_option("detach", True)
#         service = Service("D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/chromedriver-win64/chromedriver.exe")
#         self.driver = webdriver.Chrome(service=service, options=options)

#     def parse(self, response):
#         self.driver.get(response.url)
#         seen_quotes = set()  # To store already scraped quotes
#         page_count = 0  # Counter for pages scraped

#         while page_count < 100:  # Limit to the first x pages
#             try:
#                 # Wait for quotes container to load
#                 WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'quotes')]"))
#                 )
                
#                 # Create an HtmlResponse for Scrapy to process
#                 page_source = self.driver.page_source
#                 selenium_response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')
                
#                 # Extract quotes and authors
#                 items = selenium_response.xpath("//div[contains(@class, 'quote')]")
                
#                 for item in items:
#                     quote = item.xpath(".//div[contains(@class, 'quoteText')]/text()").get(default='').strip()
#                     author = item.xpath(".//span[contains(@class, 'authorOrTitle')]/text()").get(default='').strip()
                    
#                     # Extract tags
#                     tags = item.xpath(".//div[contains(@class, 'greyText')]/a/text()").getall()
#                     tags_cleaned = ", ".join(tag.strip() for tag in tags)  # Join tags with commas
                    
#                     # Skip duplicates
#                     if quote and quote not in seen_quotes:
#                         seen_quotes.add(quote)  # Mark quote as seen
#                         yield {
#                             'quote': quote,
#                             'author': author,
#                             'tags': tags_cleaned  # Include the tags in the output
#                         }

#                 # Check if the "Next" button exists and is enabled
#                 next_button = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//a[@class='next_page']"))
#                 )
#                 next_button.click()  # Click the next button

#                 # Increment the page counter
#                 page_count += 1

#                 # Optional: Add a short wait for the next page to load
#                 time.sleep(2)

#             except Exception as e:
#                 self.logger.info(f"Stopping the spider due to an error: {e}")
#                 break  # Exit the loop if an error occurs



#     def closed(self, reason):
#         self.driver.quit()

# ------------------------------------------------------------------------- FIXED BR TAG IGNORED BELOW

import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options

class PaginatorSpider(scrapy.Spider):
    name = "paginator"
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://goodreads.com/quotes"]

    def __init__(self):
        options = Options()
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options.add_experimental_option("detach", True)
        service = Service("D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        self.driver.get(response.url)
        seen_quotes = set()  # To store already scraped quotes
        page_count = 0  # Counter for pages scraped

        while page_count < 100:  # Limit to the first x pages
            try:
                # Wait for quotes container to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'quotes')]"))
                )
                
                # Create an HtmlResponse for Scrapy to process
                page_source = self.driver.page_source
                selenium_response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')
                
                # Extract quotes and authors
                items = selenium_response.xpath("//div[contains(@class, 'quote')]")
                
                for item in items:
                    # Extract quote text, including text split by <br> tags
                    quote_parts = item.xpath(".//div[contains(@class, 'quoteText')]/text() | .//div[contains(@class, 'quoteText')]/br/following-sibling::text()").getall()
                    quote = " ".join(part.strip() for part in quote_parts).replace('\n', '').strip()  # Join parts and clean up

                    # Extract author
                    author = item.xpath(".//span[contains(@class, 'authorOrTitle')]/text()").get(default='').strip()

                    # Extract tags
                    tags = item.xpath(".//div[contains(@class, 'greyText')]/a/text()").getall()
                    tags_cleaned = ", ".join(tag.strip() for tag in tags)  # Join tags with commas

                    # Extract likes
                    likes = item.xpath(".//a[contains(@class, 'smallText') and contains(@title, 'View this quote')]/text()").get(default='').strip()

                    # Skip duplicates
                    if quote and quote not in seen_quotes:
                        seen_quotes.add(quote)  # Mark quote as seen
                        yield {
                            'quote': quote,
                            'author': author,
                            'tags': tags_cleaned,  # Include the tags in the output
                            'likes': likes  # Include the likes in the output
                        }


                # Check if the "Next" button exists and is enabled
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='next_page']"))
                )
                next_button.click()  # Click the next button

                # Increment the page counter
                page_count += 1

                # Optional: Add a short wait for the next page to load
                time.sleep(2)

            except Exception as e:
                self.logger.info(f"Stopping the spider due to an error: {e}")
                break  # Exit the loop if an error occurs



    def closed(self, reason):
        self.driver.quit()
