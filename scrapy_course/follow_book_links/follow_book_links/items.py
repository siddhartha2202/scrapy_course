# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import TakeFirst, Compose


def __get_product_info(self, response, value):
    return (
        response
        .xpath('//th[text()="' + value + '"]/following-sibling::td/text()')
        .extract_first()
    )


class FollowBookLinksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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
