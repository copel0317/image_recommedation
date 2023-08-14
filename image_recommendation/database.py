import pandas as pd
import Text2Token
import TF_IDF
import translate

# 현재는 csv 파일로 만들어서 hash와 text를 넘겨 구현했습니다.
# 차후 연결할 때 이 부분을 수정해야 합니다.

# data와 vocab을 속성으로 가진다.
class Database:
    
    def __init__(self, path):
        
        data=pd.read_csv(path)                                              #값을 읽어오는 부분
        if data['Description'].isnull==1 :
            data['Description'] = data['Description'].fillna('')
            raise Exception("description에서 null값 발생.")
        
        Text2Token.Text2Token(data)                                         #토큰화 및 사전 만드는 부분.
        vocab=Text2Token.vocab(data)
        
        self.data = data
        self.vocab = vocab
        self.TF_matrix = TF_IDF.TF(data,vocab)
        self.IDF_matrix= TF_IDF.IDF(self.TF_matrix,vocab)
        self.TF_IDF_matrix = TF_IDF.TF_IDF(self.TF_matrix,self.IDF_matrix)
    
    #data는 Hash, Description, Tokenized 3개의 열로 구성
    
    def recalculate(self, new_data):
        pass
    
    

class Query:
    
    def __init__(self, userText, data): 
        print("Q : ", userText)
        query = translate.translateKrtoEn(userText)
        self.query_matrix = self.weighted_query(query,data.IDF_matrix)    #사용자의 질문을 idf matrix를 참고하여 가중치 수정.
        
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