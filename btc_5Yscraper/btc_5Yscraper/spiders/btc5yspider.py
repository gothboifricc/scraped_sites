import scrapy # Imports Scrapy library for web scraping, provides tools to parse web pages and extract data
from selenium import webdriver # Imports Selenium's WebDriver module, allows controlling a web browser
from selenium.webdriver.common.by import By # Provides strategies to locate elements in the web page, such as By.ID or By.XPATH
from selenium.webdriver.common.keys import Keys # Allows simulating keyboard input, such as pressing Enter or typing text into input fields
from selenium.webdriver.support.ui import WebDriverWait # Enables waiting for specific conditions (like elements appearing) before proceeding
from selenium.webdriver.support import expected_conditions as EC # Provides pre-defined conditions like waiting for an element to become clickable
from selenium.webdriver.chrome.service import Service # Facilitates configuring & managing the ChromeDriver service required by Selenium
from scrapy.http import HtmlResponse # Converts the Selenium-rendered web page into a Scrapy-compatible response for further parsing
import time # Provides time-related functions, e.g., delays
from selenium.common.exceptions import TimeoutException # Handles Selenium's timeout-related exceptions
from selenium.webdriver.chrome.options import Options # Enables specifying options for Chrome WebDriver behavior


class Btc5yspiderSpider(scrapy.Spider):
    name = "btc5yspider" # Defines the unique name of the Scrapy spider
    allowed_domains = ["finance.yahoo.com"] # Specifies the domains the spider is allowed to scrape
    start_urls = ["https://finance.yahoo.com"] # Sets the initial URL(s) to begin scraping

    def __init__(self):
        # Initializes the Selenium WebDriver with Chrome and custom options
        options = Options()
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe" # Sets the path to the Brave browser binary
        options.add_experimental_option("detach", True) # Keeps the browser open after the script completes
        service = Service("D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options) # Creates a new Chrome WebDriver instance using the specified service and options

    def parse(self, response):
        self.driver.get(response.url)  # Opens the response.url (the starting URL) in the Selenium-controlled browser

        try:
            # Wait for the search bar to load and interact
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ybar-sbq'))
            )
            search_bar.send_keys("bitcoin")  # Types "bitcoin" into the search bar
            search_bar.send_keys(Keys.RETURN)  # Simulates pressing the Enter key to submit the search

            # Wait for the Historical Data button (identified by an XPath) using the new element
            historical_data_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//li[@class="yf-1e6z5da"]/a[@title="Historical Data"]'))
            )
            historical_data_button.click() # Clicks the "Historical Data" button

            # Wait for the new dropdown button to load
            dropdown_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="tertiary-btn fin-size-small menuBtn rounded yf-15mk0m" and @title="Dec 05, 2023 - Dec 05, 2024"]'))
            )
            dropdown_button.click() # Clicks the dropdown to reveal the time period options
            self.logger.info("Dropdown button clicked successfully!") # Logs a message indicating the dropdown was clicked


            # Wait for the 5Y button to become clickable
            button_5y = WebDriverWait(self.driver, 10).until( 
                EC.element_to_be_clickable((By.XPATH, '//button[@value="5_Y"]'))
            )
            button_5y.click() # Selects the "5 Year" option to view 5 years of historical data


            # Wait for the table to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[@class="table yf-j5d1ld noDl"]/tbody'))
            )

            # Captures the entire HTML source of the loaded page after interaction
            page_source = self.driver.page_source

            # Converts the Selenium-rendered HTML into a Scrapy HtmlResponse object for parsing
            selenium_response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

            # Extracts all rows (<tr> elements) from the table using XPath
            rows = selenium_response.xpath('//table[@class="table yf-j5d1ld noDl"]/tbody/tr')

            for row in rows: # Loops through each row in the extracted table.
                yield { # Extracts specific data points (e.g., date, open, high, etc.) from each row using XPath, with a default value of 'N/A' if data is missing
                    'date': row.xpath('.//td[1]/text()').get(default='N/A'),
                    'open': row.xpath('.//td[2]/text()').get(default='N/A'),
                    'high': row.xpath('.//td[3]/text()').get(default='N/A'),
                    'low': row.xpath('.//td[4]/text()').get(default='N/A'),
                    'close': row.xpath('.//td[5]/text()').get(default='N/A'),
                    'adj_close': row.xpath('.//td[6]/text()').get(default='N/A'),
                    'volume': row.xpath('.//td[7]/text()').get(default='N/A'),
                }
        except TimeoutException as e: # Handles timeout exceptions specifically
            self.logger.error(f"TimeoutException: {e}") # Logs timeout errors
        except Exception as e: # Handles other exceptions
            self.logger.error(f"Error: {e}") # Logs generic errors
        # finally:
        #     pass
    
    def closed(self, reason): # Defines actions to take when the spider finishes or is closed
        pass # Currently, no cleanup or final actions are implemented



        
