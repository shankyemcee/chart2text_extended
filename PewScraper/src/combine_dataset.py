import pandas as pd
import os

from constants import *


if __name__ == "__main__":
    # Import files
    simple_df = pd.read_csv(NO_DATA_DIR + "simple_metadata.csv")
    complex_df = pd.read_csv(NO_DATA_DIR + "complex_metadata.csv")

    two_meta_df = pd.read_csv(TWO_COL_DIR + "final_metadata.csv")
    two_meta_df = two_meta_df.set_index("id").drop(9).reset_index()
    two_meta_df["id"] = two_meta_df["id"].apply(lambda x: f"two_col-{x}")
    two_meta_df["complexity"] = "simple"
    two_meta_df["chartType"] = two_meta_df["chartType"].apply(lambda x: "bar" if x == "column" else x)
    two_meta_df = two_meta_df[simple_df.columns]

    multi_meta_df = pd.read_csv(MULTI_COL_DIR + "final_metadata.csv")
    multi_meta_df = multi_meta_df.set_index("id").drop(9).reset_index()
    multi_meta_df["id"] = multi_meta_df["id"].apply(lambda x: f"multi_col-{x}")
    multi_meta_df["complexity"] = "complex"
    multi_meta_df["chartType"] = multi_meta_df["chartType"].apply(lambda x: "bar" if x == "column" else x)
    multi_meta_df = multi_meta_df[complex_df.columns]

    # Combine the two_col, multi_col and no_data
    simple_df = pd.concat([two_meta_df, simple_df]).set_index("id").reset_index().reset_index()
    simple_df.rename(columns={"index": "id", "id": "old_id"}, inplace=True)
    simple_df["id"] = simple_df["id"] + 1
    simple_df["imgPath"] = simple_df["id"].apply(lambda x: f"imgs/{x}.png")
    simple_df["dataPath"] = simple_df["id"].apply(lambda x: f"data/{x}.txt")
    simple_df["bboxesPath"] = simple_df["id"].apply(lambda x: f"bboxes/{x}.json")
    simple_df.to_csv("../dataset/metadata.csv", index=False)

    simple_df.info()


    complex_df = pd.concat([multi_meta_df, complex_df]).set_index("id").reset_index().reset_index()
    complex_df.rename(columns={"index": "id", "id": "old_id"}, inplace=True)
    complex_df["id"] = complex_df["id"] + 1
    complex_df["imgPath"] = complex_df["id"].apply(lambda x: f"multiColumn/imgs/{x}.png")
    complex_df["dataPath"] = complex_df["id"].apply(lambda x: f"multiColumn/data/{x}.txt")
    complex_df["bboxesPath"] = complex_df["id"].apply(lambda x: f"multiColumn/bboxes/{x}.json")
    complex_df.to_csv("../dataset/multiColumn/metadata.csv", index=False)

    complex_df.info()

    # Generate files
    def write_text(chart_id, text, folder):
        with open(folder + str(chart_id) + ".txt", "w+") as f:
            f.write(text)

    simple_df.apply(lambda row: write_text(row["id"], row["title"], "../dataset/titles/"), axis=1)
    simple_df.apply(lambda row: write_text(row["id"], row["caption"], "../dataset/captions/"), axis=1)

    complex_df.apply(lambda row: write_text(row["id"], row["title"], "../dataset/multiColumn/titles/"), axis=1)
    complex_df.apply(lambda row: write_text(row["id"], row["caption"], "../dataset/multiColumn/captions/"), axis=1)

    import shutil

    def copy_img(chart_id, old_id, folder):
        old_folder, old_chart_id = old_id.split("-")
        shutil.copy(f"out/{old_folder}/imgs/{old_chart_id}.png", folder + str(chart_id) + ".png")

    simple_df.apply(lambda row: copy_img(row["id"], row["old_id"], "../dataset/imgs/"), axis=1)
    complex_df.apply(lambda row: copy_img(row["id"], row["old_id"], "../dataset/multiColumn/imgs/"), axis=1)

    import shutil

    def copy_ocr(chart_id, old_id, folder, is_text):
        old_folder, old_chart_id = old_id.split("-")
        sub_folder = "ocr_data/" if is_text else "bboxes/"
        ext = ".txt" if is_text else ".json"

        shutil.copy(
            f"ocr_out/{old_folder}/{sub_folder}{old_chart_id}{ext}",
            f"{folder}{sub_folder}{chart_id}{ext}",
        )

    simple_df.apply(lambda row: copy_ocr(row["id"], row["old_id"], "../dataset/", True), axis=1)
    simple_df.apply(lambda row: copy_ocr(row["id"], row["old_id"], "../dataset/", False), axis=1)

    complex_df.apply(lambda row: copy_ocr(row["id"], row["old_id"], "../dataset/multiColumn/", True), axis=1)
    complex_df.apply(lambda row: copy_ocr(row["id"], row["old_id"], "../dataset/multiColumn/", False), axis=1)

    for i in ["titles", "captions", "bboxes", "ocr_data", "imgs"]:
        print(".DS_Store" not in (os.listdir(f"../dataset/{i}")))
        print(len(os.listdir(f"../dataset/{i}")) == 1486)
        print(".DS_Store" not in (os.listdir(f"../dataset/multiColumn/{i}")))
        print(len(os.listdir(f"../dataset/multiColumn/{i}")) == 7799)