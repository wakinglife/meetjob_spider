# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    job_title = scrapy.Field()
    job_tag = scrapy.Field()
    company_name = scrapy.Field()
    salary_max = scrapy.Field()
    salary_min = scrapy.Field()
    salary_currency = scrapy.Field()
    salary_length = scrapy.Field()
    skill_cata_tag = scrapy.Field()
    jd = scrapy.Field()
    url = scrapy.Field()
