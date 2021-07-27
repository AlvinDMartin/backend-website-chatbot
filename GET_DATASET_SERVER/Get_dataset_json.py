
#In[]
import requests
import json
  
# api-endpoint
URL = "https://quocdatit.tk/dataset/get-all-dataset/"
  
  
  
# sending get request and saving the response as response object
r = requests.get(url = URL)
  
# extracting data in json format
data = r.json()

with open('DatasetQA.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, ensure_ascii=False,indent = 1)
# %%
