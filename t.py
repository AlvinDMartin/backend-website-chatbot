#In[]
import requests

url = 'https://api.fpt.ai/hmi/tts/v5'

payload = 'xin chào các bạn'
headers = {
    'api-key': 'aDIwzZVK2KBU7J6RrvHc1SW55bv1FjY8',
    'speed': '',
    'voice': 'banmai'
}

response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

print(response.text)


#In[]
import datetime
now = datetime.datetime.now()
print(now)
# %%
