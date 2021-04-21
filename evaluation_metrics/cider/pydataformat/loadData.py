"""
Load the reference and candidate json files, which are to be evaluated using CIDEr.

Reference file: list of dict('image_id': image_id, 'caption': caption).
Candidate file: list of dict('image_id': image_id, 'caption': caption).

"""
import json
import os
from collections import defaultdict

class LoadData():
    def __init__(self, path):
        self.pathToData = path

    def readJson(self, refname, candname):

        path_to_ref_file = os.path.join(self.pathToData, refname)
        path_to_cand_file = os.path.join(self.pathToData, candname)

        with open(path_to_ref_file) as f:
            ref_list = json.load(f)
        
        with open(path_to_cand_file) as f:
            cand_list = json.load(f)



        #ref_list = json.loads(open(path_to_ref_file, 'r').read(), encoding='utf-8')
        #cand_list = json.loads(open(path_to_cand_file, 'r').read(), encoding='utf-8')

        gts = defaultdict(list)
        res = []

        for l in ref_list:
            gts[l['image_id']].append({"caption": l['caption'].encode('utf-8')})

        for l in range(len(cand_list)):
            cand_list[l]['caption'] = cand_list[l]['caption'].encode('utf-8')        

        res = cand_list;
        return gts, res
