from flask import Flask, request,jsonify
from generator import AltTextGenerator
from database import Database
from database import Query
from calculator import Recommendation  
import pandas as pd

app = Flask(__name__)


"""============================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('menu'))  # 메뉴로 리디렉션


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        selected_action = request.form['selected_action']
        if selected_action == 'getBestPictures':
            return redirect(url_for('getBestPictures'))
        elif selected_action == 'getAltText':
            return redirect(url_for('getAltText'))
    
    return render_template('menu.html')
================================================================"""


@app.route('/getData', methods=['GET'])
def getData():
    try:
        datapath = request.form['datapath']
        data=pd.read_csv(datapath)
        return data
    
    except Exception as e:    
        return str(e)
    

@app.route('/getAltText', methods=['POST'])
def getAltText():
    try:
        # 클라이언트에서 넘어온 변수 받아오기
        img_path = request.form['img_path']
        userText = request.form['userText']

        # 데이터 전송 및 처리 요청
        ml_server_url = "http://172.16.162.72:포트 번호/generateAltText"
        data = {
            'img_path': img_path
        }
        response = request.post(ml_server_url, data=data)
        
        result = response.json()                #일단 여기때문에 json 형을 거치는 걸 생각했음.
                                                #복붙한 부분.
        data = pd.read_json(result)
        # 데이터 전처리 등 추가 처리
        processed_data = preprocess_data(data)
        
        # 가공된 데이터를 JSON 형식으로 변환하여 반환
        result_json = processed_data.to_json(orient='records')
        return result_json


    except Exception as e:
        return str(e)
    
#data = pd.read_json(result) #이걸 수행하면, hash, description만 있는 영어 dataframe이 나온다.


@app.route('/Tokenize', methods=['POST'])
def Tokenize():
    #토큰 처리 및 TF-IDF 알고리즘 수행
    try:
        data = request.form['data']
        data = Database(data)
        return data
        
    except Exception as e:
        return str(e)
    
@app.route('/getBestPictures', methods=['POST'])
def getBestPictures(data,userText):
    try:
        data = request.form['data']
        userText = request.form['userText']
        q=Query(data,userText)
        r=Recommendation(q,data)
        r.printf()
        return r       
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)