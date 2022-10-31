# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MobilottItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class OttItem(scrapy.Item):
    name = scrapy.Field()
    listing_id = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    variant = scrapy.Field()
    year = scrapy.Field()
    mileage = scrapy.Field()
    transmission = scrapy.Field()
    price = scrapy.Field()
    ad_type = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    color = scrapy.Field()
    displacement = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    fetch_time = scrapy.Field()
    last_updated = scrapy.Field()
    carsome = scrapy.Field()
    seller_name = scrapy.Field()
    seller_type = scrapy.Field()
    fuel_type = scrapy.Field()


class OlxItem(scrapy.Item):
    listing_id = scrapy.Field()
    created_at = scrapy.Field()
    title = scrapy.Field()
    car_body_type = scrapy.Field()
    partner_id = scrapy.Field()
    user_type = scrapy.Field()
    price = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    are  = scrapy.Field()
    fetch_time = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    variant = scrapy.Field()
    car_year = scrapy.Field()
    mileage = scrapy.Field()
    fuel_type = scrapy.Field()
    color = scrapy.Field()
    transmission = scrapy.Field()
    engine_capacity = scrapy.Field()
    seller_type = scrapy.Field()
