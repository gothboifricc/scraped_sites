import scrapy


class N50scraperSpider(scrapy.Spider):
    name = "n50scraper"
    start_urls = ["file:///D:/Work/Data Science & Analytics/Python/wscrap_files/yfin_n50scraper/yfin_n50scraper/project_files/page.html"]

    def parse(self, response):
        # Extracting rows from the table
        rows = response.xpath('//table[@class="table yf-j5d1ld noDl"]/tbody/tr')
        
        for row in rows:
            yield {
                'date': row.xpath('.//td[1]/text()').get(),
                'open': row.xpath('.//td[2]/text()').get(),
                'high': row.xpath('.//td[3]/text()').get(),
                'low': row.xpath('.//td[4]/text()').get(),
                'close': row.xpath('.//td[5]/text()').get(),
                'adj_close': row.xpath('.//td[6]/text()').get(),
                'volume': row.xpath('.//td[7]/text()').get(),
            }

