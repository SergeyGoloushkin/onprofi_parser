import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from onprofiparser.items import OnprofiparserItem

class OnprofiSpider(scrapy.Spider):
    name = 'onprofi'
    allowed_domains = ['onprofi.ru']
    start_urls = ['https://onprofi.ru/category/semena/semena-ovoshchey/arbuz/',
                  'https://onprofi.ru/category/semena/semena-ovoshchey/kabachkovye/?',
                  'https://onprofi.ru/category/semena/semena-ovoshchey/kapusta/?',
                  'https://onprofi.ru/category/semena/semena-ovoshchey/kukuruza/',
                  'https://onprofi.ru/category/semena/semena-ovoshchey/ogurec/?',
                  'https://onprofi.ru/category/semena/semena-ovoshchey/redis/?',
                  'https://onprofi.ru/category/semena/semena-ovoshchey/tomat/?',
                  ]

    def parse(self, response : HtmlResponse):
        links = response.xpath("//div[contains(@class, 'name')]/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_seeds)


    def parse_seeds(self, response : HtmlResponse):
        loader = ItemLoader(item=OnprofiparserItem(), response=response)
        loader.add_xpath('name', '//h1/span/text()')
        loader.add_xpath('price', "//span[contains(@class, 'price nowrap')]//text()")
        photos_response = response.xpath("//div[contains(@class, 'col-lg-2 col-md-3 col-sm-6 col-xs-12 text-center to-cell')]/img/@src").getall()
        for photos in photos_response:
            photos = 'https://onprofi.ru' + photos
        loader.add_value('photos', photos)
        loader.add_xpath('category', "//div[contains(@class, 'sub')]/a//text()")
        loader.add_value('url', response.url)
        yield loader.load_item()

