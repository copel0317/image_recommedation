import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import demo_torch

import pandas as pd
from pathlib import Path
   
#Generator 객체는 실행될 때 initialize 되어 chat을 상태로 저장하고, generate라는 메소드 하나를 가진다.
class Generator:
    def __init__(self):
        self.chat = demo_torch.initialize()
        self.data = None
        
#===============Text generation==========#
    def new_text(self, img_path):
        llm_text = demo_torch.text_generate(img_path, self.chat)
        Hash=img_path.rsplit( ".", 1 )[0].rsplit("/",5)[5]

        #Hash와 사진을 Dataframe에 추가
        self.data=pd.concat([self.data, pd.DataFrame({'Hash': [Hash], 'Description': [llm_text]})], ignore_index=True)

    def generate(self, img_path):        ##generate 메소드는 자기 클래스에 data를 저장한다.'
        self.data = None
        for file in Path(img_path).iterdir():
            self.new_text(str(file))
        return self.data

AltTextGenerator = Generator()