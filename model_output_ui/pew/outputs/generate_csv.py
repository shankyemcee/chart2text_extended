import pandas as pd
import re

mapping_df = pd.read_csv("../mappings/test_index_mapping_sample.csv")
df = pd.read_csv("../dataset/metadata.csv")

# Metadata
def clean_up_title(title):
	title = title.strip()
	return re.sub(r"\s+", " ", title)

def obtain_filename(file_num):
	sub_folder = "imgs/"
	file_num = file_num.replace(".txt", ".png")

	return "pew/dataset/" + sub_folder + file_num

df["title"] = df["title"].apply(clean_up_title)
df["Gold Standard"] = df["caption"].apply(lambda x: x.strip())
df["img"] = df["File_No"].apply(obtain_filename)
df = df[["File_No", "title", "ocr-text", "img", "Gold Standard"]]


# Model outputs
original_mapping_df = pd.read_csv("../mappings/test_index_mapping.csv").set_index("File_No")
output_files_df = pd.read_csv("output_files.csv")

def add_outputs_to_df(row):
	name = row["Name"]
	filename = row["Filename"]

	with open(filename) as f:
		original_mapping_df[name] = f.read().split("\n")

output_files_df.apply(add_outputs_to_df, axis=1)

df = pd.concat([
	df,
	original_mapping_df.loc[mapping_df["File_No"]].reset_index().drop("File_No", axis=1)
], axis=1)

df.index.rename("number", inplace=True)
df.to_csv("combined.csv")
