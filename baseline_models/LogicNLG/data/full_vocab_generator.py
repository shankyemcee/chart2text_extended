
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:44:05 2020

@author: shank
"""

import pandas as pd
from collections import Counter
from os import listdir
from os.path import isfile, join
import copy
import json



max_len=0
all_list=[]

#train_data_load
mypath="../field_infusing_encoder/all_csv/"
datafiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for table in datafiles:
    d = pd.read_csv(mypath + table, sep='#',encoding='utf8')
    if len(d) > max_len: max_len = len(d)
    all_list = all_list + [str(cell) for row in d.values.tolist() for  cell in row]


with open('train_lm.json',encoding="utf8") as f:
            gold_train = json.load(f)
all_list = all_list + [str(token) for row in gold_train.values() for  ref in row[0] if type(ref)==str for token in ref.split()]



with open('test_lm.json',encoding="utf8") as f:
            gold_test = json.load(f)
all_list = all_list + [str(token) for row in gold_test.values() for  ref in row[0] if type(ref)==str for token in ref.split()]


with open('val_lm.json',encoding="utf8") as f:
            gold_val = json.load(f)
all_list = all_list + [str(token) for row in gold_val.values() for  ref in row[0] if type(ref)==str for token in ref.split()]






cnt = Counter()
for word in all_list:
    cnt[word] += 1



full_vocab_list = [ent[0] for ent in cnt.most_common()]



full_vocab_dict={"<PAD>": 0,
               	 "<SEP>": 1,
               	 "<SOS>": 2,
               	 "<EOS>": 3,
               	 "<UNK>": 4,
                 "#0": 5
                 }

k=6
for i in range(max_len):
    full_vocab_dict["#"+str(i+1)] = k;k+=1

vocab_dict=copy.deepcopy(full_vocab_dict)


for key in full_vocab_list:
    full_vocab_dict[key]=k
    if k < len(full_vocab_list)*.3:
        vocab_dict[key]=k
    k+=1;
    

with open('full_vocab.json', 'w') as json_file:
        json.dump(full_vocab_dict, json_file)    


with open('vocab.json', 'w') as json_file:
        json.dump(vocab_dict, json_file)    
