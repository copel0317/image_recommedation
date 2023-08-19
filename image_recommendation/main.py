from test_data import Generator
from database import Database
from database import Query
from calculator import Recommendation

import pandas as pd

#기존 dataframe 호출
def getPictures(path):
    data=pd.read_csv(path)
    return data

def getAltText(data,photopath):
    #텍스트 생성
    g = Generator(data)
    g.generate(photopath)
    #토큰 처리 및 TF-IDF 알고리즘 수행
    data=Database(g.data)
    return data

def getBestPictures(userText,data):
    q=Query(userText, data)
    r=Recommendation(q,data)
    r.printf()
    return r

if __name__ == '__main__':
    datapath="/home/user/SaGol/MiniGPT-4/image_recommendation/MinigptOut.csv"
    photopath="/home/user/SaGol/MiniGPT-4/Images"
    userText = "펭귄 세 마리가 찍혀있는 사진을 찾아 줘."
    
    #기존 dataframe 호출
    data=getPictures(datapath)
    
    #모델 돌리기
    data=getAltText(data,photopath)

    #사용자 질문을 처리하는 부분.
    getBestPictures(userText,data)
