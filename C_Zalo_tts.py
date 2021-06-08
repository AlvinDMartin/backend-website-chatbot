import requests
#import webbrowser

class tts():
    def Create_API(self,text):
        url = 'https://api.zalo.ai/v1/tts/synthesize'

        #text = "Xin chào tất cả anh em đã đến với động bàn tơ của tôi"

        h = {
        "apikey":"UzOuOjakq8jCc9ZmrqbcJUBEhapLqm8F",
        }
        params = {
            'input':text
        }
        response = requests.post(url, headers=h,data=params).json()
        return response['data']['url']

# _url = response['data']['url']
# webbrowser.register('chrome',
# 	None,
# 	webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
# webbrowser.get('chrome').open(_url)