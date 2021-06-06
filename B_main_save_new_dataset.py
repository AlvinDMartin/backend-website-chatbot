#In[]
import json
import os

from numpy import e
#from pathlib import Path
from B_save_new_dataset import processing_dataset

savejson = processing_dataset()
_path = "Update_dataset/newquestions.json"

class B_save_new_data():
    def run(self,new_quest, new_tag, new_res):
        with open(_path, 'r',encoding='utf-8') as in_file:
            first_data = json.load(in_file)
        in_file.close()
        if len(first_data) == 0:
            with open(_path, 'w',encoding='utf-8') as out_file:
                json.dump([], out_file, indent = 1,ensure_ascii=False)
            out_file.close()
            return "Danh sách question trống!"
        else:
            if savejson.search_tag(new_tag) == True:
                savejson.update_dataset(new_tag,new_quest,new_res)
                self.delete(new_quest)
                return "Tag được tìm thấy - Update"
            else:
                savejson.new_dataset(new_tag,new_quest,new_res)
                self.delete(new_quest)
                return "Thêm Tag mới"

    def delete(self, quest):
        with open(_path, 'r',encoding='utf-8') as in_file:
            first_data = json.load(in_file)
        in_file.close()
        with open(_path, 'r',encoding='utf-8') as in_file:
            new_data = json.load(in_file)
            for element in new_data:
                if element == quest:
                    new_data.remove(element)
        in_file.close()

        with open(_path, 'w',encoding='utf-8') as out_file:
            if len(first_data) == 0:
                json.dump([], out_file)
            else:
                print(new_data)
                json.dump(new_data, out_file)
        out_file.close()

# %%
