import subprocess

def run_scrapy_spiders():
    commands = [
        'cd technoshop && scrapy crawl technoshopSpider -O technoshopItems.json',
        'cd threedbox && scrapy crawl a3dboxSpider -O threedboxItems.json'
    ]

    for command in commands:
        subprocess.run(command, shell=True, check=True)

def main():

    run_scrapy_spiders()


if __name__ == '__main__':
    main()

# python scrapeMultiple.py