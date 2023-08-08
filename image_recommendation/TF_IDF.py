import pandas as pd
from math import log

#TF(문서 내 단어 빈도 행렬)과 idf를 분리해야 recalculate할 때 더 편할 것.
def TF(df,vocab):   
    N=len(df)
    result=[]
    
    for i in range(N):
        result.append([])
        d=df.cleaned[i]
        
        for j in range(len(vocab)):
            t = vocab[j]
            result[-1].append(d.count(t))
            
    return pd.DataFrame(result, columns=vocab)


def IDF(tf_matrix,vocab):
    result = []
    for word in vocab :
        frequency = 0
        for counts in tf_matrix[word] :
            if (counts!=0) : 
                frequency+=counts
        result.append(log(len(tf_matrix)/(frequency+1)))

    return pd.DataFrame(result, index = vocab, columns=["IDF"])


def TF_IDF(tf_matrix, idf_matrix):
    i=0
    result=[]
    for idf in idf_matrix.itertuples():
        result.append(tf_matrix.iloc[:,i] * idf_matrix.iloc[i,0]) #pandas dataFrame에서 행, 열 접근 시 iloc 사용.
        i=i+1
    return pd.DataFrame(result)