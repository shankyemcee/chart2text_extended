import pandas as pd

mapping_df = pd.read_csv("../mappings/test_index_mapping.csv").reset_index().set_index("File_No")
test_mapping_df = pd.read_csv("../mappings/sorted_test_mapping.csv")

with open("chart2text_unordered.txt") as f:
	model_outputs = f.read().split("\n")

mapping_df["captions"] = ""
mapping_df.loc[test_mapping_df["sorted_split_mapping"], "captions"] = model_outputs[:-1]
mapping_df.sort_values(by="index", inplace=True)
output = "\n".join(list(mapping_df["captions"]))

with open("chart2text.txt", "w+") as f:
	f.write(output)
