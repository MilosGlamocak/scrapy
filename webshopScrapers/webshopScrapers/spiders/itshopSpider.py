import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from ..utils.priceExtract import extractPrices

class ItshopspiderSpider(scrapy.Spider):
    name = "itshopSpider"
    allowed_domains = ["itshop.ba"]
    start_urls = ["https://itshop.ba/prodavnica/page/1/?product_count=60"]

    def __init__(self, *args, **kwargs):
        super(ItshopspiderSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Uncomment for headless mode
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.current_page = 1  # Track current page number

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)

        # Wait until the page content is loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.product'))
        )

        sel = Selector(text=self.driver.page_source)
        
        # Extract products
        products = sel.css('li.product')
        for product in products:
            name = product.css('h3.product-title a::text').get()
            url = product.css('h3.product-title a::attr(href)').get()
            img = product.css('div.featured-image img::attr(src)').get()

            if url:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_product,
                    meta={
                        'name': name,
                        #'img': img,
                    }
                )
        
        # Pagination by incrementing page number in the URL
        if products:
            self.current_page += 1
            next_page_url = f"https://itshop.ba/prodavnica/page/{self.current_page}/?product_count=60"
            self.logger.info(f"Requesting next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info("No more products found, stopping pagination.")

    def parse_product(self, response):
        #subcategory = response.css('div.category a::text').get() or response.css('li.trail-item:nth-of-type(3) a::text').get()
        category = response.css('div.product_meta span.posted_in a::text').get()
        ean = response.css('span.sku::text').get()
        img = response.css('div.woocommerce-product-gallery__image img::attr("src")').get()
        if ean:
            ean = ean.strip()
        
        # Extract price HTML and log it for debugging
        price_html = response.css('p.price').get()
        self.logger.info(f'Price HTML: {price_html}')
        regularPrice = None
        salePrice = None
        if price_html:
            regularPrice = extractPrices(price_html)["regular"]
            salePrice = extractPrices(price_html)["sale"]

        '''if price_html:
            soup = BeautifulSoup(price_html, 'html.parser')
            regular_price_elem = soup.select_one('.regular')
            sale_price_elem = soup.select_one('.sale')
            
            if regular_price_elem:
                current_price = regular_price_elem.get_text(strip=True)
                sale_price = sale_price_elem.get_text(strip=True) if sale_price_elem else None
            else:
                current_price = sale_price_elem.get_text(strip=True) if sale_price_elem else None
                sale_price = None'''
        
        # Extract and clean image URL
        #img_urls = response.meta['img'].split(' ')

        # Add the additional details to the existing data
        yield {
            'shop': 'itshop',
            'name': response.meta['name'],
            'price': {'regular': regularPrice, 'sale': salePrice},
            'category': category,
            #'subcategory': subcategory,
            'ean': ean,
            'url': response.url,
            'img': img,
        }

    def closed(self, reason):
        self.driver.quit()

# scrapy crawl itshopSpider -O itshopItems.json