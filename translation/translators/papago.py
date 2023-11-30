import sys
import json
import urllib.request  #하루 10000회 번역 가능

class Translator:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id # 네이버 개발자센터에서 발급받은 Client ID 값
        self.client_secret = client_secret # 개발자센터에서 발급받은 Client Secret 값
        self.url = "https://openapi.naver.com/v1/papago/n2mt" 

    def translate(self, text, sr="en", dest="ko"):
        encText = urllib.parse.quote(text)
        data = f"source={sr}&target={dest}&text={text}"  
        
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        
        rescode = response.getcode()
        if rescode==200:
            response_body = response.read()
            decoded_response = response_body.decode('utf-8')
            json_response = json.loads(decoded_response)
            translated_text = json_response["message"]["result"]["translatedText"]
        else:
            print("Error Code:" + rescode)
        return translated_text
    
def translate(text: str) -> str:
    return translator.translate(text)

translator = Translator("GPt_LaRJinXgdzt2Cfjl","Wfo4JWEJbD")

