#In[]
import json
import os
from pathlib import Path
from B_save_new_dataset import processing_dataset

savejson = processing_dataset()
_path = "Update_dataset/newquestions.json"

class B_save_new_data():

    def run(self, new_quest,  new_tag, new_res,):
        self.new_quest = new_quest
        self.new_tag = new_tag
        self.new_res = new_res

        if os.stat(_path).st_size == 0:
            with open(_path, 'w',encoding='utf-8') as out_file:
                json.dump([], out_file, indent = 1,ensure_ascii=False)
            return "Danh sách question trống!"
        else:
            quest =  new_quest
            tag = new_tag
            res = new_res

            if savejson.search_tag(tag) == True:
                savejson.update_dataset(tag,quest,res)
                return "Tag được tìm thấy - Update"
            else:
                savejson.new_dataset(tag,quest,res)
                return "Thêm Tag mới"

