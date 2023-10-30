import pandas as pd
from math import log
from collections import Counter

#TF(문서 내 단어 빈도 행렬)과 idf를 분리해야 recalculate할 때 더 편할 것.
def TF(df,vocab):   

    # 각 행의 Tokenized 열 값에서 vocab에 포함된 단어 빈도수 계산
    counters = []
    for row in df:
        word_counts = Counter(word for word in row if word in vocab)
        counters.append(word_counts)
        
    # 각 Counter 객체를 DataFrame으로 변환하여 단어 빈도수 테이블 생성
    word_freq_df = pd.DataFrame(counters).fillna(0).astype(int)
            
    return pd.DataFrame(word_freq_df, columns=vocab)


def IDF(tf_matrix,vocab):
    result = []
    for word in vocab :
        frequency = 0
        for counts in tf_matrix[word] :
            if (counts!=0) : 
                frequency+=counts
        if (frequency==0):
            result.append(0)
        else:
            result.append(log(len(tf_matrix)/(frequency+1)))
            
    return pd.DataFrame(result, index = vocab, columns=["IDF"]).T


