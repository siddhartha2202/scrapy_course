import scrapy
from scrapy.http import Request
from follow_book_links.items import FollowBookLinksItem
from scrapy.loader import ItemLoader


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        links = [
            response.urljoin(relative_url) for relative_url in (
                response
                .xpath('//article[@class="product_pod"]/h3/a/@href')
                .extract()
            )
        ]
        for link in links:
            yield Request(url=link, callback=self.parse_book)

        next_page_url = response.urljoin(
            response
            .xpath('//li[@class="next"]/a/@href')
            .extract_first()
        )
        yield Request(url=next_page_url, callback=self.parse)

    def __get_prdt_info_xpath(self, value):
        return '//th[text()="' + value + '"]/following-sibling::td/text()'

    def __get_book_attributes(self, response):
        loader = ItemLoader(item=FollowBookLinksItem(), response=response)

        loader.add_xpath(
            field_name='title',
            xpath='//*[@id="content_inner"]/article//h1/text()'
        )
        loader.add_xpath(
            field_name='description',
            xpath='//*[@id="content_inner"]/article/p/text()'
        )
        loader.add_xpath(
            field_name='price',
            xpath='//p[@class="price_color"]/text()'
        )
        loader.add_xpath(
            field_name='image_url',
            xpath='//*[@id="product_gallery"]//img/@src'
        )
        loader.add_xpath(
            field_name='rating',
            xpath='//*[contains(@class, "star-rating")]/@class'
        )
        loader.add_xpath(
            field_name='upc',
            xpath=self.__get_prdt_info_xpath('UPC')
        )
        loader.add_xpath(
            field_name='product_type',
            xpath=self.__get_prdt_info_xpath('Product Type')
        )
        loader.add_xpath(
            field_name='product_without_tax',
            xpath=self.__get_prdt_info_xpath('Price (excl. tax)')
        )
        loader.add_xpath(
            field_name='product_with_tax',
            xpath=self.__get_prdt_info_xpath('Price (incl. tax)')
        )
        loader.add_xpath(
            field_name='tax',
            xpath=self.__get_prdt_info_xpath('Tax')
        )
        loader.add_xpath(
            field_name='availability',
            xpath=self.__get_prdt_info_xpath('Availability')
        )
        loader.add_xpath(
            field_name='number_of_reviews',
            xpath=self.__get_prdt_info_xpath('Number of reviews')
        )

        return loader.load_item()

    def parse_book(self, response):
        return self.__get_book_attributes(response)
