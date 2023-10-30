import os
import numpy as np
from PIL import Image



import sys
sys.path.append('/home/user/SaGol/MiniGPT-4')
import demo_torch
import pandas as pd
from pathlib import Path


#Generator 객체는 실행될 때 initialize 되어 chat을 상태로 저장하고, generate라는 메소드 하나를 가진다.
class Resizer:
    def __init__(self, halve_rate, size_limit):        
        self.halve_rate = halve_rate
        self.size_limit = size_limit
    
    #halve_rate는 축소 비율, size_limit은 최소 가로, 세로 사이즈 (tuple이 아니라 단일 변수)
    def resize(self, img):
        x,y = img.size[0], img.size[1]
        
        if x<=self.size_limit and y<=self.size_limit:
            print("사진이 너무 작습니다")  
            
        x = int(x * self.halve_rate) if (x*self.halve_rate>=self.size_limit) else self.size_limit
        y = int(y * self.halve_rate) if (y*self.halve_rate>=self.size_limit) else self.size_limit
        return img.resize((x,y),resample=0)

"""
로컬에서 돌려본 코드
#사진을 넘겨주는 코드(내부에선 flask 서버를 이용하여 구현이 되어 있다.)
#초기 path만 지정해주면 내부에서 resize로 넘겨 구현.
file_path= 'C:/Users/Administrator/Desktop/images'
halve_rate = 0.5
size_limit = 10

os.chdir(file_path)
Imgs = [Image.open(_) for _ in os.listdir(file_path) if (_.endswith(r".jpg") + _.endswith(r".png") + _.endswith(r".bmp") + _.endswith(r".webp") )]
os.chdir(file_path + '\\resize')

def resize(img, halve_rate, size_limit):
    x,y = img.size[0], img.size[1]
    if x<=size_limit and y<=size_limit:
        print("사진이 너무 작습니다")     
    x = int(x * halve_rate) if (x*halve_rate>=size_limit) else size_limit
    y = int(y * halve_rate) if (y*halve_rate>=size_limit) else size_limit
    filename = 'resized_'+img.filename
    img = img.resize((x,y),resample=0)
    return filename, img

for img in Imgs:
    filename, img = resize(img,halve_rate, size_limit)
    #확인용, 실제론 여기서 리턴하면 된다.
    img.save(filename)
    
"""