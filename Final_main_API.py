# API
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.tools import T
from datetime import datetime
import json
import os

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
B_m = B_save_new_data

with open(_path,'r',encoding='utf-8') as in_file:
    data = json.load(in_file)

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
    return item

@app.get("/time")
async def root(start_date: datetime = start):
    print(start_date)
    return {"start_date": start_date}


@app.post("/chatbot/chat-nolearning")
async def create_chat(item: A_Item):

    A_m.Action(False, False)

    # new_message = {
    #     'user': item.user,
    #     'name': item.name,
    #     'request_question': item.request_question,
    # }
    # records.insert_one(new_message)

    return A_m.chat(item.request_question)

@app.get("/chatbot/chat-learning")
async def create_chat_learning():
    A_m.Action(True, True)
    return "training thanh cong"

@app.post("/newquestions")
async def create_item(item: B_Item):
    for i in range(len(data)):
        quest = data[i]
        tag = item.tag
        res = item.responses
        B_m.run(quest, tag, res)

    return data[i]
