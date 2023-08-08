import numpy as np
import pandas as pd
import Text2Token
import googletrans

def weighted_query(query_matrix, idf_matrix) : 

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


def translateKrtoEn(UserText):
    translator = googletrans.Translator()

    UserText = translator.translate(UserText, dest='en', src='auto').text
    query = pd.DataFrame({'Hash': ["Query"],
                         'Description': [UserText]})

    query = Text2Token.Text2Token(query)

    query_matrix=pd.DataFrame(np.ones(shape=(len(query[0]),1)), index = query[0])

    return query_matrix


def translateResulttoKr(hashs):
    translator = googletrans.Translator()
    for index in range(len(hashs)) :
        hashs[index][1] = translator.translate(hashs[index][1], dest='ko', src='auto').text
    return hashs



