from test_data import Generator
from database import Database
from database import Query
from calculator import Recommendation

import pandas as pd


#기존 dataframe 호출
path="/home/user/SaGol/MiniGPT-4/image_recommendation/MinigptOut.csv"
data=pd.read_csv(path)  

#모델 돌리기
photopath="/home/user/SaGol/MiniGPT-4/Images"
g = Generator(data)
g.generate(photopath)

#토큰 처리 및 TF-IDF 알고리즘
data=Database(g.data)
print(data.data)  #디버깅용

#사용자 질문을 처리하는 부분.
userText = "펭귄 세 마리가 찍혀있는 사진을 찾아 줘."
q=Query(userText, data)
r=Recommendation(q,data)

#출력
r.printf()