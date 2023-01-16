import scrapy
from scrapy.http import HtmlResponse
from books_scrape.items import BooksScrapeItem


class LabirintRuSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://labirint.ru/best/sale/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//div[@class='pagination-next']/a[@class='pagination-next__text']/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

        book_link = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in book_link:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        book_name = response.xpath("//h1/text()").get()
        book_url = response.url
        book_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        book_currency = response.xpath("//span[@class='buying-pricenew-val-currency']/text()").get()
        book_ISBN = response.xpath("//div[@class='isbn']/text()").get()
        yield BooksScrapeItem(
            name=book_name,
            url=book_url,
            price=book_price,
            currency=book_currency,
            ISBN=book_ISBN
        )
