import scrapy # Imports Scrapy library for web scraping, provides tools to parse web pages and extract data
from selenium import webdriver # Imports Selenium's WebDriver module, allows controlling a web browser
from selenium.webdriver.common.by import By # Provides strategies to locate elements in the web page, such as By.ID or By.XPATH
from selenium.webdriver.common.keys import Keys # Allows simulating keyboard input, such as pressing Enter or typing text into input fields
from selenium.webdriver.support.ui import WebDriverWait # Enables waiting for specific conditions (like elements appearing) before proceeding
from selenium.webdriver.support import expected_conditions as EC # Provides pre-defined conditions like waiting for an element to become clickable
from selenium.webdriver.chrome.service import Service # Facilitates configuring & managing the ChromeDriver service required by Selenium
from scrapy.http import HtmlResponse # Converts the Selenium-rendered web page into a Scrapy-compatible response for further parsing
import time # Provides time-related functions, e.g., delays

class N50webspiderSpider(scrapy.Spider): # Defines a custom Scrapy spider named N50webspiderSpider
    name = "n50webspider"
    start_urls = ["https://finance.yahoo.com"] # Specifies the initial URL the spider will crawl

    def __init__(self): # Defines the constructor to initialize the spider.
        # Set up Selenium WebDriver
        service = Service('D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/chromedriver-win64/chromedriver.exe') # Specifies the path to the ChromeDriver executable, used to control the browser
        self.driver = webdriver.Chrome(service=service) # Initializes the Chrome WebDriver using the service object

    def parse(self, response): # Defines the parse method, Scrapy's main method for processing responses
        self.driver.get(response.url) # Opens the response.url (the starting URL) in the Selenium-controlled browser

        # Wait for the search bar to load and interact
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ybar-sbq')) # Waits up to 10 seconds for the search bar (identified by ID ybar-sbq) to appear.
        )
        search_bar.send_keys("nsei") # Types "nsei" into the search bar
        search_bar.send_keys(Keys.RETURN) # Simulates pressing the Enter key to submit the search

        # Wait for the Historical Data button (identified by an XPath) using the new element
        historical_data_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@class="yf-1e6z5da"]/a[@title="Historical Data"]'))
        )
        historical_data_button.click()

        # Wait for the table to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table[@class="table yf-j5d1ld noDl"]/tbody'))
        )

        # Captures the entire HTML source of the loaded page after interaction
        page_source = self.driver.page_source

        # Converts the Selenium-rendered HTML into a Scrapy HtmlResponse object for parsing
        selenium_response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

        # Extracts all rows (<tr> elements) from the table using XPath.
        rows = selenium_response.xpath('//table[@class="table yf-j5d1ld noDl"]/tbody/tr')

        for row in rows: # Loops through each row in the extracted table.
            yield { # Extracts specific data points (e.g., date, open, high, etc.) from each row using XPath, with a default value of 'N/A' if data is missing.
                'date': row.xpath('.//td[1]/text()').get(default='N/A'),
                'open': row.xpath('.//td[2]/text()').get(default='N/A'),
                'high': row.xpath('.//td[3]/text()').get(default='N/A'),
                'low': row.xpath('.//td[4]/text()').get(default='N/A'),
                'close': row.xpath('.//td[5]/text()').get(default='N/A'),
                'adj_close': row.xpath('.//td[6]/text()').get(default='N/A'),
                'volume': row.xpath('.//td[7]/text()').get(default='N/A'),
            }

    def closed(self, reason): # Defines a method, called when the spider finishes or is stopped.
        # Closes the Selenium browser to free resources
        self.driver.quit()

