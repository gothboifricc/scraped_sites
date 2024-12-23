import scrapy
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service 
from scrapy.http import HtmlResponse 
import time 
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.chrome.options import Options


class Btc5yspiderSpider(scrapy.Spider):
    name = "btc5yspider" 
    allowed_domains = ["finance.yahoo.com"] 
    start_urls = ["https://finance.yahoo.com"] 

    def __init__(self):
        options = Options()
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options.add_experimental_option("detach", True)
        service = Service("D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        self.driver.get(response.url)

        try:
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ybar-sbq'))
            )
            search_bar.send_keys("bitcoin")
            search_bar.send_keys(Keys.RETURN) 

            historical_data_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//li[@class="yf-1e6z5da"]/a[@title="Historical Data"]'))
            )
            historical_data_button.click()

            dropdown_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="tertiary-btn fin-size-small menuBtn rounded yf-15mk0m" and @title="Dec 05, 2023 - Dec 05, 2024"]'))
            )
            dropdown_button.click()
            self.logger.info("Dropdown button clicked successfully!")

            button_5y = WebDriverWait(self.driver, 10).until( 
                EC.element_to_be_clickable((By.XPATH, '//button[@value="5_Y"]'))
            )
            button_5y.click() 

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[@class="table yf-j5d1ld noDl"]/tbody'))
            )

            page_source = self.driver.page_source

            selenium_response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

            rows = selenium_response.xpath('//table[@class="table yf-j5d1ld noDl"]/tbody/tr')

            for row in rows:
                yield {
                    'date': row.xpath('.//td[1]/text()').get(default='N/A'),
                    'open': row.xpath('.//td[2]/text()').get(default='N/A'),
                    'high': row.xpath('.//td[3]/text()').get(default='N/A'),
                    'low': row.xpath('.//td[4]/text()').get(default='N/A'),
                    'close': row.xpath('.//td[5]/text()').get(default='N/A'),
                    'adj_close': row.xpath('.//td[6]/text()').get(default='N/A'),
                    'volume': row.xpath('.//td[7]/text()').get(default='N/A'),
                }
        except TimeoutException as e:
            self.logger.error(f"TimeoutException: {e}") 
        except Exception as e: 
            self.logger.error(f"Error: {e}")
        # finally:
        #     pass
    
    def closed(self, reason):
        pass



        
