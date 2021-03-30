import scrapy

from scrapy.loader import ItemLoader

from ..items import VantagebankItem
from itemloaders.processors import TakeFirst


class VantagebankSpider(scrapy.Spider):
	name = 'vantagebank'
	start_urls = ['https://www.vantage.bank/en/about-us/blog/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="post-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Next Page"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="banner-content-wrap"]/h1/text()').get()
		description = response.xpath('//div[@class="small-12 medium-10 medium-centered large-10 large-centered"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=VantagebankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
