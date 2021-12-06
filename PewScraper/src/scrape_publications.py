import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from constants import PUBLICATION_SCRAPED_PATH, PUBLICATION_CLEANED_SCRAPED_PATH


class PublicationSpider(scrapy.Spider):
	"""Scrapes all the publication links.
	"""
	name = "PublicationSpider"
	start_urls = ['https://www.pewresearch.org/publications/page/1']
	allowed_domains = ['pewresearch.org', 'people-press.org', 'journalism.org', 'pewsocialtrends.org', 'pewforum.org']

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		options = Options()
		options.headless = True
		self.driver = Chrome(options=options)
		self.wait = WebDriverWait(self.driver, 10)

	def parse(self, response, **kwargs):
		# Wait until links load
		self.driver.get(response.url)
		self.wait.until(lambda x: x.find_elements_by_css_selector(".content a"))

		# Add all publication links
		for item in self.driver.find_elements_by_css_selector(".content a"):
			link = item.get_attribute("href")

			if (link not in sr):
				sr.append(link)

		# Go to next page
		for item in self.driver.find_elements_by_css_selector("a.next"):
			link = item.get_attribute("href")
			yield response.follow(link, self.parse)


if __name__ == '__main__':
	# Run crawler
	sr = []
	process = CrawlerProcess()
	process.crawl(PublicationSpider)
	process.start()
	
	# Save publication links
	frame = pd.DataFrame(sr)
	frame.to_csv(index=False, path_or_buf=PUBLICATION_SCRAPED_PATH)

	# Remove out of domain links
	frame[frame["0"].apply(lambda x: any([i in x for i in ['www.pewresearch.org', 'www.people-press.org', 'www.journalism.org', 'www.pewsocialtrends.org', 'www.pewforum.org']]))].to_csv(index=False, path_or_buf=PUBLICATION_CLEANED_SCRAPED_PATH)

	print("complete")
