from flask import Flask, request, jsonify
from tools.Text2Token import Text2Token
from tools import translator
from tools import TF_IDF
from resizer import Resizer
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from celery.result import AsyncResult

import io
import os
import sys
import json

import pandas as pd
import numpy as np 
import base64

# Celery 애플리케이션 생성


app = Flask(__name__)

#경로 테스트용 코드
@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello"


#수정중================================================
"""
from celery_config import celery
@app.route('/getAltText_ver2', methods=['POST'])
def generate_text_ver2():
    try:
        Id = request.form['Id']
        Hash = request.form['Hash']
        uploaded_file = request.files['Image']  #FileStorage 객체. Response와 같이 여러 속성을 가진다
        encoded_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
        result = celery.send_task('make_text', args=(encoded_image, Hash, Id), queue='my_queue')
        return jsonify({"task_id": result.id}), 202

    except Exception as e:    
        return jsonify({"error": str(e)})    

#결과 받아오는 부분    
@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    task = celery.AsyncResult(task_id)
    if task is None:
        return jsonify({"status": "작업을 찾을 수 없습니다."})
    if task.state == 'SUCCESS':
        #result = task.get()['index']
        return task.get()
        #return result.to_json(orient='records')
    elif task.state == 'PENDING':
        return jsonify({"status": "작업이 아직 완료되지 않았습니다."})
    else:
        return jsonify({"status": "작업이 실패하였습니다."})
"""    
        
#복원용 코드===============================================
# Generator 객체를 불러오는 데 시간이 걸려, 임시로 import문을 여기에 놓고 주석처리하여 테스트
# 여기서 불러온 generator 객체를 각 gpu에서 하나씩 독립적으로 가지고 있는 것을 목표로 진행했었음.
# (init될 때 gpu_id를 인수로 받아, self에 저장)
from generator import Generator
AltTextGenerator_0 = Generator(0)


#사진의 (x,y)를 절반으로 줄임 (최소 사이즈 10x10). 실험 진행하여 최적값 찾아야 함
halve_rate = 0.5
size_limit = 10
Resizer = Resizer(halve_rate, size_limit)

@app.route('/resizeTest', methods=['POST'])
def resizing():
    try:
        Id = request.form['Id']
        Hash = request.form['Hash']
        uploaded_file = request.files['Image'] #PIL의 Image 객체를 사용
        
        Img = Image.open(io.BytesIO(uploaded_file.read()))
        Img = Resizer.resize(Img)
        return jsonify({"result": Img})
        
    except Exception as e:    
        return jsonify({"error": str(e)})   

                                
#사진의 사이즈에 따른 소요 시간을 계산하기 위한 코드
import time 
@app.route('/getAltTexttime', methods=['POST'])
def generate_text_time():
    try:
        start = time.time()
        Id = request.form['Id']
        Hash = request.form['Hash']
        halve_rate = request.form['halve']
        uploaded_file = request.files['Image'] #PIL의 Image 객체를 사용
        Img = Image.open(io.BytesIO(uploaded_file.read()))
        
        original_size = Img.size
        Resizer.halve_rate = float(halve_rate)
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

#서비스용 코드====================================================

@app.route('/getAltText', methods=['POST'])
def generate_text():
    try:
        Id = request.form['Id']
        Hash = request.form['Hash']
        uploaded_file = request.files['Image'] #PIL의 Image 객체를 사용
        
        Img = Image.open(io.BytesIO(uploaded_file.read()))
        Img = Resizer.resize(Img)
        
        if Img:                                                   #Generator에 넣어 설명을 받는 부분
            result = AltTextGenerator_0.generate(Img, Hash, Id)
            result_json = result.to_json(orient='records')
            return result_json

        else:
            return jsonify({"result": "이미지 오류"})
        
    except Exception as e:    
        return jsonify({"error": str(e)})  

#===============================================================    
@app.route('/getBestPictures', methods=['POST'])

def getBestPictures():
    try:
        #입력받는 데이터
        userText = request.form['userText']
        pairs =json.loads(request.form['data'])
        print ("userText : " + userText)
        print (pairs)
        
        query = pd.DataFrame({"Description" : [translator.translatetoEn(userText)]})
        print(query)
        
        descriptions = pd.DataFrame({"Description":[pair['Description'] for pair in pairs]})
        merged_df = pd.concat([descriptions, query], ignore_index=True)
        print (merged_df)
        
        df = Text2Token(merged_df)
        vocab = list(set(w for words in df for w in words if len(w)>=3))
        vocab.sort()
        
        print(vocab)
        
        #TF-IDF 알고리즘
        TF_matrix = TF_IDF.TF(df,vocab)
        IDF_matrix= TF_IDF.IDF(TF_matrix,vocab)
        TF_IDF_matrix = TF_matrix* IDF_matrix.values
        
        #cosine_similarity_matrix
        cosine_sim_matrix = cosine_similarity(TF_IDF_matrix.values)

        
        #추천 알고리즘
        query_similarity = cosine_sim_matrix[-1][:-1] #query가 제일 마지막에 나오므로, 자기자신(1)을 제외하고 최대값 탐색
        print (type(query_similarity))
        photo_index = np.argmax(query_similarity)
        print (photo_index)

        return pairs[photo_index]['Hash']
                
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

