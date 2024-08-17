import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from urllib.parse import urljoin
from ..utils.priceExtract import extractPrices
import re

class MediamarketspiderSpider(scrapy.Spider):
    name = "mediamarketSpider"
    allowed_domains = ["mediamarket.rs.ba"]
    start_urls = ["https://www.mediamarket.rs.ba/index.php/artikli?limit=200&start=0"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, *args, **kwargs):
        super(MediamarketspiderSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Use headless mode for performance
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.current_page = 0  # Track current page number
        self.total_products = None

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        try:
            self.driver.get(response.url)

            # Wait until the page content is loaded
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product'))
            )

            sel = Selector(text=self.driver.page_source)
            
            # Extract the total number of products if not already done
            if self.total_products is None:
                product_number_text = sel.css('div.floatright.display-number span::text').get()
                if product_number_text:
                    match = re.search(r'od\s+(\d+)', product_number_text)
                    if match:
                        self.total_products = int(match.group(1))
                        self.logger.info(f"Total products: {self.total_products}")
            
            # Extract products
            products = sel.css('div.product')
            for product in products:
                name = product.css('div.vm-product-descr-container-1 h2 a::text').get()
                relative_url = product.css('div.vm-product-descr-container-1 h2 a::attr(href)').get()
                img = product.css('img.browseProductImage::attr(src)').get()

                if relative_url:
                    absolute_url = urljoin(response.url, relative_url)
                    yield scrapy.Request(
                        url=absolute_url,
                        callback=self.parse_product,
                        meta={
                            'name': name,
                            'img': img,
                        }
                    )

            # Calculate the total number of pages and stop if the threshold is reached
            products_per_page = 200
            max_pages = (self.total_products // products_per_page) + (1 if self.total_products % products_per_page > 0 else 0)

            if products and (self.current_page // products_per_page) < max_pages:
                self.current_page += products_per_page
                next_page_url = f"https://www.mediamarket.rs.ba/index.php/artikli?limit=200&start={self.current_page}"
                self.logger.info(f"Requesting next page: {next_page_url}")
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                self.logger.info("Reached the end or no more products found, stopping pagination.")
        except Exception as e:
            self.logger.error(f"Error in parse method: {e}")

    def parse_product(self, response):
        try:
            subcategory = response.css('li.breadcrumb-item:nth-of-type(3) a span::text').get() or None
            category = response.css('li.breadcrumb-item:nth-of-type(2) a span::text').get()
            ean = response.css('span.sku::text').get() or None
            img = response.css('div.main-image a::attr("href")').get()

            if ean:
                ean = ean.strip()

            # Extract price HTML and log it for debugging
            price_html = response.css('div.PricesalesPrice, span.price-crossed').getall()
            prices_string = " ".join(price_html)
            self.logger.info(f'Price HTML: {price_html}')
            regularPrice = None
            salePrice = None
            if price_html:
                prices = extractPrices(prices_string)
                regularPrice = prices.get("regular")
                salePrice = prices.get("sale")

            # Add the additional details to the existing data
            yield {
                'shop': 'mediamarket',
                'name': response.meta['name'],
                'price': {'regular': regularPrice, 'sale': salePrice},
                'category': category,
                'subcategory': subcategory,
                'ean': ean,
                'url': response.url,
                'img': img,
            }
        except Exception as e:
            self.logger.error(f"Error in parse_product method: {e}")

    def closed(self, reason):
        self.driver.quit()

# Command to run the spider:
# scrapy crawl mediamarketSpider -O mediamarketItems.json
