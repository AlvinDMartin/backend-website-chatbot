import requests

class fpt_tts():
    def Create_API(self,text):
        url = 'https://api.fpt.ai/hmi/tts/v5'

        #text = "Xin chào tất cả anh em đã đến với động bàn tơ của tôi"

        h = {
        "api_key":"aDIwzZVK2KBU7J6RrvHc1SW55bv1FjY8",
        "voice":"banmai",
        }
        params = {
            "":text
        }
        response = requests.post(url, headers=h,data=params).json()
        return response["async"]

u = fpt_tts()
print(u.Create_API("xin chào"))
