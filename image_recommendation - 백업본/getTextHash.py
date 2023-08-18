# 현재는 csv 파일로 만들어서 hash와 text를 넘겨 구현했습니다.
# 차후 연결할 때 이 부분을 수정해야 합니다.

import pandas as pd

def getTextHash(path):
    df=pd.read_csv(path)
    if df['Description'].isnull==1 :
        df['Description'] = df['Description'].fillna('')
        raise Exception("description에서 null값 발생.")
    return df