import os
import numpy as np
from PIL import Image
import sys
sys.path.append('/home/user/SaGol/MiniGPT-4')

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
