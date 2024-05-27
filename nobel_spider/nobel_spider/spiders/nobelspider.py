import scrapy
import logging

class NobelSpider(scrapy.Spider):
    name = 'nobelspider'
    allowed_domains = ['nobelprize.org']
    
    start_urls = [
        f'https://www.nobelprize.org/nomination/archive/list.php?prize={n}&year={year}'
        for n in range(1, 6)
        for year in range(1901, 1974)
    ]

    def parse(self, response):
        self.log(f'Parsing URL: {response.url}', level=logging.INFO)
        self.log(f'Response status: {response.status}', level=logging.INFO)
        
        if response.status != 200:
            self.log(f'Failed to retrieve {response.url}', level=logging.ERROR)
            return
        
        # Extract URLs under the 'Show »' links
        urls = response.css('a.butt::attr(href)').extract()
        
        # Log the extracted URLs for debugging
        self.log(f'Extracted URLs: {urls}', level=logging.DEBUG)
        
        # Filter and join the URLs
        filtered_urls = [
            response.urljoin(url) for url in urls
            if 'show.php' in url and 'nobelprize.org' in response.urljoin(url)
        ]
        
        # Log the filtered URLs for debugging
        self.log(f'Filtered URLs: {filtered_urls}', level=logging.DEBUG)

        for url in filtered_urls:
            yield {
                'url': url
            }

# Save the spider in a file named `nobelspider.py` inside the `spiders` directory.
