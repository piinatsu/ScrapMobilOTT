import scrapy
from scrapy.extensions.closespider import CloseSpider
from ..items import OttItem
from datetime import datetime


class OttbotSpider(scrapy.Spider):
    name = 'ottbotwork'

    start_urls = ["https://www.mobil123.com/mobil-dijual/indonesia_jabodetabek?type=used&page_number=1&page_size=50"]

    def parse(self, response):
        item = OttItem()

        listing_page_links = response.css('h2 > a.ellipsize[href]')
        yield from response.follow_all(listing_page_links, self.parse_listing)

        next_page = response.css('li.next a::attr(data-page)').get()
        print("---***---")
        page_num = int(next_page)
        print(page_num)
        try:
            if page_num < 555: #elapsed_time 3081 mins
                pagination_links = response.css('li.next a')
                yield from response.follow_all(pagination_links, self.parse)
            else:
                raise CloseSpider('Limit Reached')
        except AttributeError as AE:
            print("__________AE HAPPENING__________")

    def parse_listing(self, response):
        def fetch(query):
            return response.css(query).get()

        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")
        try:
            price = response.css('.listing__item-price h3 ::text').extract_first()
            if price is not None:
                price = price.replace('Rp', '')
                price = price.replace('.', '')
                price = int(price)
            else:
                price = response.css('article').attrib['data-default-line-text']
                price = price.split("(")[1]
                price = price.split(")")[0]
                price = price.replace('Rp', '')
                price = price.replace('.', '')
                price = int(price)
        except AttributeError:
            print("AttributeError: Price doesn't exist")

        last_updated = ((response.css('.c-section--masthead .u-flex .u-color-muted ::text').get()).strip()).split(': ')[1]

        yield {
            'listing_id': fetch('article::attr(data-listing-id)'),
            'year': fetch('article::attr(data-year)'),
            'make': (response.css('h1.listing__title ::text').get()).split(' ')[1],
            'model': fetch('article::attr(data-model)'),
            'variant': fetch('article::attr(data-variant)'),
            'displacement': int((response.css('span.u-text-bold.u-block ::text')[4].get()).split(' ')[0]),
            'transmission': response.css('span.u-text-bold.u-block ::text')[5].get(),
            'color': response.css('span.u-text-bold.u-block ::text')[3].get(),
            'mileage': fetch('article::attr(data-mileage)'),
            'price': price,
            'city': fetch('div.u-flex--wrap :nth-child(3) ::text'),
            'last_updated': last_updated,
        }
