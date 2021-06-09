import pandas as pd

multi_df = pd.read_csv("original_dataset_mapping_multi_col.csv", index_col=0)
two_df = pd.read_csv("original_dataset_mapping_two_col.csv", index_col=0)
test_df = pd.read_csv("test_index_mapping.csv")

def obtain_original_filename(file_num):
	col_type, filename = file_num.split("-")

	if col_type == "two_col":
		df = two_df
	elif col_type == "multi_col":
		df = multi_df
	else:
		raise Exception("Unknown folder name")

	id = int(filename.split(".txt")[0])
	return df.loc[id, "File_No"]

test_df["Original_File_No"] = test_df["File_No"].apply(obtain_original_filename)
test_df.to_csv("original_test_index_mapping.csv", index=False)
