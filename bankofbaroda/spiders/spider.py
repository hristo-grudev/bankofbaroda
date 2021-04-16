import scrapy

from scrapy.loader import ItemLoader

from ..items import BankofbarodaItem
from itemloaders.processors import TakeFirst


class BankofbarodaSpider(scrapy.Spider):
	name = 'bankofbaroda'
	start_urls = ['https://www.bankofbaroda.ug/latest-news.htm']

	def parse(self, response):
		post_links = response.xpath('//div[@class="thumbTitle"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		if 'pdf' in response.url:
			return
		title = response.xpath('//h3/text()').get()
		description = response.xpath('//div[@class="newsDetailRow cf"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="newsDate"]/text()[normalize-space()]').get()

		item = ItemLoader(item=BankofbarodaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
