# 현재는 csv 파일로 만들어서 hash와 text를 넘겨 구현했습니다.
# 차후 연결할 때 이 부분을 수정해야 합니다.

import pandas as pd

def getTextHash():
    df=pd.read_csv("C:/Users/Administrator/Desktop/MinigptOut.csv")
    return df