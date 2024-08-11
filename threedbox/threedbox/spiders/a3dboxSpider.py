import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import math
from bs4 import BeautifulSoup
import re

class A3dboxSpider(scrapy.Spider):
    name = "3dboxSpider"
    allowed_domains = ["3dbox.ba"]
    start_urls = [
        "https://3dbox.ba/product-category/televizori-i-oprema/televizori/page/1/?orderby=menu_order",
        "https://3dbox.ba/product-category/televizori-i-oprema/projektori/page/1/",
        "https://3dbox.ba/product-category/televizori-i-oprema/soundbar-sistemi/page/1/",
        "https://3dbox.ba/product-category/televizori-i-oprema/ostala-tv-oprema/page/1/",
        "https://3dbox.ba/product-category/televizori-i-oprema/blu-ray-dvd-uredjaji/",
        "https://3dbox.ba/product-category/televizori-i-oprema/tv-stikovi/",
        "https://3dbox.ba/product-category/televizori-i-oprema/tv-box-uredjaji/",
        "https://3dbox.ba/product-category/televizori-i-oprema/kucno-kino/",
        "https://3dbox.ba/product-category/televizori-i-oprema/tv-nosaci-i-stalci/",
        "https://3dbox.ba/product-category/gaming/pc/",
        "https://3dbox.ba/product-category/gaming/playstation/",
        "https://3dbox.ba/product-category/gaming/gaming-oprema/",
        "https://3dbox.ba/product-category/gaming/nintendo/",
        "https://3dbox.ba/product-category/informatika/racunari/",
        "https://3dbox.ba/product-category/informatika/laptopi/",
        "https://3dbox.ba/product-category/informatika/tableti/",
        "https://3dbox.ba/product-category/informatika/monitori/",
        "https://3dbox.ba/product-category/informatika/softveri/",
        "https://3dbox.ba/product-category/informatika/racunarska-oprema/",
        "https://3dbox.ba/product-category/informatika/racunarske-komponente/",
        "https://3dbox.ba/product-category/informatika/racunarska-periferija/",
        "https://3dbox.ba/product-category/informatika/mrezna-oprema/",
        "https://3dbox.ba/product-category/informatika/skladistenje-podataka/",
        "https://3dbox.ba/product-category/informatika/printeri-i-potrosni-materijali/",
        "https://3dbox.ba/product-category/audio-i-multimedija/audio-sistemi/",
        "https://3dbox.ba/product-category/audio-i-multimedija/auto-oprema/",
        "https://3dbox.ba/product-category/audio-i-multimedija/diktafoni/",
        "https://3dbox.ba/product-category/audio-i-multimedija/foto-video-oprema/",
        "https://3dbox.ba/product-category/audio-i-multimedija/foto-aparati/",
        "https://3dbox.ba/product-category/audio-i-multimedija/gramofoni/",
        "https://3dbox.ba/product-category/audio-i-multimedija/kamere/",
        "https://3dbox.ba/product-category/audio-i-multimedija/slusalice/",
        "https://3dbox.ba/product-category/audio-i-multimedija/mikrofoni/",
        "https://3dbox.ba/product-category/audio-i-multimedija/radio-prijemnici/",
        "https://3dbox.ba/product-category/audio-i-multimedija/zvucnici/",
        "https://3dbox.ba/product-category/bijela-tehnika/frizideri/",
        "https://3dbox.ba/product-category/bijela-tehnika/sporeti/",
        "https://3dbox.ba/product-category/bijela-tehnika/mikrovalne-rerne/",
        "https://3dbox.ba/product-category/bijela-tehnika/ugradbeni-elementi/",
        "https://3dbox.ba/product-category/bijela-tehnika/nape/",
        "https://3dbox.ba/product-category/bijela-tehnika/zamrzivaci/",
        "https://3dbox.ba/product-category/bijela-tehnika/masine-za-sudje/",
        "https://3dbox.ba/product-category/bijela-tehnika/ves-masine/",
        "https://3dbox.ba/product-category/bijela-tehnika/susilice-vesa/",
        "https://3dbox.ba/product-category/bijela-tehnika/ves-masine-susilice/",
        "https://3dbox.ba/product-category/bijela-tehnika/dijelovi-i-oprema/",
        "https://3dbox.ba/product-category/bijela-tehnika/bojleri/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/blenderi/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/kafe-aparati/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/kafe-dodaci/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/kuhala/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/kuhinjske-vage/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/mikseri/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/pekaci/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/sokovnici/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/tosteri/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/pegle/",
        "https://3dbox.ba/product-category/mali-kucanski-aparati/pribor-i-dijelovi/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/cetke-i-uvijaci-za-kosu/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/cetkice-za-zube/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/depilatori-i-epilatori/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/dodatna-oprema/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/fenovi-za-kosu/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/fiksni-i-bezicni-telefoni/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/grijalice-i-ventilatori/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/ovlazivaci-vazduha/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/klima-uredjaji/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/vage/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/pegle-za-kosu/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/prociscivaci-vazduha/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/trimeri-i-brijaci/",
        "https://3dbox.ba/product-category/dom-i-licna-njega/usisivaci/",
        "https://3dbox.ba/product-category/ostalo/dronovi/",
        "https://3dbox.ba/product-category/ostalo/e-vozila/",
        "https://3dbox.ba/product-category/ostalo/elektricni-trotineti/",
        "https://3dbox.ba/product-category/ostalo/trotineti-za-djecu/",
        "https://3dbox.ba/product-category/ostalo/igracke/",
        "https://3dbox.ba/product-category/ostalo/pametni-satovi/",
        "https://3dbox.ba/product-category/ostalo/punjaci-power-bank/",
        "https://3dbox.ba/product-category/ostalo/slusalice-za-djecu/",
        "https://3dbox.ba/product-category/ostalo/gadgets/",
        # Add more category URLs as needed
    ]

    def __init__(self, *args, **kwargs):
        super(A3dboxSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.items_per_page = 12
        self.current_page = 1  # Track current page number
        self.current_url_index = 0  # Track current URL index

    def start_requests(self):
        # Generate initial URL for each category with the first page
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        
        # Wait until the page content is loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.ast-grid-common-col'))
        )

        sel = Selector(text=self.driver.page_source)
        
        # Extract the total number of items
        total_items_text = sel.css('p.woocommerce-result-count::text').get()
        if total_items_text:
            total_items = int(total_items_text.split('od')[1].split('rezultata')[0].strip())
            total_pages = math.ceil(total_items / self.items_per_page)
        else:
            total_pages = 1
        
        products = sel.css('li.ast-grid-common-col')
        for product in products:
            name = product.css('h2.woocommerce-loop-product__title::text').get()
            url = product.css('a.woocommerce-LoopProduct-link::attr(href)').get()
            img = product.css('div.wpcbm-wrapper img::attr(data-lazy-srcset)').get()

            if url:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_product,
                    meta={
                        'name': name,
                        'img': img,
                    }
                )
        
        # Pagination handling
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            # Move to the next URL
            self.current_url_index += 1
            if self.current_url_index < len(self.start_urls):
                # Reset to the first page for the new category
                next_url = self.start_urls[self.current_url_index]
                yield scrapy.Request(next_url, callback=self.parse)

    def parse_product(self, response):
    # Extract additional details from the product page
        subcategory = response.css('nav.woocommerce-breadcrumb a:nth-of-type(3)::text').get()
        category = response.css('nav.woocommerce-breadcrumb a:nth-of-type(2)::text').get()
        ean = response.css('span.sku::text').get()
        if ean:
            ean = ean.strip()
        
        # Extract price HTML and log it for debugging
        price_html = response.css('p.price').get()
        self.logger.info(f'Price HTML: {price_html}')
        if price_html:
            soup = BeautifulSoup(price_html, 'html.parser')
            current_price = soup.select_one('.woocommerce-Price-amount').get_text(strip=True) if soup.select_one('.woocommerce-Price-amount') else None
        else:
            current_price = None
        
        # Extract and clean image URL
        img_urls = response.meta['img'].split(' ')
        first_img_url = img_urls[0] if img_urls else None

        # Add the additional details to the existing data
        yield {
            'name': response.meta['name'],
            'price': current_price,
            'category': category,
            'subcategory': subcategory,
            'ean': ean,
            'url': response.url,
            'img': first_img_url,
        }

    def closed(self, reason):
        self.driver.quit()

# scrapy crawl 3dbox -O threedboxItems.json