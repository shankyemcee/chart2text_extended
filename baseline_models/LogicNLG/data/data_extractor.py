# -*- coding: utf-8 -*-


import json

with open('test_lm.json',encoding="utf8") as f:
            gold = json.load(f)


with open('field_infusing.json',encoding="utf8") as f:
            generated = json.load(f)

gen_list=[]
gold_list=[]
for key in generated:
    gen_list.append(generated[key][0])
    gold_list.append(gold[key][0][0])


with open("generated-p80.txt", "w",encoding="utf8") as text_file:
    for item in gen_list:
        text_file.write("%s\n" % item)


with open("testOriginalSummary.txt", "w",encoding="utf8") as text_file:
    for item in gold_list:
         text_file.write("%s\n" % item)