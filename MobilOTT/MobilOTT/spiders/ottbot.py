import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


class OttbotSpider(scrapy.Spider):
    name = 'ottbot'

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
            link = elem.get_attribute('data-url')
            print(link)
            yield scrapy.Request(link)

    def parse(self, response):
        print('___________')
        resp = response.css('span.u-text-bold.u-block ::text').extract()
        color = resp[3]
        eng_cap = resp[4]
        resp = response.css('div.c-card span.c-chip ::text').extract()
        province = resp[-2]
        city = resp[-1]
        yield {'color': color,
               'eng_cap': eng_cap,
               'province': province,
               'city': city}

    def parse2(self, response):
        pass
