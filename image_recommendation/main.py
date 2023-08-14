import translate
import vectorization

from database import Database
from database import Query

#인공지능에서 받아온 data를 가공하는 부분.
path="C:/Users/Administrator/Desktop/image_recommendation/MinigptOut.csv"
data=Database(path)
df=data.data
vocab = data.vocab

#TF-IDF 알고리즘을 적용하는 부분.          #여기도 다른 클래스 사용하여 제거할 예정이다.
tf_matrix=data.TF_matrix
idf_matrix=data.IDF_matrix
TF_IDF_matrix=data.TF_IDF_matrix


#사용자 질문을 처리하는 부분.
userText = "선인장 사진을 찾아줘"

q=Query(userText, data)
query_matrix = q.query_matrix              #일단은 여기까지 수정 완료,

#사전에 있는 단어만 추린 결과
validwords= vectorization.validwords(query_matrix)

#cosine similarity 비교하는 부분.
query_vector=vectorization.vectorization(validwords,vocab)
cos_sim_matrix=vectorization.cos_sim_matrix(query_vector, TF_IDF_matrix)

#비교하여 hash값과 설명을 return
hashs=vectorization.recommend(cos_sim_matrix, df)               #추천 강도 수정 예정
hashs=translate.translateResulttoKr(hashs)

#검증용
print("A : 찾은 사진 : ", len(hashs), "개")
print(hashs)