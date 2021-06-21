import requests

class fpt_tts():
    def Create_FPT_API(self,text):
        url = 'https://api.fpt.ai/hmi/tts/v5'

        #text = "Xin chào tất cả anh em đã đến với động bàn tơ của tôi"

        h = {
        "api_key":"aDIwzZVK2KBU7J6RrvHc1SW55bv1FjY8",
        "voice":"thuminh",
        "speed":"0",
        }
        response = requests.post(url, headers=h,data=text.encode('utf-8')).json()
        return response["async"]

