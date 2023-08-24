import numpy as np
import pandas as pd
import translator
        
"""
score가 일정 이상인 값인 사진을 여러 장 return하는 함수.
현재 사양은 similarity가 최대인 사진 하나를 return.
    def recommend(cos_sim_matrix, df):
        result=[]
        for index in cos_sim_matrix:
            if index[1]!=0  :                              
                result.append([df['Hash'][index[0]],df['Description'][index[0]]])
        return result
"""

def recommend(cos_sim_matrix, data):  
    past_similarity=0             
    for index in cos_sim_matrix:
        if index[1]!=0  :
            if index[1]>past_similarity:
                number=index[0]
                past_similarity=index[1]
    if past_similarity==0:
        raise Exception("해당하는 사진을 찾을 수 없습니다.")
    return [data['Hash'][number],data['Description'][number]]


def validwords (query_matrix) :
    result=[]                                   # 0이 아닌 key값.
    for i in range(len(query_matrix)):
        if query_matrix[0][i]!=0:
            result.append((query_matrix.index[i],query_matrix[0][i]))
            
    data = pd.DataFrame(result, columns=['word','value'])
    return data
            
def vectorization(validwords,vocab):
    vector = np.zeros(len(vocab))
    for i in range(len(validwords)) :
        for j in range(len(vocab)) :
            if(validwords['word'][i]==vocab[j]):
                break
        vector[j]=validwords['value'][i]
    return vector

def cos_sim(A,B):
    return np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))

def cos_sim_matrix(query_vector, TF_IDF_matrix):
    result=[]
    for vector in TF_IDF_matrix:   
        result.append((vector,cos_sim(query_vector,TF_IDF_matrix[vector])))
    return result
    