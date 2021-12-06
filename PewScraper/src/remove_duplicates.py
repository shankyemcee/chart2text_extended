import pandas as pd
from ast import literal_eval

from constants import *

if __name__ == '__main__':
	for base_dir in [TWO_COL_DIR, MULTI_COL_DIR, NO_DATA_DIR]:
		path = META_PATH
		no_duplicates_path = META_NO_DUPLICATES_PATH

		# Compare captions
		meta_df = pd.read_csv(base_dir + path, converters={"columns": literal_eval, "caption": literal_eval})
		meta_df["caption_text"] = meta_df["caption"].apply(lambda x: "\n".join([i[0] for i in x]))
		url_col_df = pd.DataFrame(meta_df[["URL", "caption_text"]])

		# Find duplicated URLs that have exactly the same caption
		url_col_df = url_col_df.drop_duplicates()
		urls_to_drop = url_col_df[url_col_df["caption_text"].duplicated()]["URL"]

		# Remove duplicates
		meta_df = pd.read_csv(base_dir + path, converters={"columns": literal_eval, "caption": literal_eval})
		meta_df = meta_df[~meta_df["URL"].isin(urls_to_drop)]
		meta_df.to_csv(index=False, path_or_buf=base_dir + no_duplicates_path)
