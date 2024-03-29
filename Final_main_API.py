# API
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.tools import T
from datetime import datetime
import json

# from fastapi.middleware.cors import CORSMiddleware

_path = "Update_dataset/newquestions.json"
_path_dataset = "dataset/intents_VN.json"


app = FastAPI(debug=True)

# origins = [
#     "https://chopper-shop-1.herokuapp.com",
#     "http://localhost:3000",
#     "http://localhost:5000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# from pymongo import MongoClient
# client = MongoClient("mongodb+srv://dbUser:dbUser123@cluster0.nrpsz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db=client.get_database('webshopping')
# records = db.message_chat_bot


# Library
from A_main import A_main
A_m = A_main()
from B_main_save_new_dataset import B_save_new_data
B_m = B_save_new_data()
from B_save_new_dataset import processing_dataset
savejson = processing_dataset()
from C_Zalo_tts import tts
audio_zalo = tts()
from C_fpt_tts import fpt_tts
audio_fpt = fpt_tts()


class A_Item(BaseModel):
    user: str
    name: str
    request_question: str

class B_Item(BaseModel):
    tag: str
    responses: str
class B_Item_2(BaseModel):
    tag: str
class B_Item_3(BaseModel):
    tag: str
    patterns : str
    responses : str
class C_Item(BaseModel):
    text: str



#------------------------- API -------------------------

@app.get("/")
async def home():
    return "Hãy bắt đầu gọi API"

@app.get("/time")
async def get_time():
    start = datetime.utcnow()
    print(start)
    return {"start_date": start}
#-------------------------------------------------------

@app.post("/chatbot/chat-hello")
async def run_chat_hello(item: C_Item):
    x = A_m.hello(item.text)
    return x, audio_zalo.Create_API(x)


@app.post("/chatbot/chat-run")
async def run_chat(item: A_Item):
    A_m.Action(False, False)
    # new_message = {
    #     'user': item.user,
    #     'name': item.name,
    #     'request_question': item.request_question,
    # }
    # records.insert_one(new_message)
    return A_m.chat(item.request_question)

@app.get("/chatbot/chat-training")
async def training_chat():
    A_m.Action(True, True)
    return "training dữ liệu mới thành công"



#---------------------update new question-----------------
@app.get("/update/chat-getlistquestions")
async def list_questions():

    with open(_path,'r',encoding='utf-8') as in_file:
        data = json.load(in_file)
    in_file.close()    
    return data
    
@app.get("/update/chat-getlistquestions/{item_id}")
async def read_item(item_id: int):
    with open(_path,'r',encoding='utf-8') as in_file:
        data = json.load(in_file)
    in_file.close()  
    count = len(data)
    if item_id <= count-1:
        return data[item_id]
    else:
        return "Error: Danh sách hiện đang có: " + str(count) + " câu hỏi!"

@app.post("/update/chat-newquestions/{item_id}")
async def newquestion_chat(item: B_Item, item_id:int):
    with open(_path,'r',encoding='utf-8') as in_file:
        data = json.load(in_file)
    in_file.close()
    count = len(data)
    if item_id <= count-1:
        quest = data[item_id]
        tag = item.tag
        res = item.responses
        return B_m.run(quest,tag,res)
    else:
        return "Không có câu hỏi nào mới"

@app.get("/update/chat-delete-newquestions/{item_id}")
async def new_question_del(item_id: int):
    with open(_path,'r',encoding='utf-8') as in_file:
        data = json.load(in_file)
    in_file.close()
    count = len(data)
    if item_id <= count-1:
        B_m.delete(data[item_id])
        return "Xóa thành công câu số " + str(item_id)
    else:
        return "Không có câu hỏi nào để xóa"


#-------------------------------chức năng cho dataset--------------------

@app.get("/dataset/get-all-dataset/")
async def get_dataset():
    with open(_path_dataset,'r',encoding='utf-8') as in_file:
        _dataset = json.load(in_file)
    in_file.close()
    return _dataset

@app.get("/dataset/get-tag-dataset/")
async def get_dataset():
    with open(_path_dataset,'r',encoding='utf-8') as in_file:
        _dataset = json.load(in_file)
    in_file.close()
    save_tag = []
    for element in _dataset['intents']:
        save_tag.append(str(element["tag"]))
    return save_tag

@app.get("/dataset/get-tag-dataset/{item_id}")
async def get_one_dataset(item_id: int):
    with open(_path_dataset,'r',encoding='utf-8') as in_file:
        _dataset = json.load(in_file)
    in_file.close()
    save_tag = []
    for element in _dataset['intents']:
        save_tag.append(str(element["tag"]))

    if item_id >= len(save_tag):
        return "Danh sách chỉ có: " + str(len(save_tag)) + " Tag,  không thể vượt quá!"
    elif item_id < 0:
        return "Không thể là số âm"
    else:
        for i in range(len(save_tag)):
            if i == item_id:
                value = save_tag[i]
        return value

@app.post("/dataset/create-dataset/")
async def create_dataset(item: B_Item_3):
    tag = item.tag
    quest = item.patterns
    res = item.responses
    boo = False

    with open(_path_dataset,'r',encoding='utf-8') as in_file:
        data = json.load(in_file)
        for element in data['intents']:
            if element["tag"] == tag:
                boo = True
                break
    in_file.close()
    if boo == True:
        return "Tag bạn thêm đã có, vui lòng chọn Add"
    else:   
        savejson.new_dataset(tag, quest, res)   
        return "Create thành công"


@app.post("/dataset/edit-dataset/")
async def edit_dataset(item: B_Item_3):
    tag = item.tag
    quest = item.patterns
    res = item.responses
    return savejson.update_dataset(tag, quest, res)

@app.post("/dataset/delete-dataset/")
async def dataset_del (item: B_Item_2):
    return savejson.delete_dataset(item.tag)


#----------------------TTS----------------------------
@app.post("/texttospeech/soundAPI/")
async def soundAPI (item: C_Item):
    if item.text == "":
        return "Error: Text chưa được truyền vào"
    else:
        return audio_zalo.Create_API(item.text)

@app.post("/texttospeech/soundAPI/fpt/")
async def soundAPI (item: C_Item):
    if item.text == "":
        return "Error: Text chưa được truyền vào"
    else:
        return audio_fpt.Create_FPT_API(item.text)
