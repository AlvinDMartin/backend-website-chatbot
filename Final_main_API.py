# API
import re
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.tools import T
from datetime import datetime
import json
import os
from typing import Optional

_path = "Update_dataset/newquestions.json"

#start = datetime.today()
start = datetime.utcnow()

app = FastAPI(debug=True)

from pymongo import MongoClient
client = MongoClient("mongodb+srv://dbUser:dbUser123@cluster0.nrpsz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.get_database('webshopping')
records = db.message_chat_bot


# Library
from A_main import A_main
A_m = A_main()
from B_main_save_new_dataset import B_save_new_data
B_m = B_save_new_data()


class A_Item(BaseModel):
    user: str
    name: str
    request_question: str

class B_Item(BaseModel):
    tag: str
    responses: str



#------------------------- API -------------------------

@app.get("/")
async def home(item: A_Item):
    return "Hãy bắt đầu gọi API"

@app.get("/time")
async def get_time(start_date: datetime = start):
    print(start_date)
    return {"start_date": start_date}


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
    return "training thanh cong"

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
    
   
