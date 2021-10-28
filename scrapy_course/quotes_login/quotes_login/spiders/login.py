import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token = (
            response
            .xpath('//*[@name="csrf_token"]/@value')
            .extract_first()
        )
        yield FormRequest(
            url='https://quotes.toscrape.com/login',
            callback=self.parse_after_login,
            formdata={
                'csrf_token': csrf_token,
                'username': 'foobar',
                'password': 'foobar'
            }
        )

    def parse_after_login(self, response):
        open_in_browser(response)
