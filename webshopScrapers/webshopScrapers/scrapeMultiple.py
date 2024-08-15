import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_scrapy_spider(command):
    subprocess.run(command, shell=True, check=True)

def run_scrapy_spiders():
    commands = [
        #'scrapy crawl technoshopSpider -O technoshopItems.json',
        #'scrapy crawl threedboxSpider -O threedboxItems.json',
        'scrapy crawl deltapcSpider -O deltapcItems.json',
        'scrapy crawl mintictSpider -O mintictItems.json',
    ]
    
    # Run the commands concurrently using a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=len(commands)) as executor:
        executor.map(run_scrapy_spider, commands)

def main():
    run_scrapy_spiders()

if __name__ == '__main__':
    main()
