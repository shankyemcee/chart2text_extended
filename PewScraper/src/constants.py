__all__ = [
	"PEW_CHART_LINKS_PATH",
	"PUBLICATION_SCRAPED_PATH",
	"PUBLICATION_CLEANED_SCRAPED_PATH",
	"BASE_DIR",
	"TWO_COL_DIR",
	"MULTI_COL_DIR",
	"NO_DATA_DIR",
	"IMGS_DIR",
	"DATA_DIR",
	"CAPTIONS_DIR",
	"CROPPED_CAPTIONS_DIR",
	"CONFIRMED_CAPTIONS_DIR",
	"META_PATH",
	"META_NO_DUPLICATES_PATH",
	"META_FILTERED_PATH",
	"CROPPED_META_PATH",
	"CROPPED_META_FILTERED_PATH",
	"MANUAL_CROPPED_PATH",
]

# Links
LINK_DIR = "../links/"

PEW_CHART_LINKS_PATH = LINK_DIR + "pew_chart_links.csv"
PUBLICATION_SCRAPED_PATH = LINK_DIR + "publication_scraped.csv"
PUBLICATION_CLEANED_SCRAPED_PATH = LINK_DIR + "publication_scraped_cleaned.csv"  # No out of domain links

# Directories
BASE_DIR = "../out/"

TWO_COL_DIR = BASE_DIR + "two_col/"
MULTI_COL_DIR = BASE_DIR + "multi_col/"
NO_DATA_DIR = BASE_DIR + "no_data/"

# Subdirectories
IMGS_DIR = "imgs/"
DATA_DIR = "data/"
CAPTIONS_DIR = "captions/"
CROPPED_CAPTIONS_DIR = "cropped_captions/"
CONFIRMED_CAPTIONS_DIR = "confirmed_captions/"

# Metadata files
META_PATH = "metadata.csv"
META_NO_DUPLICATES_PATH = "metadata_no_duplicates.csv"
META_FILTERED_PATH = "metadata_filtered.csv"
CROPPED_META_PATH = "cropped_metadata.csv"
CROPPED_META_NO_DUPLICATES_PATH = "cropped_metadata_no_duplicates.csv"
CROPPED_META_FILTERED_PATH = "cropped_metadata_filtered.csv"
MANUAL_CROPPED_PATH = "manual_cropped.csv"
