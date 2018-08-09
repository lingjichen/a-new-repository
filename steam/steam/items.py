# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    url = Field()
    id = Field()
    tag = Field()
    user_tag = Field()
    developers = Field()
    distributors = Field()
    release_date = Field()
    review = Field()
    review_num = Field()
    review_des = Field()
    all_review = Field()
    all_review_num = Field()
    all_review_des = Field()
    description = Field()
    description_text = Field()
    mac = Field()
    win = Field()
    linux = Field()
    discount = Field()
    original_price = Field()
    final_price = Field()
    price = Field()