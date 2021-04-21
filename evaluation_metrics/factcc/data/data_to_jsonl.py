# -*- coding: utf-8 -*-

import json

with open("fi_data/testOriginalSummary.txt", 'r', encoding='utf-8') as actualfile:
            actual = actualfile.readlines()
            

with open("fi_data/generated-p80.txt", 'r', encoding='utf-8') as generatedfile:
            generated = generatedfile.readlines()
    
output_list = []
count = 0;
for i,j in zip(actual,generated):
    data = { "id":str(count), "text":i, "claim":j , "label":"CONSISTENT"}; count+=1;
    output_list.append(data)
    #json_data = json.dumps(data)
    # output_dict['id'] = count; count+=1;
    # output_dict['text'] = i;
    # output_dict['claim'] = j;


      
with open('fi_data/data-dev.jsonl','w', encoding='utf-8') as f:
    json.dump(output_list,f)



# with open(input_file, "r", encoding="utf-8") as f:
#            a = json.load(f)