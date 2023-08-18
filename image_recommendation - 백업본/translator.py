import numpy as np
import pandas as pd
import Text2Token
import googletrans             #googletrans 3.1.0a0이 아닐 경우 오류 발생.
                                #pip uninstall googletrans
                                #pip install googletrans==3.1.0a0 

def translateKrtoEn(UserText):
    translator = googletrans.Translator()

    UserText = translator.translate(UserText, dest='en', src='auto').text
    query = pd.DataFrame({'Hash': ["Query"],
                         'Description': [UserText]})

    query = Text2Token.Text2Token(query)

    query_matrix=pd.DataFrame(np.ones(shape=(len(query[0]),1)), index = query[0])

    return query_matrix

def translateResulttoKr(hash):
    translator = googletrans.Translator()
    hash[1] = translator.translate(hash[1], dest='ko', src='auto').text
    return hash

"""
여러 장의 사진을 추천할 때.
def translateResulttoKr(hashs):
    translator = googletrans.Translator()
    for index in range(len(hashs)) :
        hashs[index][1] = translator.translate(hashs[index][1], dest='ko', src='auto').text
    return hashs
"""