import subprocess
from concurrent.futures import ThreadPoolExecutor
import time

def run_scrapy_spider(command):
    subprocess.run(command, shell=True, check=True)

def run_scrapy_spiders():
    commands = [
        'scrapy crawl technoshopSpider -O technoshopItems.json',
        'scrapy crawl threedboxSpider -O threedboxItems.json',
        'scrapy crawl mintictSpider -O mintictItems.json',
        'scrapy crawl itshopSpider -O itshopItems.json',
        'scrapy crawl mediamarketSpider -O mediamarketItems.json',
        'scrapy crawl deltapcSpider -O deltapcItems.json',
    ]

    '''
    # only for stronger cpu, if used, comment out "for command in commands"
    maxWorkers = 2

    # Run the commands concurrently using a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        executor.map(run_scrapy_spider, commands)
        time.sleep(5)'''
    
    for command in commands:
        run_scrapy_spider(command)

def main():
    run_scrapy_spiders()

if __name__ == '__main__':
    main()
