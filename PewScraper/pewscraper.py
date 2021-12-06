# -*- coding: utf-8 -*-
"""PewScraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1co5TQTllPpaJQ-kbf4YJHbsVSjmi7FUq
"""

from google.colab import drive

drive.mount('/content/gdrive', force_remount=True)

# Commented out IPython magic to ensure Python compatibility.
# % cd gdrive/MyDrive/PewScraper/

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

FACT_SHEET_SCRAPED_PATH = "fact_sheet_scraped.csv"
PUBLICATION_SCRAPED_PATH = "publication_scraped.csv"
PUBLICATION_CLEANED_SCRAPED_PATH = "publication_scraped_cleaned.csv" # No out of domain links

BASE_DIR = "out/"

TWO_COL_DIR = BASE_DIR + "two_col/"
MULTI_COL_DIR = BASE_DIR + "multi_col/"
NO_DATA_DIR = BASE_DIR + "no_data/"

IMGS_DIR = "imgs/"
DATA_DIR = "data/"
CAPTIONS_DIR = "captions/"
CROPPED_CAPTIONS_DIR = "cropped_captions/"
CONFIRMED_CAPTIONS_DIR = "confirmed_captions/"
META_PATH = "metadata.csv"
META_NO_DUPLICATES_PATH = "metadata_no_duplicates.csv"
CROPPED_META_PATH = "cropped_metadata.csv"
CROPPED_META_NO_DUPLICATES_PATH = "cropped_metadata_no_duplicates.csv"
EVALUATE_CROPPED_CAPTIONS_PATH = "evaluate_cropped_captions.csv"
META_FILTERED_PATH = "metadata_filtered.csv"
CROPPED_META_FILTERED_PATH = "cropped_metadata_filtered.csv"

"""# Create CSV for Modelling"""

"""# Combined Dataset"""
