import time
import pandas as pd
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

from constants import *


def process_urls(urls):
	start_time = time.time()

	# Process links
	for i, url in enumerate(urls):
		if i % 10 == 0:
			print(i, url)

			if i % 100 == 0:
				# Store meta lists
				no_data_meta_df = pd.DataFrame(no_data_meta_list)
				no_data_meta_df.to_csv(index=False, path_or_buf=NO_DATA_DIR + META_PATH)
				print("Saving", len(no_data_meta_list), "images at time", time.time() - start_time)

		process_url(url)

	# Store meta lists
	no_data_meta_df = pd.DataFrame(no_data_meta_list)
	no_data_meta_df.to_csv(index=False, path_or_buf=NO_DATA_DIR + META_PATH)
	print("Saving", len(no_data_meta_list), "images at time", time.time() - start_time)
	
	print("complete")


def process_url(url):
	global no_data_id
	# print(url)

	try:
		html = urlopen(url).read()
		soup = BeautifulSoup(html, "html5lib")
		# urlretrieve(url, "test.html")

		if not soup.body:
			return

		# Process images
		img_list = soup.select(".post-content img")

		if len(img_list) > 0:
			# Parse images
			for i, img in enumerate(img_list):
				img_url = img["src"]
				title = img["alt"] if img.has_attr("alt") else None


				# Find parent
				cur_parent = img
				skip = False

				while cur_parent.parent:
					if cur_parent.parent.has_attr("id"):
						if cur_parent.parent["id"] == "js-end-of-fact-tank-post":
							skip = True
							break

					if cur_parent.parent.has_attr("class"):
						classes = set(cur_parent.parent["class"])

						if "post-content" in classes:
							break

						elif "toc-chapter-icon" in classes:
							skip = True
							break

					cur_parent = cur_parent.parent

				if skip:
					break
				

				# Get caption elements
				caption_paras = []

				# Caption before chart
				prev_siblings = cur_parent.find_previous_siblings("p")
				num_prev_siblings = len(prev_siblings)

				for i, captionElement in enumerate(reversed(prev_siblings)):
					if captionElement and captionElement.get_text().strip() != "":
						caption = captionElement.get_text().strip()
						if caption != "":
							caption_paras.append(
								(caption, i - num_prev_siblings))

				# Caption at chart
				if cur_parent and cur_parent.get_text().strip() != "":
					caption = cur_parent.get_text().strip()
					if caption != "":
						caption_paras.append((caption, 0))

				# Caption after chart
				for i, captionElement in enumerate(cur_parent.find_next_siblings("p")):
					if captionElement and captionElement.get_text().strip() != "":
						caption = captionElement.get_text().strip()
						if caption != "":
							caption_paras.append((caption, i + 1))


				if len(caption_paras) != 0:
					process_no_data(url, title, caption_paras, img_url)
					no_data_id += 1

	except Exception as ex:
		print(ex)


def process_no_data(url, title, caption_paras, img_url):
	# Paths
	imgPath = NO_DATA_DIR + IMGS_DIR + str(no_data_id) + ".png"
	captionPath = NO_DATA_DIR + CAPTIONS_DIR + str(no_data_id) + ".txt"

	# Save data, image and captions
	urlretrieve(img_url, imgPath)
	caption_text = "\n".join([i[0] for i in caption_paras])
	with open(captionPath, "w") as f:
		f.write(caption_text)
	
	# Store metadata
	no_data_meta_list.append({
		'id': no_data_id,
		'title': title,
		'imgPath': imgPath,
		'caption': caption_paras,
		'URL': url
	})


if __name__ == '__main__':
	no_data_meta_list = []
	no_data_id = 1

	# Get scraped links
	frame = pd.read_csv(PUBLICATION_CLEANED_SCRAPED_PATH)
	sr = list(frame["0"])
	
	process_urls(sr)
