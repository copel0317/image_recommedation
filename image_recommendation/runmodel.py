from flask import Flask, request, jsonify
from tools.Text2Token import Text2Token
from tools import translator
from tools import TF_IDF
from tools.resizer import Resizer
from tools.generator import Generator
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

import io
import os
import sys
import json
import time 

import pandas as pd
import numpy as np 
import base64

# Celery 애플리케이션 생성


app = Flask(__name__)

#Flask test용 코드
@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello"


#사진의 (x,y)를 절반으로 줄임 (최소 사이즈 10x10).기본값.
halve_rate = 0.5
size_limit = 10
Resizer = Resizer(halve_rate, size_limit)

#텍스트 생성 개체(그래픽카드 번호)
AltTextGenerator_0 = Generator(0)

#Resizer의 인수 조절 경로
@app.route('/config', methods=['POST'])
def configuration():
    try:
        Resizer.halve_rate = float(request.form['halve'])
        Resizer.size_limit = int(request.form['min_size'])
        return jsonify({"halve_rate" : Resizer.halve_rate, "min_size" : Resizer.size_limit })
    except Exception as e:    
        return jsonify({"error": str(e)})   


#=============================================서비스용 코드 - 사진 설명 생성
@app.route('/getAltText', methods=['POST'])
def generate_text():
    try:
        Id = request.form['Id']
        Hash = request.form['Hash']
        uploaded_file = request.files['Image'] #PIL의 Image 객체를 사용
        Img = Image.open(io.BytesIO(uploaded_file.read()))
        
        original_size = Img.size
        Img = Resizer.resize(Img)
        resized = Img.size        
        if Img:
            result = AltTextGenerator_0.generate(Img, Hash, Id)
            result_json = result.to_json(orient='records')
            return result_json

        else:
            return jsonify({"result": "이미지 오류"})
        
    except Exception as e:    
        return jsonify({"error": str(e)})   

#=============================================서비스용 코드 - 사진 추천  
@app.route('/getBestPictures', methods=['POST'])
def getBestPictures():
    try:
        #입력받는 데이터
        userText = request.form['userText']
        pairs =json.loads(request.form['data'])
        print ("userText : " + userText)

        
        query = pd.DataFrame({"Description" : [translator.translatetoEn(userText)]})

        
        descriptions = pd.DataFrame({"Description":[pair['Description'] for pair in pairs]})
        merged_df = pd.concat([descriptions, query], ignore_index=True)

        
        df = Text2Token(merged_df)
        vocab = list(set(w for words in df for w in words if len(w)>=3))
        vocab.sort()

        
        #TF-IDF 알고리즘
        TF_matrix = TF_IDF.TF(df,vocab)
        IDF_matrix= TF_IDF.IDF(TF_matrix,vocab)
        TF_IDF_matrix = TF_matrix* IDF_matrix.values
        
        #cosine_similarity_matrix
        cosine_sim_matrix = cosine_similarity(TF_IDF_matrix.values)

        #추천 알고리즘
        query_similarity = cosine_sim_matrix[-1][:-1] #query가 제일 마지막에 나오므로, 자기자신(1)을 제외하고 최대값 탐색
        photo_index = np.argmax(query_similarity)
        
        return " "+pairs[photo_index]['Hash']+" "
                
    except Exception as e:    
        return jsonify({"error": str(e)})
    
    
@app.route('/translate', methods=['POST'])
def translatetoKr():
    try:
        Description = request.form['Description']
        return translator.translatetoKr(Description)
    except Exception as e:    
        return jsonify({"error": str(e)})

    
    
if __name__ == '__main__':
    app.run(host='172.16.162.72', port="8890")
    
    
    
    
    
#사진의 사이즈에 따른 소요 시간을 계산하기 위한 코드
@app.route('/getAltText_time', methods=['POST'])
def generate_text_time():
    try:
        start = time.time()
        Id = request.form['Id']
        Hash = request.form['Hash']
        uploaded_file = request.files['Image'] #PIL의 Image 객체를 사용
        Img = Image.open(io.BytesIO(uploaded_file.read()))
        
        original_size = Img.size
        Img = Resizer.resize(Img)
        resized = Img.size
        
        if Img:                                                   #Generator에 넣어 설명을 받는 부분
            result = AltTextGenerator_0.generate(Img, Hash, Id)
            end = time.time()
            duration = end - start
            result['original_size'] = [original_size]
            result['resized'] = [resized]
            result['duration'] = [duration]
            result_json = result.to_json(orient='records')
            return result_json

        else:
            return jsonify({"result": "이미지 오류"})
        
    except Exception as e:    
        return jsonify({"error": str(e)})

