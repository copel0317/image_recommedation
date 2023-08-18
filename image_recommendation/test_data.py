import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import demo_torch

import pandas as pd
from pathlib import Path

class Generator:
    def __init__(self,data):
        self.chat = demo_torch.initialize()
        self.data=data

#===============Text generation==========#
    def new_text(self, img_path):
        llm_text = demo_torch.text_generate(img_path, self.chat)
        Hash=img_path.rsplit( ".", 1 )[0].rsplit("/",5)[5]

        #Hash와 사진을 Dataframe에 추가
        self.data=pd.concat([self.data, pd.DataFrame({'Hash': [Hash], 'Description': [llm_text]})], ignore_index=True)

    def generate(self, photopath):
        for file in Path(photopath).iterdir():
            self.new_text(str(file))

