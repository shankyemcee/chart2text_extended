import pandas as pd

df = pd.read_csv("test_index_mapping.csv")
df.sample(500).to_csv("test_index_mapping_sample.csv", index=False)
