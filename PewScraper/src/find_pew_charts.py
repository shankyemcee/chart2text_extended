import time
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

from constants import *


def find_pew_charts(urls):
    start_time = time.time()
    links_with_charts = []

    # Process links
    for i, url in enumerate(urls):
        if i % 10 == 0:
            print(i, url)

            if i % 100 == 0:
                # Store list
                links_with_charts_df = pd.DataFrame(links_with_charts)
                links_with_charts_df.to_csv(index=False, path_or_buf=PEW_CHART_LINKS_PATH)
                print("Saving", len(links_with_charts_df), "links at time", time.time() - start_time)

        try:
            html = urlopen(url).read()
            soup = BeautifulSoup(html, "html5lib")

            if not soup.body:
                return

            # Look for pew charts
            table_list = soup.select(".pew-chart")

            if len(table_list) > 0:
                links_with_charts.append(url)

        except Exception as ex:
            print(ex)

    # Store meta lists
    links_with_charts_df = pd.DataFrame(links_with_charts)
    links_with_charts_df.to_csv(index=False, path_or_buf=PEW_CHART_LINKS_PATH)

    print("complete")


if __name__ == '__main__':
    frame = pd.read_csv(PUBLICATION_CLEANED_SCRAPED_PATH)
    sr = list(frame["0"])

    find_pew_charts(sr)
