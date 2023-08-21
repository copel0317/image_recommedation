import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pandas as pd
from pathlib import Path
   
#Generator 객체는 실행될 때 initialize 되어 chat을 상태로 저장하고, generate라는 메소드 하나를 가진다.
class Generator:
    def __init__(self):
        self.chat = ["apple"]
        self.data = None
        
#===============Text generation==========#
    def generate(self, img_path):        ##generate 메소드는 자기 클래스에 data를 저장한다.'
        self.data = "generated" + img_path
        return self.data

AltTextGenerator = Generator()