# -*- coding: utf-8 -*-

import pandas as pd
import os
import re


output_bboxdir="../data/test/testBbox.txt"
mappingdir="../../../../c2t_dataset_pew/test_index_mapping.csv"
bbox_mapping_dir="../../../../c2t_dataset_pew/dataset/testing_ocr_bboxes.csv"
ocr_datadir="../data/test/testDataOCR.txt"




bboxes=[]

mapping = pd.read_csv(mappingdir,encoding='utf8')
bbox_mapping = pd.read_csv(bbox_mapping_dir,encoding='utf8')










def extract_bboxes(bbox_text,bboxes_list_text):
    
    processed_bboxes=[]
    bbox_list = bbox_text.split("</s>")
    bbox_list = list(filter(None, bbox_list))
    if len(bbox_list) == len(bboxes_list_text.split(" ")): #condition triggers when taking ocr text when actual table is available
        for row in bbox_list:
            items = [str(round(float(i),2)) for i in row.split(",")]
            processed_bboxes.append("|".join(items))
    else:
            processed_bboxes= " ".join(['0|0|0|0']*len(bboxes_list_text.split(" ")))
            return processed_bboxes
    
    
    return " ".join(processed_bboxes)
    
    

with open(ocr_datadir, 'r', encoding='utf-8') as file:
                bboxes_list= file.readlines()



for index,row in mapping.iterrows():
    # if 'two_col' in row[0]:
        file_no = int(re.findall(r'\d+', row[0])[0])
        if file_no in bbox_mapping['Image Index'].tolist():
            assert file_no == bbox_mapping.iloc[index]['Image Index']
            bbox_text = bbox_mapping.iloc[index]['bboxes_text']
            processed_bboxes = extract_bboxes(bbox_text,bboxes_list[index])
            
            
        else:
            print(file_no)
            
            
            processed_bboxes= " ".join(['0|0|0|0']*len(bboxes_list[index].split(" ")))
        
        bboxes.append(processed_bboxes)
            
            
            
            
            

            
            


with open(output_bboxdir, mode='wt', encoding='utf8') as file:
        file.writelines("%s\n" % line for line in bboxes)



