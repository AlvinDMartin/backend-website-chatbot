
#In[1]
import json
import os
_path = "dataset/intents_VN.json"

class processing_dataset():

    def ktra_emplylist(self):
        if os.stat(_path).st_size == 0:
            with open(_path, 'w',encoding='utf-8') as out_file:
                json.dump([], out_file, indent = 1,ensure_ascii=False)
            out_file.close()
            return "Danh sách dataset đang trống !"

    def new_dataset( self,val_tag, val_patt, val_res):
        self.val_tag = val_tag
        self.val_patt = val_patt
        self.val_res = val_res

        self.ktra_emplylist()

        with open(_path,'r',encoding='utf-8') as in_file:
            data = json.load(in_file)
            data['intents'].append({
                'tag': str(val_tag),
                'patterns': [str(val_patt)],
                'responses':[str(val_res)],
                'context_set':''
            })
        in_file.close()

        with open(_path, 'w',encoding='utf-8') as out_file:
            json.dump(data, out_file, indent = 1,ensure_ascii=False)
        out_file.close()
        print("Save new dataset thành công!")

    def delete_dataset( self,val_tag):
        self.val_tag = val_tag
        boot = False
        self.ktra_emplylist()

        with open(_path,'r',encoding='utf-8') as in_file:
            data = json.load(in_file)
            for element in data['intents']:
                if element["tag"] == val_tag:
                    data['intents'].remove(element)
                    boot = True

        in_file.close()

        with open(_path, 'w',encoding='utf-8') as out_file:
            json.dump(data, out_file, indent = 1,ensure_ascii=False)
        out_file.close()
        if boot == True:
            return "Delete thành công"
            
    def update_dataset(self, val_tag,  val_patt, val_res):
        self.val_tag = val_tag
        self.val_patt = val_patt
        self.val_res = val_res
        boot = False
        self.ktra_emplylist()

        with open(_path,'r',encoding='utf-8') as in_file:
            data = json.load(in_file)
            for element in data['intents']:
                if element["tag"] == val_tag:
                    if str(val_patt) != '' and str(val_res) != '':
                        element["patterns"].append(str(val_patt))
                        element["responses"].append(str(val_res))
                        boot = True
                    elif str(val_patt) != '':
                        element["patterns"].append(str(val_patt))
                        boot = True
                    elif str(val_res) != '':
                        element["responses"].append(str(val_res))
                        boot = True

        in_file.close()
        with open(_path, 'w',encoding='utf-8') as out_file:
            json.dump(data, out_file, indent = 1,ensure_ascii=False)
        out_file.close()
        if boot == True:
            return "Update thành công"
        else:
            return "Có thể Tag đã sai, bạn không thể thay đổi tag, không được update"

    def search_tag(self, val_tag):
        self.val_tag = val_tag
        boot = False
        self.ktra_emplylist()
        with open(_path,'r',encoding='utf-8') as in_file:
            data = json.load(in_file)
            for element in data['intents']:
                if element["tag"] == val_tag:
                    boot = True

        in_file.close()
        return boot


# #test         
# u = processing_dataset()
# x = 'Bé gái'
# y = 'ten cua ban là gi 222'
# z = 'ten cua toi là dat'
# u.update_dataset(x,y,z)
# # #u.delete_dataset(x)

