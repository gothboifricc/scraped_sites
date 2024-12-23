import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

class FlipkartspiderSpider(scrapy.Spider):
    name = "flipkartspider"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://flipkart.com"]

    def __init__(self):
        options = Options()
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options.add_experimental_option("detach", True)
        service = Service("D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        self.driver.get(response.url)

        try:
            # Search for products
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search for Products, Brands and More']"))
            )
            search_bar.send_keys("motorola mobiles under 30000")
            search_bar.send_keys(Keys.RETURN)
            
            # Start a loop for pagination
            page_number = 1
            while True:
                # Wait for page load and extract content
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'DOjaWF gdgoEp')]"))
                )
                page_source = self.driver.page_source
                selenium_response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')
                
                # Extract product details
                parent_container = selenium_response.xpath("//*[@id='container']/div/div[3]/div[1]/div[2]")
                if not parent_container:
                    self.logger.warning("Parent container not found")
                    return

                items = parent_container.xpath(".//div[contains(@class, 'cPHDOP col-12-12')]")
                if not items:
                    self.logger.warning("No items found inside the parent container")
                    return
                
                for item in items:
                    yield {
                        'name': item.xpath(".//div[contains(@class, 'KzDlHZ')]/text()").get(default='N/A'),
                        'price': item.xpath(".//div[contains(@class, 'Nx9bqj _4b5DiR')]/text()").get(default='N/A')
                    }

                # Check for "Next" button and navigate to the next page
                try:
                    # Look for the "Next" button and click it
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//a[@class='_9QVEpD']"))
                    )
                    next_button.click()  # Click the next button

                    time.sleep(10)

                    # Wait for the next page to load
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'DOjaWF gdgoEp')]"))
                    )

                    # Log page navigation to debug
                    self.logger.info(f"Navigating to page {page_number}")
                    page_number += 1
                    
                except StaleElementReferenceException:
                    self.logger.error("Stale element reference error while clicking the 'Next' button.")
                    break
                except TimeoutException:
                    self.logger.info("No more pages to scrape.")
                    break
                except Exception as e:
                    self.logger.error(f"An error occurred while navigating to the next page: {e}")
                    break

        except TimeoutException:
            self.logger.error("Timeout occurred while waiting for elements.")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
        finally:
            self.driver.quit()

