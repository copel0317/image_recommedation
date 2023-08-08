import getTextHash
import Text2Token
import TF_IDF
import UserQuestion
import vectorization



#인공지능에서 Hash와 Text를 가져오는 부분.
df=getTextHash.getTextHash()

if df['Description'].isnull==1 :
    df['Description'] = df['Description'].fillna('')
    print("description에서 null값 발생.")

#가져온 Text를 Token화 하고, 사전을 만드는 부분.
Text2Token.Text2Token(df)
vocab=Text2Token.vocab(df)

#TF-IDF 알고리즘을 적용하는 부분.
tf_matrix=TF_IDF.TF(df,vocab)
idf_matrix=TF_IDF.IDF(tf_matrix,vocab)
TF_IDF_matrix=TF_IDF.TF_IDF(tf_matrix,idf_matrix)


#사용자 질문을 처리하는 부분.
userText = "선인장 사진을 찾아줘"
print("Q : ", userText)

query_matrix = UserQuestion.translateKrtoEn(userText)
query_matrix = UserQuestion.weighted_query(query_matrix,idf_matrix)         #사용자의 질문을 idf matrix를 참고하여 가중치 수정.

#사전에 있는 단어만 추린 결과
validwords= vectorization.validwords(query_matrix)

#cosine similarity 비교하는 부분.
query_vector=vectorization.vectorization(validwords,vocab)
cos_sim_matrix=vectorization.cos_sim_matrix(query_vector, TF_IDF_matrix)

#비교하여 hash값과 설명을 return
hashs=vectorization.recommend(cos_sim_matrix, df)               #추천 강도 수정 예정
hashs=UserQuestion.translateResulttoKr(hashs)

#검증용
print("A : 찾은 사진 : ", len(hashs), "개")
print(hashs)