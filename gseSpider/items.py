# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GsespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    GSE_num = scrapy.Field()
    Status = scrapy.Field()
    Title = scrapy.Field()
    Organism = scrapy.Field()
    ExperimentType = scrapy.Field()
    Summary = scrapy.Field()
    OverallDesign = scrapy.Field()
    Platform = scrapy.Field()
    Samples = scrapy.Field()
