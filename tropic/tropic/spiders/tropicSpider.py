import scrapy
import math

"""from bs4 import BeautifulSoup
import re

class TropicspiderSpider(scrapy.Spider):
    name = "tropicSpider"
    allowed_domains = ["eshop.tropic.ba"]

    def __init__(self, *args, **kwargs):
        super(TropicspiderSpider, self).__init__(*args, **kwargs)
        self.current_page = 1
        self.total_pages = math.ceil(19767/36)  # Calculate total pages dynamically based on items per page

    def start_requests(self):
        start_url = f"https://eshop.tropic.ba/?product-page={self.current_page}"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        products = response.css('li.product')

        for product in products:
            name = product.css('h2.woocommerce-loop-product__title::text').get()
            price_html = product.css('span.price').get()
            url = response.urljoin(product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href'])

            price_data = self.extract_price(price_html)

            yield {
                "name": name,
                "price": price_data.get('currentPrice'),
                "discountPrice": price_data.get('discountPrice'),
                "url": url,
            }

        if self.current_page < self.total_pages:
            self.current_page += 1
            next_page_url = f"https://eshop.tropic.ba/?product-page={self.current_page}"
            self.log(f'Following next page: {next_page_url}')
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.log('No more pages to follow.')

    def extract_price(self, price_html):
        if not price_html:
            return {}

        soup = BeautifulSoup(price_html, 'lxml')
        price_text = soup.get_text(separator=' ').strip()

        # Regular expression to extract price and currency symbol
        price_match = re.search(r'(\d+(\.\d+)?)\s*(KM)', price_text)
        
        if price_match:
            price = price_match.group(1)
            currency = price_match.group(3)
            
            # Check if there's a discount
            discount = soup.find('del')
            if discount:
                discount_price_match = re.search(r'(\d+(\.\d+)?)\s*(KM)', discount.get_text(separator=' ').strip())
                if discount_price_match:
                    discount_price = discount_price_match.group(1)
                    return {
                        'currentPrice': f"{price} {currency}",
                        'discountPrice': f"{discount_price} {currency}"
                    }
            
            return {
                'currentPrice': f"{price} {currency}"
            }
        
        return {}"""

# kod koji kao razumijem:

'''class TropicspiderSpider(scrapy.Spider):
    name = "tropicSpider"
    allowed_domains = ["eshop.tropic.ba"]
    
    # Initialize the starting page number
    def __init__(self, *args, **kwargs):
        super(TropicspiderSpider, self).__init__(*args, **kwargs)
        self.current_page = 1
        self.total_pages = math.ceil(19767/36)  # Calculate total pages dynamically based on items per page

    def start_requests(self):
        # Generate URL for the first page
        start_url = f"https://eshop.tropic.ba/?product-page={self.current_page}"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        # Extract product data
        products = response.css('li.product')

        for product in products:
            yield {
                "name": product.css('h2.woocommerce-loop-product__title::text').get(),
                "price": product.css('span.price').get(),
                "url": response.urljoin(product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']),
            }

        # Proceed to the next page if it exists
        if self.current_page < self.total_pages:
            self.current_page += 1
            next_page_url = f"https://eshop.tropic.ba/?product-page={self.current_page}"
            self.log(f'Following next page: {next_page_url}')
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.log('No more pages to follow.')'''

import scrapy
import math
import re
from bs4 import BeautifulSoup

class TropicspiderSpider(scrapy.Spider):
    name = "tropicSpider"
    allowed_domains = ["eshop.tropic.ba"]
    
    # Initialize the starting page number
    def __init__(self, *args, **kwargs):
        super(TropicspiderSpider, self).__init__(*args, **kwargs)
        self.current_page = 1
        # hardkodovao sam 19767 / 36 jer mi se nije dalo zajebavati oko toga trenutno, moram popraviti poslije
        # 19767 - toliko ima trenutno artikala na sajtu, 36 - koliko se artikala pokazuje po stranici
        self.total_pages = math.ceil(19767 / 36)  # Calculate total pages dynamically based on items per page

    def start_requests(self):
        # Generate URL for the first page
        start_url = f"https://eshop.tropic.ba/?product-page={self.current_page}"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        # Extract product data
        products = response.css('li.product')

        for product in products:
            name = product.css('h2.woocommerce-loop-product__title::text').get()
            price_html = product.css('span.price').get()
            price_info = self.extract_price(price_html)
            product_url = response.urljoin(product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href'])
            
            # Store basic product info and send request to the product page
            yield scrapy.Request(url=product_url, callback=self.parse_product_page, meta={'name': name, 'price': price_info, 'url': product_url})

        # Proceed to the next page if it exists
        if self.current_page < self.total_pages:
            self.current_page += 1
            next_page_url = f"https://eshop.tropic.ba/?product-page={self.current_page}"
            self.log(f'Following next page: {next_page_url}')
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.log('No more pages to follow.')

    def parse_product_page(self, response):
        # Retrieve basic product info from meta
        name = response.meta['name']
        price = response.meta['price']
        url = response.meta['url']
        
        # Extract GTIN from the product page
        gtin = self.extract_gtin(response)

        yield {
            "name": name,
            "price": price,
            "url": url,
            "gtin": gtin
        }

    def extract_price(self, price_html):
        if not price_html:
            return {}

        soup = BeautifulSoup(price_html, 'lxml')
        price_text = soup.get_text(separator=' ').strip()

        # Regular expression to extract price and currency symbol
        price_match = re.search(r'(\d+(\.\d+)?)\s*(KM)', price_text)
        suffix = None

        # Check if there's a suffix like "/kg" after the price
        suffix_match = re.search(r'\/\w+', price_text)
        if suffix_match:
            suffix = suffix_match.group(0)

        if price_match:
            price = price_match.group(1)
            currency = price_match.group(3)
            
            # Check if there's a discount
            discount = soup.find('del')
            if discount:
                discount_price_match = re.search(r'(\d+(\.\d+)?)\s*(KM)', discount.get_text(separator=' ').strip())
                if discount_price_match:
                    discount_price = discount_price_match.group(1)
                    return {
                        'currentPrice': f"{price} {currency}{suffix if suffix else ''}",
                        'discountPrice': f"{discount_price} {currency}{suffix if suffix else ''}"
                    }
            
            return {
                'currentPrice': f"{price} {currency}{suffix if suffix else ''}"
            }
        
        return {}

    def extract_gtin(self, response):
        # Example GTIN extraction (you need to modify this according to actual HTML structure)
        gtin = response.css('span.hwp-gtin').get().replace('<span class=\"hwp-gtin\">GTIN: <span>', '').replace('</span></span>', '')  # This is just an example
        if not gtin:
            # Try to find GTIN in another way if the first method fails
            gtin = response.xpath('//span[@class="gtin"]/text()').get()  # Another example
        return gtin
