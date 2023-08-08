import numpy as np
import pandas as pd

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
    

def recommend(cos_sim_matrix, df):
    result=[]
    for index in cos_sim_matrix:
        if index[1]!=0  :                              #조건 수정 예정. (일단 최대값으로 수정할 예정)
            result.append([df['Hash'][index[0]],df['Description'][index[0]]])
    return result