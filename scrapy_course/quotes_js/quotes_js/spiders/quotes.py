import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='render.html'
            )

    def parse(self, response):
        script = """
            function main(splash)
                assert(splash:go(splash.args.url))
                splash:wait(0.3)
                button = splash:select("li[class=next] a")
                splash:set_viewport_full()
                splash:wait(0.1)
                button:mouse_click()
                splash:wait(1)
                return {url = splash:url(),
                       html = splash:html()}
            end
        """
        for quote in response.xpath('//*[@class="quote"]'):
            quote_text = (
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
                'Text ': quote_text,
                'Author ': quote_author,
                'Tags ': tags
            }

        yield SplashRequest(
            url=response.url,
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': script}
        )
