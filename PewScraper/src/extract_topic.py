import re
import json
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from ast import literal_eval

from constants import *

def add_topic(meta_df):
    meta_df.set_index("id", inplace=True)

    topic_mapping = {
        'global': "Global Attributes & Trends",
        'hispanic': "Hispanic Trends",
        'internet': "Internet & Technology",
        'methods': "Methods",
        'politics': "U.S. Politics & Policy",
        'science': "Science & Society",
    }

    def extract_topic(url):
        # Pew Research
        pew_research_match = re.match(r"https:\/\/www\.pewresearch.org\/([^\/]+)\/", url)

        if pew_research_match is not None:
            topic_url = pew_research_match.group(1)

            if topic_url in topic_mapping:
                return topic_mapping[topic_url]
            else:
                return "Uncategorised"
        
        # Journalism
        journalism_match = re.match(r"https:\/\/www\.journalism.org\/", url)

        if journalism_match is not None:
            return "Journalism & Media"

        # Pew Social Trends
        pew_social_trends_match = re.match(r"https:\/\/www\.pewsocialtrends.org\/", url)

        if pew_social_trends_match is not None:
            return "Social & Demographic Trends"

        # Pew Forum
        pew_forum_match = re.match(r"https:\/\/www\.pewforum.org\/", url)

        if pew_forum_match is not None:
            return "Religion & Public Life"
        
        # Others
        return "Uncategorised"

    meta_df["topic"] = meta_df["URL"].apply(extract_topic)

    def extract_schema_topic(url):
        try:
            html = urlopen(url).read()
            soup = BeautifulSoup(html, "html5lib")

            if not soup.body:
                return

            schema = soup.select("head script.yoast-schema-graph")

            if len(schema) != 1:
                print(url, "has not schema")

            schema_dict = json.loads(schema[0].string)
            schema_graph = schema_dict["@graph"]

            for item in schema_graph:
                if item["@type"] == "BreadcrumbList":
                    breadcrumb_list = item["itemListElement"]
                    if len(breadcrumb_list) < 2:
                        break
                    
                    return breadcrumb_list[1]["item"]["name"].replace("&amp;", "&")
            
            programs = soup.find_all("meta", {"name": "programs"})
            print(url)
            return [program["content"].replace("&amp;", "&") for program in programs]
            
        except Exception as ex:
            print(ex)
            print(url)

    uncategorised_urls = meta_df.loc[meta_df["topic"] == "Uncategorised", "URL"]
    new_topics = uncategorised_urls.apply(extract_schema_topic)

    new_topic_mapping = {
        "Politics & Policy": "U.S. Politics & Policy",
        "Religion": "Religion & Public Life",
        "International Relations": "Global Attributes & Trends",
        "Internet & Technology": "Internet & Technology",
        # "Economy & Work": "",
        "News Habits & Media": "Journalism & Media",
        "Immigration & Migration": "Global Attributes & Trends",
        "Race & Ethnicity": "Social & Demographic Trends",
        "Science": "Science & Society",
        "Generations & Age": "Social & Demographic Trends",
        "Family & Relationships": "Social & Demographic Trends",
        "Other Topics": "Uncategorised",
        "Gender & LGBT": "Social & Demographic Trends",
        "Methodological Research": "Methods",
        "Population & Demographics": "Social & Demographic Trends",
        # "Coronavirus Disease (COVID-19)": "",
        "Content Analysis": "Methods",
        "Political Ideals & Systems": "U.S. Politics & Policy",
        "Political Issues": "U.S. Politics & Policy",
        "Immigration Issues": "Global Attributes & Trends",
        "Politics Online": "U.S. Politics & Policy",
    }

    programs_mapping = {
        'Data Labs': "Internet & Technology",
        'Global': "Global Attributes & Trends",
        'Global Migration and Demography': "Global Attributes & Trends",
        'Internet and Technology': "Internet & Technology",
        'Journalism': "Journalism & Media",
        'Methods': "Methods",
        'Politics': "U.S. Politics & Policy",
        'Religion': "Religion & Public Life",
        'Science': "Science & Society",
        'Social Trends': "Social & Demographic Trends",
    }

    list_ids = new_topics.apply(lambda programs: type(programs) == list)
    new_topics[list_ids] = new_topics[list_ids].apply(lambda programs: programs_mapping[programs[0]] if len(programs) == 1 else "Uncategorised")
    meta_df.loc[meta_df["topic"] == "Uncategorised", "topic"] = new_topics.apply(lambda topic: new_topic_mapping[topic] if topic in new_topic_mapping else topic)

    meta_df["topic"].value_counts().plot.pie(figsize=(20,10))
    return meta_df


if __name__ == '__main__':
    filename = NO_DATA_DIR + META_NO_DUPLICATES_PATH
    
    meta_df = pd.read_csv(filename, converters={"caption": literal_eval})
    meta_df = add_topic(meta_df)
    meta_df.to_csv(filename)
