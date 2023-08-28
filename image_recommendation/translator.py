import numpy as np
import pandas as pd
import Text2Token
import googletrans             #googletrans 3.1.0a0이 아닐 경우 오류 발생.
                                #pip uninstall googletrans
                                #pip install googletrans==3.1.0a0 
translator = googletrans.Translator()
        
def translateKrtoEn(UserText):

    UserText = translator.translate(UserText, dest='en', src='auto').text
    query = pd.DataFrame({'Hash': ["Query"],
                         'Description': [UserText]})

    query = Text2Token.Text2Token(query)

    query_matrix=pd.DataFrame(np.ones(shape=(len(query[0]),1)), index = query[0])

    return query_matrix

def translateResulttoKr(recommend):
    recommend[1] = translator.translate(recommend[1], dest='ko', src='auto').text
    return recommend


def translatetoKr(description):
    description = translator.translate(description, dest='ko', src='auto').text
    return description

"""
여러 장의 사진을 추천할 때.
def translateResulttoKr(hashs):
    translator = googletrans.Translator()
    for index in range(len(hashs)) :
        hashs[index][1] = translator.translate(hashs[index][1], dest='ko', src='auto').text
    return hashs
"""