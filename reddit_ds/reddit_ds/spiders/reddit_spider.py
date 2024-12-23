import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options


class RedditSpiderSpider(scrapy.Spider):
    name = "reddit_spider"
    allowed_domains = ["old.reddit.com"]
    start_urls = ["https://old.reddit.com"]

    def __init__(self):
        options = Options()
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options.add_experimental_option("detach", True)  # Set to True if want browser kept open for debugging
        service = Service("D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        self.driver.get(response.url)

        # Wait for the main content to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'content')]"))
        )

        # Click the "controversial" button
        contro_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li/a[@class='choice' and contains(@href, 'controversial')]"))
        )
        contro_button.click()

        # Click the dropdown and select "all time"
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown lightdrop' and contains(@onclick, 'open_menu')]"))
        )
        dropdown.click()

        all_time_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form[input[@value='all']]/a[contains(text(), 'all time')]"))
        )
        all_time_button.click()

        # Parse the page source with Scrapy
        time.sleep(2)  # Allow time for the page to load fully
        page_source = self.driver.page_source
        selenium_response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

        # Extract captions
        # captions = selenium_response.xpath("//div[@class='entry unvoted']//p[@class='title']/a[@class='title may-blank ']/text()").getall()

        captions = selenium_response.xpath("//div[@class='entry unvoted']//p[@class='title']/a[contains(@class, 'title')]/text()").getall()

        for caption in captions:
            yield {
                'caption': caption
            }

        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='nav-buttons']//span[@class='next-button']/a"))
        )
        next_button.click()  # Click the next button

        # Recursive call to parse the next page
        self.parse(HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8'))

