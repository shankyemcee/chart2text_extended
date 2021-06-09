import pandas as pd

mapping_df = pd.read_csv("../mappings/test_index_mapping.csv")

# Gold standard
def obtain_text(file_num, is_title):
	col_type, filename = file_num.split("-")

	if col_type == "two_col":
		folder = "../dataset/"
	elif col_type == "multi_col":
		folder = "../dataset/multiColumn/"
	else:
		raise Exception("Unknown folder name")

	with open(folder + ("titles_old/" if is_title else "captions_old/") + filename) as f:
		return f.read().strip()

def obtain_filename(file_num, is_img):
	col_type, filename = file_num.split("-")

	if col_type == "two_col":
		folder = "dataset/"
	elif col_type == "multi_col":
		folder = "dataset/multiColumn/"
	else:
		raise Exception("Unknown folder name")

	return folder + ("imgs/" if is_img else "data/") + filename

mapping_df["title"] = mapping_df["File_No"].apply(lambda x: obtain_text(x, True))
mapping_df["Gold Standard"] = mapping_df["File_No"].apply(lambda x: obtain_text(x, False))
mapping_df["img"] = mapping_df["File_No"].apply(lambda x: obtain_filename(x, True)).str.replace(".txt", ".png")
mapping_df["data"] = mapping_df["File_No"].apply(lambda x: obtain_filename(x, False)).str.replace(".txt", ".csv")

# Model outputs
output_files_df = pd.read_csv("output_files.csv")

def add_outputs_to_df(row):
	print(row)
	name = row["Name"]
	filename = row["Filename"]

	with open(filename) as f:
		mapping_df[name] = f.read().split("\n")

output_files_df.apply(add_outputs_to_df, axis=1)

mapping_df.index.rename("id", inplace=True)
mapping_df.to_csv("combined.csv")