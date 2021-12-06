import re
import pandas as pd
from ast import literal_eval
from extract_topic import add_topic

from constants import *


def get_cropped_caption(paras):
	relevant_paras = paras[paras["is_relevant"]]
	if len(relevant_paras) > 0:
		return list(relevant_paras.apply(lambda para: (para["caption"], para["proximity"]), axis=1))
	else:
		return []


def get_paras_for_modelling(caption):
	caption = caption.replace("\xa0", " ").replace("&amp;", "&")
	caption = re.sub(r"^\d+([A-Z])", r"\1", caption)
	caption = re.sub(r"\n\d+([A-Z])", r"\n\1", caption)

	return caption


if __name__ == '__main__':
	for base_dir in [TWO_COL_DIR, MULTI_COL_DIR]:
		meta_df = pd.read_csv(base_dir + META_NO_DUPLICATES_PATH, converters={"columns": literal_eval, "caption": literal_eval})
		annotated_df = pd.read_csv(base_dir + MANUAL_CROPPED_PATH)

		# Create cropped meta df
		cropped_captions = annotated_df.groupby(by=["id"]).apply(get_cropped_caption)
		cropped_meta_df = meta_df.copy().set_index("id")
		cropped_meta_df["croppedCaption"] = cropped_captions
		cropped_meta_df.head()
		cropped_meta_df.to_csv(base_dir + CROPPED_META_PATH)

		# Prepare final CSV for modelling
		cropped_meta_df["chartType"] = cropped_meta_df["chartType"].str.replace("column", "bar")
		cropped_meta_df["caption"] = cropped_meta_df["croppedCaption"].apply(lambda x: "\n".join([i[0] for i in x]))
		cropped_meta_df = cropped_meta_df[cropped_meta_df["caption"] != ""]
		cropped_meta_df.drop("croppedCaption", axis=1, inplace=True)
		
		# Clean up captions
		cropped_meta_df["caption"] = cropped_meta_df["caption"].apply(get_paras_for_modelling)

		# Add topic
		cropped_meta_df = add_topic(cropped_meta_df)

		cropped_meta_df.to_csv(base_dir + "final_metadata.csv")
