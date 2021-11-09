from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    rules = [
        Rule(
            link_extractor=LinkExtractor(),
            callback='parse_page',
            follow=False
        )
    ]

    def parse_page(self, response):
        pass
