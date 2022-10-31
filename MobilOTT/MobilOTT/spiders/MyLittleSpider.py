import scrapy
import json
from datetime import datetime
from ..items import OlxItem

class QuotesSpider(scrapy.Spider):
    name = 'myspider'
    start_urls = [
        # 'https://www.mobil123.com/mobil-dijual/'
        # 'indonesia_jabodetabek?type=used&page_number=1&page_size=5',
        # 'https://www.olx.co.id/jakarta-dki_g2000007/mobil-bekas_c198'
        'https://www.olx.co.id/api/relevance/v2/'
        'search?category=198&location=2000007&page=1&platform=web-desktop&size=40'
    ]

    def parse(self, response):

        item = OlxItem()
        data = json.loads(response.text)

        for d in data["data"]:
            print(d['title'])
            print(d["id"])
            # print(d["parameters"][0]["value_name"])
            # print(d["parameters"][1]["value_name"])
            # print(d["parameters"][2]["value_name"])
            # print(d["parameters"][3]["value_name"])
            # print(d["parameters"][4]["value"])
            # print(d["parameters"][5]["value_name"])
            # print(d["parameters"][6]["value_name"])
            # print(d["parameters"][7]["value_name"])
            # print(d["parameters"][8]["value_name"])
            # print(d["parameters"][9]["value_name"])

            make, model, variant, car_year, mileage, fuel_type, color, transmission, body_type, engine_capacity, seller_type = \
                '', '', '', '', '', '', '', '', '', '', ''

            for i in d["parameters"]:
                print('-----------***------------')
                print(i)
                match i["key"]:
                    case "make":
                        make = i["value_name"]
                    case "m_tipe":
                        model = i["value_name"]
                    case "m_tipe_variant":
                        variant = i["value_name"]
                    case "m_year":
                        car_year = i["value_name"]
                    case "mileage":
                        mileage = i["value"]
                    case "m_fuel":
                        fuel_type = i["value_name"]
                    case "m_color":
                        color = i["value_name"]
                    case "m_transmission":
                        transmission = i["value_name"]
                    case "m_body":
                        body_type = i["value_name"]
                    case "m_engine_capacity":
                        engine_capacity = i["value"]
                    case "m_seller_type":
                        seller_type = i["value_name"]

            # make = d["parameters"][0]["value_name"]
            # model = d["parameters"][1]["value_name"]
            # variant = d["parameters"][2]["value_name"]
            # car_year = d["parameters"][3]["value_name"]
            # mileage = d["parameters"][4]["value_name"]
            # fuel_type = d["parameters"][5]["value_name"]
            # color = d["parameters"][6]["value_name"]
            # transmission = d["parameters"][7]["value_name"]
            # engine_capacity = d["parameters"][8]["value_name"]
            # seller_type = d["parameters"][9]["value_name"]

            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            yield {
                "listing_id": d["id"],
                "created_at": d["created_at"],
                "title": d["title"],
                # "car_body_type": d["car_body_type"],
                # "partner_id": d["partner_id"],
                "user_type": d["user_type"],
                "price": d["price"]["value"]["raw"],
                "province": d["locations_resolved"]["ADMIN_LEVEL_1_name"],
                "city": d["locations_resolved"]["ADMIN_LEVEL_3_name"],
                "area": d["locations_resolved"]["SUBLOCALITY_LEVEL_1_name"],
                "display_date": d["display_date"],
                "fetch_time": now,

                # "make": d["parameters"][0]["value_name"],
                # "model": d["parameters"][1]["value_name"],
                # "variant": d["parameters"][2]["value_name"],
                # "car_year": d["parameters"][3]["value_name"],
                # "mileage": d["parameters"][4]["value"],
                # "fuel_type": d["parameters"][5]["value_name"],
                # "color": d["parameters"][6]["value_name"],
                # "transmission": d["parameters"][7]["value_name"],
                # "engine_capacity": d["parameters"][8]["value_name"],
                # "seller_type": d["parameters"][9]["value_name"]

                "make": make,
                "model": model,
                "variant": variant,
                "car_year": car_year,
                "mileage": mileage,
                "fuel_type": fuel_type,
                "color": color,
                "transmission": transmission,
                "engine_capacity": engine_capacity,
                "body_type": body_type,
                "seller_type": seller_type
            }

            # data = json.loads(response.text)
            # for quote in data["quotes"]:make,
            #
            #     yield {"quote": quote["text"]}
            # if data["has_next"]:
            #     self.page += 1
            #     url = f"https://quotes.toscrape.com/api/quotes?page={self.page}"
            #     yield scrapy.Request(url=url, callback=self.parse)


        # print(response.css('div._2Gr10::text').getall())
        print('---------------------------------------')


        # yield response.css

        # for frontlink in range(1,7):
        #     # keep looking for next page until page 6
        #     # yield the css
        #     yield('the list of links from all page (5 prodcut detail links each page)')
        #
        # for frontlink in response.css('the_css_that_points_to_each_detail_page')
        #     yield ('pass the links to other function')

        # for quote in response.css('div.quote'):
        #     yield {
        #         'quote': quote.css('span.text::text').get(),
        #         'author': quote.xpath('span/small/text()').get(),
        #         'tags': quote.css('a.tag::text').extract()
        #     }
        #
        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page)