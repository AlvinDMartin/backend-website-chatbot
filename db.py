#In[1]
from pymongo import MongoClient
from pydantic.tools import T

client = MongoClient("mongodb+srv://dbUser:dbUser123@cluster0.nrpsz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.get_database('webshopping')
records = db.message_chat_bot


#In[2]: Count Documents
records.count_documents({})


#In[3]: create new documents
new_message = {
    'user': 'a',
    'request_question': 'xin chào'
}
records.insert_one(new_message)


#In[4]: Find documents
list(records.find())

records.find_one({'user':'a'})

#In[5]: Update documents

new_message_updates = {
    'request_question': 'xin chào update'
}

records.update_one({'user':'a'},{'$set': new_message_updates})

#In[6]: delete documents
records.delete_one({'user': 'a'})

