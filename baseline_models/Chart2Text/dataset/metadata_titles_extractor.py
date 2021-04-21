# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 12:23:34 2021

@author: Dell G7 User 2
"""

import pandas 


df = pandas.read_csv("metadata.csv", encoding = 'utf-8')


for index, row in df.iterrows():
    title = row.title
    title = title.replace("\n","")
    title = " ".join(title.split())
    #df.loc[index,'title'] = title
    with open("titles_old/" + str(index+1) + ".txt",'w' , encoding = 'utf-8') as file:
        file.write(title)

