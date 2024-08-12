import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import math

class TechnoshopSpider(scrapy.Spider):
    name = "technoshopSpider"
    allowed_domains = ["technoshop.ba"]
    currentPage = 1
    start_urls = [
        "https://technoshop.ba/proizvodi?odcijene=4.40&docijene=47999.00&prikaz=limit36&sortiranje=sortSuggested"
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.items_per_page = 36
        self.total_pages = 1
        self.current_url_index = 0  # Track current URL index

    def start_requests(self):
        if self.current_url_index < len(self.start_urls):
            url = f"{self.start_urls[self.current_url_index]}&stranica={self.currentPage}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)

        # Wait until the page content is loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.shop__item'))
        )

        sel = Selector(text=self.driver.page_source)
        
        # Extract the total number of items
        total_items_text = sel.css('div.sc__top-right h4::text').get()
        if total_items_text:
            total_items = int(total_items_text.split('od ukupno')[1].split('rezultata')[0].strip())
            self.total_pages = math.ceil(total_items / self.items_per_page)
        else:
            self.total_pages = 1
        
        products = sel.css('div.shop__item')
        for product in products:
            name = product.css('div.shop__item-top a h2::text').get()
            url = product.css('a.shop__item-image').attrib['href'] or None
            img = product.css('a.shop__item-image img').attrib['src'] or None

            # Follow the product URL to scrape additional data
            if url:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_product,
                    meta={
                        'name': name,
                        'img': img,
                    }
                )
        
        # Print for debugging
        print(f"Scraping page: {self.currentPage} of {self.total_pages} for URL: {self.start_urls[self.current_url_index]}")

        # Check if there are more pages
        if self.currentPage < self.total_pages:
            self.currentPage += 1
            next_page_url = f"{self.start_urls[self.current_url_index]}&stranica={self.currentPage}"
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            # Move to the next URL
            self.currentPage = 1
            self.current_url_index += 1
            if self.current_url_index < len(self.start_urls):
                next_url = self.start_urls[self.current_url_index]
                yield scrapy.Request(f"{next_url}&stranica={self.currentPage}", callback=self.parse)

    def parse_product(self, response):
        # Extract additional details from the product page
        category = response.css('div.breadcrumb ul li:nth-of-type(2) a::text').get()
        subcategory = response.css('div.breadcrumb ul li:nth-of-type(3) a::text').get()
        ean = response.css('div.product__title h2::text').get()
        newPrice = response.css('div.cp__np::text').get()

        if newPrice:
            newPrice = newPrice.strip()

        # Add the additional details to the existing data
        yield {
            'shop': 'technoshop',
            'name': response.meta['name'],
            'price': newPrice,
            'category': category,
            'subcategory': subcategory,
            'ean': ean,
            'url': response.url,
            'img': response.meta['img'],
        }

    def closed(self, reason):
        self.driver.quit()

# scrapy crawl technoshopSpider -O technoshopItems.json