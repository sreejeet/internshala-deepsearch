# -*- coding: utf-8 -*-

# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime

class InternshalaItem(scrapy.Item):
    heading = scrapy.Field()
    recruiter = scrapy.Field()
    start_date = scrapy.Field()
    duration = scrapy.Field()
    stipend = scrapy.Field()
    locations = scrapy.Field()
    posted_on = scrapy.Field()
    apply_by = scrapy.Field()
    vacancies_available = scrapy.Field()
    scraped_on = scrapy.Field()
    link = scrapy.Field()
