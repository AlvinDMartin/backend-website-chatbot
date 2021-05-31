from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.tools import T

app = FastAPI(debug=True)

class Item(BaseModel):
        name: str = "You"
        request_question: str

@app.get("/")
async def home(item: Item):
    return item

@app.post("/items/")
async def create_item(item: Item):
    print(item)
    return "save thang cong"


# #data
# with open("intents_VN.json",encoding='utf-8') as f:
#     data = json.load(f)

# @app.get("/")
# async def get_data():
#     return {"data":data}





