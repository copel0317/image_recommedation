import numpy as np
import pandas as pd
import Text2Token
import googletrans

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



