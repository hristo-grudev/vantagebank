import scrapy


class VantagebankItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
