import scrapy
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from ..items import OttItem
from datetime import datetime


class OttbotSpider(scrapy.Spider):
    name = 'ottbot4'

    def start_requests(self):

        for x in range(2):

            item = OttItem()
            page_number = x
            page_size = 5
            ott_url = f"https://www.mobil123.com/mobil-dijual/indonesia?" \
                      f"type=used&sort=modification_date_search.desc&" \
                      f"page_number={page_number}&page_size={page_size}"
            options = ChromeOptions()
            options.headless = True
            driver = Chrome(options=options)
            driver.get(ott_url)

            el = driver.find_elements(By.CLASS_NAME, 'listing')
            for elem in el:
                the_url = elem.get_attribute('data-url')
                yield scrapy.Request(the_url)


    def parse(self, response):

        item = OttItem()
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
        except AttributeError as atrer:
            print("AttributeError: Price doesn't exist")

        displacement = response.css('span.u-text-bold.u-block ::text')[4].extract()
        displacement = displacement.split(' ')
        displacement = int(displacement[0])

        now = datetime.now()
        # dd/mm/YY H:M:S
        dt = now.strftime("%d/%m/%Y %H:%M:%S")

        item['listing_id'] = response.css('article').attrib['data-listing-id']
        item['title'] = response.css('article').attrib['data-title']
        item['url'] = response.url
        item['price'] = price
        item['make'] = response.css('article').attrib['data-make']
        item['model'] = response.css('article').attrib['data-model']
        item['variant'] = response.css('article').attrib['data-variant']
        item['year'] = response.css('article').attrib['data-year']
        item['mileage'] = response.css('article').attrib['data-mileage']
        item['ad_type'] = response.css('article').attrib['data-ad-type']
        item['province'] = response.css('div.c-card span.c-chip ::text')[-2].extract()
        item['city'] = response.css('div.c-card span.c-chip ::text')[-1].extract()
        item['color'] = response.css('span.u-text-bold.u-block ::text')[3].extract()
        item['displacement'] = displacement
        item['transmission'] = response.css('span.u-text-bold.u-block ::text')[5].extract()
        item['name'] = response.css('h1.listing__title ::text').extract_first()
        item['fetch_date'] = dt

        print('___________')
        print(item)
        print(type(item))

        yield item
