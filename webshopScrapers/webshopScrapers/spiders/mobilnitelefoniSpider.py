import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from ..utils.priceExtract import extractPrices

class MobilnitelefonispiderSpider(scrapy.Spider):
    name = "mobilnitelefoniSpider"
    allowed_domains = ["mobilnitelefoni.ba"]
    start_urls = ["https://mobilnitelefoni.ba/shop/page/1/?yith_wcan=1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.current_page = 1

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.ast-grid-common-col'))
        )
        sel = Selector(text=self.driver.page_source)
        products = sel.css('li.ast-grid-common-col')

        for product in products:
            name = product.css('h2.woocommerce-loop-product__title::text').get()
            url = product.css('a.woocommerce-LoopProduct-link::attr(href)').get()
            img = product.css('div.wpcbm-wrapper img::attr(data-src)').get() or None

            if url:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_product,
                    meta={'name': name, 'img': img}
                )

        if products:
            self.current_page += 1
            next_page_url = f"https://mobilnitelefoni.ba/shop/page/{self.current_page}/?yith_wcan=1"
            self.logger.info(f"Requesting next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info("No more products found, stopping pagination.")

    def parse_product(self, response):
        subcategory = response.css('nav.woocommerce-breadcrumb a:nth-of-type(3)::text').get()
        category = response.css('nav.woocommerce-breadcrumb a:nth-of-type(2)::text').get()
        ean = response.css('span.sku::text').get().strip() if response.css('span.sku::text').get() else None
        
        price_html = response.css('p.price').get()
        self.logger.info(f'Price HTML: {price_html}')
        prices = extractPrices(price_html) if price_html else {}
        regularPrice = prices.get("regular")
        salePrice = prices.get("sale")

        yield {
            'shop': '3dbox',
            'name': response.meta['name'],
            'price': {"regular": regularPrice, "sale": salePrice},
            'category': category,
            'subcategory': subcategory,
            'ean': ean,
            'url': response.url,
            'img': response.meta['img']
        }

    def closed(self, reason):
        self.driver.quit()

# scrapy crawl mobilnitelefoniSpider -O scrapedItems/mobilnitelefoniItems.json
