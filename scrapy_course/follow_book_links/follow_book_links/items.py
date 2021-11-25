# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from abc import ABC
from itemloaders.processors import TakeFirst, Compose
from itemadapter import ItemAdapter
from scrapy.loader import ItemLoader


class FollowBookLinksItem(scrapy.item.Item):
    title = scrapy.Field(output_processor=TakeFirst())

    price = scrapy.Field(output_processor=TakeFirst())

    image_url = scrapy.Field(
        input_processor=Compose(
            lambda v: v[0].replace(
                '../..',
                'http://books.toscrape.com'
            )
        ),
        output_processor=TakeFirst()
    )

    rating = scrapy.Field(
        input_processor=Compose(
            lambda v: v[0].replace(
                'star-rating ',
                ''
            )
        ),
        output_processor=TakeFirst()
    )

    description = scrapy.Field(
        output_processor=TakeFirst()
    )

    upc = scrapy.Field(
        output_processor=TakeFirst()
    )

    product_type = scrapy.Field(
        output_processor=TakeFirst()
    )

    product_without_tax = scrapy.Field(
        output_processor=TakeFirst()
    )

    product_with_tax = scrapy.Field(
        output_processor=TakeFirst()
    )

    tax = scrapy.Field(
        output_processor=TakeFirst()
    )

    availability = scrapy.Field(
        output_processor=TakeFirst()
    )

    number_of_reviews = scrapy.Field(
        output_processor=TakeFirst()
    )


class ItemFactoryAbc(ABC):
    def get_item(self):
        pass


class AdminFactoryAbc(ABC):
    def get_factory(self):
        pass


class FactoryAdministrator(AdminFactoryAbc):
    def __init__(self, factoryType, *args):
        self.factoryType = factoryType
        self.args = args

    def get_factory(self):
        if self.factoryType == 'HTML':
            return ItemHtmlFactory(*self.args)
        elif self.factoryType == 'JSON':
            return ItemJsonFactory(*self.args)


class ItemJsonFactory(ItemFactoryAbc):
    def get_item():
        pass


class ItemHtmlFactory(ItemFactoryAbc):
    def __init__(self, response, extractors, item):
        self.response = response
        self.extractors = extractors
        self.item = item

    def __add_extractors(self, loader: ItemLoader):
        for extractor in self.extractors:
            if extractor['type'] == 'xpath':
                loader.add_xpath(
                    field_name=extractor['field'],
                    xpath=extractor['selector']
                )
            elif extractor['type'] == 'css':
                loader.add_css(
                    field_name=extractor['field'],
                    css=extractor['selector']
                )
            else:
                loader.add_value(
                    field_name=extractor['field'],
                    value=extractor['selector']
                )

    def get_item(self):
        loader = ItemLoader(
            item=self.item(),
            response=self.response
        )
        self.__add_extractors(loader)

        return loader.load_item()
