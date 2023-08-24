import json
from flask import Flask, request, jsonify
from generator import AltTextGenerator
from Text2Token import Text2Token
import translator
import TF_IDF
import calculator

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)


#테스트용 코드
@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello"


@app.route('/getAltText_img_path', methods=['POST'])
def generate_text_path():
    img_path = None
    try:
        img_path = request.form['img_path']
        if img_path:
            result = AltTextGenerator.generate(img_path)
            result_json = result.to_json(orient='records')
            return result_json
    
        else:
            return jsonify({"result": "이미지 경로 오류"})
        
    except Exception as e:    
        return jsonify({"error": str(e)})

    
@app.route('/getAltText', methods=['POST'])
# TODO : img_path가 아니라 단일 이미지를 받아도 처리가 가능하도록 함수 수정
def generate_text():
    img_path = None
    try:
        img_path = request.form['img_path']
        if img_path:
            result = AltTextGenerator.generate(img_path)
            result_json = result.to_json(orient='records')
            return result_json
    
        else:
            return jsonify({"result": "이미지 경로 오류"})
        
    except Exception as e:    
        return jsonify({"error": str(e)})    
    
    
@app.route('/getBestPictures', methods=['POST'])
def getBestPictures():
    try:
        #입력받는 데이터
        userText = request.form['userText']
        json_data = request.form['data']
        
        #한글로 입력받은 질문 -> 영어 토큰으로 전처리
        query = translator.translateKrtoEn(userText)
        query_dict = query[0].to_dict()
        data = json.loads(json_data)
        
        #data에서 등장하는 단어들로 vocabulary 만들기
        descriptions = pd.DataFrame({"Description":[item['Description'] for item in data]})
        data=pd.DataFrame(data)
        df = Text2Token(descriptions)
        vocab = list(set(w for words in df for w in words if len(w)>=3))
        vocab.sort()
        
        #TF-IDF 알고리즘
        TF_matrix = TF_IDF.TF(df,vocab)
        IDF_matrix= TF_IDF.IDF(TF_matrix,vocab)
        TF_IDF_matrix = TF_IDF.TF_IDF(TF_matrix,IDF_matrix)
        
        #사용자 질문 가중치 계산
        query_matrix = TF_IDF.weighted_query(query,IDF_matrix)
        validwords= calculator.validwords(query_matrix)
        query_vector=calculator.vectorization(validwords,vocab)
        
        cos_sim_matrix = calculator.cos_sim_matrix(query_vector, TF_IDF_matrix)
        BestPicture = calculator.recommend(cos_sim_matrix, data)

        #BestPicture의 [0]은 Hash, 1은 Description(영어). 목적에 따라 한글 description을 return하는 것도 가능함
        return json.dumps(BestPicture[0])
                
    except Exception as e:    
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='172.16.162.72', port="8890")