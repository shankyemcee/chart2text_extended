import time
import re
from io import BytesIO
from PIL import Image
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from constants import *


# Selenium settings
options = Options()
options.add_argument('--disable-notifications')
options.add_argument("headless")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = Chrome(options=options)


def process_urls(urls):
	# Process links
	for url in urls:
		process_url(url)

	# Store meta lists
	two_col_meta_df = pd.DataFrame(two_col_meta_list)
	two_col_meta_df.to_csv(index=False, path_or_buf=TWO_COL_DIR + META_PATH)

	multi_col_meta_df = pd.DataFrame(multi_col_meta_list)
	multi_col_meta_df.to_csv(index=False, path_or_buf=MULTI_COL_DIR + META_PATH)

	print("complete")

def process_url(url):
	global two_col_id, multi_col_id
	print(url)

	try:
		html = urlopen(url).read()
		soup = BeautifulSoup(html, "html5lib")
		# urlretrieve(url, "test.html")

		if not soup.body:
			return

		# Process tables
		table_list = soup.select(".pew-chart")

		if len(table_list) > 0:
			print("TABLES:", len(table_list))

			# Take a screenshot of the whole page to be cropped
			full_img = take_full_screenshot(url)

			# Parse tables
			for i, table in enumerate(table_list):
				# Convert HTML table to Dataframe
				dfs = pd.read_html(str(table))[0]


				# Get image
				parent_id = table.parent.parent["id"]
				img = crop_to_img(full_img, parent_id)


				# Get chart type
				script_text = table.parent.parent.find_next_sibling("script").string
				high_chart_type = re.search(r"\"chart\":\{\"type\":\"(\w+)\"[,\}]", script_text).group(1)
				chart_type = high_chart_type


				# Get title
				titleElement = table.parent.parent.find("h3")
				if titleElement is None:
					titleElement = table.parent.parent.find_previous_sibling(["h2", "h3", "h4", "section"])

				if titleElement is None:
					titleElement = table.parent.parent.parent.find_previous_sibling(["h2", "h3", "h4", "section"])

				title = titleElement.get_text().strip() if titleElement else None


				# Get subtitle
				subtitle = None

				try:
					subtitleElements = driver.find_elements_by_css_selector(f"#{parent_id} .highcharts-subtitle tspan")
					subtitle = " ".join([element.text for element in subtitleElements])
				except:
					pass
				

				# Get credits
				credits = None

				try:
					creditsElement = driver.find_elements_by_css_selector(f"#{parent_id} .chart_credits")
					credits = "\n".join([element.text for element in creditsElement])
				except:
					pass
				

				# Get caption elements
				caption_paras = []

				# Caption before chart
				prev_siblings = table.parent.parent.find_previous_siblings("p")
				num_prev_siblings = len(prev_siblings)

				for i, captionElement in enumerate(reversed(prev_siblings)):
					if captionElement and captionElement.get_text().strip() != "":
						caption = captionElement.get_text().strip()
						if caption != "":
							caption_paras.append((caption, i - num_prev_siblings))

				# Caption after chart
				for i, captionElement in enumerate(table.parent.parent.find_next_siblings("p")):
					if captionElement and captionElement.get_text().strip() != "":
						caption = captionElement.get_text().strip()
						if caption != "":
							caption_paras.append((caption, i + 1))


				if len(caption_paras) != 0:
					print(title)

					# Two col
					if (dfs.shape[1] == 2):
						print("TWO_COL:", two_col_id)
						process_two_col_data(url, title, subtitle, caption_paras, dfs, img, chart_type, credits, script_text)
						two_col_id += 1

					# Multi col
					else:
						print("MULTI_COL:", multi_col_id)
						process_multi_col_data(url, title, subtitle, caption_paras, dfs, img, chart_type, credits, script_text)
						multi_col_id += 1

	except Exception as ex:
		print(ex)


def take_full_screenshot(url):
	# Open the webpage
	driver.get(url)
	S = lambda X: driver.execute_script("return document.body.parentNode.scroll" + X)
	driver.set_window_size(S("Width"), S("Height"))

	# Adjust if the charts don't get fully loaded
	time.sleep(2)

	# Saves a screenshot of entire page
	screenshot_bytes = driver.get_screenshot_as_png()

	# Uses PIL library to open the image in memory
	return Image.open(BytesIO(screenshot_bytes))


def crop_to_img(full_img, parent_id):
	element = driver.find_element_by_css_selector(f"#{parent_id} #chart")
	location = element.location
	size = element.size

	left = location['x']
	top = location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']

	return full_img.crop((left, top, right, bottom))


def process_two_col_data(url, title, subtitle, caption_paras, dFrame, img, chart_type, credits, script_text):
	# Paths
	dataPath = TWO_COL_DIR + DATA_DIR + str(two_col_id) + ".csv"
	imgPath = TWO_COL_DIR + IMGS_DIR + str(two_col_id) + ".png"
	captionPath = TWO_COL_DIR + CAPTIONS_DIR + str(two_col_id) + ".txt"


	# Save data, image and captions
	dFrame.to_csv(index=False, path_or_buf=dataPath)
	img.save(imgPath)

	caption_text = "\n".join([i[0] for i in caption_paras])
	with open(captionPath, "w") as f:
		f.write(caption_text)


	# Store metadata
	xAxis = dFrame.columns[0]
	yAxis = dFrame.columns[1]

	two_col_meta_list.append({
		'id': two_col_id,
		'title': title,
		'subtitle': subtitle,
		'credits': credits,
		'script': script_text,
		'dataPath': dataPath,
		'imgPath': imgPath,
		'caption': caption_paras,
		'chartType': chart_type,
		'xAxis': xAxis,
		'yAxis': yAxis,
		'URL': url
	})

def process_multi_col_data(url, title, subtitle, caption_paras, dFrame, img, chart_type, credits, script_text):
	# Paths
	dataPath = MULTI_COL_DIR + DATA_DIR + str(multi_col_id) + ".csv"
	imgPath = MULTI_COL_DIR + IMGS_DIR + str(multi_col_id) + ".png"
	captionPath = MULTI_COL_DIR + CAPTIONS_DIR + str(multi_col_id) + ".txt"
	
	# Save data, image and captions
	dFrame.to_csv(index=False, path_or_buf=dataPath)
	img.save(imgPath)

	caption_text = "\n".join([i[0] for i in caption_paras])
	with open(captionPath, "w") as f:
		f.write(caption_text)

	# Store metadata
	columns = []
	for row in dFrame.columns:
		columns.append(row)

	multi_col_meta_list.append({
		'id': multi_col_id,
		'title': title,
		'subtitle': subtitle,
		'credits': credits,
		'script': script_text,
		'dataPath': dataPath,
		'imgPath': imgPath,
		'caption': caption_paras,
		'chartType': chart_type,
		'columns': columns,
		'URL': url
	})


if __name__ == '__main__':
	two_col_meta_list = []
	multi_col_meta_list = []

	two_col_id = 1
	multi_col_id = 1

	# Get scraped links
	frame = pd.read_csv(PEW_CHART_LINKS_PATH)
	sr = list(frame["0"])
	
	process_urls(sr)
