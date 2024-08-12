from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from threedbox.threedbox.spiders.a3dboxSpider import A3dboxSpider

from technoshop.technoshop.spiders.technoshopSpider import TechnoshopSpider

configure_logging()

# Set output settings for JSON file
settings = get_project_settings()
settings.set('FEEDS', {
    'scrapedItems.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 4,
    },
})

runner = CrawlerRunner(settings)

runner.crawl(A3dboxSpider)
runner.crawl(TechnoshopSpider)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()  # the script will block here until all crawling jobs are finished
