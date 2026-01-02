# main.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


def run():
    # Ensure output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')

    # Set settings module
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'wwm.settings')

    process = CrawlerProcess(get_project_settings())
    process.crawl('wwm_spider')
    process.start()


if __name__ == '__main__':
    run()