from database import Database
from database import Query
from calculator import Recommendation

import pandas as pd
import test_data

#기존 dataframe
path="C:/Users/Administrator/Desktop/image_recommedation/image_recommendation/MinigptOut.csv"
data=pd.read_csv(path)  

from test_data import Imgs
data=Database(Imgs)

#사용자 질문을 처리하는 부분.
userText = "펭귄 세 마리 사진"
q=Query(userText, data)
r=Recommendation(q,data)

#출력
r.printf()