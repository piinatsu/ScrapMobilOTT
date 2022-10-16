import scrapy
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from ..items import OttItem
import datetime


class OttbotSpider(scrapy.Spider):
    name = 'ottbot'

    def start_requests(self):

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
                listing_id = elem.get_attribute('data-listing-id')
                title = elem.get_attribute('data-title')
                url = elem.get_attribute('data-url')

                price = elem.find_element(By.CLASS_NAME, 'listing__price').text
                price = price.replace('Rp', '')
                price = price.replace('.', '')
                price = int(price)

                make = elem.get_attribute('data-make')
                model = elem.get_attribute('data-model')
                variant = elem.get_attribute('data-variant')
                year = int(elem.get_attribute('data-year'))
                mileage = int(elem.get_attribute('data-mileage'))
                transmission = elem.get_attribute('data-transmission')
                ad_type = elem.get_attribute('data-ad-type')
                location = elem.find_element(By.CSS_SELECTOR, 'div.listing__specs :nth-child(3)').text

                listing_ids.append(listing_id)
                titles.append(title)
                urls.append(url)
                prices.append(price)
                makes.append(make)
                models.append(model)
                variants.append(variant)
                years.append(year)
                mileages.append(mileage)
                transmissions.append(transmission)
                ad_types.append(ad_type)
                provinces.append(location)
                scrap_times.append(datetime.datetime.now())

                print(listing_id, make, model, variant, year, mileage, transmission, price, ad_type, location)
                print(title, url)
                print('-*-*-*-*-*-----*-*-*-*-*-')
                item['location'] = location
                print(item)
                # print(url)
                yield scrapy.Request(url)
        df_one = pd.DataFrame({
            'listing_id': listing_ids,
            'title': titles,
            'url': urls,
            'price': prices,
            'make': makes,
            'model': models,
            'variant': variants,
            'year': years,
            'mileage': mileages,
            'transmission': transmissions,
            'ad_type': ad_types,
            'province': provinces,
            'scrap_time': scrap_times,
            'color': item['color'],
            'eng_cap': item['eng_cap'],
            'city': item['city']
        })
        df_one.to_csv('ott.csv')

    def parse(self, response):
        print('___________')
        resp_one = response.css('span.u-text-bold.u-block ::text').extract()
        resp_two = response.css('div.c-card span.c-chip ::text').extract()
        url = response.url
        url = url.split("/")
        if '?' in url:
            url = url.split("?")
        print(url[5])
        print('*****')
        listing_id = url[5]

        item = OttItem()
        item['color'] = resp_one[3]
        item['eng_cap'] = resp_one[4]
        item['city'] = resp_two[-1]



        yield item
