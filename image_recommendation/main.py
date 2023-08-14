from database import Database
from database import Query
from calculator import Recommendation


#인공지능에서 받아온 data를 가공하는 부분.
path="C:/Users/Administrator/Desktop/image_recommedation/image_recommendation/MinigptOut.csv"
data=Database(path)

#사용자 질문을 처리하는 부분.
userText = "낙엽이 떨어지는 도시 사진"
q=Query(userText, data)
r=Recommendation(q,data)

#출력
r.printf()