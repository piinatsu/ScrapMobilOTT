import scrapy
from scrapy.extensions.closespider import CloseSpider
from scrapy.selector import Selector
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
        page_num = int(next_page)

        try:
            if page_num < 10:  # elapsed_time 3081 secs
                pagination_links = response.css('li.next a')
                yield from response.follow_all(pagination_links, self.parse)
            else:
                raise CloseSpider('Limit Reached')
        except AttributeError as AE:
            print("__________AE HAPPENING__________")

    def parse_listing(self, response):
        def fetch(query):
            return response.css(query).get()

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

        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")

        last_updated = (response.css('.c-section--masthead div.u-flex span.u-color-muted ::text').get()).strip().split(': ')[0]
        # response.css('.c-section--masthead div.u-flex span.u-color-muted ::text').get()
        # response.css('.c-section--masthead div.u-flex span.u-color-muted ::text')[1].get()

        if 'Diperbarui' in last_updated:
            last_updated = (response.css('.c-section--masthead div.u-flex span.u-color-muted ::text')
                            .get()).strip().split(': ')[1]
        if last_updated == '·' or last_updated is None or last_updated == '':
            last_updated = (response.css('.c-section--masthead div.u-flex span.u-color-muted ::text')
                            [1].get()).strip().split(': ')[1]

        temp_date = last_updated.split(' ')
        # for index in range(len(temp_date)):
        #     print(temp_date[index])
        match temp_date[1]:
            case "Januari":
                temp_date[1] = "January"
            case "Februari":
                temp_date[1] = "February"
            case "Maret":
                temp_date[1] = "March"
            case "Mei":
                temp_date[1] = "May"
            case "Juni":
                temp_date[1] = "June"
            case "Juli":
                temp_date[1] = "July"
            case "Agustus":
                temp_date[1] = "August"
            case "Oktober":
                temp_date[1] = "October"
            case "Desember":
                temp_date[1] = "December"
            case other:
                print("*** *** CHECK YO DATE *** ***")
        temp_date = '-'.join(temp_date)
        dt_object1 = datetime.strptime(temp_date, "%d-%B-%Y")

        url = response.url
        if "carsome=true" in url:
            carsome = 'true'
        else:
            carsome = 'false'

        seller_name = response.css('div.c-card__body h6.u-margin-bottom-xxs ::text').get()
        if seller_name is None:
            # seller_name = response.css("meta[name='ga:cad:details:dealership_name']").attrib['content']
            seller_name = response.css("meta[name='ga:cad:details:dealership_name']::attr(content)").get()
            # seller_name = Selector(text=nam).css('text').get()
            # response.css('article').attrib['data-default-line-text']

        # seller_type = (response.css('div.u-flex--wrap :nth-child(1) ::text')[5].get()).strip()
        # if seller_type == 'Dealer' or seller_type == 'Sales Agent':
        #     province = response.css('div.u-flex--wrap :nth-child(2) ::text')[0].get(),
        #     city = "",
        #     area = response.css('div.u-flex--wrap :nth-child(3) ::text')[0].get(),
        # else:
        #     province = response.css('div.u-flex--wrap :nth-child(3) ::text')[0].get(),
        #     city = response.css('div.u-flex--wrap :nth-child(4) ::text').get(),
        #     area = response.css('div.u-flex--wrap :nth-child(5) ::text').get(),

        seller_type = response.css('#stickySummary div.u-flex div.u-flex :nth-child(1) ::text')[5].get().strip()
        if seller_type is None or seller_type == '':
            seller_type = response.css('#stickySummary div.u-flex div.u-flex :nth-child(1) ::text').get().strip()

        province = response.css('#stickySummary div.u-flex div.u-flex :nth-child(2) ::text').get(),
        city = response.css('#stickySummary div.u-flex div.u-flex :nth-child(3) ::text').get(),
        area = response.css('#stickySummary div.u-flex div.u-flex :nth-child(4) ::text').get(),

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
            # 'province': fetch('div.u-flex--wrap :nth-child(2) ::text'),
            # 'city': fetch('div.u-flex--wrap :nth-child(3) ::text'),

            'seller_type': seller_type,
            'province': province,
            'city': city,
            'area': area,
            # 'seller': fetch('div.c-card__body h6.u-margin-bottom-xxs ::text'),
            'seller_name': seller_name,
            # 'seller_type': response.css("meta[name='ga:cad:details:profile_type']::attr(content)").get(),

            'fuel_type': response.css("meta[name='ga:cad:details:fuel_type']::attr(content)").get(),
            'carsome': carsome,
            'last_updated': dt_object1,
            'fetch_time': dt,
            'url': response.url
        }
