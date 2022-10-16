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
    fetch_date = scrapy.Field()
