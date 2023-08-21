from flask import Flask, request, jsonify
#현재 연구실 서버와 port가 아직 연결되어 있지 않아 test 모듈을 사용
from generator_test import AltTextGenerator

app = Flask(__name__)
#AltTextGenerator라는 객체를 import.
#상태 chat과 generate(img_path) 메소드 하나만 가지는 객체.
#추가적으로 추천도 머신러닝 서버에서 구현하게 된다면, generator.py에 추가 예정

@app.route('/generateAltText', methods=['POST'])
def generate_text():
    try:
        img_path = request.form['img_path']
        if img_path:
            result = AltTextGenerator.generate(img_path)
            return jsonify({"result": result})
    
        else:
            return jsonify({"result": "이미지 경로 오류"})
        
    except Exception as e:    
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='172.16.162.72', port="포트 열어야 함")