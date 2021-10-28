import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        #  tags = (
        #  response
        #  .xpath('//*[@class="tag-item"]/a/text()')
        #  .extract()
        #  )
        #  yield {'tags': tags}
        for quote in response.xpath('//*[@class="quote"]'):
            qoute_text = (
                quote
                .xpath('.//span[@class="text"]/text()')
                .extract_first()
            )
            quote_author = (
                quote
                .xpath('.//*[@itemprop="author"]/text()')
                .extract_first()
            )
            tags = (
                quote
                .xpath('.//*[@itemprop="keywords"]/@content')
                .extract_first()
            )
            yield {
                'Text ': qoute_text,
                'Author ': quote_author,
                'Tags ': tags
            }

        next_page = (
            response
            .xpath('.//*[@class="next"]/a/@href')
            .extract_first()
        )
        absolute_next_page_url = response.urljoin(next_page)
        yield scrapy.Request(absolute_next_page_url)
