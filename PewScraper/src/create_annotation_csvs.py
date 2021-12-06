import pandas as pd
from ast import literal_eval

from constants import *

INCLUDE_CHARTS_WITH_CONFIRMED_PARAS = False

if __name__ == '__main__':
	cropped_meta_df = pd.read_csv(NO_DATA_DIR + CROPPED_META_FILTERED_PATH, converters={"caption": literal_eval, "croppedCaption": literal_eval})
	cropped_meta_df.set_index("id", inplace=True)

	captions = cropped_meta_df['croppedCaption']

	# Paras to annotate
	paras_to_annotate = captions.apply(lambda x: [i for i in x if not i[3]])
	paras_to_annotate = paras_to_annotate.apply(lambda x: [(i[0].replace("\xa0", " "),) + i[1:] for i in x])
	paras_to_annotate = paras_to_annotate.apply(lambda x: [(i[0].replace("&amp;", "&"),) + i[1:] for i in x])

	cropped_meta_df["num_paras"] = paras_to_annotate.apply(len)
	cropped_meta_df["paragraphs"] = paras_to_annotate.apply(lambda x: "[DIVIDER]".join([i[0] for i in x]))
	cropped_meta_df["proximities"] = paras_to_annotate.apply(lambda x: ",".join([str(i[2]) for i in x]))
	cropped_meta_df["img_url"] = cropped_meta_df["imgPath"].apply(lambda x: x.split("out/no_data/imgs/")[1])
	has_confirmed_paras = captions.apply(lambda x: any([i[3] for i in x]))

	# Overly long paragraphs
	cropped_meta_df["longest_paragraph"] = paras_to_annotate.apply(lambda x: max([len(i[0]) for i in x]) if len(x) != 0 else 0)
	cropped_meta_df["multi_paragraph"] = paras_to_annotate.apply(lambda x: any(["\n" in i[0] for i in x]))

	overly_long_paras = (cropped_meta_df["multi_paragraph"]) | (cropped_meta_df["longest_paragraph"] > 1500)
	overly_long_df = cropped_meta_df.loc[overly_long_paras & (~has_confirmed_paras), ["img_url", "paragraphs", "proximities", "num_paras"]]
	overly_long_df.to_csv(NO_DATA_DIR + "for_annotation/" + "long_annotation.csv")

	# Confirmed paras
	confirmed_meta_df = pd.read_csv(NO_DATA_DIR + CROPPED_META_FILTERED_PATH, converters={"caption": literal_eval, "croppedCaption": literal_eval})
	confirmed_meta_df.set_index("id", inplace=True)

	captions = confirmed_meta_df['croppedCaption']

	confirmed_paras = captions.apply(lambda x: [i for i in x if i[3]])
	confirmed_paras = confirmed_paras.apply(lambda x: [(i[0].replace("\xa0", " "),) + i[1:] for i in x])
	confirmed_paras = confirmed_paras.apply(lambda x: [(i[0].replace("&amp;", "&"),) + i[1:] for i in x])

	confirmed_meta_df["num_paras"] = confirmed_paras.apply(len)
	confirmed_meta_df["paragraphs"] = confirmed_paras.apply(lambda x: "[DIVIDER]".join([i[0] for i in x]))
	confirmed_meta_df["proximities"] = confirmed_paras.apply(lambda x: ",".join([str(i[2]) for i in x]))
	confirmed_meta_df["img_url"] = confirmed_meta_df["imgPath"].apply(lambda x: x.split("out/no_data/imgs/")[1])

	# Overly long confirmed paragraphs
	confirmed_meta_df["longest_paragraph"] = confirmed_paras.apply(lambda x: max([len(i[0]) for i in x]) if len(x) != 0 else 0)
	confirmed_meta_df["multi_paragraph"] = confirmed_paras.apply(lambda x: any(["\n" in i[0] for i in x]))

	overly_long_paras_confirmed = (confirmed_meta_df["multi_paragraph"]) | (confirmed_meta_df["longest_paragraph"] > 1500)
	overly_long_paras_confirmed_df = confirmed_meta_df.loc[overly_long_paras_confirmed, ["img_url", "paragraphs", "proximities", "num_paras"]]
	overly_long_paras_confirmed_df.to_csv(NO_DATA_DIR + "for_annotation/" + "long_annotation_confirmed.csv")

	# Paragraphs for annotation
	indices = (cropped_meta_df["proximities"] != "") & (~overly_long_paras)
	indices = indices & (~has_confirmed_paras)

	annotation_df = cropped_meta_df.loc[indices, ["img_url", "paragraphs", "proximities", "num_paras"]]

	pre_test = [2279, 11235, 22605]
	buckets = {
		"1_2_paras": [1, 2],
		"3_4_paras": [3, 4],
		"5_and_more_paras": [5, 6, 7, 8, 9, 10, 11],
	}

	# Remove pre-test IDs
	without_pretest = annotation_df.drop(pre_test)

	# Create files for each bucket
	for filename, num_para_range in buckets.items():
		bucket_df = without_pretest[without_pretest["num_paras"].isin(num_para_range)]
		bucket_df.to_csv(NO_DATA_DIR + "for_annotation/" + filename + ".csv")
		print(filename, len(bucket_df))

	bucket_df = without_pretest[without_pretest["num_paras"].isin([1, 2])]
	bucket_df.iloc[:500].to_csv(NO_DATA_DIR + "for_annotation/1_2_paras_first_500.csv")
	bucket_df.iloc[500:].to_csv(NO_DATA_DIR + "for_annotation/1_2_paras_rest.csv")
	annotation_df.loc[pre_test].to_csv(NO_DATA_DIR + "for_annotation/" + "pretest.csv")
