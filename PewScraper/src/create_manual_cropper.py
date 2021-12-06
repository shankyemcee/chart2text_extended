import pandas as pd
from ast import literal_eval
from constants import TWO_COL_DIR, MULTI_COL_DIR, META_NO_DUPLICATES_PATH, MANUAL_CROPPED_PATH


if __name__ == '__main__':
	for base_dir in [TWO_COL_DIR, MULTI_COL_DIR]:
		meta_df = pd.read_csv(base_dir + META_NO_DUPLICATES_PATH, converters={"caption": literal_eval})

		output = []

		for i, item in meta_df.iterrows():
			item_id = item["id"]
			title = item["title"]
			subtitle = item["subtitle"]
			credits = item["credits"]
			dataPath = item["dataPath"]
			imgPath = item["imgPath"]
			chartType = item["chartType"]
			url = item["URL"]
			raw_caption = item["caption"]

			for para, proximity in raw_caption:
				output.append({
					"id": item_id,
					"title": title,
					"subtitle": subtitle,
					"credits": credits,
					"dataPath": dataPath,
					"imgPath": imgPath,
					"chartType": chartType,
					"url": url,
					"proximity": proximity,
					"caption": para,
				})

		output_df = pd.DataFrame(output)
		output_df.to_csv(index=False, path_or_buf=base_dir + MANUAL_CROPPED_PATH)
