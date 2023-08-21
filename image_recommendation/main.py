from generator import AltTextGenerator
from database import Database
from database import Query
from calculator import Recommendation

import pandas as pd

#기존 dataframe 호출
def getPictures(path):
    data=pd.read_csv(path)
    return data

def getAltText(img_path):
    #텍스트 생성
    data=AltTextGenerator.generate(img_path)
    return data

def Tokenize(data):
    #토큰 처리 및 TF-IDF 알고리즘 수행
    data=Database(data)
    
def getBestPictures(data,userText):
    q=Query(data,userText)
    r=Recommendation(q,data)
    r.printf()
    return r

if __name__ == '__main__':
    #모델이 back에서 돌아간다고 생각할 때 (테스트용)
    
    datapath="/home/user/SaGol/MiniGPT-4/image_recommendation/MinigptOut.csv"
    img_path="/home/user/SaGol/MiniGPT-4/Images"
    userText = "펭귄 세 마리가 찍혀있는 사진을 찾아 줘."
    
    #기존 dataframe 호출
    data=getPictures(datapath)
    
    #모델 돌리기
    data=getAltText(img_path)
    
    #토큰 처리 및 TF-IDF 알고리즘 수행
    data=Database(data)
    
    #사용자 질문을 처리하는 부분.
    getBestPictures(data,userText)
