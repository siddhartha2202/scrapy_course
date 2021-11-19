import scrapy
import json
from scrapy.http import Request
from follow_book_links.items import ItemSelectorFactory, FollowBookLinksItem
from scrapy.utils.conf import closest_scrapy_cfg
from scrapy.utils.project import get_project_settings
import os


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def __init__(self, *a, **kw):
        super(BooksSpider, self).__init__(*a, **kw)
        self.__load_extractors()
        self.__add_extractors()

    def __get_extractor_file_path(self):
        root_directory = os.path.abspath(
            os.path.dirname(closest_scrapy_cfg())
        )
        project_name = get_project_settings().get('BOT_NAME')
        path = [root_directory, project_name, 'extractors.json']
        return '/'.join(path)

    def __load_extractors(self):
        with open(self.__get_extractor_file_path()) as json_file:
            self.extractors = json.load(json_file).get('extractors')

    def __get_prdt_info_xpath(self, value):
        return '//th[text()="' + value + '"]/following-sibling::td/text()'

    def __add_extractors(self):
        for field, value in [('upc', 'UPC'), ('product_type', 'Product Type'),
                             ('product_without_tax', 'Price (excl. tax)'),
                             ('product_with_tax', 'Price (incl. tax)'),
                             ('tax', 'Tax'), ('availability', 'Availability'),
                             ('number_of_reviews', 'Number of reviews')]:
            extractor = {
                'type': 'xpath',
                'field': field,
                'selector': self.__get_prdt_info_xpath(value)
            }
            self.extractors.append(extractor)

    def __scrape_books(self, response):
        return ItemSelectorFactory(
            response=response,
            extractors=self.extractors,
            item=FollowBookLinksItem
        ).get_item()

    def __get_next_page_url(self, response) -> str:
        next_page_url = response.urljoin(
            response
            .xpath('//li[@class="next"]/a/@href')
            .extract_first()
        )
        return next_page_url

    def __get_links_of_books(self, response):
        return (
            response.urljoin(relative_url) for relative_url in (
                response
                .xpath('//article[@class="product_pod"]/h3/a/@href')
                .extract()
            )
        )

    def parse(self, response):
        for link in self.__get_links_of_books(response):
            yield Request(url=link, callback=self.parse_book_page)

        #  yield Request(
            #  url=self.__get_next_page_url(response),
            #  callback=self.parse
        #  )

    def parse_book_page(self, response):
        yield self.__scrape_books(response)
