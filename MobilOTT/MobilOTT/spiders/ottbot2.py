






import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from ..items import OttItem


class OttbotSpider(scrapy.Spider):
    name = 'ottbot2'

    def start_requests(self):
        page_number = 1
        page_size = 2
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

            print(listing_id, make, model, variant, year, mileage, transmission, price, ad_type, location)
            print(title, url)
            print('-*-*-*-*-*-----*-*-*-*-*-')

            # print(url)
            yield scrapy.Request(url)

    def parse(self, response):
        for lid in response.css('article').attrib['data-listing-id']:
            yield OttItem(listing_id=lid)
        for url in response.css('section#classified-listings-result').attrib['data-url']:
            yield scrapy.Request(url, self.parse_two)

    def parse_two(self, response):
        print('___________')
        resp_one = response.css('span.u-text-bold.u-block ::text').extract()
        resp_two = response.css('div.c-card span.c-chip ::text').extract()
        item = OttItem()
        item['color'] = resp_one[3]
        item['eng_cap'] = resp_one[4]
        item['city'] = resp_two[-1]
        yield item
        pass
