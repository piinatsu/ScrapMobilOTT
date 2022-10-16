import scrapy
import pandas as pd
from scrapy.extensions.closespider import CloseSpider
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from ..items import OttItem
from datetime import datetime


class OttbotSpider(scrapy.Spider):
    name = 'ottbot5'

    start_urls = ["https://www.mobil123.com/mobil-dijual/indonesia?type=used&page_number=1&page_size=5"]

    def parse(self, response):
        item = OttItem()

        # author_page_links = response.css('.author + a')
        # yield from response.follow_all(author_page_links, self.parse_author)

        # Got Five
        # response.css('article.listing::attr(data-url)')
        # 'https://www.mobil123.com/dijual/honda-jazz-rs-jawa-barat-jatimulya/8995163?carsome=true'

        # Got One
        # response.css('article.listing::attr(data-url)').get()
        # 'https://www.mobil123.com/dijual/honda-jazz-rs-jawa-barat-jatimulya/8995163?carsome=true'
        # response.css('article.listing::attr(data-url)')[4].get()

        listing_page_links = response.css('h2 > a.ellipsize[href]')
        print('------')
        print(listing_page_links)
        print(type(listing_page_links))
        yield from response.follow_all(listing_page_links, self.parse_listing)

        # pagination_links = response.css('li.next a')
        # yield from response.follow_all(pagination_links, self.parse)



        # try:


        next_page = response.css('li.next a::attr(data-page)').get()
        print("---***---")
        page_num = int(next_page)
        print(page_num)
        try:
            if page_num <= 5:
                pagination_links = response.css('li.next a')
                yield from response.follow_all(pagination_links, self.parse)
            else:
                raise CloseSpider('Limit Reached')
        except AttributeError as AE:
            print("__________AE HAPPENING__________")

        # if page_num >= 7:
        #     print("---***---")
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        # else:
        #     next_page = None
        # yield item

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

        # response.css('article').attrib['data-listing-id']
        # response.css('div.u-flex--wrap :nth-child(2) ::text')
        yield {
            'listing_id': fetch('article::attr(data-listing-id)'),
            'title': fetch('article::attr(data-title)'),
            'name': fetch('h1.listing__title ::text'),
            'price': price,
            'fetch_time': dt,
            'color': response.css('span.u-text-bold.u-block ::text')[3].get(),
            'displacement': int((response.css('span.u-text-bold.u-block ::text')[4].get()).split(' ')[0]),
            'transmission': response.css('span.u-text-bold.u-block ::text')[5].get(),
            # 'make': fetch('article::attr(date-make)'),
            'make': (response.css('h1.listing__title ::text').get()).split(' ')[1],
            'model': fetch('article::attr(data-model)'),
            'variant': fetch('article::attr(data-variant)'),
            'year': fetch('article::attr(data-year)'),
            'mileage': fetch('article::attr(data-mileage)'),
            'ad_type': fetch('article::attr(data-ad-type)'),
            'province': fetch('div.u-flex--wrap :nth-child(2) ::text'),
            'city': fetch('div.u-flex--wrap :nth-child(3) ::text'),
            'url': response.url,
            # item['province'] = response.css('div.c-card span.c-chip ::text')[-2].extract()
            # item['city'] = response.css('div.c-card span.c-chip ::text')[-1].extract()
        }
