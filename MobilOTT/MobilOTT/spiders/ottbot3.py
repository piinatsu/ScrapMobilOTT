import scrapy
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from ..items import OttItem
from datetime import datetime


class OttbotSpider(scrapy.Spider):
    name = 'ottbot3'

    def start_requests(self):

        sel_urls = []
        listing_ids = []
        titles = []
        urls = []
        prices = []
        makes = []
        models = []
        variants = []
        years = []
        mileages = []
        transmissions = []
        ad_types = []
        provinces = []
        scrap_times = []

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
        #         print(sel_urls)
        #     print('-----')
        #     print(type(sel_urls))
        #     print(sel_urls)
        # yield scrapy.Request(sel_urls)


        # df_one = pd.DataFrame({
        #     'listing_id': listing_ids,
        #     'title': titles,
        #     'url': urls,
        #     'price': prices,
        #     'make': makes,
        #     'model': models,
        #     'variant': variants,
        #     'year': years,
        #     'mileage': mileages,
        #     'transmission': transmissions,
        #     'ad_type': ad_types,
        #     'province': provinces,
        #     'scrap_time': scrap_times,
        #     'color': item['color'],
        #     'eng_cap': item['eng_cap'],
        #     'city': item['city']
        # })
        # df_one.to_csv('ott.csv')


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

        # listing_ids.append(listing_id)
        # titles.append(title)
        # urls.append(url)
        # prices.append(price)
        # makes.append(make)
        # models.append(model)
        # variants.append(variant)
        # years.append(year)
        # mileages.append(mileage)
        # transmissions.append(transmission)
        # ad_types.append(ad_type)
        # provinces.append(location)
        # scrap_times.append(datetime.datetime.now())
        #
        # print(listing_id, make, model, variant, year, mileage, transmission, price, ad_type, location)
        # print(title, url)
        # print('-*-*-*-*-*-----*-*-*-*-*-')
        # item['location'] = location
        # print(item)
        # # print(url)
        # yield scrapy.Request(url)

        print('___________')
        # resp_one = response.css('span.u-text-bold.u-block ::text').extract()
        # resp_two = response.css('div.c-card span.c-chip ::text').extract()
        # url = response.url
        # url = url.split("/")
        # if '?' in url:
        #     url = url.split("?")
        # print(url[5])
        # print('*****')
        # listing_id = url[5]
        #
        # item = OttItem()
        # item['color'] = resp_one[3]
        # item['eng_cap'] = resp_one[4]
        # item['city'] = resp_two[-1]

        yield item
