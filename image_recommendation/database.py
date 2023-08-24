import pandas as pd
import Text2Token
import TF_IDF
import translator
import calculator

# data와 vocab을 속성으로 가진다.
class Database:
    
    def __init__(self, data):
        if data['Description'].isnull==1 :
            data['Description'] = data['Description'].fillna('')
            raise Exception("description에서 null값 발생.")
        
        Text2Token.Text2Token(data)                                         #토큰화 및 사전 만드는 부분.
        vocab=Text2Token.vocab(data)
                                                                            #알고리즘 계산 부분.
        self.data = data
        self.vocab = vocab
        self.TF_matrix = TF_IDF.TF(data,vocab)
        self.IDF_matrix= TF_IDF.IDF(self.TF_matrix,vocab)
        self.TF_IDF_matrix = TF_IDF.TF_IDF(self.TF_matrix,self.IDF_matrix)
    
    #data는 Hash, Description, Tokenized 3개의 열로 구성
    
    def recalculate(self, new_data):
        pass
    
    
#생성 시 사전과 userText를 받고, query_vector를 가지고 있는 객체
class Query:
    
    def __init__(self, userText, data): 
        print("\nQ : ", userText, "\n")
        query = translator.translateKrtoEn(userText)                       #영어로 처리
        self.query_matrix = self.weighted_query(query,data.IDF_matrix)    #사용자의 질문을 idf matrix를 참고하여 가중치 수정.
        self.validwords= calculator.validwords(self.query_matrix)      #사전에 있는 단어만 고려 
        self.query_vector=calculator.vectorization(self.validwords,data.vocab)
        
    def weighted_query(self, query_matrix, idf_matrix) : 
        i=0
        for index in query_matrix.index:
            j=0
            for word in idf_matrix.index:    
                if word==index:
                    query_matrix.at[word,0] = query_matrix.iloc[i,0]*idf_matrix.iloc[j,0]
                    break
                j=j+1
            if j==len(idf_matrix) : query_matrix.iloc[i,0]=0
            i=i+1
        return query_matrix
    