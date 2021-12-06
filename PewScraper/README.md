# PewScraper
- This repository contains the code for scraping the charts and metadata for the Pew dataset in the Chart-to-Text benchmark
- Take note that this code was used to scrape the Pew website in January 2021, so the website may have changed since then
    - Hence, the some of the files may not work for the current structure of the website
    - e.g. the `extract_topic.py` no longer works due to the new format of the topic display on the websites

## Folder Structure
- `dataset/`: Final dataset
- `links/`: Publication links to scrape
- `out/`: Raw outputs from `process_no_data.py` & `process_data.py`
- `ocr_data/`: OCR data outputs
- `src`: Contains the python files
    - Refer to [How to Run](#how-to-run) for more information on which file does
    
### Folders that aren't included here
- Due to the large size of these folders, they are not included in this repository, instead they can be found in a Google Drive link included in the `README.md` files
- These folders are
    - `ocr_out/`: https://drive.google.com/drive/folders/1-cRCeRz0YqLX0ecEBU0RnZz8hOtPNoGR?usp=sharing
    - `out/no_data/`: https://drive.google.com/drive/folders/1TG1h58pJbiRZqQt-m3gkRKGO4azkoK6a?usp=sharing
    - `dataset/`: https://drive.google.com/drive/folders/1CwI-lIS1Z0Qgtrz2ZFBjoJu_I1qzrgL0?usp=sharing

## How to Run
1. `cd src/`

### Scrape links to publications
1. `python publication_scrape.py`
    - Fills up `publication_scraped.csv` with the links from all publications
2. `python find_pew_charts.py`
    - Fills up `pew_chart_links.csv` with the publication links that contain charts with underlying data tables

### Extract charts from publications
1. `python process_no_data.py`
    - Takes the links in `publication_scraped.csv` & extracts the captions and images
    - For `out/no_data/`
2. `python process_data.py`
    - Takes the links in `pew_chart_links.csv` & extracts the captions and images
- For `out/two_col/` & `out/multi_col/`


### Clean up charts
1. `python remove_duplicates.py`
    - Removes charts from duplicated URLs for all folders
    - Some URLs contain exactly the same content or redirect to the same page (e.g. https://www.pewsocialtrends.org/2017/03/17/the-data-on-women-leaders/ & https://www.pewsocialtrends.org/fact-sheet/the-data-on-women-leaders/, https://www.journalism.org/fact-sheet/hispanic-and-african-american-news-media/ & https://www.journalism.org/fact-sheet/hispanic-and-black-news-media/)
    - Generates the `metadata_without_duplicates.csv` files
2. `python extract_topic.py`
    - Add topic for each chart in `out/no_data/`
3. `python filter_no_data.py`
    - Removes the images that are not charts and foreign language articles from the `out/no_data/` folder
    - IDs of non-chart images were manually identified by looking at the
     `out/no_data/imgs/` folder
     - Generates the `metadata_filtered.csv` file
4. `python crop_no_data.py`
    - Identifies cropped paragraphs and confirmed paragraphs for each chart in the `out/no_data/` folder
        - Cropped paragraphs: Paragraphs that may be relevant
        - Confirmed paragraphs: Paragraphs that are very likely to be relevant (subset of cropped paragraphs)
    - Generates the cropped and confirmed captions by combining the cropped and confirmed paragraphs respectively
    - Generates the `cropped_metadata_filtered.csv` file
5. `python create_annotation_csvs.py`
    - Generates the csvs for the annotation of the `out/no_data/` paragraphs
    - These csvs were used to run the Mechanical Turk study
6. `python clean_no_data.py`
    - Should run after the annotation
    - Generates the `final_metadata.csv`, `simple_metadata.csv` and `complex_metadata.csv` files for `out/no_data/`
7. `python create_manual_cropper.py`
    - Creates a csv of the paragraphs for each chart to be annotated
    - To annotate, create a column `is_relevant` and put `TRUE`/`FALSE` depending on whether the paragraph is relevant to the chart
8. `python clean_data.py`
    - Should run after the annotation
    - Generates the `cropped_metadata.csv` & `final_metadata.csv` files for `out/two_col/` & `out/multi_col/`
    - Adds chart topics
9. `python combine_dataset.py`
    - Combines the files from the `out/` folder to form the `dataset/` folder
    - The two column charts from `out/two_col/` and `out/no_data/` are combined are reindexed
    - The multi column charts from `out/multi_col/` and `out/no_data/` are combined are reindexed
    - Formats the files in the format ready for modelling