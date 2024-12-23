import scrapy

class WikispiderSpider(scrapy.Spider):
    name = "wikispider"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/World_War_II_casualties"]

    def parse(self, response):
        # Extracting the table rows
        rows = response.xpath('//table[contains(@class, "wikitable")]//tr')

        # Skip the first row (header row)
        for row in rows[1:]:
            columns = row.xpath('.//td')

            # Check if the row has at least 9 columns
            if len(columns) >= 9:
                # Extracting the country name from the <a> tag inside the <td> (with the flag)
                country = row.xpath('.//td/b//a//text()').get(default='').strip()

                data = {
                    'country': country,  # Extracted country name
                    'total_pop (01_01_1939)': columns[1].xpath('.//text()').get(default='').strip(),
                    'military deaths (all_causes)': columns[2].xpath('.//text()').get(default='').strip(),
                    'civilian deaths to military activity and crimes against humanity': columns[3].xpath('.//text()').get(default='').strip(),
                    'civilian deaths due to war related famine and disease': columns[4].xpath('.//text()').get(default='').strip(),
                    'total deaths': columns[5].xpath('.//text()').get(default='').strip(),
                    # 'deaths as percentage of 1939 population': columns[5].xpath('.//text()').get(default='').strip(),
                    'average death percent': columns[7].xpath('.//text()').get(default='').strip(),
                    'military wounded': columns[8].xpath('.//text()').get(default='').strip(),
                }
                yield data
