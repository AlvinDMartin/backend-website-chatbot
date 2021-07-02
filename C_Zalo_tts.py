import requests
#import webbrowser

class tts():
    def Create_API(self,text):
        url = 'https://api.zalo.ai/v1/tts/synthesize'

        #text = "Xin chào tất cả anh em đã đến với động bàn tơ của tôi"

        h = {
        "apikey":"DPACevwjw4i5BmOPIrvwK4dpGQ7b0IHX",
        #"apikey":"3ebqLqDjxEox5i4lNtNtl4f8pswGoi2A",
        }
        params = {
            'input':text
        }
        response = requests.post(url, headers=h,data=params).json()
        return response['data']['url']
